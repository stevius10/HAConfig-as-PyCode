# General

EXPR_TIME_DAY = "range(00:00, 24:00)"
EXPR_TIME_DAYTIME = "cron(* 8-22 * * *)"
EXPR_TIME_GENERAL_WORKTIME =  "cron(* 8-20 * * 1-6)"

# Automation

EXPR_TIME_MOTION_DAY = EXPR_TIME_DAY

# Services

EXPR_TIME_FILEBACKUP = "cron(15 1 * * *)"
EXPR_TIME_SYNC_GIT = "cron(30 1 * * *)"
EXPR_TIME_SCRAPE_HOUSINGS_UPDATE = "cron(30 8-18 * * 1-5)"

EXPR_TIME_AIR_AUTOMATION = EXPR_TIME_DAYTIME
EXPR_STATE_AIR_AUTOMATION_SEASON = "sensor.season in ['spring', 'summer']"