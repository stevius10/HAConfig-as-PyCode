AUTO_MOTION_TRANSITION_K = 20
AUTO_MOTION_SUN_DIFF_K = 30

AUTO_TIMEOUT_ADGUARD = 600
AUTO_TIMEOUT_HEIZDECKE = 1800
AUTO_TIMEOUT_SOFA = 1800
AUTO_TIMEOUT_BETT = 1800
AUTO_TIMEOUT_LUFT = 7200
AUTO_TIMEOUT_WZ_VENTILATOR = 600
AUTO_TIMEOUT_SZ_VENTILATOR = 5400
AUTO_TIMEOUT_LUFT_HELPER = 600
AUTO_TIMEOUT_SCHLAFZIMMER = 3600

HOUR_IN_SECONDS = 3600
AUTO_TIMEOUT_DELAY_ADGUARD = 0.5 * HOUR_IN_SECONDS
AUTO_TIMEOUT_DELAY_HEIZDECKE = 0.5 * HOUR_IN_SECONDS
AUTO_TIMEOUT_DELAY_SOFA = 0.5 * HOUR_IN_SECONDS
AUTO_TIMEOUT_DELAY_BETT = 0.5 * HOUR_IN_SECONDS
AUTO_TIMEOUT_DELAY_LUFTREINIGER = 6 * HOUR_IN_SECONDS
AUTO_TIMEOUT_DELAY_SZ_VENTILATOR = 1 * HOUR_IN_SECONDS
AUTO_TIMEOUT_DELAY_SCHLAFZIMMER = 1 * HOUR_IN_SECONDS

SCRIPT_AIR_CLEANER_TIMEOUT_AUTOMATION = HOUR_IN_SECONDS / 6 # script_air_cleaner

AUTO_ENTITIES = {
  "climate.k": { "default": "off", "func": "climate.turn_off" },
  "switch.adguard_home_schutz": { "default": "on", "delay": AUTO_TIMEOUT_ADGUARD }, 
  "switch.heizdecke": { "default": "off", "delay": AUTO_TIMEOUT_HEIZDECKE }, 
  "switch.sofa": { "default": "off", "delay": AUTO_TIMEOUT_SOFA }, 
  "switch.bett": { "default": "off", "delay": AUTO_TIMEOUT_BETT },
  "media_player.schlafzimmer": { "default": "idle", "delay": AUTO_TIMEOUT_SCHLAFZIMMER },
  "fan.luft": { "default": "off", "delay": AUTO_TIMEOUT_LUFT }, 
  "fan.wz_luft": { "default": "off", "delay": AUTO_TIMEOUT_LUFT }, 
  "fan.sz_luft": { "default": "off", "delay": AUTO_TIMEOUT_LUFT }, 
  "switch.wz_ventilator": { "default": "off", "delay": AUTO_TIMEOUT_LUFT_HELPER }, 
  "fan.sz_ventilator": { "default": "off", "delay": AUTO_TIMEOUT_SZ_VENTILATOR }, 
  "switch.sz_luftung": { "default": "off", "delay": AUTO_TIMEOUT_LUFT_HELPER }
}

AUTO_MOTION_ENTITIES = { 
  "binary_sensor.k_sensor_occupancy": { "on": "scene.k_normal", "off": "scene.k_aus", "transition": float(AUTO_MOTION_TRANSITION_K), "sun_diff": AUTO_MOTION_SUN_DIFF_K }, 
  "binary_sensor.g_sensor_occupancy": { "on": "scene.g_tisch", "off": "scene.g_aus", }
}