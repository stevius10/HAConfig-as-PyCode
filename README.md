# HAConfig-as-PyCode

HAConfig-as-PyCode is an event-driven, programmatic Home Assistant configuration project that leverages Python for enhanced reusability, encapsulation, and modular expandability. This project takes a hybrid approach, combining declarative data structures to describe entities with imperative logic to process these structures in an event-driven manner. It aims to provide an alternative approach to home automation more focused on developers compared to Home Assistant's default YAML-based declaration.

![Desktop](www/overview-desktop.png)

## Implementation

The core functionality of HAConfig-as-PyCode is built around an event-driven architecture, utilizing Python scripts with PyScript and Home Assistant's built-in automation capabilities to enable dynamic and responsive smart home behavior.

### Main home automation

- **[`auto_entities.py`](pyscript/auto_entities.py)**: Defines entity behavior based on deviating states and their correlated condition based behavior, leveraging the `AUTO_ENTITIES` data structure to map entities to their desired states.
- **[`auto_motion.py`](pyscript/auto_motion.py)**: Manages motion sensor-based automations, mapping sensors to actions using the `AUTO_MOTION_ENTITIES` data structure.
- **[`auto_notify.py`](pyscript/auto_notify.py)**: Sends notifications to other devices e. g. mobile, utilizing the `notify_immo` function, which parses housing offers from various Berlin housing associations.
- **[`config_control.py`](pyscript/config_control.py)**: Defines controller behavior and maps it to scenes and actions using the `CONFIG_CONTROL` data structure.

### Leverage home automation capabilities

#### Apps

- **[`services.py`](pyscript/apps/services.py)**: Defines a service factory that creates periodically executed services based on provided cron expressions, e.g., `filebackup.sh` for backing up Home Assistant configuration and data.
- **[`sync_git.py`](pyscript/apps/sync_git.py)**: Synchronizes the configuration automatically to this Git repository.

#### Scripts 

For the purpose of integration:
- **[`ha_helper.py`](pyscript/scripts/ha_helper.py)**: Provides helper functions for interacting with Home Assistant resources.
- **[`ha_system.py`](pyscript/scripts/ha_system.py)**: Manages system-related tasks, adopt configuration management tasks and system monitoring.

For the purpose of functionality:  
- **[`script_air_cleaner.py`](pyscript/scripts/script_air_cleaner.py)**: Controls automatic air purification based on pollen concentration, scheduled according to various thresholds.
- **[`script_off.py`](pyscript/scripts/script_off.py)**: Provides functionality to turn off all types of integrated entities, either individually or by domain.

### Modules

The `/pyscript/modules` directory contains reusable Python modules that encapsulate various functionalities used throughout the project that do not use homeassistant capabilities:

- **[`config.py`](pyscript/modules/config.py)**: Contains configuration settings used across the project, promoting code organization and maintainability.
- **[`entities.py`](pyscript/modules/entities.py)**: Describes the default desired state for entities and conditions for default behavior, such as timeouts.
- **[`helper.py`](pyscript/modules/helper.py)**: Provides helper functions and utilities for repeating general tasks such as defining conditions and expressions, handling state triggers, and managing time-based triggers.
- **[`mapping.py`](pyscript/modules/mapping.py)**: Contains naming and mappings to entities and device capabilities.
- **[`settings.py`](pyscript/modules/settings.py)**: Contains settings or configuration values specific to application logic. 
- **[`utils.py`](pyscript/modules/utils.py)**: Contains utility functions that do not use home automation capabilities. 

## Constraints

1. The folder structure is dictated by the PyScript integration. Given these restrictions, it aims for a well-structured and logical approach, leveraging the benefits of varied visibility offered by PyScript.
2. No error or warning logs should occur in consequence of implementation, which is implying a project's focus on stability and extended debugging functionality over features.

## Exemplary Functionality

- **System Monitoring**: Monitoring of system resources and performance metrics.
- **Backup and Synchronization**: Automated backup and synchronization of the Home Assistant configuration and data.
- **Berlin Housing Offers**: Scraping for housing offers and real estate listings from various companies in Berlin. 
- **Lovelace UI Customization**: Customization of Home Assistant's Lovelace UI, e. g.  **Calendar Integration** or **Weather Monitoring with Derived Metric Calculations**.

## Images

![Mobile](www/overview-mobile.png)