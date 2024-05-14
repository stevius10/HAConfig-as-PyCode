AUTO_ENTITIES = {
  "climate.k": { "default": "off", "func": "climate.turn_off" },
  "fan.luft": { "default": "off", "delay": 7200 }, 
  "fan.sz_luft": { "default": "off", "delay": 7200 }, 
  "fan.sz_ventilator": { "default": "off", "delay": 5400 }, 
  "fan.wz_luft": { "default": "off", "delay": 7200 }, 
  "media_player.schlafzimmer": { "default": "idle", "delay": 3600 },
  "switch.adguard_home_schutz": { "default": "on", "delay": 600 }, 
  "switch.bett": { "default": "off", "delay": 1800 },
  "switch.heizdecke": { "default": "off", "delay": 1800 }, 
  "switch.sofa": { "default": "off", "delay": 1800 }, 
  "switch.sz_luftung": { "default": "off", "delay": 600 },
  "switch.wz_ventilator": { "default": "off", "delay": 600 }
}

AUTO_MOTION_ENTITIES = { 
  "binary_sensor.g_sensor_occupancy": { "on": "scene.g_tisch", "off": "scene.g_aus" },
  "binary_sensor.k_sensor_occupancy": { "on": "scene.k_normal", "off": "scene.k_aus", "transition": 20, "sun_diff": 30 }
}

CONFIG_CONTROL_ENTITIES = {
  'sensor.wz_schalter_action': {
    'on': 'scene.wz_indirekt',
    'off': ['scene.wz_aus', 'scene.k_aus'],
    'up': 'scene.wz_hell',
    'down': 'scene.wz_schwach'
  }, 
  'sensor.sz_schalter_action': {
    'on': 'scene.sz_indirekt',
    'off': 'scene.sz_aus',
    'up': 'scene.sz_hell',
    'down': 'scene.sz_schwach'
  },
  'sensor.g_schalter_action': {
    'single': 'scene.g_indirekt',
    'double': 'scene.g_aus',
    'long': ''
  }
}