import sys
import unittest
from unittest.mock import MagicMock, patch
import asyncio
from datetime import datetime

from mocks.mock_pyscript import MockPyscript


class TestHaHelper(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Pyscript-Mock initialisieren
        cls.mock_pyscript = MockPyscript()
        cls.mock_task = cls.mock_pyscript.MockTask()

        # Globale Namespace-Konfiguration
        global_namespace = globals()
        global_namespace.update({
            "task_unique": cls.mock_pyscript.task_unique,
            "event_trigger": cls.mock_pyscript.event_trigger,
            "state_trigger": cls.mock_pyscript.state_trigger,
            "time_trigger": cls.mock_pyscript.time_trigger,
            "state_active": cls.mock_pyscript.state_active,
            "time_active": cls.mock_pyscript.time_active,
        })

        # `ha_helper` in den Namespace mocken
        sys.modules["ha_helper"] = cls.create_mock_ha_helper()

        # Funktionen aus ha_helper patchen
        cls.patches = [
            patch("ha_helper.task.sleep", cls.mock_task.sleep),
            patch("ha_helper.task.wait_until", cls.mock_task.wait_until),
            patch("constants.config.CFG_PATH_FILE_LOG", 'test.log'),  # Standardpfad überschreiben
        ]
        for p in cls.patches:
            p.start()

    @classmethod
    def tearDownClass(cls):
        patch.stopall()

    @classmethod
    def create_mock_ha_helper(cls):
        class MockHaHelper:
            task = cls.mock_task
            event_trigger = globals()["event_trigger"]
            state_trigger = globals()["state_trigger"]
            time_trigger = globals()["time_trigger"]
            state_active = globals()["state_active"]
            time_active = globals()["time_active"]
            task_unique = globals()["task_unique"]

            def __init__(self):
                # Dateioperationen als Mock bereitstellen
                self.file_read = MagicMock()
                self.file_write = MagicMock()

            # Mock-Implementierung der Funktionen
            async def ha_log_truncate(self, trigger_type, event_type=None):
                print(f"ha_log_truncate called with trigger_type={trigger_type}, event_type={event_type}")

            async def log_truncate(self, logfile, log_size_truncated, log_tail_size, log_history_size):
                print(f"log_truncate called with logfile={logfile}, log_size_truncated={log_size_truncated}, "
                      f"log_tail_size={log_tail_size}, log_history_size={log_history_size}")

            async def log_rotate(self, file):
                print(f"log_rotate called with file={file}")

        return MockHaHelper()

    def setUp(self):
        # Gemockte Dateioperationen importieren
        from ha_helper import file_read, file_write
        self.file_read = file_read
        self.file_write = file_write

    def test_ha_log_truncate_event_modified(self):
        # Mock-Daten für file_read bereitstellen
        self.file_read.side_effect = [
            ['log1', 'log2', 'log3'],      # Dateiinhalt
            ['history1', 'history2']       # Historie
        ]

        async def run_test():
            from ha_helper import ha_log_truncate
            await ha_log_truncate(trigger_type="event", event_type="modified")
            self.file_read.assert_any_call('test.log')

        asyncio.run(run_test())

    def test_log_truncate(self):
        # Mock-Daten für file_read bereitstellen
        self.file_read.side_effect = [
            ['line1', 'line2', 'line3', 'line4', 'line5'],  # Dateiinhalt
            ['history1', 'history2']                       # Historie
        ]

        async def run_test():
            from ha_helper import log_truncate
            await log_truncate(
                logfile='test.log',  # Pfad explizit setzen
                log_size_truncated=2,
                log_tail_size=2,
                log_history_size=4
            )
            self.file_write.assert_any_call(
                'test.log',
                ['line4', 'line5', '# 5 / 2 at ' + str(datetime.now()) + '\n']
            )
            self.file_write.assert_any_call(
                'test.log.history',
                ['line3', 'line4', 'line5', 'history1', 'history2']
            )

        asyncio.run(run_test())

    def test_log_rotate(self):
        # Mock-Daten für file_read bereitstellen
        self.file_read.side_effect = [
            ['line1', 'line2', 'line3'],  # Dateiinhalt
            ['archive1', 'archive2']      # Archivinhalt
        ]

        async def run_test():
            from ha_helper import log_rotate
            await log_rotate(file='test.log')

            self.file_write.assert_called_with(
                'test.log.archive',
                ['line3', 'line2', 'line1', 'archive1', 'archive2']
            )

        asyncio.run(run_test())


if __name__ == "__main__":
    unittest.main()