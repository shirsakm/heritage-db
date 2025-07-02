import json
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException


def get_grades():
    driver = webdriver.Firefox()
    driver.get("http://111.93.160.42:8084/stud25e.aspx")

    with open("autonomy_rolls.json", "r") as f:
        autonomy_rolls = json.load(f)

    f = open("grades.csv", "w")
    writer = csv.writer(f)
    writer.writerow(
        ["College Roll", "Autonomy Roll", "Name", "GPA Sem 1", "GPA Sem 2", "Branch"]
    )

    for roll_no, autonomy_roll in autonomy_rolls.items():
        if int(roll_no) <= 2457019:
            continue
        driver.find_element(By.NAME, "roll").send_keys(autonomy_roll)
        select = Select(driver.find_element(By.NAME, "sem"))
        select.select_by_value("2")
        driver.find_element(By.ID, "Button1").click()

        try:
            name = " ".join(
                driver.find_element(By.ID, "lblname").text.split()[2:]
            ).title()
            branch = driver.find_element(By.ID, "lbltop").text
            gpa_1 = driver.find_element(By.ID, "lblbottom1").text.split()[-1]
            gpa_2 = driver.find_element(By.ID, "lblbottom2").text.split()[-1]
        except NoSuchElementException:
            name = gpa_1 = gpa_2 = branch = "N/A"
        except IndexError:
            gpa_1 = gpa_2 = "N/A"

        writer.writerow([roll_no, autonomy_roll, name, gpa_1, gpa_2, branch])
        driver.back()
        driver.find_element(By.NAME, "reset1").click()

    f.close()
    driver.quit()


if __name__ == "__main__":
    get_grades()
    # main()  # Uncomment this line to run the main function from the previous code snippet
