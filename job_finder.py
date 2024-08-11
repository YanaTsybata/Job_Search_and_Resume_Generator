import time
import random
import logging
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class JobFinder:
    def __init__(self):
        self.user_agents = [
            # List of user agents to rotate for avoiding detection
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        ]
        # Set up Chrome options for headless browsing
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument(f"user-agent={random.choice(self.user_agents)}")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        logger.info("JobFinder initialized")

    def search_jobs(self, keyword, location):
        # Search for jobs on Indeed.com based on keyword and location.
        logger.info(f"Searching for '{keyword}' jobs in '{location}'")
        url = f"https://www.indeed.com/jobs?q={keyword}&l={location}"
        driver = webdriver.Chrome(options=self.chrome_options)

        try:
            logger.info(f"Navigating to URL: {url}")
            driver.get(url)
            time.sleep(random.uniform(5, 10))  # Wait for page to load

            # Check for captcha
            if "captcha" in driver.current_url.lower():
                logger.warning("CAPTCHA detected. Please solve it manually and restart the script.")
                return []

            # List of possible selectors for job listings
            selectors = [
                (By.CLASS_NAME, "jobsearch-ResultsList"),
                (By.CLASS_NAME, "job_seen_beacon"),
                (By.ID, "resultsCol"),
                (By.CLASS_NAME, "jobCard_mainContent")
            ]

            # Try to find any of the job listing elements
            element_found = False
            for selector in selectors:
                try:
                    WebDriverWait(driver, 30).until(  # increase time to 30 sec
                        EC.presence_of_element_located(selector)
                    )
                    element_found = True
                    logger.info(f"Found element with selector: {selector}")
                    break
                except TimeoutException:
                    continue

            if not element_found:
                logger.error("Could not find any job-related elements on the page.")
                return []

            self._scroll_page(driver)

            # Parse the page content
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            job_cards = soup.find_all('div', class_='job_seen_beacon') or \
                        soup.find_all('div', class_='jobCard_mainContent') or \
                        soup.find_all('div', class_='jobsearch-ResultsList')

            logger.info(f"Number of job cards found: {len(job_cards)}")

            jobs = []
            for card in job_cards:
                job = self._parse_job_card(card)
                if job:
                    jobs.append(job)

            logger.info(f"Total jobs extracted: {len(jobs)}")
            return jobs

        except Exception as e:
            logger.error(f"An error occurred while searching for jobs: {str(e)}", exc_info=True)
            return []

        finally:
            driver.quit()

    def _scroll_page(self, driver):
        # Scroll the page to load more job listings
        logger.info("Scrolling down the page...")
        last_height = driver.execute_script("return document.body.scrollHeight")
        for _ in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def _parse_job_card(self, card):
        # Extract job information from a single job card
        title = card.find('h2', class_='jobTitle') or card.find('a', class_='jobtitle')
        company = card.find('span', {'data-testid': 'company-name'}) or card.find('span', class_='company')
        location = card.find('div', {'data-testid': 'text-location'}) or card.find('div', class_='location')
        job_link = card.find('a', class_='jcs-JobTitle') or card.find('a', class_='jobtitle')

        if all([title, company, location, job_link]):
            return {
                'title': title.text.strip(),
                'company': company.text.strip(),
                'location': location.text.strip(),
                'url': "https://www.indeed.com" + job_link['href'] if job_link['href'].startswith('/') else job_link[
                    'href'],
            }
        else:
            logger.warning("Skipping job card due to missing information")
            return None

    def parse_job_details(self, url):
        # Parse detailed job description from the job's URL
        logger.info(f"Parsing job details from: {url}")
        driver = webdriver.Chrome(options=self.chrome_options)

        try:
            driver.get(url)
            time.sleep(random.uniform(5, 10))

            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.ID, "jobDescriptionText"))
            )

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            job_description = soup.find('div', {'id': 'jobDescriptionText'})

            if job_description:
                return job_description.text.strip()
            else:
                logger.warning("Job description not found")
                return None

        except Exception as e:
            logger.error(f"An error occurred while parsing job details: {str(e)}", exc_info=True)
            return None

        finally:
            driver.quit()

    def save_jobs_to_csv(self, jobs, filename='jobs.csv'):
        # Save the found jobs to a CSV file
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['title', 'company', 'location', 'url'])
            writer.writeheader()
            for job in jobs:
                writer.writerow(job)
        logger.info(f"Saved {len(jobs)} jobs to {filename}")


if __name__ == "__main__":
    # csv file with job example
    finder = JobFinder()
    jobs = finder.search_jobs("Python Developer", "New York")

    if jobs:
        finder.save_jobs_to_csv(jobs)
        logger.info("Attempting to parse details for the first job")
        job_details = finder.parse_job_details(jobs[0]['url'])
        if job_details:
            logger.info("Details of the first job:")
            logger.info(job_details)
        else:
            logger.warning("Failed to get details of the first job")
    else:
        logger.warning("No jobs found")