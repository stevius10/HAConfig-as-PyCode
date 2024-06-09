# HAConfig-as-PyCode

HAConfig-as-PyCode is an event-driven, programmatic Home Assistant configuration project that utilizes Python for improved reusability, encapsulation, and modular expandability. Thus offering an alternative automation approach more focused on developers compared to Home Assistant's default YAML-based configuration.

![Desktop](www/overview-desktop.png)

## Implementation

HAConfig-as-PyCode is built around an event-driven architecture integrating Python using PyScript and Home Assistant's built-in automation capabilities. This project takes a hybrid approach, combining declarative data structures for desired state configuration with imperative logic to process these data structures in an event-driven manner leveraging a MQTT broker. 


### Main Home Automation

- **[`auto_entities.py`](pyscript/auto_entities.py)**: Defines entity behavior based on deviating states and their correlated condition-based actions, utilizing the `AUTO_ENTITIES` data structure for entity-state mapping.
- **[`auto_motion.py`](pyscript/auto_motion.py)**: Manages motion sensor-based automations, mapping sensors to actions through the `AUTO_MOTION_ENTITIES` data structure.
- **[`auto_notify.py`](pyscript/auto_notify.py)**: Handles notifications to external devices, e.g., mobile, employing the `notify_immo` function to parse and deliver housing offers from various Berlin housing associations.
- **[`config_control.py`](pyscript/config_control.py)**: Defines controller behavior and maps it to scenes and actions using the `CONFIG_CONTROL` data structure.

### Home Automation Capabilities

For integration purposes:
- **[`ha_helper.py`](pyscript/scripts/ha_helper.py)**: Provides helper functions for interaction with Home Assistant resources, focusing on system logging.
- **[`ha_system.py`](pyscript/scripts/ha_system.py)**: Handles system-related setup, configuration management tasks, and system monitoring.
- **[`ha_utils.py`](pyscript/scripts/ha_utils.py)**: Contains utility functions, e.g., mobile notifications and triggers for mobile event-based shortcuts.

For functionality purposes:
- **[`script_air_cleaner.py`](pyscript/scripts/script_air_cleaner.py)**: Implements automatic air purification control based on pollen concentration, with scheduling according to various thresholds.
- **[`script_off.py`](pyscript/scripts/script_off.py)**: Provides functionality to turn off all types of integrated entities, either individually or by domain.

For service-based purposes:
- **[`services.py`](pyscript/apps/services.py)**: Implements a service factory that generates periodically executed services based on provided cron expressions, e.g., `filebackup.sh` for automated backup of Home Assistant configuration and data.
- **[`sync_git.py`](pyscript/apps/sync_git.py)**: Enables automatic synchronization of the configuration to this Git repository.

### Modules

The `/pyscript/modules` directory contains reusable Python modules that encapsulate various functionalities used throughout the project, independent of Home Assistant capabilities.

- **[`constants.py`](pyscript/modules/constants.py)**
    - **[`config.py`](pyscript/modules/constants/config.py)**: Centralizes configuration settings used across the project, promoting code organization and maintainability.
    - **[`devices.py`](pyscript/modules/constants/devices.py)**: Manages device-specific configurations and mappings.
    - **[`entities.py`](pyscript/modules/constants/entities.py)**: Describes the default desired state for entities and conditions for default behavior, such as timeouts.
    - **[`events.py`](pyscript/modules/constants/events.py)**: Defines event constants used throughout the project.
    - **[`expressions.py`](pyscript/modules/constants/expressions.py)**: Contains expressions for various automation scenarios.
    - **[`mappings.py`](pyscript/modules/constants/mappings.py)**: Provides naming and mappings to entities and device capabilities.
    - **[`settings.py`](pyscript/modules/constants/settings.py)**: Contains settings or configuration values specific to application and service logic.

- **[`utils.py`](pyscript/modules/utils.py)**: Contains central functions for generating expressions and implements project-wide logging functionality

### Native Python

Native Python is used within this project to handle privileged and I/O tasks that could potentially interfere with PyScript's main loop handling of asynchronous tasks.

- **[`filesystem.py`](pyscript/python/filesystem.py)**: Provides file system operations for tasks that require privileges beyond the PyScript sandbox.
- **[`logfile.py`](pyscript/python/logfile.py)**: Manages structured logging operations, differentiating between a file logger for application or service logs and a debug logger for debugging purposes, implemented using a singleton pattern for project-wide accessibility.

### Customization

- **User Interface**: The project includes various custom templates for the Home Assistant Lovelace UI. These are implemented through the **[`templates/`](templates/)** directory and external data integration.

    -  **[`templates/badges.yaml`](templates/badges.yaml)**: Defines badge cards for displaying system status, backup information, air quality, and providing quick access to common actions like turning everything off.
    -  **[`templates/bar.yaml`](templates/bar.yaml)**: Implements customizable button bars for room-specific lighting and device control.
    -  **[`templates/calendar.yaml`](templates/calendar.yaml)**: Includes a customized calendar view for displaying upcoming events from various calendars.
    -  **[`templates/card-art.yaml`](templates/card-art.yaml)**: Provides a comprehensive overview card with weather information, badges, and a calendar view.
    -  **[`templates/card.yaml`](templates/card.yaml)**: Defines room-specific overview cards with dynamic images, thermostat controls, and button bars.
    -  **[`templates/clima.yaml`](templates/clima.yaml)**: Implements a custom thermostat card with temperature graphs and trend indicators.
    -  **[`templates/weather.yaml`](templates/weather.yaml)**: Includes a weather forecast card and a custom weather display.

- **Backup and Synchronization**: Automated backup and synchronization of the Home Assistant configuration and data.

- **External Data**: The project integrates external data from various sources through sensors defined in the **[`config/.sensors/`](config/.sensors/)** directory:

    -  **Housing Offers**: Scrapes and delivers housing offers and real estate listings from various companies in Berlin. The data is delivered via notifications to trigger mobile services.

- **Customized Shell**: The project includes a customized shell environment with an optimized configuration for the Zsh shell, located in **[`files/.zshrc`](files/.zshrc)**.