import pandas as pd
from config import (
    COL_LOCATION, COL_EQUIPMENT, COL_POWER_W, COL_POWER_KW,
    COL_QUANTITY, COL_TOTAL_POWER_KW, COL_DAILY_HOURS, COL_MONTHLY_DAYS,
    COL_DAILY_KWH, COL_MONTHLY_KWH, USER_REQUIRED_COLUMNS, ALL_COLUMNS
)

# ── Helper: Compute derived columns ────────────────────────────────────────
def compute_derived(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate Power (kW), Total Power (kW), Daily and Monthly Consumption."""
    df = df.copy()
    df[COL_POWER_KW] = df[COL_POWER_W] / 1000
    df[COL_TOTAL_POWER_KW] = df[COL_POWER_KW] * df[COL_QUANTITY]
    df[COL_DAILY_KWH] = df[COL_TOTAL_POWER_KW] * df[COL_DAILY_HOURS]
    df[COL_MONTHLY_KWH] = df[COL_DAILY_KWH] * df[COL_MONTHLY_DAYS]
    return df


# ── Helper: Validate uploaded data ──────────────────────────────────────────
def validate_data(df: pd.DataFrame):
    """Return (cleaned_df, error_message). error_message is None if valid."""
    df = df.copy()
    df.columns = df.columns.astype(str).str.strip()

    # Check for required user-fillable columns
    required = set(USER_REQUIRED_COLUMNS)
    missing = required - set(df.columns)
    if missing:
        return None, f"Missing required columns: {', '.join(sorted(missing))}"

    # Keep relevant columns
    cols_to_keep = [c for c in df.columns if c in set(ALL_COLUMNS)]
    df = df[cols_to_keep].copy()

    # Filter out summary/total rows
    df = df[
        df[COL_LOCATION].astype(str).str.strip().str.lower()
        != "total campus energy audit"
    ]

    # Drop rows where key user columns are all NaN
    df.dropna(subset=[COL_LOCATION, COL_EQUIPMENT, COL_POWER_W], inplace=True)

    if df.empty:
        return None, "The file contains no valid data rows after removing blanks."

    # Convert numeric columns
    numeric_cols = [COL_POWER_W, COL_QUANTITY, COL_DAILY_HOURS, COL_MONTHLY_DAYS]
    for col in numeric_cols:
        try:
            df[col] = pd.to_numeric(df[col])
        except (ValueError, TypeError):
            return None, f"Column '{col}' must contain numeric values."

    if df[numeric_cols].isna().any().any():
        bad_col = df[numeric_cols].isna().any().idxmax()
        return None, f"Column '{bad_col}' contains invalid or non-numeric values."

    # Validate ranges
    if (df[COL_POWER_W] <= 0).any():
        return None, f"'{COL_POWER_W}' must contain positive values."
    if (df[COL_QUANTITY] <= 0).any():
        return None, f"'{COL_QUANTITY}' must contain positive values."
    if (df[COL_DAILY_HOURS] < 0).any():
        return None, f"'{COL_DAILY_HOURS}' contains negative values."
    if (df[COL_MONTHLY_DAYS] <= 0).any():
        return None, f"'{COL_MONTHLY_DAYS}' must contain positive values."

    # Clean string columns
    df[COL_LOCATION] = df[COL_LOCATION].astype(str).str.strip()
    df[COL_EQUIPMENT] = df[COL_EQUIPMENT].astype(str).str.strip()

    # Compute derived columns (always recalculate for consistency)
    df = compute_derived(df)

    # Reorder columns
    df = df[[c for c in ALL_COLUMNS if c in df.columns]]

    return df, None


# ── Helper: Generate dynamic insights ──────────────────────────────────────
def generate_insights(df: pd.DataFrame):
    """Analyse the data and return a list of insight strings (HTML safe)."""
    insights = []
    total_monthly = df[COL_MONTHLY_KWH].sum()
    total_daily = df[COL_DAILY_KWH].sum()
    total_power = df[COL_TOTAL_POWER_KW].sum()

    if total_monthly == 0:
        return ["No energy consumption recorded in the uploaded data."]

    # --- Location analysis ---
    loc_usage = df.groupby(COL_LOCATION)[COL_MONTHLY_KWH].sum().sort_values(ascending=False)
    n_locations = len(loc_usage)
    top_loc = loc_usage.index[0]
    top_loc_val = loc_usage.iloc[0]
    top_loc_pct = top_loc_val / total_monthly * 100
    avg_loc = loc_usage.mean()

    if top_loc_val > avg_loc * 1.5 and n_locations > 1:
        excess = top_loc_val - avg_loc
        insights.append(
            f"<b>{top_loc}</b> consumes <b>{top_loc_pct:.1f}%</b> of total monthly energy "
            f"({top_loc_val:,.1f} kWh), which is <b>{excess:,.1f} kWh above</b> the "
            f"location average of {avg_loc:,.1f} kWh. Prioritise an energy audit here."
        )
    elif n_locations > 1:
        insights.append(
            f"<b>{top_loc}</b> is the highest consumer at <b>{top_loc_pct:.1f}%</b> "
            f"({top_loc_val:,.1f} kWh/month) but is within a normal range relative to the "
            f"average ({avg_loc:,.1f} kWh per location)."
        )

    # --- Equipment analysis ---
    equip_usage = df.groupby(COL_EQUIPMENT)[COL_MONTHLY_KWH].sum().sort_values(ascending=False)
    top_equip = equip_usage.index[0]
    top_equip_val = equip_usage.iloc[0]
    top_equip_pct = top_equip_val / total_monthly * 100

    insights.append(
        f"<b>{top_equip}</b> is the most energy-intensive equipment, "
        f"responsible for <b>{top_equip_pct:.1f}%</b> of total monthly consumption "
        f"({top_equip_val:,.1f} kWh). Consider scheduling usage during off-peak "
        f"hours or upgrading to higher-efficiency models."
    )

    # --- Power density analysis ---
    loc_power = df.groupby(COL_LOCATION)[COL_TOTAL_POWER_KW].sum().sort_values(ascending=False)
    top_power_loc = loc_power.index[0]
    top_power_val = loc_power.iloc[0]
    top_power_pct = top_power_val / total_power * 100
    insights.append(
        f"<b>{top_power_loc}</b> has the highest installed power capacity at "
        f"<b>{top_power_val:,.2f} kW</b> ({top_power_pct:.1f}% of total). "
        f"Evaluate whether all equipment is necessary or if load shedding schedules "
        f"could reduce peak demand."
    )

    # --- Utilization analysis (hours * days) ---
    df_util = df.copy()
    df_util["Utilization_Score"] = df_util[COL_DAILY_HOURS] * df_util[COL_MONTHLY_DAYS]
    high_util = df_util.nlargest(2, "Utilization_Score")
    for _, row in high_util.iterrows():
        insights.append(
            f"<b>{row[COL_EQUIPMENT]}</b> at <b>{row[COL_LOCATION]}</b> runs "
            f"<b>{row[COL_DAILY_HOURS]:.0f} hrs/day</b> for <b>{row[COL_MONTHLY_DAYS]:.0f} days/month</b> "
            f"(utilization score: {row['Utilization_Score']:,.0f}). "
            f"Reducing daily hours by even 1 hour could save "
            f"~<b>{row[COL_TOTAL_POWER_KW] * row[COL_MONTHLY_DAYS]:,.1f} kWh/month</b>."
        )

    # --- Concentration / diversity ---
    if len(equip_usage) >= 3:
        top3_pct = equip_usage.iloc[:3].sum() / total_monthly * 100
        if top3_pct > 70:
            top3_names = ", ".join(equip_usage.index[:3])
            insights.append(
                f"Energy use is highly concentrated: the top 3 equipment types "
                f"(<b>{top3_names}</b>) account for <b>{top3_pct:.1f}%</b> of total "
                f"consumption. Diversifying reduction efforts across these categories "
                f"would yield the greatest impact."
            )

    # --- Lowest consumer opportunity ---
    if n_locations > 1:
        low_loc = loc_usage.index[-1]
        low_loc_val = loc_usage.iloc[-1]
        low_loc_pct = low_loc_val / total_monthly * 100
        insights.append(
            f"<b>{low_loc}</b> is the most efficient location at "
            f"<b>{low_loc_pct:.1f}%</b> ({low_loc_val:,.1f} kWh/month). Study its "
            f"operational practices to replicate savings across other locations."
        )

    # --- Savings projection ---
    reduction_5 = total_monthly * 0.05
    reduction_10 = total_monthly * 0.10
    insights.append(
        f"Total campus consumption is <b>{total_monthly:,.1f} kWh/month</b> "
        f"(~<b>{total_daily:,.1f} kWh/day</b>, total installed power: "
        f"<b>{total_power:,.2f} kW</b>). "
        f"A <b>5% reduction target</b> would save ~<b>{reduction_5:,.1f} kWh</b>, "
        f"while a <b>10% target</b> would save ~<b>{reduction_10:,.1f} kWh</b> monthly."
    )

    return insights
