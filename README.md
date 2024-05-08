# HAConfig-as-PyCode

HAConfig-as-PyCode is a declarative Home Assistant configuration prtoject that aims to use a Python programming language-based approach over the default Home Assistant's low-code model, focusing on standardization, encapsulation and reusability. As Home Assistant currently offers only limited resources for developers I would like to share this configuration. 

## Implementation

The project's core functionality follows an event-driven approach, leveraging Python scripts using PyScript and Home Assistant's built-in automation capabilities to enable dynamic and responsive smart home behavior. 

It's implemented through scripts like [`auto_entities.py`](pyscript/auto_entities.py), [`auto_motion.py`](pyscript/auto_motion.py), or [`auto_notify.py`](pyscript/auto_notify.py). These scripts define the behavior of various entities, handle motion-based automations, and trigger notifications based on events or state changes.

- [`auto_entities.py`](pyscript/auto_entities.py) defines entity behavior based on a deviating state and correlated timeouts, leveraging the `AUTO_ENTITIES` data struction to map entities to desired states.
- [`auto_motion.py`](pyscript/auto_motion.py) handles motion sensor-based automations, mapping sensors to scenes or actions using the `AUTO_MOTION_ENTITIES` data structure.
- [`auto_notify.py`](pyscript/auto_notify.py) sends notifications to mobile devices or channels based on events or state changes, utilizing the `notify_immo` function, which crawls for housing offers on different Berlin housing associations. 

Other key scripts include:

- [`config_control.py`](pyscript/config_control.py) defines controller behavior and maps sensors to scenes or actions using the `CONFIG_CONTROL` data structure.
- [`ha_helper.py`](pyscript/scripts/ha_helper.py) provides helper functions for interacting with Home Assistant entities, services, and events. Manages logging capability. 
- [`ha_system.py`](pyscript/scripts/ha_system.py) handles system-related tasks, such as managing files, setup the environment and parts of system monitoring.
- [`script_air_cleaner.py`](pyscript/scripts/script_air_cleaner.py) manages an air cleaner device, including scheduling, react on various sensoric thresholdes and timeout handling.
- [`script_off.py`](pyscript/scripts/script_off.py) handles the "off" state for various entities, ensuring they are properly turned off or set to their desired state.
- [`services.py`](pyscript/apps/services.py) defines a service factory function that creates services based on a provided cron expression. An example might be 'filebackup.sh', a script that automates the backup process for the Home Assistant configuration and data to an external device. 
- [`sync_git.py`](pyscript/apps/sync_git.py) synchronizes the configuration automatically with this  Git repository for version control. 

The /pyscript/modules directory contains reusable Python modules that encapsulate various functionalities and utilities used throughout the project:

[`config.py`](pyscript/modules/config.py): This module contains configuration settings and constants used across the project, promoting code organization and maintainability.
[`entities.py`](pyscript/modules/entities.py): This module defines helper functions and utilities for working with Home Assistant entities, such as updating entities, handling state changes, and interacting with the Home Assistant API.
[`helper.py`](pyscript/modules/helper.py): This module provides helper functions and utilities for various tasks, such as evaluating expressions, handling state triggers, and managing time-based triggers.
[`mapping.py`](pyscript/modules/mapping.py): This module contains naming and string mapping as well as data transformation. 
[`settings.py`](pyscript/modules/settings.py): This module contains settings or configuration values specific to certain components or functionalities.
[`utils.py`](pyscript/modules/utils.py): This module contains utility functions for logging, setting log contexts, and other general-purpose tasks used throughout the project.

## Exemplary functionality

- **System Monitoring**: Monitoring of system resources and performance metrics.
- **Backup and Synchronization**: Automated backup and synchronization of the Home Assistant configuration and data.
- **Calendar Integration**: The project integrates with calendars (e.g., Apple iCloud, Google Calendar) to sync events and schedules.
- **Lovelace UI Customization**: Customization of the Home Assistant's Lovelace UI using various custom cards and plugins.
- **Weather Monitoring**: Integration with weather services to monitor and display current weather conditions.

## Images

![Desktop](www/overview-desktop.png)
![Mobile](www/overview-desktop.png)