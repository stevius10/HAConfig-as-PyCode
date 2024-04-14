x-anchors:

  &badge_alarm
  type: entity-filter
  conditions:
    - condition: state
      state_not: ["unavailable", "none", ""]
  entities: 
  - entity: '[[entity]]'
    name: '[[name]]'
    card_mod:
      style: | 
        :host { 
          {% if [[condition]] %}{% if [[conditional]] == true %}display: none;{% endif %}
            --label-badge-red: #556B2F;
          {% else %}
            --label-badge-text-color: rgba(128, 0, 0, 0.5); 
            --label-badge-red: maroon; 
          {% endif %} 
        }
    tap_action: '[[tap_action]]'
  card:
    type: custom:badge-card
    
template_badge_webfilter: 
  card: 
    <<: *badge_alarm
  default:
  - entity: sensor.adguard_home_dns_abfragen_blockiert
  - name: Web-filter
  - condition: "states('switch.adguard_home_schutz') == 'on'"
  - conditional: true
  - style: ":host {}"
  - tap_action:
      action: call-service
      service: switch.toggle
      data:
        entity_id: switch.adguard_home_schutz
    
      
template_badge_backup: 
  card:
    <<: *badge_alarm
  default:
    - entity: sensor.v_last_backup
    - name: Sicherung
    - condition: "'d' not in states('sensor.v_last_backup')"
    - conditional: false
    - style: ":host {}"
    - tap_action:
        action: navigate
        navigation_path: /cebe7a76_hassio_google_drive_backup/ingress

template_badges_alarms: 
  card: 
    type: 'custom:badge-card'
    badges: 
    - <<: *badge_alarm
      entities:
      - type: custom:decluttering-card
        template: template_badge_webfilter
  
      - type: custom:decluttering-card
        template: template_badge_backup
    
# Badges 

template_badges_general: 
  card:
    type: custom:layout-card
    layout: vertical
    cards: 

    - type: 'custom:badge-card'
      badges: 
      - type: custom:decluttering-card
        template: template_badges_alarms
  
      - entity: sensor.fritz_box_7530_download_durchsatz
        name: "⇩"
      - entity: sensor.fritz_box_7530_upload_durchsatz
        name: "⇧"

      - type: entity-filter
        entities: 
          - entity: timer.timer_adguard_home_schutz
            tap_action:
              action: call-service
              service: timer.finish
          - entity: timer.timer_heizdecke
            tap_action:
              action: call-service
              service: timer.finish
          - entity: timer.timer_sofa
            tap_action:
              action: call-service
              service: timer.finish
          - entity: timer.timer_bett
            tap_action:
              action: call-service
              service: timer.finish
          - entity: timer.timer_luftreiniger
            tap_action:
              action: call-service
              service: timer.finish
          - entity: timer.timer_sz_ventilator
            tap_action:
              action: call-service
              service: timer.finish
          - entity: timer.timer_schlafzimmer
            tap_action:
              action: call-service
              service: timer.finish
        conditions:
        - condition: state
          state_not: ["idle", "unavailable", "none", ""]
          
      - type: entity-filter
        entities:
          - entity: media_player.wohnzimmer
          - entity: media_player.bad
          - entity: media_player.kueche
          - entity: media_player.schlafzimmer
        state_filter:
          - playing
              
      - type: entity-filter
        entities: 
        - entity: timer.h_timer_schlafzimmer
          tap_action:
            action: call-service
            service: timer.finish
            target:
              entity_id: timer.h_timer_schlafzimmer
        - entity: timer.h_timer_luftreiniger
          name: Reiniger
          tap_action:
            action: call-service
            service: timer.finish
            target:
              entity_id: timer.h_timer_luftreiniger
        - entity: timer.h_timer_sz_ventilator
          name: Ventilator
          tap_action:
            action: call-service
            service: timer.finish
            target:
              entity_id: timer.h_timer_sz_ventilator
        - entity: sensor.qbittorrent_status
        conditions:
        - condition: state
          state_not: ["idle", "unavailable", "none", ""]
            
