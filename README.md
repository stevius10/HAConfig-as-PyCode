# HAConfig-as-PyCode

HAConfig-as-PyCode is an event-driven, programmatic Home Assistant configuration project leveraging Python for enhanced reusability, encapsulation, and modular expandability. This project provides an alternative automation approach, focusing on developers compared to Home Assistant's default YAML-based configuration.

![Desktop](www/overview-desktop.png)

---

## Implementation

HAConfig-as-PyCode is built on an event-driven architecture, integrating Python via PyScript and Home Assistant's built-in automation capabilities. It combines declarative data structures for desired state configuration with imperative logic to process these data structures in an event-driven manner, leveraging an MQTT broker.

### Main Home Automation

- **[`auto_control.py`](pyscript/auto_control.py)**: Manages control behavior for entities based on state triggers, utilizing the `ENTITIES_CONTROL` data structure with multi-condition handling.
- **[`auto_entities.py`](pyscript/auto_entities.py)**: Automates entity state management, including default states and timeout handling, using the `ENTITIES_AUTO` data structure with fallback mechanisms.
- **[`auto_motion.py`](pyscript/auto_motion.py)**: Implements motion sensor-based automations, mapping motion sensors to actions through the `ENTITIES_MOTION` data structure with adaptive lighting.
- **[`auto_notify.py`](pyscript/auto_notify.py)**: Manages external communication via notifications, leveraging the `DATA_DEVICES` structure from `data.py` for mobile push notifications and automation shortcuts.
- **[`auto_presence.py`](pyscript/auto_presence.py)**: Handles presence detection and actions based on weighted indicators and exclusions in the `ENTITIES_PRESENCE` data structure.

### Home Automation Capabilities

- **[`ha_helper.py`](pyscript/scripts/ha_helper.py)**: Provides comprehensive helper functions for interacting with Home Assistant resources like system logging and generic utility operations.
- **[`ha_system.py`](pyscript/scripts/ha_system.py)**: Manages system-related setup, configuration tasks, and environmental settings, handling runtime initialization and integration routines.
- **[`ha_utils.py`](pyscript/scripts/ha_utils.py)**: Includes utility functions for mobile notifications and event shortcuts, using the `DATA_DEVICES` structure for managing notification targets.
- **[`ha_off.py`](pyscript/scripts/ha_off.py)**: Implements functionality to turn off various entities.

### Services

- **[`air_control.py`](pyscript/apps/air_control.py)**: Controls air-based functionality.
- **[`scrape_housing.py`](pyscript/apps/scrape_housing.py)**: Scrapes housing offers from various Berlin housing providers, processes data, and sends notifications using the `DATA_SCRAPE_HOUSING_PROVIDERS` structure. Integrates with `auto_notify.py` for push notifications and mobile shortcuts via `ha_utils.py`.
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
  - **[`mappings.py`](pyscript/modules/constants/mappings.py)**: Naming and mappings.
  - **[`settings.py`](pyscript/modules/constants/settings.py)**: Specific configuration values for independent service logic.
- **[`generic.py`](pyscript/modules/generic.py)**: Generic classes like various enumerations and custom exceptions for error handling.
- **[`utils.py`](pyscript/modules/utils.py)**: Central functions for project-wide logging, log rotation, expression generation, and diagnostics.

---

## Project Structure

