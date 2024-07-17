# HAConfig-as-PyCode

HAConfig-as-PyCode is an event-driven, programmatic Home Assistant configuration project that leverages Python for enhanced reusability, encapsulation, and modular expandability. This project offers an alternative automation approach, focusing more on developers compared to Home Assistant's default YAML-based configuration.

![Desktop](www/overview-desktop.png)

## Implementation

HAConfig-as-PyCode is built around an event-driven architecture integrating Python using PyScript and Home Assistant's built-in automation capabilities. It combines declarative data structures for desired state configuration with imperative logic to process these data structures in an event-driven manner, leveraging an MQTT broker.

### Main Home Automation

- **[`auto_control.py`](pyscript/auto_control.py)**: Defines control behavior for entities based on state triggers, managing actions through the `ENTITIES_CONTROL` data structure with multi-condition handling.
- **[`auto_entities.py`](pyscript/auto_entities.py)**: Automates entity state management, including default states and timeout handling, using the `ENTITIES_AUTO` data structure with fallback mechanisms.
- **[`auto_motion.py`](pyscript/auto_motion.py)**: Motion sensor-based automations, mapping motion sensors to actions through the `ENTITIES_MOTION` data structure with adaptive lighting.
- **[`auto_notify.py`](pyscript/auto_notify.py)**: Handles external communication via notifications, using the `DATA_DEVICES` structure from `data.py` for mobile push notifications and automation shortcuts.
- **[`auto_presence.py`](pyscript/auto_presence.py)**: Manages presence detection and actions based on weighted indicators and exclusions in the `ENTITIES_PRESENCE` data structure.

### Home Automation Capabilities

- **[`ha_helper.py`](pyscript/scripts/ha_helper.py)**: Helper functions for interacting with Home Assistant resources, focusing on system logging and diagnostics.
- **[`ha_system.py`](pyscript/scripts/ha_system.py)**: Manages system-related setup, configuration tasks, and configure environment.
- **[`ha_utils.py`](pyscript/scripts/ha_utils.py)**: Utility functions for mobile notifications and event shortcuts, using the `DATA_DEVICES` structure for managing notification targets.
- **[`ha_off.py`](pyscript/scripts/ha_off.py)**: Implements functionality to turn off various entities.

### Services

- **[`air_control.py`](pyscript/apps/air_control.py)**: Controls air based functionality. 
- **[`scrape_housing.py`](pyscript/apps/scrape_housing.py)**: Scrapes housing offers from various Berlin housing providers, processes data, and sends notifications using the `DATA_SCRAPE_HOUSING_PROVIDERS` structure. Integrates with `auto_notify.py` for push notifications and mobile shortcuts via `ha_utils.py`.

### Service-based Automations

- **[`subprocesses.py`](pyscript/scripts/subprocesses.py)**: Manages and executes scheduled subprocesses and commands from `data.py`:
  - **File Backup**: Scheduled backups of Home Assistant configuration files.
  - **Git Sync**: Automatic synchronization of the configuration to the Git repository.
  - **Compile**: Compiles project files, listing the structure and contents at specified times using `time_trigger`.

### Modules

- **[`constants.py`](pyscript/modules/constants.py)**: Centralizes configuration settings, entity definitions, expressions, mappings, and settings by importing them from sub-modules:
  - **[`config.py`](pyscript/modules/constants/config.py)**: General configuration settings and structure.
  - **[`data.py`](pyscript/modules/constants/data.py)**: Specific input data for automations. 
  - **[`entities.py`](pyscript/modules/constants/entities.py)**: Default state for entities and conditions for behavior.
  - **[`expressions.py`](pyscript/modules/constants/expressions.py)**: Expressions for various automation scenarios.
  - **[`mappings.py`](pyscript/modules/constants/mappings.py)**: Naming, mappings in particular. 
  - **[`settings.py`](pyscript/modules/constants/settings.py)**: Specific configuration values for independent service logic.
- **[`exceptions.py`](pyscript/modules/exceptions.py)**: Custom exception classes for error handling with enhanced reporting.
- **[`utils.py`](pyscript/modules/utils.py)**: Central functions for project-wide logging including log rotate and expression generation.

### Native Python

- **[`filesystem.py`](pyscript/python/filesystem.py)**: File system operations for tasks requiring privileges beyond the PyScript sandbox.
- **[`logfile.py`](pyscript/python/logfile.py)**: Structured file logging operations with a partly singleton pattern for consistent log handling. 