template_badges_services: 
  card:
    type: custom:layout-card
    layout: vertical
    cards: 
    - type: 'custom:badge-card'
      state_color: false
      show_header_toggle: false
      badges:
      - entity: sensor.luftreiniger
        name: Luft reinigen
        tap_action:
          action: call-service
          service: pyscript.script_air_cleaner
        hold_action:
          action: more-info
        double_tap_action:
          action: call-service
          service: homeassistant.turn_off
          data:
            entity_id: pyscript.script_air_cleaner
        card_mod: 
          style: |
            :host { 
              {% if states('sensor.luftreiniger_geschwindigkeit') == "Sleep" %}
                --label-badge-background-color: white;
              {% elif  states('sensor.luftreiniger_geschwindigkeit') | int(0) | int > 30 %}
                --label-badge-text-color: #556B2F;
              {% elif  states('sensor.luftreiniger_geschwindigkeit') | int(0) | int > 50 %}
                --label-badge-text-color: maroon;
              {% endif %}
              {% if states('sensor.luftreiniger_pm_25') | int(0) | int > 15 %}
                --label-badge-background-color: maroon;
              {% endif %}
            }
            
      - entity: sensor.none
        name: Alles aus- schalten
        style: |
          :host { 
            display: none
    
            {% if states('script.gh_luften') == "on" or
              states('climate.wz_klima') == "on" or
              states('climate.sz_klima') == "on" or
              states('light.wz_beleuchtung') == "on" or
              states('light.sz_beleuchtung') == "on" or
              states('switch.wz_ventilator') == "on" or
              states('switch.g_tischlampe') == "on" or
              states('light.sz_beleuchtung') == "on" or
              states('light.k_beleuchtung') == "on" or
              states('light.g_lampe') == "on" or
              states('switch.g_tischlampe') == "on" or
              states('fan.sz_ventilator') == "on" or         
              states('switch.sofa') == "on" or
              states('switch.heizdecke') == "on" or
              states('switch.bett') == "on" or
    
              states('media_player.kueche') == "playing" or
              states('media_player.bad') == "playing" or
              states('media_player.schlafzimmer') == "playing" or
              states('media_player.wohnzimmer') == "playing" %}
              
                display: block;
    
            {% endif %}
          }
        tap_action:
          action: call-service
          service: pyscript.script_off
        hold_action:
          action: more-info
        double_tap_action:
          action: call-service
          service: homeassistant.turn_off
          data:
            entity_id: pyscript.script_off
            
template_badges_system: 
  card:
    type: custom:layout-card
    layout: vertical
    cards: 
    - type: 'custom:badge-card'
      state_color: false
      show_header_toggle: false
      badges:
      - type: custom:decluttering-card
        template: template_badge_webfilter
        variables: 
          - conditional: false
  
      - type: custom:decluttering-card
        template: template_badge_backup
        variables: 
          - conditional: false
          
      - entity: sensor.fritz_box_7530_gb_empfangen
        name: Erneut verbinden
        double_tap_action:
          action: call-service
          service: button.press
          data:
            entity_id: button.fritz_box_7530_neu_verbinden
          confirmation:
            text: Internetverbindung trennen und neu herstellen? 
        tap_action:
          action: more-info
        
      - entity: switch.fritz_box_7530_wi_fi_generation_lockdown_gast
        name: Gäste-WLAN
        double_tap_action:
          action: call-service
          service: switch.toggle
          data:
            entity_id: switch.fritz_box_7530_wi_fi_generation_lockdown_gast
          confirmation:
            text: "Gäste-WLAN umschalten"
        tap_action:
          action: call-service
          service: browser_mod.more_info
          data:
            entity: image.fritz_box_7530_generation_lockdown_gast
            large: true