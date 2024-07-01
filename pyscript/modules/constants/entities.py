# Automation

AUTO_ENTITIES = {
  "climate.k": { "default": "off", "func": "climate.turn_off" },
  "media_player.schlafzimmer": { "default": ["off", "paused"], "delay": 4800 },
  "switch.adguard_home_schutz": { "default": "on", "delay": 1800 }, 
  "switch.bett": { "default": "off", "delay": 1800 },
  "switch.heizdecke": { "default": "off", "delay": 1800 }, 
  "switch.sofa": { "default": "off", "delay": 1800 }, 
  "fan.wz_ventilator": { "default": "off", "delay": 7200 }, 
  "fan.sz_ventilator": { "default": "off", "delay": 7200 }, 
  "fan.wz_luft": { "default": "off", "delay": 21600 }, 
  "fan.sz_luft": { "default": "off", "delay": 21600 }, 
  "switch.wz_luftung": { "default": "off", "delay": 600 },
  "switch.sz_luftung": { "default": "off", "delay": 600 }
}

AUTO_MOTION_ENTITIES = { 
  "binary_sensor.g_sensor_occupancy": { "on": "scene.g_tisch", "off": "scene.g_aus" },
  "binary_sensor.k_sensor_occupancy": { "on": "scene.k_normal", "off": "scene.k_aus", "transition": 20, "sun_diff": 30 }
}

AUTO_CONTROL_ENTITIES = {
  'sensor.wz_schalter_action': { 'on': 'scene.wz_indirekt', 'off': ['scene.wz_aus', 'scene.k_aus'], 'up': 'scene.wz_hell', 'down': 'scene.wz_schwach' }, 
  'sensor.sz_schalter_action': { 'on': 'scene.sz_indirekt', 'off': 'scene.sz_aus', 'up': 'scene.sz_hell', 'down': 'scene.sz_schwach' },
  'sensor.g_schalter_action': { 'single': 'scene.g_indirekt', 'double': 'scene.g_aus', 'long': '' }
}

AUTO_PRESENCE_ENTITIES = {
  "wohnzimmer": {
    "indicators": {
      "media_player.wz_fernseher": {"condition": "playing"},
      "fan.wz_ventilator": {"condition": "playing", "weight": 0.1}
    },
    "exclusions": {
      "media_player.sz_fernseher": {"condition": "playing"},
      "media_player.schlafzimmer": {"condition": "playing"},
    }
  },
  "schlafzimmer": {
    "indicators": {
      "media_player.schlafzimmer": {"condition": "playing"},
      "media_player.sz_fernseher": {"condition": "playing"},
      "fan.sz_ventilator": {"condition": "playing", "weight": 0.1}
    },
    "exclusions": {
      "media_player.wz_fernseher": {"condition": "playing"}
    }
  },
  "away": {
    "indicators": {
      "person.steven": {"condition": "not_home"}
    },
    "exclusions": {
      "media_player.schlafzimmer": {"condition": "playing"},
      "media_player.sz_fernseher": {"condition": "playing"},
      "media_player.wz_fernseher": {"condition": "playing"}
    }
  }
}

CLUSTER_ENTITIES_AIR = [ "humidifier.luftbefeuchter", "fan.wz_ventilator", "fan.sz_ventilator", "fan.wz_luft", "fan.sz_luft", "switch.wz_luftung", "switch.sz_luftung" ]
CLUSTER_ENTITIES_HEATING = [ "clima.wz_heizung", "clima.sz_heizung", "clima.k_heizung" ]
CLUSTER_ENTITIES_MEDIA= [ "media_player.bad", "media_player.kueche", "media_player.schlafzimmer", "media_player.wohnzimmer", "media_player.uberall" ]
CLUSTER_ENTITIES_LIGHT = [ "light.wz_beleuchtung", "light.sz_beleuchtung", "light.k_beleuchtung", "light.g_beleuchtung" ]
CLUSTER_ENTITIES = [ "switch.bett", "switch.sofa", "switch.heizdecke" ]
CLUSTER_ENTITIES_TV = [ "media.wz_fernseher", "media.sz_fernseher" ]

# Services

AIR_CONTROL_ENTITIES = {
  "wz_luft": { "fan": "fan.wz_luft", "sensor": "sensor.wz_luft", "luftung": "switch.wz_luftung" },
  "sz_luft": { "fan": "fan.sz_luft", "sensor": "sensor.sz_luft", "luftung": "switch.sz_luftung" }
}