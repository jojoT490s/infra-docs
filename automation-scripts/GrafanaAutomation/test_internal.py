from login import start_browser, login
from config import GRAFANA_INSTANCES
from linux_health import (
    open_dashboard,
    read_linux_health_internal
)

# Find the Internal instance
instance = next(i for i in GRAFANA_INSTANCES if i["name"] == "Internal")

driver = start_browser()

try:
    print("Opening login...")
    driver.get(instance["base_url"] + "/login")

    login(driver)

    linux_dashboard = instance["dashboards"]["linux"]

    print("Opening Linux Health dashboard...")
    open_dashboard(driver, linux_dashboard)

    print("Reading Linux Health...")

    rows = read_linux_health_internal(driver)

    print("\nRows returned:\n")

    for row in rows:
        print(row)

finally:
    driver.quit()
