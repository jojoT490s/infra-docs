from login import start_browser, login
from config import GRAFANA_INSTANCES
from edr_summary import (
    open_dashboard,
    read_total_alerts,
    read_categories,
    read_highest_agent
)

driver = start_browser()

try:
    instance = GRAFANA_INSTANCES[0]   # Pesaflow

    print("Opening login...")
    driver.get(instance["base_url"] + "/login")
    login(driver)

    print("\nOpening EDR Summary...")
    print(instance["dashboards"]["summary"])

    open_dashboard(driver, instance["dashboards"]["summary"])

    print("\nCurrent URL:")
    print(driver.current_url)

    print("\nPage Title:")
    print(driver.title)

    print("\n========================")
    print("TOTAL ALERTS")
    print("========================")
    alerts = read_total_alerts(driver)
    print(alerts)

    print("\n========================")
    print("ALL CATEGORIES")
    print("========================")
    categories = read_categories(driver, "ALERTS BY CATEGORY")

    if categories:
        for category in categories:
            print(category)
    else:
        print("No categories found.")

    print("\n========================")
    print("HIGHEST AGENT")
    print("========================")
    agent = read_highest_agent(driver, "ALERTS BY AGENT")

    if agent:
        print(agent)
    else:
        print("No agent found.")

    input("\nPress Enter to close the browser...")

finally:
    driver.quit()
