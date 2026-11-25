from login import start_browser, login
from config import GRAFANA_INSTANCES
from selenium.webdriver.common.by import By
from discord import build_report, send_discord

from edr_summary import (
    open_dashboard,
    read_total_alerts,
    read_categories,
    read_highest_agent
)

from vulnerabilities import (
    open_dashboard as open_vuln_dashboard,
    read_stat_panel
)

from linux_health import (
    open_dashboard as open_linux_dashboard,
    read_linux_health,
    read_linux_health_internal
)


SHEET_MAP = {
    "instnce1": "1",
    "instance2": "2",
    "instance3": "3",
    "Instaance4": "4",
    "instance5": "5",
    "instance6": "6"
}

from sheets import (
    get_spreadsheet,
    find_day_row,
    write_summary,
    write_linux_health,
    write_linux_health_only,
    write_today_date
)
import time
from selenium.webdriver.common.action_chains import ActionChains

from discord import send_discord, build_report
driver = start_browser()

report = []

for instance in GRAFANA_INSTANCES:

    print("\n" + "=" * 60)
    print(f"PROCESSING {instance['name']}")
    print("=" * 60)
    
    dashboards = instance.get("dashboards", {})
    
    driver.get(instance["base_url"] + "/login")

    print("Logging in...")
    login(driver, instance)
    print("Login successful!")

    #
    # SUMMARY
    if dashboards.get("summary"):
        dashboard = instance["dashboards"]["summary"]

        print("Opening EDR Summary...")
        open_dashboard(driver, dashboard)

        # Give Grafana time to finish rendering
        time.sleep(15)

        print("\nCurrent URL:")
        print(driver.current_url)
 
        print("\nPage Title:")
        print(driver.title)

        alerts = read_total_alerts(driver)

        category = read_categories(driver, "ALERTS BY CATEGORY")

        print("\n==============================")
        print("CATEGORIES")
        print("==============================")

        if category:
            for item in category:
                print(item)
        else:
            print("No categories found.")
   
        agent = read_highest_agent(driver, "ALERTS BY AGENT")

        print("\n==============================")
        print("HIGHEST AGENT")
        print("==============================")
        print(agent) 
    
    else:
        print("Skipping Summary: not configured for this instance.")
    #
    # VULNERABILITIES
    #

    #
    # VULNERABILITIES
    #

    print("\n==============================")
    print("VULNERABILITIES DASHBOARD")
    print("==============================")
    
    if dashboards.get("vulnerabilities"):
        vuln_dashboard = instance["dashboards"]["vulnerabilities"]

        open_vuln_dashboard(driver, vuln_dashboard)

        # Wait for Grafana to finish rendering the panel
        time.sleep(15)

        print("Current URL:", driver.current_url)
        print("Page Title:", driver.title)

        vulnerability_events = read_stat_panel(
        driver,
        "VULNERABILITY EVENTS"
        )
 
        print("VULNERABILITY EVENTS:", vulnerability_events)
    
    else:
        print("Skipping Vulnerabilities: not configured for this instance.")
    #
    # LINUX HEALTH
    #

    print("\n==============================")
    print("LINUX HEALTH DASHBOARD")
    print("==============================")
    
    if dashboards.get("linux"):
        linux_dashboard = instance["dashboards"]["linux"]

        open_linux_dashboard(driver, linux_dashboard)

        actions = ActionChains(driver)

        cpu_button = driver.find_element(
            By.XPATH,
            "//button[contains(., 'CPU Utilization')]"
        )

        memory_button = driver.find_element(
            By.XPATH,
            "//button[contains(., 'Memory Usage')]"
        )

        partition_button = driver.find_element(
            By.XPATH,
            "//button[contains(., 'Partition usage')]"
        )


         # CPU
         #

        actions.double_click(cpu_button).perform()

        print("Double clicked CPU header")

        time.sleep(3)

        if instance["name"] == "2":
            cpu_rows = read_linux_health_internal(driver)
        else:
            cpu_rows = read_linux_health(driver)

        #
        # MEMORY
        #

        # Let CPU sorting settle first
        time.sleep(10)

        actions.double_click(memory_button).perform()

        print("Double clicked Memory header")

        # Wait for Memory sorting to complete
        time.sleep(10)
    else:
        print("Skipping Linux Health: not configured for this instance.") 

    if instance["name"] == "Internal":
        memory_rows = read_linux_health_internal(driver)
    else:
        memory_rows = read_linux_health(driver)
   
    # Let Memory sorting settle
    time.sleep(10)

    driver.execute_script(
    "arguments[0].scrollIntoView({block: 'center'});",
    partition_button
    )

    time.sleep(10)

    actions.double_click(partition_button).perform()

    print("Double clicked Partition header")

    # Wait for Partition sorting to complete
    time.sleep(10)

    if instance["name"] == "2":
        partition_rows = read_linux_health_internal(driver)
    else:
        partition_rows = read_linux_health(driver)

    

    #
    # HIGH USAGE
    #

    high = []

    for row in cpu_rows:
        if row["cpu"] >= 75:
            high.append({
                "server": row["server"],
                "metric": "cpu",
                "value": row["cpu"]
            })

    for row in memory_rows:
        if row["memory"] >= 75:
            high.append({
                "server": row["server"],
                "metric": "memory",
                "value": row["memory"]
            })

    for row in partition_rows:
        if row["partition"] >= 75:
            high.append({
                "server": row["server"],
                "metric": "partition",
                "value": row["partition"]
            })

    print()

    print("SERVERS ABOVE 75%\n")

    for item in high:
        print(item)

    print("\n==============================")
    print("ALL SERVERS")
    print("==============================")

    for row in partition_rows:
        print(
            row["server"],
            "CPU:", row["cpu"],
            "MEM:", row["memory"],
            "PART:", row["partition"]
        )

    print("\nPartition values\n")

    for r in partition_rows:
        print(r["server"], r["partition"])

    sheet_name = SHEET_MAP[instance["name"]]

    worksheet, row = find_day_row(sheet_name)
    
    print(f"Writing {instance['name']} to {sheet_name}, row {row}")
    write_today_date(worksheet, row)
    write_summary(
        worksheet,
        row,
        alerts,
        category,
        agent,
        vulnerability_events
    )

    write_linux_health(
        worksheet,
        row,
        high
    )
    report = {
        "name": instance["name"],
        "alerts": alerts,
        "category": category,
        "agent": agent,
        "vulnerabilities": vulnerability_events,
        "high": high
    }

    message = build_report(report)
    send_discord(message)
 
print("Automation completed successfully.")

driver.quit()

