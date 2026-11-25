from login import start_browser, login
from config import GRAFANA_INSTANCES
from vulnerabilities import (
    open_dashboard,
    read_stat_panel
)

import time

instance = GRAFANA_INSTANCES[0]      

driver = start_browser()

try:

    print("Opening login...")

    driver.get(instance["base_url"] + "/login")

    login(driver)

    print("Opening Vulnerabilities Dashboard...")

    open_dashboard(
        driver,
        instance["dashboards"]["vulnerabilities"]
    )

    time.sleep(15)

    print("\nCurrent URL:")
    print(driver.current_url)

    print("\nPage Title:")
    print(driver.title)

    print("\n==============================")
    print("VULNERABILITY EVENTS")
    print("==============================")

    value = read_stat_panel(driver, "VULNERABILITY EVENTS")

    print(value)

    input("\nPress Enter to close the browser...")

finally:

    driver.quit()
