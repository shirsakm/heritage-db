import csv

INPUT_FILE = "grades_cleaned.csv"
OUTPUT_FILE = "grades_with_ygpa.csv"


def safe_float(val):
    try:
        return float(val)
    except Exception:
        return None


def main():
    with open(INPUT_FILE, newline="", encoding="utf-8") as infile:
        reader = list(csv.reader(infile))
        if not reader:
            print("Input file is empty.")
            return
        header = reader[0]
        # Insert yGPA 1 column after GPA Sem 2
        new_header = header[:5] + ["yGPA 1"] + header[5:]
        rows = [new_header]
        for row in reader[1:]:
            gpa1 = safe_float(row[3])
            gpa2 = safe_float(row[4])
            if gpa1 is not None and gpa2 is not None:
                ygpa = f"{(gpa1 + gpa2) / 2:.2f}"
            else:
                ygpa = "N/A"
            new_row = row[:5] + [ygpa] + row[5:]
            rows.append(new_row)
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        writer.writerows(rows)
    print(f"Output written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
