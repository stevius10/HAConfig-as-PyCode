# HAConfig-as-PyCode

HAConfig-as-PyCode is an event-driven, programmatic Home Assistant configuration project that leverages Python for enhanced reusability, encapsulation, and modular expandability. This project adopts a hybrid approach, combining declarative data structures to describe entities with imperative logic to process these structures in an event-driven manner. It aims to provide a robust alternative to Home Assistant's default YAML configuration, enhancing configurational capabilities for developers.

![Desktop](www/overview-desktop.png)

## Implementation

The core functionality of HAConfig-as-PyCode is built around an event-driven architecture, utilizing Python scripts with PyScript and Home Assistant's built-in automation capabilities to enable dynamic and responsive smart home behavior.

### Key Scripts

- **[`auto_entities.py`](pyscript/auto_entities.py)**: Defines entity behavior based on deviating states and their correlated timeouts, leveraging the `AUTO_ENTITIES` data structure to map entities to their desired states.
- **[`auto_motion.py`](pyscript/auto_motion.py)**: Manages motion sensor-based automations, mapping sensors to actions using the `AUTO_MOTION_ENTITIES` data structure.
- **[`auto_notify.py`](pyscript/auto_notify.py)**: Sends notifications to mobile devices or channels based on state changes, utilizing the `notify_immo` function, which uses BeautifulSoup to parse housing offers from various Berlin housing associations.
- **[`config_control.py`](pyscript/config_control.py)**: Defines controller behavior and maps it to scenes and actions using the `CONFIG_CONTROL` data structure.

### Additional Scripts

- **[`ha_helper.py`](pyscript/scripts/ha_helper.py)**: Provides helper functions for interacting with Home Assistant resources, including logging.
- **[`ha_system.py`](pyscript/scripts/ha_system.py)**: Manages system-related tasks, such as configuration management and system monitoring.
- **[`script_air_cleaner.py`](pyscript/scripts/script_air_cleaner.py)**: Controls automatic air purification based on pollen concentration, scheduled according to various thresholds.
- **[`script_off.py`](pyscript/scripts/script_off.py)**: Offers functionality to turn off entities based on conditions such as being away or shutdown, ensuring their state.
- **[`services.py`](pyscript/apps/services.py)**: Defines a service factory that creates periodically executed services based on provided cron expressions, e.g., `filebackup.sh` for backing up Home Assistant configuration and data.
- **[`sync_git.py`](pyscript/apps/sync_git.py)**: Synchronizes the configuration automatically to this Git repository.

### Modules

The `/pyscript/modules` directory contains reusable Python modules that encapsulate various functionalities used throughout the project:

- **[`config.py`](pyscript/modules/config.py)**: Contains configuration settings used across the project, promoting code organization and maintainability.
- **[`entities.py`](pyscript/modules/entities.py)**: Describes the default desired state for entities and conditions for behavior, such as timeouts.
- **[`helper.py`](pyscript/modules/helper.py)**: Provides helper functions and utilities for tasks such as defining conditions and expressions, handling state triggers, and managing time-based triggers.
- **[`mapping.py`](pyscript/modules/mapping.py)**: Contains naming and string mappings.
- **[`settings.py`](pyscript/modules/settings.py)**: Contains settings or configuration values specific to certain components or functionalities.
- **[`utils.py`](pyscript/modules/utils.py)**: Contains utility functions for logging, contexts, and other general-purpose tasks used throughout the project.

## Exemplary Functionality

- **System Monitoring**: Monitoring of system resources and performance metrics.
- **Backup and Synchronization**: Automated backup and synchronization of the Home Assistant configuration and data.
- **Berlin Housing Offers**: Scraping for housing offers and real estate listings from various companies in Berlin.
- **Lovelace UI Customization**: Customization of Home Assistant's Lovelace UI, including **Calendar Integration** and **Weather Monitoring with Derived Metric Calculations**.

## Images

![Mobile](www/overview-mobile.png)