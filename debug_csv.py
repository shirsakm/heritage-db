#!/usr/bin/env python3
"""
Diagnostic script to check CSV column names and sample data
"""

import csv
import sys
from pathlib import Path


def analyze_csv(file_path, batch_name):
    """Analyze CSV file structure"""
    print(f"\n=== Analysis for {batch_name} ===")
    print(f"File: {file_path}")

    if not Path(file_path).exists():
        print(f"❌ File not found: {file_path}")
        return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            # Get column names
            columns = reader.fieldnames
            print(f"📋 Columns ({len(columns)}): {', '.join(columns)}")

            # Get first few rows
            sample_rows = []
            for i, row in enumerate(reader):
                if i >= 3:  # Only get first 3 rows
                    break
                sample_rows.append(row)

            print(f"📊 Sample data ({len(sample_rows)} rows):")
            for i, row in enumerate(sample_rows, 1):
                print(f"  Row {i}: {row.get('Name', 'Unknown')}")
                for col in columns:
                    if col not in [
                        "Name",
                        "College Roll",
                        "Autonomy Roll",
                        "Branch",
                        "Department",
                    ]:
                        value = row.get(col, "N/A")
                        print(f"    {col}: {value}")
                print()

    except Exception as e:
        print(f"❌ Error reading file: {e}")


def main():
    """Main function"""
    print("🔍 CSV Column Analysis Tool")
    print("=" * 50)

    # Define batch files
    batches = {
        "2024": "data/2024/final.csv",
        "2023": "data/2023/final.csv",
        "2022": "data/2022/final.csv",
    }

    for batch, file_path in batches.items():
        analyze_csv(file_path, batch)

    print("\n✅ Analysis complete!")


if __name__ == "__main__":
    main()