```json
{
  "project_overview": {
    "structure": [
      {
        "name": "pyscript",
        "description": "Core directory for Home Assistant automations and reusable logic.",
        "contents": [
          {
            "name": "apps",
            "description": "Contains application-specific automation scripts.",
            "dependencies": ["modules/constants", "modules/utils"],
            "files": [
              {
                "name": "air_control.py",
                "description": "Automates air control.",
                "depends_on": [
                  "modules/constants/config.py",
                  "modules/constants/entities.py",
                  "modules/constants/expressions.py",
                  "modules/constants/mappings.py",
                  "modules/constants/settings.py",
                  "modules/utils.py"
                ]
              },
              {
                "name": "app_debug.py",
                "description": "Debugging tools for testing.",
                "depends_on": [
                  "modules/constants/expressions.py",
                  "modules/constants/secrets.py",
                  "modules/constants/settings.py",
                  "modules/utils.py"
                ]
              },
              {
                "name": "run_tests.py",
                "description": "Executes test cases.",
                "depends_on": [
                  "modules/utils.py"
                ]
              },
              {
                "name": "scrape_housing.py",
                "description": "Scrapes housing data.",
                "depends_on": [
                  "modules/constants/config.py",
                  "modules/constants/data.py",
                  "modules/constants/expressions.py",
                  "modules/constants/mappings.py",
                  "modules/constants/settings.py",
                  "modules/utils.py"
                ]
              },
              {
                "name": "subprocesses.py",
                "description": "Handles subprocess execution.",
                "depends_on": [
                  "modules/constants/data.py",
                  "modules/constants/mappings.py",
                  "modules/utils.py"
                ]
              }
            ]
          },
          {
            "name": "modules",
            "description": "Reusable components for constants and utilities.",
            "contents": [
              {
                "name": "constants",
                "description": "Defines global constants used across automations.",
                "files": [
                  {
                    "name": "config.py",
                    "description": "Configuration constants.",
                    "depends_on": ["modules/constants/secrets.py"]
                  },
                  {
                    "name": "data.py",
                    "description": "Data-related constants.",
                    "depends_on": [
                      "modules/constants/expressions.py",
                      "modules/constants/secrets.py",
                      "modules/constants/settings.py",
                      "modules/utils.py"
                    ]
                  },
                  {
                    "name": "entities.py",
                    "description": "Entity mappings.",
                    "depends_on": [
                      "modules/constants/settings.py",
                      "modules/utils.py"
                    ]
                  },
                  {
                    "name": "expressions.py",
                    "description": "Predefined expressions.",
                    "depends_on": []
                  },
                  {
                    "name": "mappings.py",
                    "description": "Mappings for state handling.",
                    "depends_on": []
                  },
                  {
                    "name": "settings.py",
                    "description": "General project settings.",
                    "depends_on": []
                  }
                ]
              },
              {
                "name": "utils",
                "description": "Provides shared helper functions for debugging and automation tasks.",
                "depends_on": [
                  "modules/constants/config.py",
                  "modules/constants/mappings.py",
                  "modules/generic.py"
                ]
              }
            ]
          },
          {
            "name": "scripts",
            "description": "High-level automation scripts integrating constants and utilities.",
            "dependencies": ["modules/constants", "modules/utils"]
          },
          {
            "name": "tests",
            "description": "Test cases for validating scripts and modules.",
            "dependencies": ["apps", "modules"]
          }
        ]
      },
      {
        "name": "templates",
        "description": "Dashboard and UI templates for Home Assistant."
      },
      {
        "name": "www",
        "description": "Static assets for the Home Assistant frontend, such as CSS, images, and JavaScript."
      }
    ]
  },
  "dependency_map": {
    "relationships": [
      {
        "source": "pyscript/apps/air_control.py",
        "targets": [
          "pyscript/modules/constants/config.py",
          "pyscript/modules/constants/entities.py",
          "pyscript/modules/constants/expressions.py",
          "pyscript/modules/constants/mappings.py",
          "pyscript/modules/constants/settings.py",
          "pyscript/modules/utils.py"
        ]
      },
      {
        "source": "pyscript/apps/app_debug.py",
        "targets": [
          "pyscript/modules/constants/expressions.py",
          "pyscript/modules/constants/secrets.py",
          "pyscript/modules/constants/settings.py",
          "pyscript/modules/utils.py"
        ]
      },
      {
        "source": "pyscript/apps/run_tests.py",
        "targets": [
          "pyscript/modules/utils.py"
        ]
      },
      {
        "source": "pyscript/apps/scrape_housing.py",
        "targets": [
          "pyscript/modules/constants/config.py",
          "pyscript/modules/constants/data.py",
          "pyscript/modules/constants/expressions.py",
          "pyscript/modules/constants/mappings.py",
          "pyscript/modules/constants/settings.py",
          "pyscript/modules/utils.py"
        ]
      },
      {
        "source": "pyscript/apps/subprocesses.py",
        "targets": [
          "pyscript/modules/constants/data.py",
          "pyscript/modules/constants/mappings.py",
          "pyscript/modules/utils.py"
        ]
      }
    ]
  },
  "access_guidelines": {
    "paths": [
      {
        "path": "pyscript/apps",
        "description": "Explore application-specific automation logic."
      },
      {
        "path": "pyscript/modules/constants",
        "description": "Access global constants for entity definitions and behavior settings."
      },
      {
        "path": "pyscript/modules/utils",
        "description": "Use shared utility functions for debugging and automation."
      },
      {
        "path": "pyscript/scripts",
        "description": "Review high-level logic combining constants and utilities."
      },
      {
        "path": "templates",
        "description": "Browse reusable UI templates for dashboards."
      },
      {
        "path": "www",
        "description": "Locate static assets for frontend integration."
      }
    ]
  }
}
```
