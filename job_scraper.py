"""
Job Scraper for Data Science Positions
Scrapes jobs from LinkedIn, Indeed, and Seek (Australia)
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import json
import time
from urllib.parse import quote_plus

class JobScraper:
    def __init__(self):
        self.jobs = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def scrape_seek(self, keywords="data scientist", location="Sydney"):
        """Scrape jobs from Seek.com.au"""
        print(f"🔍 Scraping Seek for {keywords} in {location}...")

        url = f"https://www.seek.com.au/{quote_plus(keywords)}-jobs/in-{quote_plus(location)}"

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Note: Seek's structure may require selenium for dynamic content
            # This is a basic structure - you'll need to inspect and adjust selectors
            job_cards = soup.find_all('article', {'data-card-type': 'JobCard'})

            for card in job_cards[:20]:  # Limit to 20 jobs
                try:
                    title_elem = card.find('a', {'data-automation': 'jobTitle'})
                    company_elem = card.find('a', {'data-automation': 'jobCompany'})
                    location_elem = card.find('a', {'data-automation': 'jobLocation'})

                    if title_elem:
                        job = {
                            'title': title_elem.text.strip(),
                            'company': company_elem.text.strip() if company_elem else 'N/A',
                            'location': location_elem.text.strip() if location_elem else location,
                            'url': 'https://www.seek.com.au' + title_elem.get('href', ''),
                            'source': 'Seek',
                            'date_scraped': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'applied': False
                        }
                        self.jobs.append(job)
                except Exception as e:
                    continue

        except Exception as e:
            print(f"❌ Error scraping Seek: {e}")

    def scrape_indeed(self, keywords="data scientist", location="Sydney NSW"):
        """Scrape jobs from Indeed Australia"""
        print(f"🔍 Scraping Indeed for {keywords} in {location}...")

        url = f"https://au.indeed.com/jobs?q={quote_plus(keywords)}&l={quote_plus(location)}"

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Indeed job cards
            job_cards = soup.find_all('div', class_='job_seen_beacon')

            for card in job_cards[:20]:
                try:
                    title_elem = card.find('h2', class_='jobTitle')
                    company_elem = card.find('span', class_='companyName')
                    location_elem = card.find('div', class_='companyLocation')
                    link_elem = card.find('a', class_='jcs-JobTitle')

                    if title_elem:
                        job = {
                            'title': title_elem.text.strip(),
                            'company': company_elem.text.strip() if company_elem else 'N/A',
                            'location': location_elem.text.strip() if location_elem else location,
                            'url': 'https://au.indeed.com' + link_elem.get('href', '') if link_elem else '',
                            'source': 'Indeed',
                            'date_scraped': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'applied': False
                        }
                        self.jobs.append(job)
                except Exception as e:
                    continue

        except Exception as e:
            print(f"❌ Error scraping Indeed: {e}")

    def scrape_linkedin(self, keywords="data scientist", location="Sydney"):
        """Scrape jobs from LinkedIn (Note: LinkedIn heavily restricts scraping)"""
        print(f"🔍 Scraping LinkedIn for {keywords} in {location}...")
        print("⚠️  Note: LinkedIn requires authentication and may block scraping.")
        print("    Consider using LinkedIn's official API or Selenium with login.")

        # LinkedIn Jobs URL
        url = f"https://www.linkedin.com/jobs/search/?keywords={quote_plus(keywords)}&location={quote_plus(location)}"

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            # LinkedIn structure (may be blocked without login)
            job_cards = soup.find_all('div', class_='base-card')

            for card in job_cards[:20]:
                try:
                    title_elem = card.find('h3', class_='base-search-card__title')
                    company_elem = card.find('h4', class_='base-search-card__subtitle')
                    location_elem = card.find('span', class_='job-search-card__location')
                    link_elem = card.find('a', class_='base-card__full-link')

                    if title_elem:
                        job = {
                            'title': title_elem.text.strip(),
                            'company': company_elem.text.strip() if company_elem else 'N/A',
                            'location': location_elem.text.strip() if location_elem else location,
                            'url': link_elem.get('href', '') if link_elem else '',
                            'source': 'LinkedIn',
                            'date_scraped': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'applied': False
                        }
                        self.jobs.append(job)
                except Exception as e:
                    continue

        except Exception as e:
            print(f"❌ Error scraping LinkedIn: {e}")

    def save_to_csv(self, filename='jobs.csv'):
        """Save scraped jobs to CSV"""
        if self.jobs:
            df = pd.DataFrame(self.jobs)
            df.to_csv(filename, index=False)
            print(f"✅ Saved {len(self.jobs)} jobs to {filename}")
        else:
            print("⚠️  No jobs to save")

    def save_to_json(self, filename='jobs.json'):
        """Save scraped jobs to JSON"""
        if self.jobs:
            with open(filename, 'w') as f:
                json.dump(self.jobs, f, indent=2)
            print(f"✅ Saved {len(self.jobs)} jobs to {filename}")
        else:
            print("⚠️  No jobs to save")

    def get_jobs(self):
        """Return all scraped jobs"""
        return self.jobs


def main():
    # Initialize scraper
    scraper = JobScraper()

    # Job search parameters
    keywords = "data scientist"
    location = "Sydney"

    print("🚀 Starting job search...")
    print(f"   Keywords: {keywords}")
    print(f"   Location: {location}\n")

    # Scrape from different sources
    scraper.scrape_seek(keywords, location)
    time.sleep(2)  # Be respectful with requests

    scraper.scrape_indeed(keywords, f"{location} NSW")
    time.sleep(2)

    scraper.scrape_linkedin(keywords, location)

    # Save results
    print(f"\n📊 Total jobs found: {len(scraper.get_jobs())}")
    scraper.save_to_csv('/Users/ABRAHAM/job_application_system/jobs.csv')
    scraper.save_to_json('/Users/ABRAHAM/job_application_system/jobs.json')

    # Display sample
    if scraper.get_jobs():
        print("\n📋 Sample jobs:")
        for job in scraper.get_jobs()[:5]:
            print(f"   • {job['title']} at {job['company']} ({job['source']})")


if __name__ == "__main__":
    main()
