from enum import Enum


class ScanStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class ScanResult(str, Enum):
    NONE = "NONE"
    CLEAN = "CLEAN"
    PROBLEM = "PROBLEM"

