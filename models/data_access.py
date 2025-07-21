# Data access layer for CSV operations

import csv
import logging
from typing import List, Dict, Optional, Any
from pathlib import Path

from config import config

# Set up logging
logger = logging.getLogger(__name__)


class DataAccessError(Exception):
    """Custom exception for data access errors"""
    pass


class CSVDataAccess:
    """Handles all CSV data operations"""
    
    def __init__(self):
        self.config = config
        self._validate_csv_files()
    
    def _validate_csv_files(self) -> None:
        """Validate that all CSV files exist"""
        for batch, file_path in self.config.CSV_FILES.items():
            if not Path(file_path).exists():
                logger.warning(f"CSV file for batch {batch} not found: {file_path}")
    
    def load_data(self, batch: str) -> List[Dict[str, Any]]:
        """
        Load data from CSV file for the specified batch
        
        Args:
            batch: The batch year (e.g., "2024", "2023", "2022")
            
        Returns:
            List of dictionaries containing student data
            
        Raises:
            DataAccessError: If the file cannot be read or batch is invalid
        """
        try:
            file_path = self.config.CSV_FILES.get(batch, self.config.CSV_FILES["2024"])
            
            if not Path(file_path).exists():
                raise DataAccessError(f"CSV file not found: {file_path}")
            
            with open(file_path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                data = list(reader)
            
            logger.info(f"Loaded {len(data)} records from {file_path}")
            return data
            
        except (IOError, OSError) as e:
            logger.error(f"Error reading CSV file {file_path}: {e}")
            raise DataAccessError(f"Failed to load data for batch {batch}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error loading data for batch {batch}: {e}")
            raise DataAccessError(f"Unexpected error loading data: {e}")
    
    def get_branches(self, data: List[Dict[str, Any]]) -> List[str]:
        """
        Extract unique branches/departments from the data
        
        Args:
            data: List of student records
            
        Returns:
            Sorted list of unique branches/departments
        """
        if not data:
            return []
        
        # Determine the correct key (Branch vs Department)
        key = "Branch" if "Branch" in data[0] else "Department"
        
        branches = set()
        for row in data:
            branch = row.get(key)
            if branch and branch.strip():
                branches.add(branch.strip())
        
        return sorted(branches)
    
    def get_available_batches(self) -> List[str]:
        """
        Get list of available batch years
        
        Returns:
            List of available batch years
        """
        return list(self.config.CSV_FILES.keys())
    
    def validate_batch(self, batch: str) -> bool:
        """
        Validate if the given batch exists
        
        Args:
            batch: The batch year to validate
            
        Returns:
            True if batch exists, False otherwise
        """
        return batch in self.config.CSV_FILES


# Create global data access instance
data_access = CSVDataAccess()
