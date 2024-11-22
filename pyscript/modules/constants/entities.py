from constants.settings import SET_CONTROL_ON_LONG_DURATION, SET_ENTITIES_GLOBAL_VOLUME_MAX

from utils import expr 

# Automation

ENTITIES_AUTO = {
  
  # General
  "switch.adguard_home_schutz": { "default": "on", "delay": 1800 }, 

  # Küche
  "climate.k": { "default": "off", "call": "climate.turn_off" },
  "switch.k_lampe": { "default": "off", "delay": 600 }, 

  # Gang
  "switch.g_tischlampe": { "default": "off", "delay": 90 }, 

  # Wohnzimmer
  "fan.wz_luft": { "default": "off", "delay": 21600 }, 
  "fan.wz_ventilator": { "default": "off", "delay": 7200 }, 
  "switch.heizdecke": { "default": "off", "delay": 1800 }, 
  "switch.sofa": { "default": "off", "delay": 1800 }, 
  "switch.wz_luftung": { "default": "off", "delay": 600 },
  
  # Schlafzimmer
  "fan.sz_luft": { "default": "off", "delay": 21600 }, 
  "fan.sz_ventilator": { "default": "off", "delay": 7200 }, 
  "light.sz_beleuchtung": { "default": "off", "delay": 1800 },
  "switch.bett": { "default": "off", "delay": 1800 },
  "switch.sz_luftung": { "default": "off", "delay": 600 },

  # Erweitert
  # "switch.sofa": { 'default': 'switch.sofa == on and sensor.sofa_current_power > 5', 'duration': 60, 'delay': 4800 },
  # "media_player.schlafzimmer": { "default": ["off", "paused"], "call": "media_player.media_stop", "duration": 60, "delay": 4800 },
  # "media_player.schlafzimmer": { "default": f"media_player.schlafzimmer.volume_level < {SET_ENTITIES_GLOBAL_VOLUME_MAX}", "call": "media_player.volume_set", "params": {"volume_level": (SET_ENTITIES_GLOBAL_VOLUME_MAX / 100) } }
  
}

ENTITIES_MOTION = { 
  "binary_sensor.g_sensor_occupancy": { "on": "scene.g_tisch", "off": "scene.g_aus" },
  "binary_sensor.k_sensor_occupancy": { "on": "scene.k_normal", "off": "scene.k_aus", "transition": 20, "sun_diff": 30 }
}

ENTITIES_CONTROL = {
  'sensor.wz_schalter_action': { 'on': 'scene.wz_normal', 'off': ['scene.wz_aus', 'scene.k_aus'], 'up': 'scene.wz_hell', 'down': 'scene.wz_indirekt' }, 
  'sensor.sz_schalter_action': { 'on': 'scene.sz_normal', 'off': 'scene.sz_aus', 'up': 'scene.sz_hell', 'down': 'scene.sz_indirekt' },
  'sensor.g_schalter_action': { 'on': 'scene.g_normal', 'off': [ 'scene.g_aus', 'scene.wz_aus', 'scene.k_aus' ], 'up': 'scene.g_hell', 'down': 'scene.g_indirekt' },
}

ENTITIES_PRESENCE = {
  "wohnzimmer": {
    "indicators": {
      "media_player.wz_fernseher": {"condition": "playing"},
      "fan.wz_ventilator": {"condition": "on", "weight": 0.1}
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
      "fan.sz_ventilator": {"condition": "on", "weight": 0.1}
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

# Service

ENTITIES_CLUSTER_TURNOFF_AIR = [ "humidifier.luftbefeuchter", "fan.wz_ventilator", "fan.sz_ventilator", "fan.wz_luft", "fan.sz_luft", "switch.wz_luftung", "switch.sz_luftung" ]
ENTITIES_CLUSTER_TURNOFF_HEATING = [ "clima.wz_heizung", "clima.sz_heizung", "clima.k_heizung" ]
ENTITIES_CLUSTER_TURNOFF_MEDIA= [ "media_player.bad", "media_player.kueche", "media_player.schlafzimmer", "media_player.wohnzimmer", "media_player.uberall" ]
ENTITIES_CLUSTER_TURNOFF_LIGHT = [ "light.wz_beleuchtung", "light.sz_beleuchtung", "light.k_beleuchtung", "light.g_beleuchtung" ]
ENTITIES_CLUSTER_TURNOFF_SWITCHES = [ "switch.bett", "switch.sofa", "switch.heizdecke" ]
ENTITIES_CLUSTER_TURNOFF_TV = [ "media.wz_fernseher", "media.sz_fernseher" ]

ENTITIES_SERVICE_AIR_CONTROL = {
  "wz_luft": { "fan": "fan.wz_luft", "sensor": "sensor.wz_luft", "luftung": "switch.wz_luftung" },
  "sz_luft": { "fan": "fan.sz_luft", "sensor": "sensor.sz_luft", "luftung": "switch.sz_luftung" }
}