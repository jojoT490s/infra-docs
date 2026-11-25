from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def read_total_alerts(driver):

    time.sleep(8)

    headings = driver.find_elements(By.TAG_NAME, "h2")

    for heading in headings:

        if heading.text.strip() == "ALERTS":

            print("=" * 60)
            print("TOTAL ALERTS PANEL")
            print("=" * 60)

            panel = heading.find_element(By.XPATH, "./ancestor::section[1]")

            lines = panel.text.splitlines()

            if len(lines) >= 2:

                value = lines[1].replace(",", "").strip()

                print(value)

                return int(value)

    return 0



def open_dashboard(driver, url):
    driver.get(url)

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    time.sleep(10)


def read_categories(driver, table_title):
    headings = driver.find_elements(By.TAG_NAME, "h2")

    for heading in headings:

        if heading.text.strip() == table_title:

            panel = heading.find_element(
                By.XPATH,
                "./ancestor::section[1]"
            )

            cells = panel.find_elements(
                By.CSS_SELECTOR,
                "[role='cell']"
            )

            categories = []

            i = 0

            while i < len(cells) - 1:

                name = cells[i].text.strip()
                count = cells[i + 1].text.strip()

                if name != "" and count != "":
                    categories.append({
                        "name": name,
                        "count": count
                    })

                i += 2

            return categories

    return []
def read_highest_agent(driver, table_title):

    headings = driver.find_elements(By.TAG_NAME, "h2")

    for heading in headings:

        if heading.text.strip() == table_title:

            panel = heading.find_element(
                By.XPATH,
                "./ancestor::section[1]"
            )

            cells = panel.find_elements(
                By.CSS_SELECTOR,
                "[role='cell']"
            )

            highest = None
            highest_count = -1

            i = 0

            while i < len(cells) - 1:

                name = cells[i].text.strip()
                count_text = cells[i + 1].text.strip()

                if name and count_text:

                    try:
                        count = int(count_text)

                        if count > highest_count:
                            highest_count = count
                            highest = {
                                "name": name,
                                "count": count
                            }

                    except ValueError:
                        pass

                i += 2

            return highest

    return None
