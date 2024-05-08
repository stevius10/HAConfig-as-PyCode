# HAConfig-as-PyCode

HAConfig-as-PyCode is a declarative Home Assistant configuration prtoject that aims for a Python programming language-based approach over the default Home Assistant's low-code model, focusing on reusability, encapsulation and modular expandability. As Home Assistant currently offers only limited resources for developers I'd like to share my configuration. 

![Desktop](www/overview-desktop.png)

## Implementation

The project's core functionality follows an event-driven approach, leveraging Python scripts with PyScript and Home Assistant's built-in automation capabilities to enable dynamic and responsive smart home behavior. 

Implementation like [`auto_entities.py`](pyscript/auto_entities.py), [`auto_motion.py`](pyscript/auto_motion.py), or [`auto_notify.py`](pyscript/auto_notify.py) define the behavior of various entities, automations, and trigger based on events or state changes.

- [`auto_entities.py`](pyscript/auto_entities.py) defines entity behavior based on a deviating states and their correlated timeouts, leveraging the `AUTO_ENTITIES` data structure to map entities to their desired states.
- [`auto_motion.py`](pyscript/auto_motion.py) handles motion sensor-based automations, mapping sensors to actions using the `AUTO_MOTION_ENTITIES` data structure.
- [`auto_notify.py`](pyscript/auto_notify.py) sends notifications to mobile devices or channels based on state changes, utilizing the `notify_immo` function, which uses BeautifulSoup to parse housing offers on different Berlin housing associations. 
- [`config_control.py`](pyscript/config_control.py) defines controller behavior and maps it to scenes and actions using the `CONFIG_CONTROL` data structure.

Other key scripts include:

- [`ha_helper.py`](pyscript/scripts/ha_helper.py) provides helper functions for interacting with Home Assistant ressources including logging. 
- [`ha_system.py`](pyscript/scripts/ha_system.py) handles system-related tasks, such as managing files in reference to configuration management tools, configuring the runtime environment and satisfy prerequisites for system monitoring.
- [`script_air_cleaner.py`](pyscript/scripts/script_air_cleaner.py) controls automatic air purification with regard to pollen concentration for the purpose of pollen allergy, scheduled based on various thresholds. 
- [`script_off.py`](pyscript/scripts/script_off.py) offers functionality to turn off entities considering conditions e. g. being away or shut down and ensuring their state. 
- [`services.py`](pyscript/apps/services.py) defines a service factory that creates periodically executed services defined by provided cron expression. An example might be `filebackup.sh`, a script to backup Home Assistant configuration and data file based to an external device.  
- [`sync_git.py`](pyscript/apps/sync_git.py) synchronizes the configuration automatically to this Git repository.

The `/pyscript/modules` directory contains reusable Python modules that encapsulate various functionalities used throughout the project:

- [`config.py`](pyscript/modules/config.py): This module contains configuration settings used across the project, promoting code organization and maintainability.
- [`entities.py`](pyscript/modules/entities.py): This module describes the default desired state for entities and conditions how to behave, e. g. timeout. 
- [`helper.py`](pyscript/modules/helper.py): This module provides helper functions and utilities for various tasks, such as defining conditions and expressions, handling state triggers, and managing time-based triggers.
- [`mapping.py`](pyscript/modules/mapping.py): This module contains naming and string mapping. 
- [`settings.py`](pyscript/modules/settings.py): This module contains settings or configuration values specific to certain components or functionalities.
- [`utils.py`](pyscript/modules/utils.py): This module contains utility functions for logging, contexts, and other general-purpose tasks used throughout the project.

## Exemplary functionality

- **System Monitoring**: Monitoring of system resources and performance metrics.
- **Backup and Synchronization**: Automated backup and synchronization of the Home Assistant configuration and data. 
- **Berlin housing offers**: Scraping for housing offers and real estate listenings by various companies in Berlin**
- **Lovelace UI Customization**: Customization of the Home Assistant's Lovelace UI, e. g. **Calendar Integration** or **Weather Monitoring and derived Metric Calculations**

## Images

![Mobile](www/overview-mobile.png)