import csv
import re

INPUT_FILE = 'grades_.csv'
OUTPUT_FILE = 'grades_cleaned.csv'


# Regex to extract branch from the last column value
BRANCH_REGEX = re.compile(r'First Year [^ ]+ in (.+?) \([A-Z]+\)')

def extract_branch(full_string):
    match = BRANCH_REGEX.search(full_string)
    if match:
        return match.group(1).strip()
    # fallback: try to extract before 'Second Semester' if regex fails
    if ' in ' in full_string:
        s = full_string.split(' in ', 1)[1]
        return s.split(' Second Semester')[0].strip()
    return full_string

def is_all_na(row):
    # Only check columns after the first two
    return all(cell.strip() == 'N/A' for cell in row[2:])

def main():
    with open(INPUT_FILE, newline='', encoding='utf-8') as infile:
        reader = list(csv.reader(infile))
        if not reader:
            print('Input file is empty.')
            return
        header = reader[0]
        cleaned_rows = [header]
        for row in reader[1:]:
            if not is_all_na(row):
                # Replace last column with branch name if possible
                if len(row) > 5:
                    row[-1] = extract_branch(row[-1])
                cleaned_rows.append(row)
    # Write cleaned data
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(cleaned_rows)
    print(f'Cleaned data written to {OUTPUT_FILE}')

if __name__ == '__main__':
    main()
