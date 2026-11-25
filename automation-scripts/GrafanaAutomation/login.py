from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def start_browser():
    options = Options()
    options.add_argument("--headless")

    # Real Firefox binary (Snap)
    options.binary_location = "/snap/firefox/current/usr/lib/firefox/firefox"

    service = Service("/snap/bin/geckodriver")

    driver = webdriver.Firefox(
        service=service,
        options=options
    )

    driver.set_window_size(1920, 1080)

    return driver


def login(driver, instance):
    """
    Log in to a Grafana instance using its own credentials.

    Args:
        driver: Selenium WebDriver instance.
        instance: Dictionary containing the Grafana instance's
                  username and password.
    """

    wait = WebDriverWait(driver, 60)

    # Get credentials for the specific instance
    username_value = instance["username"]
    password_value = instance["password"]

    username = wait.until(
        EC.visibility_of_element_located((By.NAME, "user"))
    )

    password = wait.until(
        EC.visibility_of_element_located((By.NAME, "password"))
    )

    # Clear any previously populated credentials
    username.clear()
    password.clear()

    # Enter credentials for the current instance
    username.send_keys(username_value)
    password.send_keys(password_value)

    login_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[.//span[normalize-space()='Log in']]")
        )
    )

    login_button.click()

    # Wait until login finishes
    wait.until(lambda d: "/login" not in d.current_url)

    print(f"Login successful: {instance.get('name', 'Grafana instance')}")
