# Global

EXPR_TIME_DAY = "range(00:00, 24:00)"
EXPR_TIME_DAYTIME = "cron(* 8-22 * * *)"
EXPR_TIME_GENERAL_WORKTIME =  "cron(* 8-20 * * 1-6)"

# Auto Motion
EXPR_TIME_RANGE_DAY_MOTION = EXPR_TIME_DAY

# Auto Notify
EXPR_TIME_UPDATE_SENSORS_HOUSING = "cron(30 8-18 * * 1-5)"

# Services
EXPR_TIME_SERVICE_FILEBACKUP_CRON = "cron(0 1 * * *)"
EXPR_TIME_SERVICE_GIT_CRON = "cron(15 1 * * *)"

EXPR_TIME_AIR_AUTOMATION = EXPR_TIME_DAYTIME
EXPR_STATE_AIR_AUTOMATION_SEASON = "sensor.season in ['spring', 'summer']"

# Misc
EXPR_STATE_OPEN_WINDOW = "sensor.open_window == 'true'"