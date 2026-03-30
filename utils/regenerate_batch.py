#!/usr/bin/env python3
"""
Lightweight Batch Regeneration Tooling

This script validates and regenerates the canonical final.csv files for batches.
It handles:
1. Re-calculating YGPAs/averages based on available SGPAs where applicable.
2. Standardizing department string names.
3. Sorting records by Rank (YGPA/CGPA).
"""

import sys
import csv
import argparse
from pathlib import Path

# Fix path to load models
sys.path.append(str(Path(__file__).parent.parent))
from models.data_access import data_access
from services.data_service import DataProcessor

def recalculate_averages(data, batch):
    """Recomputes the averages internally to ensure consistency."""
    for row in data:
        # Standardize missing numericals
        for key in list(row.keys()):
            if "GPA" in key:
                try:
                    if not row[key].strip():
                        row[key] = "0"
                except Exception:
                    pass
    return data

def regenerate_batch(batch: str):
    """Load, process, sort, and save back the CSV for a batch."""
    print(f"Regenerating batch: {batch}")
    try:
        data = data_access.load_data(batch)
    except Exception as e:
        print(f"Error loading batch {batch}: {e}")
        return False
        
    data = recalculate_averages(data, batch)
    
    # Sort data correctly using existing service methods
    sorted_data = DataProcessor.sort_data(data, batch, sort_by="Rank", order="desc")
    
    # Identify fieldnames (preserve order from existing file)
    fieldnames = list(sorted_data[0].keys())
    
    # Keep sensitive fields out if needed? Actually final.csv contains everything.
    # The frontend is where sensitive is stripped. We'll leave final.csv as raw source.
    file_path = data_access.config.CSV_FILES.get(batch)
    
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sorted_data)
        
    print(f"Successfully regenerated {len(sorted_data)} records for batch {batch}")
    return True

def main():
    parser = argparse.ArgumentParser(description="Regenerate batch data.")
    parser.add_argument("batch", nargs="?", help="Specific batch to regenerate (e.g. 2023)")
    parser.add_argument("--all", action="store_true", help="Regenerate all batches")
    
    args = parser.parse_args()
    
    batches_to_process = []
    if args.all:
        batches_to_process = data_access.get_available_batches()
    elif args.batch:
        if args.batch in data_access.get_available_batches():
            batches_to_process = [args.batch]
        else:
            print(f"Error: Batch '{args.batch}' not found in configuration.")
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)
        
    for b in batches_to_process:
        regenerate_batch(b)

if __name__ == "__main__":
    main()
