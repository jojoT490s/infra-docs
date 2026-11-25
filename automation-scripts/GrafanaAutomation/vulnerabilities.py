from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def open_dashboard(driver, dashboard):
    driver.get(dashboard)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "h2"))
    )

def read_stat_panel(driver, panel_title):

    headings = driver.find_elements(By.TAG_NAME, "h2")

    for heading in headings:

        if heading.text.strip() == panel_title:

            panel = heading.find_element(
                By.XPATH,
                "./ancestor::section[1]"
            )

            lines = panel.text.splitlines()

            if len(lines) >= 2:

                value = lines[1].strip()

                return value

    return "0"
