# HAConfig-as-PyCode

HAConfig-as-PyCode is an event-driven, programmatic Home Assistant configuration project that leverages Python for enhanced reusability, encapsulation, and modular expandability. This project offers an alternative automation approach, more focused on developers compared to Home Assistant's default YAML-based configuration.

![Desktop](www/overview-desktop.png)

## Implementation

HAConfig-as-PyCode is built around an event-driven architecture integrating Python using PyScript and Home Assistant's built-in automation capabilities. This project combines declarative data structures for desired state configuration with imperative logic to process these data structures in an event-driven manner, leveraging an MQTT broker.

### Main Home Automation

- **`auto_control.py`**: Defines control behavior for entities based on state triggers, managing actions through the `ENTITIES_CONTROL` data structure.
- **`auto_entities.py`**: Automates entity state management, including default states and timeout handling, using the `ENTITIES_AUTO` data structure.
- **`auto_motion.py`**: Manages motion sensor-based automations, mapping sensors to actions through the `ENTITIES_MOTION` data structure.
- **`auto_notify.py`**: Handles notifications to external devices, such as mobile phones, leveraging the `notify` function.
- **`auto_presence.py`**: Manages presence detection and actions based on indicators and exclusions defined in the `ENTITIES_PRESENCE` data structure.

### Home Automation Capabilities

For integration purposes:
- **`ha_helper.py`**: Provides helper functions for interaction with Home Assistant resources, focusing on system logging and log management.
- **`ha_system.py`**: Handles system-related setup, configuration management tasks, and environment setup.
- **`ha_utils.py`**: Contains utility functions for mobile notifications and event-based shortcuts.
- **`ha_off.py`**: Implements functionality to turn off various integrated entities, either individually or by domain.

For service-based purposes:
- **`sync_git.py`**: Enables automatic synchronization of the configuration to this Git repository.
- **`subprocesses.py`**: Manages and executes subprocesses based on predefined schedules and commands. Implements services by taking a list of shell commands from `/pyscript/modules/data.py`: 
  - **File Backup Service**: Runs a backup of Home Assistant configuration files at scheduled intervals.
  - **Compile Service**: Compiles and structures the project files, listing the project structure and content for code sharing, e. g. AI based programming.

### Modules

The `/pyscript/modules` directory contains reusable Python modules that encapsulate various functionalities used throughout the project, independent of Home Assistant capabilities.

- **`constants.py`**: Centralizes configuration settings, entity definitions, expressions, mappings, and settings by importing them from sub-modules:
  - **`config.py`**: Contains general configuration settings and paths.
  - **`data.py`**: Defines data structures used for automation, presence detection, subprocess services, and scraping housing providers.
  - **`entities.py`**: Describes the default desired state for entities and conditions for default behavior.
  - **`expressions.py`**: Contains cron and state expressions for various automation scenarios.
  - **`mappings.py`**: Provides mappings for states, services, events, and persistence prefixes.
  - **`settings.py`**: Contains specific configuration values for application and service logic.
- **`exceptions.py`**: Defines custom exception classes used for error handling within the project.
- **`utils.py`**: Contains central functions for generating expressions and implementing project-wide logging functionality.

### Native Python

Native Python is used within this project to handle privileged and I/O tasks that could potentially interfere with PyScript's main loop handling of asynchronous tasks.

- **`filesystem.py`**: Provides file system operations for tasks that require privileges beyond the PyScript sandbox.
- **`logfile.py`**: Manages structured logging operations, differentiating between a file logger for application or service logs and a debug logger for debugging purposes, implemented using a singleton pattern for project-wide accessibility.

### Customization

- **User Interface**: The project includes various custom templates for the Home Assistant Lovelace UI. These are implemented through the **`templates/`** directory and external data integration.

    - **`badges.yaml`**: Defines badge cards for displaying system status, backup information, air quality, and providing quick access to common actions like turning everything off.
    - **`bar.yaml`**: Implements customizable button bars for room-specific lighting and device control.
    - **`calendar.yaml`**: Includes a customized calendar view for displaying upcoming events from various calendars.
    - **`card-art.yaml`**: Provides a comprehensive overview card with weather information, badges, and a calendar view.
    - **`card.yaml`**: Defines room-specific overview cards with dynamic images, thermostat controls, and button bars.
    - **`clima.yaml`**: Implements a custom thermostat card with temperature graphs and trend indicators.
    - **`weather.yaml`**: Includes a weather forecast card and a custom weather display.

- **Backup and Synchronization**: Automated backup and synchronization of the Home Assistant configuration and data.

- **External Data**: The project integrates external data from various sources through sensors defined in the **`config/.sensors/`** directory:
  
  - **Housing Offers**: Scrapes and delivers housing offers and real estate listings from various companies in Berlin. The data is delivered via notifications to trigger mobile services.

- **Customized Shell**: The project includes a customized shell environment with an optimized configuration for the Zsh shell, located in **`files/.zshrc`**.

### Notifications

- **`scrape_housing.py`**: Scrapes housing offers from various providers, processes the data, and sends notifications to users about new listings.

### Logging

- **Log Management**: The project includes comprehensive logging functionality using the `logfile` module, with capabilities for structured logging, log rotation, and archival.

### Testing

- **Unit Tests and Mocks**: The project includes a suite of unit tests and mock classes to ensure robust testing of different components. Tests are located in the **`tests`** directory.

## Project Structure

```plaintext
apps/
  air_control.py
  scrape_housing.py
  sync_git.py
auto_control.py
auto_entities.py
auto_motion.py
auto_notify.py
auto_presence.py
modules/
  constants.py
  constants/
    config.py
    data.py
    entities.py
    expressions.py
    mappings.py
    settings.py
  exceptions.py
  utils.py
python/
  filesystem.py
  logfile.py
requirements.txt
scripts/
  ha_helper.py
  ha_off.py
  ha_system.py
  ha_utils.py
  subprocesses.py
  tests.py

```plaintext
config/
  assistant.yaml
  calendar.yaml
  frontend.yaml
  http.yaml
  log.yaml
  pyscript.yaml
  sensors.yaml
  timer.yaml
  utils.yaml
files/
  .zshrc