# ── Column Constants ────────────────────────────────────────────────────────
COL_LOCATION = "Location / Department"
COL_EQUIPMENT = "Appliance / Equipment"
COL_POWER_W = "Power (W)"
COL_POWER_KW = "Power (kW)"
COL_QUANTITY = "Quantity"
COL_TOTAL_POWER_KW = "Total Power (kW)"
COL_DAILY_HOURS = "Daily Usage (Hours)"
COL_MONTHLY_DAYS = "Monthly Days Open"
COL_DAILY_KWH = "Daily Consumption (kWh)"
COL_MONTHLY_KWH = "Monthly Consumption (kWh)"

USER_REQUIRED_COLUMNS = [
    COL_LOCATION, COL_EQUIPMENT, COL_POWER_W,
    COL_QUANTITY, COL_DAILY_HOURS, COL_MONTHLY_DAYS,
]

ALL_COLUMNS = [
    COL_LOCATION, COL_EQUIPMENT, COL_POWER_W, COL_POWER_KW,
    COL_QUANTITY, COL_TOTAL_POWER_KW, COL_DAILY_HOURS, COL_MONTHLY_DAYS,
    COL_DAILY_KWH, COL_MONTHLY_KWH,
]
