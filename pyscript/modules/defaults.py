AUTO_TIMEOUT_ADGUARD = 600
AUTO_TIMEOUT_HEIZDECKE = 1800
AUTO_TIMEOUT_SOFA = 1800
AUTO_TIMEOUT_BETT = 1800
AUTO_TIMEOUT_LUFTREINIGER = 7200
AUTO_TIMEOUT_SZ_VENTILATOR = 3600
AUTO_TIMEOUT_SCHLAFZIMMER = 3600

AUTO_ENTITIES_DEFAULT = {
  "climate.k": { "default": "off", "func": "climate.turn_off" },
  "switch.adguard_home_schutz": { "default": "on", "delay": AUTO_TIMEOUT_ADGUARD }, 
  "switch.heizdecke": { "default": "off", "delay": AUTO_TIMEOUT_HEIZDECKE }, 
  "switch.sofa": { "default": "off", "delay": AUTO_TIMEOUT_SOFA }, 
  "switch.bett": { "default": "off", "delay": AUTO_TIMEOUT_BETT },
  "fan.luftreiniger": { "default": "off", "delay": AUTO_TIMEOUT_LUFTREINIGER, "timer": "timer.h_timer_luftreiniger" }, 
  "fan.sz_ventilator": { "default": "off", "delay": AUTO_TIMEOUT_SZ_VENTILATOR, "timer": "timer.h_timer_sz_ventilator" }, 
  "media_player.schlafzimmer": { "default": "idle", "delay": AUTO_TIMEOUT_SCHLAFZIMMER, "timer": "timer.h_timer_schlafzimmer" } 
}