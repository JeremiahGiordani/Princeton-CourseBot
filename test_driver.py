from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Path to your ChromeDriver
chrome_driver_path = "/Users/jeremiahgiordani/Documents/chromedriver-mac-x64/chromedriver"

# Set up Chrome options (headless is disabled to observe the process)
options = Options()
# options.add_argument("--headless")  # Comment out headless to see the browser window
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Set up ChromeDriver service
service = Service(chrome_driver_path)

# Initialize WebDriver
driver = webdriver.Chrome(service=service, options=options)

# Navigate to the course page
driver.get("https://registrar.princeton.edu/course-offerings?term=1252&subject=AAS")

# Wait for the course table to load
try:
    # Adjust the timeout as needed (e.g., 10 seconds)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "tbody tr"))
    )
    print("Course content loaded successfully!")
except Exception as e:
    print("Error: Course content did not load in time.", str(e))

# (Optional) Interact with the content or take further actions here

# Keep the browser open for a while to observe (e.g., 10 seconds)
import time
time.sleep(10)  # Adjust the time as needed to observe the page

# Clean up by closing the browser
driver.quit()
