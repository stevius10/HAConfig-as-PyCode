import sys
from unittest.mock import MagicMock, patch
from mocks.mock_pyscript import MockPyscript


class MockHelper:
    """
    Mock-Klasse für `ha_helper`-Funktionen.
    """
    def __init__(self, mock_task):
        self.task = mock_task
        self.file_read = MagicMock()
        self.file_write = MagicMock()

    async def ha_log_truncate(self, trigger_type, event_type=None):
        print(f"ha_log_truncate called with trigger_type={trigger_type}, event_type={event_type}")

    async def log_truncate(self, logfile, log_size_truncated, log_tail_size, log_history_size):
        print(f"log_truncate called with logfile={logfile}, log_size_truncated={log_size_truncated}, "
              f"log_tail_size={log_tail_size}, log_history_size={log_history_size}")

    async def log_rotate(self, file):
        print(f"log_rotate called with file={file}")


def setup_test_environment():
    """
    Bereitet das gesamte Test-Setup vor, einschließlich Patches und globaler Konfigurationen.
    Gibt das MockPyscript-Objekt, den MockTask und die Patches zurück.
    """
    mock_pyscript = MockPyscript()
    mock_task = mock_pyscript.MockTask()

    # Globale Funktionen bereitstellen
    global_namespace = globals()
    global_namespace.update({
        "task_unique": mock_pyscript.task_unique,
        "event_trigger": mock_pyscript.event_trigger,
        "state_trigger": mock_pyscript.state_trigger,
        "time_trigger": mock_pyscript.time_trigger,
        "state_active": mock_pyscript.state_active,
        "time_active": mock_pyscript.time_active,
    })

    # MockHaHelper als sys.modules["ha_helper"] einfügen
    mock_helper = MockHelper(mock_task)
    sys.modules["ha_helper"] = mock_helper

    # Patches aktivieren
    patches = [
        patch("ha_helper.task.sleep", mock_task.sleep),
        patch("ha_helper.task.wait_until", mock_task.wait_until),
    ]
    for p in patches:
        p.start()

    return mock_pyscript, mock_task, mock_helper, patches