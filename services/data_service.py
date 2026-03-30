# Business logic for data processing and filtering

import logging
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass

# Set up logging
logger = logging.getLogger(__name__)


@dataclass
class FilterParams:
    """Parameters for filtering data"""

    search_query: Optional[str] = None
    selected_branches: Optional[List[str]] = None
    sort_by: Optional[str] = None
    order: str = "desc"


class DataProcessor:
    """Handles data processing, filtering, and sorting operations"""

    @staticmethod
    def safe_float(value: Any, reverse: bool = False) -> float:
        """
        Safely convert value to float with fallback for sorting

        Args:
            value: Value to convert
            reverse: Whether sorting is in reverse order

        Returns:
            Float value or infinity for invalid values
        """
        try:
            return float(value)
        except (ValueError, TypeError):
            return float("-inf") if reverse else float("inf")

    @staticmethod
    def calculate_average_ygpa(
        row: Dict[str, Any], batch: str, reverse: bool = False
    ) -> float:
        """
        Calculate average YGPA based on batch year

        Args:
            row: Student record
            batch: Batch year
            reverse: Whether sorting is in reverse order

        Returns:
            Average YGPA value
        """
        try:
            if batch == "2023":
                # 2023: 4 CGPAs, 2 YGPAs
                ygpa1 = float(row.get("YGPA 1", 0))
                ygpa2 = float(row.get("YGPA 2", 0))
                return (ygpa1 + ygpa2) / 2
            elif batch == "2022":
                # 2022: 6 CGPAs, 3 YGPAs
                ygpa1 = float(row.get("YGPA 1", 0))
                ygpa2 = float(row.get("YGPA 2", 0))
                ygpa3 = float(row.get("YGPA 3", 0))
                return (ygpa1 + ygpa2 + ygpa3) / 3
            else:
                # Default for 2024 and other batches
                return float(row.get("yGPA 1", 0))
        except (ValueError, TypeError):
            return float("-inf") if reverse else float("inf")

    @classmethod
    def filter_by_search(
        cls, data: List[Dict[str, Any]], search_query: str
    ) -> List[Dict[str, Any]]:
        """
        Filter data by search query in student names

        Args:
            data: List of student records
            search_query: Search string

        Returns:
            Filtered list of student records
        """
        if not search_query or not search_query.strip():
            return data

        search_term = search_query.strip().lower()
        filtered_data = []

        for row in data:
            name = row.get("Name", "").lower()
            if search_term in name:
                filtered_data.append(row)

        logger.info(f"Search '{search_query}' returned {len(filtered_data)} results")
        return filtered_data

    @classmethod
    def filter_by_branches(
        cls, data: List[Dict[str, Any]], selected_branches: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Filter data by selected branches/departments

        Args:
            data: List of student records
            selected_branches: List of selected branch names

        Returns:
            Filtered list of student records
        """
        # Filter out empty strings and None values
        valid_branches = [
            branch for branch in (selected_branches or []) if branch and branch.strip()
        ]

        if not valid_branches:
            logger.info("No branch filter applied - showing all records")
            return data

        if not data:
            return data

        # Determine the correct key (Branch vs Department)
        key = "Branch" if "Branch" in data[0] else "Department"

        filtered_data = []
        for row in data:
            if row.get(key) in valid_branches:
                filtered_data.append(row)

        logger.info(
            f"Branch filter '{', '.join(valid_branches)}' returned {len(filtered_data)} results"
        )
        return filtered_data

    @classmethod
    def sort_data(
        cls,
        data: List[Dict[str, Any]],
        batch: str,
        sort_by: Optional[str] = None,
        order: str = "desc",
    ) -> List[Dict[str, Any]]:
        """
        Sort data based on specified column and order

        Args:
            data: List of student records
            batch: Batch year for determining sort logic
            sort_by: Column to sort by
            order: Sort order ("asc" or "desc")

        Returns:
            Sorted list of student records
        """
        if not data:
            return data

        reverse = order == "desc"

        # Default sorting logic based on batch
        if not sort_by or sort_by == "Rank":
            # Sort by average YGPA for ranking
            sort_key = lambda row: cls.calculate_average_ygpa(row, batch, reverse)
            data.sort(key=sort_key, reverse=True)  # Always descending for ranking
        elif sort_by in data[0]:
            # Sort by specified column
            sort_key = lambda row: cls.safe_float(row.get(sort_by, "N/A"), reverse)
            data.sort(key=sort_key, reverse=reverse)
        else:
            logger.warning(f"Sort column '{sort_by}' not found in data")

        return data

    @classmethod
    def add_ranking(cls, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Add ranking to the data based on current order

        Args:
            data: List of student records

        Returns:
            Data with ranking added
        """
        for i, row in enumerate(data, 1):
            row["Rank"] = i

        return data

    @classmethod
    def clean_sensitive_data(cls, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Remove sensitive data from the records

        Args:
            data: List of student records

        Returns:
            Data with sensitive fields removed
        """
        sensitive_fields = ["Autonomy Roll"]

        for row in data:
            for field in sensitive_fields:
                if field in row:
                    del row[field]

        return data

    @classmethod
    def process_data(
        cls, data: List[Dict[str, Any]], batch: str, filter_params: FilterParams
    ) -> List[Dict[str, Any]]:
        """
        Apply all processing steps to the data

        Args:
            data: Raw student data
            batch: Batch year
            filter_params: Filter parameters

        Returns:
            Processed and filtered data
        """
        # Apply filters
        if filter_params.selected_branches:
            data = cls.filter_by_branches(data, filter_params.selected_branches)

        if filter_params.search_query:
            data = cls.filter_by_search(data, filter_params.search_query)

        # Sort data
        data = cls.sort_data(data, batch, filter_params.sort_by, filter_params.order)

        # Add ranking and clean sensitive data
        data = cls.add_ranking(data)
        data = cls.clean_sensitive_data(data)

        return data

    @classmethod
    def get_aggregate_stats(cls, data: List[Dict[str, Any]], batch: str) -> Dict[str, Any]:
        """
        Compute aggregate statistics for the batch
        """
        if not data:
            return {}

        key = "Branch" if "Branch" in data[0] else "Department"
        stats = {
            "branch_averages": {},
            "grade_distribution": {"Outstanding (>=9)": 0, "Excellent (8-9)": 0, "Good (7-8)": 0, "Average (6-7)": 0, "Below Average (<6)": 0},
        }

        branch_totals = {}
        branch_counts = {}

        for row in data:
            branch = row.get(key, "Unknown").strip()
            ygpa = cls.calculate_average_ygpa(row, batch)
            
            if ygpa and ygpa != float("-inf") and ygpa != float("inf") and ygpa > 0:
                branch_totals[branch] = branch_totals.get(branch, 0) + ygpa
                branch_counts[branch] = branch_counts.get(branch, 0) + 1
                
                # Distribution
                if ygpa >= 9.0:
                    stats["grade_distribution"]["Outstanding (>=9)"] += 1
                elif ygpa >= 8.0:
                    stats["grade_distribution"]["Excellent (8-9)"] += 1
                elif ygpa >= 7.0:
                    stats["grade_distribution"]["Good (7-8)"] += 1
                elif ygpa >= 6.0:
                    stats["grade_distribution"]["Average (6-7)"] += 1
                else:
                    stats["grade_distribution"]["Below Average (<6)"] += 1

        for branch in branch_totals:
            stats["branch_averages"][branch] = round(branch_totals[branch] / branch_counts[branch], 2)

        return stats

    @classmethod
    def get_student_details(cls, data: List[Dict[str, Any]], batch: str, roll_no: str) -> Optional[Dict[str, Any]]:
        """
        Extract specific student record and prepare SGPA trend data.
        """
        # Search by Name
        student = next((row for row in data if str(row.get('Name', '')) == str(roll_no)), None)
        if not student:
            return None
            
        trend = []
        labels = []
        for key, value in student.items():
            k_upper = key.strip().upper()
            if k_upper.startswith("SGPA") or k_upper.startswith("CGPA") or k_upper.startswith("GPA SEM"):
                val = cls.safe_float(value)
                if val != float('inf') and val > 0:
                    trend.append(val)
                    labels.append(key)
                    
        # Sort labels to ensure SGPA 1, SGPA 2, etc. are ordered correctly
        # Assuming keys are like "SGPA 1", "SGPA 2"
        try:
            sorted_pairs = sorted(zip(labels, trend), key=lambda x: int(x[0].split()[-1]))
            labels, trend = zip(*sorted_pairs) if sorted_pairs else ([], [])
        except Exception:
            pass

        return {
            "record": student,
            "trend_labels": list(labels),
            "trend_data": list(trend),
            "ygpa": cls.calculate_average_ygpa(student, batch)
        }

