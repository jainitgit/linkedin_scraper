from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import pandas as pd

# Scroll down the page to load more job listings
def scroll_page(driver, scroll_times=10, delay=2):
    for _ in range(scroll_times):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

# Extract brief job description from individual job page
def get_job_description(job_url, driver):
    try:
        driver.execute_script("window.open('');")  # open new tab
        driver.switch_to.window(driver.window_handles[1])
        driver.get(job_url)

        # Wait until job description is loaded
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'show-more-less-html__markup')))
        desc = driver.find_element(By.CLASS_NAME, 'show-more-less-html__markup').text.strip()

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        # Return first 300 characters for brevity
        return desc[:300] + "..." if len(desc) > 300 else desc

    except Exception as e:
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return "Description not available"

# Set up Chrome in headless mode (no GUI)
options = Options()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

# Open LinkedIn job listings for Bhubaneswar
driver.get("https://www.linkedin.com/jobs/search/?keywords=&location=Bhubaneswar")
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'base-card')))
scroll_page(driver, scroll_times=10, delay=2)

# Find all job cards
jobs = driver.find_elements(By.CLASS_NAME, 'base-card')
print(f"Total job cards found: {len(jobs)}")

jobs_data = []

# Loop through each job listing (limit to 50)
for idx, job in enumerate(jobs[:50]):
    try:
        # Scroll to the job element to ensure it loads
        driver.execute_script("arguments[0].scrollIntoView(true);", job)
        time.sleep(0.5)

        # Extract job details
        title = job.find_element(By.CLASS_NAME, 'base-search-card__title').text.strip()
        company = job.find_element(By.CLASS_NAME, 'base-search-card__subtitle').text.strip()
        location = job.find_element(By.CLASS_NAME, 'job-search-card__location').text.strip()
        link = job.find_element(By.TAG_NAME, 'a').get_attribute('href')

        # Try to get posted date
        try:
            posted = job.find_element(By.CLASS_NAME, 'job-search-card__listdate').text.strip()
        except:
            posted = "N/A"

        # Try to get company logo URL
        try:
            logo_url = job.find_element(By.CLASS_NAME, 'artdeco-entity-image').get_attribute('src')
        except:
            logo_url = "N/A"

        # Get job description from individual job page
        description = get_job_description(link, driver)

        # Add the collected job data
        jobs_data.append({
            "logo_url": logo_url,
            "company": company,
            "title": title,
            "location": location,
            "description": description,
            "posted": posted,
            "link": link
        })

    except Exception as e:
        print(f"Job {idx+1}: Skipped due to error: {e}")

# Close browser after scraping
driver.quit()

# Save as JSON
with open('jobs_bhubaneswar.json', 'w') as f:
    json.dump(jobs_data, f, indent=2)

# Save as CSV
pd.DataFrame(jobs_data).to_csv('jobs_bhubaneswar.csv', index=False)

print(f"Scraped {len(jobs_data)} jobs. Files saved as JSON and CSV.")

