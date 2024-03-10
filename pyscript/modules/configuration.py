AUTO_DEFAULT_DELAY_ADGUARD = 600
AUTO_DEFAULT_DELAY_HEIZDECKE = 1800
AUTO_DEFAULT_DELAY_SOFA = 1800
AUTO_DEFAULT_DELAY_BETT = 1800
AUTO_DEFAULT_DELAY_LUFTREINIGER = 7200
AUTO_DEFAULT_DELAY_SZ_VENTILATOR = 3600
AUTO_DEFAULT_DELAY_SCHLAFZIMMER = 3600

AUTO_DEFAULT_ENTITIES = {
  "climate.k": { "default": "off", "delay": None },
  "switch.adguard_home_schutz": { "default": "on", "delay": AUTO_DEFAULT_DELAY_ADGUARD }, 
  "switch.heizdecke": { "default": "off", "delay": AUTO_DEFAULT_DELAY_HEIZDECKE }, 
  "switch.sofa": { "default": "off", "delay": AUTO_DEFAULT_DELAY_SOFA }, 
  "switch.bett": { "default": "off", "delay": AUTO_DEFAULT_DELAY_BETT },
  "fan.luftreiniger": { "default": "off", "delay": AUTO_DEFAULT_DELAY_LUFTREINIGER, "timer": "timer.h_timer_luftreiniger" }, 
  "fan.sz_ventilator": { "default": "off", "delay": AUTO_DEFAULT_DELAY_SZ_VENTILATOR, "timer": "timer.h_timer_sz_ventilator" }, 
  "media_player.schlafzimmer": { "default": "idle", "delay": AUTO_DEFAULT_DELAY_SCHLAFZIMMER, "timer": "timer.h_timer_schlafzimmer" } 
}