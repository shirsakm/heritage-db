import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException


def main():
    driver = webdriver.Firefox()
    driver.get("https://theheritage.ac.in/knowyourautonomyrollno.aspx")

    results = dict()
    missing = set()
    null_count = 0
    
    for i in range(51, 64):
        for j in range(1, 210):
            if null_count >= 5:
                break
            roll_no = "24" + str(i) + str(j).zfill(3)
                
            autonomy_roll = get_autonomy_roll(driver, roll_no)
            if autonomy_roll is None:
                null_count += 1
                missing.add(roll_no)
                continue
            elif autonomy_roll == "":
                missing.add(roll_no)
                continue
            results[roll_no] = autonomy_roll

    with open("autonomy_rolls.json", "w") as f:
        json.dump(results, f, indent=4)

    with open("missing_rolls.txt", "w") as f:
        for roll in sorted(missing):
            f.write(roll + "\n")

    driver.quit()


def get_autonomy_roll(driver, roll_no):
    college_roll = driver.find_element(By.ID, "txtCollegeRollNo")
    driver.execute_script(
        "arguments[0].setAttribute('value', arguments[1])", college_roll, str(roll_no)
    )

    driver.find_element(By.ID, "btnCollegeRollNo").click()

    year = Select(driver.find_element(By.ID, "DrYear"))
    year.select_by_value("1")

    driver.find_element(By.ID, "btnCollegeRollNo").click()

    try:
        autonomy_roll = driver.find_element(By.ID, "lblAutonomyExamRollNo").text
    except NoSuchElementException:
        return None
    return autonomy_roll


if __name__ == "__main__":
    main()
