# Global
EXPR_TIME_DAY = "range(00:00, 24:00)"
EXPR_TIME_WORKTIME =  "cron(* 9-19 * * 1-6)"

# 
# EXPR_TIME_ACTIVE_RANGE_EVENING = "range(19:00, 24:00)"
#EXPR_TIME_ACTIVE_RANGE_NIGHT = "range(24:00, 6:00)"

# Specific 

# Air Cleaner
EXPR_STATE_SEASON_POLLEN = "sensor.season in ['spring', 'summer']"
EXPR_TIME_AVTIVE_THRESHOLDS = EXPR_TIME_WORKTIME

# Auto Motion
EXPR_TIME_RANGE_DAY_MOTION = EXPR_TIME_DAY

# Auto Notify
EXPR_TIME_UPDATE_SENSORS_HOUSING = "cron(30 16 * * 1-7)"

# Misc
EXPR_STATE_OPEN_WINDOW = "sensor.open_window == 'true'"