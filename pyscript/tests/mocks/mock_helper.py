import sys
from unittest.mock import patch
from mocks.mock_pyscript import MockPyscript

def setup_helper(cls):
    def setup_helper(cls):
        class MockHelper:
            task = cls.mock_task
            event_trigger = globals()["event_trigger"]
            state_trigger = globals()["state_trigger"]
            time_trigger = globals()["time_trigger"]
            state_active = globals()["state_active"]
            time_active = globals()["time_active"]
            task_unique = globals()["task_unique"]

        return MockHelper()