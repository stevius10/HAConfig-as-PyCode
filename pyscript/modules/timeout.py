TIMEOUT_HOUR_SECONDS = 3600

AUTO_TIMEOUT_DELAY_ADGUARD = 0.5 * TIMEOUT_HOUR_SECONDS
AUTO_TIMEOUT_DELAY_HEIZDECKE = 0.5 * TIMEOUT_HOUR_SECONDS
AUTO_TIMEOUT_DELAY_SOFA = 0.5 * TIMEOUT_HOUR_SECONDS
AUTO_TIMEOUT_DELAY_BETT = 0.5 * TIMEOUT_HOUR_SECONDS
AUTO_TIMEOUT_DELAY_LUFTREINIGER = 6 * TIMEOUT_HOUR_SECONDS
AUTO_TIMEOUT_DELAY_SZ_VENTILATOR = 1 * TIMEOUT_HOUR_SECONDS
AUTO_TIMEOUT_DELAY_SCHLAFZIMMER = 1 * TIMEOUT_HOUR_SECONDS

AUTO_TIMEOUT_ENTITIES = {
  "switch.adguard_home_schutz": { "default": "on", "delay": AUTO_TIMEOUT_DELAY_ADGUARD }, 
  "switch.heizdecke": { "default": "off", "delay": AUTO_TIMEOUT_DELAY_HEIZDECKE }, 
  "switch.sofa": { "default": "off", "delay": AUTO_TIMEOUT_DELAY_SOFA }, 
  "switch.bett": { "default": "off", "delay": AUTO_TIMEOUT_DELAY_BETT },
  "fan.luftreiniger": { "default": "off", "delay": AUTO_TIMEOUT_DELAY_LUFTREINIGER, "timer": "timer.h_timer_luftreiniger" }, 
  "fan.sz_ventilator": { "default": "off", "delay": AUTO_TIMEOUT_DELAY_SZ_VENTILATOR, "timer": "timer.h_timer_sz_ventilator" }, 
  "media_player.schlafzimmer": { "default": "idle", "delay": AUTO_TIMEOUT_DELAY_SCHLAFZIMMER, "timer": "timer.h_timer_schlafzimmer" } 
}

# script_air_cleaner
SCRIPT_AIR_CLEANER_TIMEOUT_AUTOMATION = TIMEOUT_HOUR_SECONDS / 6
SCRIPT_AIR_CLEANER_TIMEOUT_SLEEP = AUTO_TIMEOUT_DELAY_LUFTREINIGER