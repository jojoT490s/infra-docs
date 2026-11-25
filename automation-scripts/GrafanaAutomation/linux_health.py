from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def open_dashboard(driver, dashboard):
    driver.get(dashboard)

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (By.XPATH, "//button[contains(., 'CPU Utilization')]")
        )
    )


def read_linux_health(driver):
    """
    Reads the currently displayed table.
    Assumes the table has already been sorted.
    """

    time.sleep(3)

    rows = driver.find_elements(By.CSS_SELECTOR, "div[role='row']")

    print(f"Grafana rendered {len(rows)} rows")

    results = []

    for row in rows:

        # IMPORTANT: read cells from THIS row only
        cells = row.find_elements(By.CSS_SELECTOR, "div[role='cell']")

        if len(cells) < 8:
            continue

        try:

            server = cells[0].text.strip()

            cpu = float(cells[5].text.replace("%", "").strip())

            memory = float(cells[6].text.replace("%", "").strip())

            partition = float(cells[7].text.replace("%", "").strip())

        except ValueError:
            continue

        results.append({
            "server": server,
            "cpu": cpu,
            "memory": memory,
            "partition": partition
        })

    return results

def read_linux_health_internal(driver):
    """
    Reads the currently displayed table.
    Assumes the table has already been sorted.
    """

    time.sleep(3)

    rows = driver.find_elements(By.CSS_SELECTOR, "div[role='row']")

    print(f"Grafana rendered {len(rows)} rows")

    results = []

    for row in rows:

        # IMPORTANT: read cells from THIS row only
        cells = row.find_elements(By.CSS_SELECTOR, "div[role='gridcell']")

        if len(cells) < 8:
            continue

        try:

            server = cells[0].text.strip()

            cpu = float(cells[5].text.replace("%", "").strip())

            memory = float(cells[6].text.replace("%", "").strip())

            partition = float(cells[7].text.replace("%", "").strip())

        except ValueError:
            continue

        results.append({
            "server": server,
            "cpu": cpu,
            "memory": memory,
            "partition": partition
        })

    return results

