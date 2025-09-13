import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException


def get_grades_2021():
    driver = webdriver.Firefox()
    driver.get("http://111.93.160.42:8084/stud25e.aspx")

    f = open("data/2021/grades_2021.csv", "w", newline="")
    writer = csv.writer(f)
    writer.writerow(
        [
            "Autonomy Roll",
            "Name",
            "CGPA 1",
            "CGPA 2",
            "YGPA 1",
            "CGPA 3",
            "CGPA 4",
            "YGPA 2",
            "CGPA 5",
            "CGPA 6",
            "YGPA 3",
            "CGPA 7",
            "CGPA 8",
            "YGPA 4",
            "Department",
        ]
    )

    missing = set()
    for branch_code in range(1, 21):
        null_count = 0
        for roll_num in range(1, 201):
            if null_count >= 10:
                break
            autonomy_roll = f"126210{str(branch_code).zfill(2)}{str(roll_num).zfill(3)}"
            # Initialize all variables
            cgpa_1 = cgpa_2 = ygpa_1 = cgpa_3 = cgpa_4 = ygpa_2 = cgpa_5 = cgpa_6 = ygpa_3 = cgpa_7 = cgpa_8 = ygpa_4 = name = dept = "N/A"
            
            # Try Sem 2 (1st year)
            driver.find_element(By.NAME, "roll").clear()
            driver.find_element(By.NAME, "roll").send_keys(autonomy_roll)
            select = Select(driver.find_element(By.NAME, "sem"))
            select.select_by_value("2")
            driver.find_element(By.ID, "Button1").click()
            try:
                name = " ".join(
                    driver.find_element(By.ID, "lblname").text.split()[2:]
                ).title()
                dept = driver.find_element(By.ID, "lbltop").text
                cgpa_1 = driver.find_element(By.ID, "lblbottom1").text.split()[-1]
                cgpa_2 = driver.find_element(By.ID, "lblbottom2").text.split()[-1]
                ygpa_1 = driver.find_element(By.ID, "lblbottom3").text.split()[-1]
            except (NoSuchElementException, IndexError):
                null_count += 1
                missing.add(autonomy_roll)
                driver.back()
                driver.find_element(By.NAME, "reset1").click()
                continue
            
            # Try Sem 4 (2nd year)
            driver.back()
            driver.find_element(By.NAME, "reset1").click()
            driver.find_element(By.NAME, "roll").clear()
            driver.find_element(By.NAME, "roll").send_keys(autonomy_roll)
            select = Select(driver.find_element(By.NAME, "sem"))
            select.select_by_value("4")
            driver.find_element(By.ID, "Button1").click()
            try:
                cgpa_3 = driver.find_element(By.ID, "lblbottom1").text.split()[-1]
                cgpa_4 = driver.find_element(By.ID, "lblbottom2").text.split()[-1]
                ygpa_2 = driver.find_element(By.ID, "lblbottom3").text.split()[-1]
            except (NoSuchElementException, IndexError):
                pass  # Continue to next semester

            # Try Sem 6 (3rd year)
            driver.back()
            driver.find_element(By.NAME, "reset1").click()
            driver.find_element(By.NAME, "roll").clear()
            driver.find_element(By.NAME, "roll").send_keys(autonomy_roll)
            select = Select(driver.find_element(By.NAME, "sem"))
            select.select_by_value("6")
            driver.find_element(By.ID, "Button1").click()
            try:
                cgpa_5 = driver.find_element(By.ID, "lblbottom1").text.split()[-1]
                cgpa_6 = driver.find_element(By.ID, "lblbottom2").text.split()[-1]
                ygpa_3 = driver.find_element(By.ID, "lblbottom3").text.split()[-1]
            except (NoSuchElementException, IndexError):
                pass  # Continue to next semester

            # Try Sem 8 (4th year)
            driver.back()
            driver.find_element(By.NAME, "reset1").click()
            driver.find_element(By.NAME, "roll").clear()
            driver.find_element(By.NAME, "roll").send_keys(autonomy_roll)
            select = Select(driver.find_element(By.NAME, "sem"))
            select.select_by_value("8")
            driver.find_element(By.ID, "Button1").click()
            try:
                cgpa_7 = driver.find_element(By.ID, "lblbottom1").text.split()[-1]
                cgpa_8 = driver.find_element(By.ID, "lblbottom2").text.split()[-1]
                ygpa_4 = driver.find_element(By.ID, "lblbottom3").text.split()[-1]
            except (NoSuchElementException, IndexError):
                pass  # Default to "N/A"

            writer.writerow(
                [
                    autonomy_roll,
                    name,
                    cgpa_1,
                    cgpa_2,
                    ygpa_1,
                    cgpa_3,
                    cgpa_4,
                    ygpa_2,
                    cgpa_5,
                    cgpa_6,
                    ygpa_3,
                    cgpa_7,
                    cgpa_8,
                    ygpa_4,
                    dept,
                ]
            )
            driver.back()
            driver.find_element(By.NAME, "reset1").click()
            null_count = 0  # Reset on successful entry
        # Reset null_count for next branch
        null_count = 0
    f.close()
    with open("data/2021/missing_rolls_2021.txt", "w") as mf:
        for roll in sorted(missing):
            mf.write(roll + "\n")
    driver.quit()


if __name__ == "__main__":
    get_grades_2021()