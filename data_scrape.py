import requests
from bs4 import BeautifulSoup
import json
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def get_subject_codes():
    # URL of the course offerings page
    url = "https://registrar.princeton.edu/course-offerings"

    # Send a GET request to the page
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the <script> tag that contains the JSON data
    script_tag = soup.find('script', type='application/json', attrs={'data-drupal-selector': 'drupal-settings-json'})

    # Extract the JSON data from the script tag
    json_data = json.loads(script_tag.string)

    # Navigate to the relevant part of the JSON data
    subjects = json_data['ps_registrar']['subjects']['1252']

    # Extract the subject codes
    subject_codes = [subject['code'] for subject in subjects]

    # Print out the subject codes for inspection
    # for code in subject_codes:
    #     print(code)

    return subject_codes

def get_course_urls_selenium(subject_codes, term="1252"):
    base_url = "https://registrar.princeton.edu/course-offerings"
    domain_url = "https://registrar.princeton.edu"
    course_urls = []

    # Set up Chrome options for headless mode (no GUI)
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Set up the Selenium WebDriver
    service = Service('/Users/jeremiahgiordani/Documents/chromedriver-mac-x64/chromedriver')  # Replace with your path to chromedriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    total_departments = len(subject_codes)

    for index, dept_code in enumerate(subject_codes, start=1):
        # Construct the URL for the department
        subject_url = f"{base_url}?term={term}&subject={dept_code}"
        
        # Open the subject URL
        driver.get(subject_url)

        try:
            # Adjust the timeout as needed (e.g., 10 seconds)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "tbody tr"))
            )
            print(f"Course content for {dept_code} loaded - (Dept {index}/{total_departments})")
        except Exception as e:
            print("Error: Course content did not load in time.", str(e))

        # Parse the page source after the content has loaded
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find the table body that contains the course listings
        tbody = soup.find('tbody')

        if tbody:
            # Counter to track the number of course URLs added per department
            # course_count = 0

            # Iterate through each row in the table body
            for row in tbody.find_all('tr'):
                # Find the anchor tag that contains the link to the course page
                course_link = row.find('a', href=True)

                if course_link:
                    # Construct the full URL and add it to the list
                    full_url = domain_url + course_link['href']
                    course_urls.append({"url":full_url, "dept":dept_code})
                    # course_count += 1

                    # Stop after adding four course URLs
                    # if course_count >= 4:
                    #     break

    # Close the browser after scraping
    driver.quit()

    return course_urls

def get_course_details(course_urls):
    # Path to your ChromeDriver
    chrome_driver_path = "/Users/jeremiahgiordani/Documents/chromedriver-mac-x64/chromedriver"
    
    # Set up Chrome options
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--headless")  # Running with head, remove this if you don't want to see the browser

    # Set up ChromeDriver service
    service = Service(chrome_driver_path)

    # Initialize WebDriver
    driver = webdriver.Chrome(service=service, options=options)

    total_courses = len(course_urls)

    course_data = []

    for index, url in enumerate(course_urls, start=1):
        course_info = {}

        try:
            # Navigate to the course details page
            driver.get(url["url"])

            # Wait for the course title to load as an indicator that the page has loaded
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h2.course-title"))
            )
            
            # Extract the course id from the URL
            course_id = url["url"].split("courseid=")[1]
            course_info["courseid"] = course_id

            # Extract the course id from the URL
            course_dept = url["dept"]
            course_info["department"] = course_dept

            # Extract course name
            course_name_element = driver.find_element(By.CSS_SELECTOR, "h2.course-title")
            course_info["course name"] = course_name_element.text.strip()

            # Extract course code(s)
            try:
                course_code_element = driver.find_element(By.CSS_SELECTOR, "div.subject-associations")
                course_codes = course_code_element.get_attribute('innerHTML').replace("<br>", "").strip().split('\n')
                course_info["course code"] = "; ".join([code.strip() for code in course_codes])
            except:
                course_info["course code"] = "N/A"

            # Extract the department code from the first course code
            # if course_codes:
            #     department_code = course_codes[0][:3]  # Take the first three letters
            #     course_info["department"] = department_code
            # else:
            #     course_info["department"] = "Unknown"  # In case there's no course code

            # Extract distribution area
            try:
                distribution_area_element = driver.find_element(By.CSS_SELECTOR, "div.distribution-area")
                course_info["distribution area"] = distribution_area_element.text.split(":")[1].strip()
            except:
                course_info["distribution area"] = "N/A"

            # Extract description
            try:
                description_element = driver.find_element(By.CSS_SELECTOR, "div.description p")
                course_info["description"] = description_element.text.strip()
            except:
                course_info["description"] = "N/A"

            # Extract reading/writing assignments
            try:
                assignments_element = driver.find_element(By.CSS_SELECTOR, "div.reading-and-writing-assignments p span")
                course_info["assignments"] = assignments_element.text.strip()
            except:
                course_info["assignments"] = "N/A"

            # Extract grading
            try:
                grading_elements = driver.find_elements(By.CSS_SELECTOR, "div.requirements-and-grading ul li")
                grading = [element.text.strip() for element in grading_elements]
                course_info["grading"] = "; ".join(grading)
            except:
                course_info["grading"] = "N/A"

            # Append the course information to the list
            course_data.append(course_info)

            print(f"Course {course_id} scraped successfully - (Course {index}/{total_courses})")

        except Exception as e:
            print(f"Failed to scrape {url}: {str(e)}")

    # Clean up by closing the browser
    driver.quit()

    return course_data

# Example usage: Limit to the first 5 departments for testing
subject_codes = get_subject_codes()
limited_subject_codes = subject_codes[:2]

course_urls = get_course_urls_selenium(subject_codes)
# Print out the course URLs for inspection
# for url in course_urls:
#     print(url)

limited_course_urls = course_urls[:6]
course_details = get_course_details(course_urls)

# Pretty print the results
# for course in course_details:
#     pprint(course)
#     print("\n" + "-"*50 + "\n")  # Add a separator between courses

# Save the data to a JSON file
with open("course_details.json", "w") as outfile:
    json.dump(course_details, outfile, indent=4)  # indent=4 makes the JSON file pretty-printed for readability


print("\n" + "-"*50 + "\n")
print("Course details saved to course_details.json")