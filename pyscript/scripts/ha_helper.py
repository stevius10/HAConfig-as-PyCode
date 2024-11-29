import os
import sys
import unittest
from unittest.mock import AsyncMock, patch, MagicMock
import asyncio
from datetime import datetime

from constants.config import *
from ha_helper import ha_log_truncate, log_truncate, log_rotate, file_read, file_write

class TestHaHelper(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pyscript_paths = [
            '/config/pyscript',
            '/config/pyscript/apps',
            '/config/pyscript/modules',
            '/config/pyscript/scripts',
            '/config/pyscript/tests',
            '/config/pyscript/tests/unit',
            '/config/pyscript/tests/integration',
            '/config/pyscript/tests/functional'
        ]
        for path in pyscript_paths:
            if path not in sys.path:
                sys.path.append(path)

        cls.mock_files = {
            CFG_PATH_FILE_LOG: ['line1\n', 'line2\n', 'line3\n', 'line4\n', 'line5\n'],
            f"{CFG_PATH_FILE_LOG}.{CFG_LOG_HISTORY_SUFFIX}": ['history1\n', 'history2\n'],
            f"{CFG_PATH_FILE_LOG}.{CFG_LOG_ARCHIV_SUFFIX}": ['archive1\n', 'archive2\n'],
        }

    def setUp(self):
        self.file_read_patch = patch("ha_helper.file_read", new=AsyncMock(side_effect=self.mock_file_read))
        self.file_write_patch = patch("ha_helper.file_write", new=AsyncMock())
        self.mock_file_read = self.file_read_patch.start()
        self.mock_file_write = self.file_write_patch.start()
        self.sleep_patch = patch("ha_helper.task.sleep", new=AsyncMock())
        self.mock_sleep = self.sleep_patch.start()

    def tearDown(self):
        self.file_read_patch.stop()
        self.file_write_patch.stop()
        self.sleep_patch.stop()

    def mock_file_read(self, logfile):
        return self.mock_files.get(logfile, [])

    def test_ha_log_truncate_time_trigger(self):
        async def run_test():
            await ha_log_truncate(trigger_type="time")
            self.mock_file_write.assert_called_with(CFG_PATH_FILE_LOG, [])
            self.mock_sleep.assert_awaited_with(CFG_LOG_SETTINGS_DELAY_BLOCK)
        asyncio.run(run_test())

    def test_ha_log_truncate_event_trigger(self):
        async def run_test():
            await ha_log_truncate(trigger_type="event", event_type="modified")
            self.mock_file_write.assert_any_call(CFG_PATH_FILE_LOG, ['line4\n', 'line5\n', f"# 5 / 2 at {datetime.now()}\n"])
            self.mock_file_write.assert_any_call(
                f"{CFG_PATH_FILE_LOG}.{CFG_LOG_HISTORY_SUFFIX}",
                ['line3\n', 'line4\n', 'line5\n', 'history1\n', 'history2\n']
            )
            self.mock_sleep.assert_awaited_with(CFG_LOG_SETTINGS_DELAY_BLOCK)
        asyncio.run(run_test())

    def test_log_truncate(self):
        async def run_test():
            await log_truncate()
            self.mock_file_write.assert_any_call(CFG_PATH_FILE_LOG, ['line4\n', 'line5\n', f"# 5 / 2 at {datetime.now()}\n"])
            self.mock_file_write.assert_any_call(
                f"{CFG_PATH_FILE_LOG}.{CFG_LOG_HISTORY_SUFFIX}",
                ['line3\n', 'line4\n', 'line5\n', 'history1\n', 'history2\n']
            )
        asyncio.run(run_test())

    def test_log_rotate(self):
        async def run_test():
            await log_rotate()
            self.mock_file_write.assert_any_call(
                f"{CFG_PATH_FILE_LOG}.{CFG_LOG_ARCHIV_SUFFIX}",
                ['history2\n', 'history1\n', 'archive1\n', 'archive2\n']
            )
            self.mock_file_write.assert_called_with(CFG_PATH_FILE_LOG, [])
        asyncio.run(run_test())

    def test_file_read(self):
        async def run_test():
            content = await file_read(CFG_PATH_FILE_LOG)
            self.assertEqual(content, ['line1\n', 'line2\n', 'line3\n', 'line4\n', 'line5\n'])
        asyncio.run(run_test())

    def test_file_write(self):
        async def run_test():
            result = await file_write(CFG_PATH_FILE_LOG, ['new line 1\n', 'new line 2\n'])
            self.assertTrue(result)
            self.mock_file_write.assert_called_with(CFG_PATH_FILE_LOG, ['new line 1\n', 'new line 2\n'])
        asyncio.run(run_test())

if __name__ == "__main__":
    unittest.main()