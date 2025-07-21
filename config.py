# Configuration settings for the application

import os
from dataclasses import dataclass
from typing import Dict


@dataclass
class Config:
    """Application configuration settings"""

    # File paths
    DATA_DIR: str = "data"
    CSV_FILES: Dict[str, str] = None

    # Flask settings
    DEBUG: bool = True
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "dev-key-change-in-production")

    # Pagination settings
    DEFAULT_PAGE_SIZE: int = 50
    MAX_PAGE_SIZE: int = 200

    # Sorting settings
    DEFAULT_SORT_COLUMN: str = "yGPA 1"
    DEFAULT_SORT_ORDER: str = "desc"

    def __post_init__(self):
        """Initialize CSV files mapping after creation"""
        if self.CSV_FILES is None:
            self.CSV_FILES = {
                "2024": f"{self.DATA_DIR}/2024/final.csv",
                "2023": f"{self.DATA_DIR}/2023/final.csv",
                "2022": f"{self.DATA_DIR}/2022/final.csv",
            }


# Create global config instance
config = Config()
