"""
Auto-fill Job Application System using Selenium
Automatically fills job application forms with your resume data
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import json
import time

class ApplicationAutoFiller:
    def __init__(self, resume_data_path='/Users/ABRAHAM/job_application_system/resume_data.json'):
        """Initialize with resume data"""
        with open(resume_data_path, 'r') as f:
            self.data = json.load(f)

        self.driver = None

    def init_browser(self, headless=False):
        """Initialize Chrome browser"""
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)

    def fill_field(self, field_identifier, value, by=By.NAME):
        """Fill a form field"""
        try:
            element = self.wait.until(EC.presence_of_element_located((by, field_identifier)))
            element.clear()
            element.send_keys(value)
            print(f"✅ Filled: {field_identifier}")
            return True
        except Exception as e:
            print(f"❌ Could not fill {field_identifier}: {e}")
            return False

    def fill_common_fields(self):
        """Auto-fill common application fields"""
        personal = self.data['personal_info']

        # Common field names to try
        name_fields = ['name', 'full_name', 'fullname', 'applicant_name', 'firstName', 'first_name']
        email_fields = ['email', 'email_address', 'e-mail', 'emailAddress']
        phone_fields = ['phone', 'telephone', 'mobile', 'phone_number', 'phoneNumber']
        location_fields = ['location', 'address', 'city', 'current_location']

        # Try to fill name
        for field in name_fields:
            if self.fill_field(field, personal['name']):
                break

        # Try to fill email
        for field in email_fields:
            if self.fill_field(field, personal['email']):
                break

        # Try to fill phone
        for field in phone_fields:
            if self.fill_field(field, personal['phone']):
                break

        # Try to fill location
        for field in location_fields:
            if self.fill_field(field, personal['location']):
                break

    def upload_resume(self, resume_path='/Users/ABRAHAM/Documents/CV_Abraham Kuriakose.pdf'):
        """Upload resume file"""
        try:
            # Common file upload identifiers
            upload_fields = [
                (By.NAME, 'resume'),
                (By.NAME, 'cv'),
                (By.ID, 'resume'),
                (By.ID, 'cv'),
                (By.XPATH, "//input[@type='file']")
            ]

            for by, identifier in upload_fields:
                try:
                    element = self.driver.find_element(by, identifier)
                    element.send_keys(resume_path)
                    print(f"✅ Uploaded resume")
                    return True
                except:
                    continue

            print("⚠️  Could not find resume upload field")
            return False
        except Exception as e:
            print(f"❌ Error uploading resume: {e}")
            return False

    def fill_linkedin_easy_apply(self, job_url):
        """Fill LinkedIn Easy Apply application"""
        print(f"📝 Opening LinkedIn Easy Apply: {job_url}")
        self.driver.get(job_url)
        time.sleep(2)

        try:
            # Click Easy Apply button
            easy_apply_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'jobs-apply-button')]"))
            )
            easy_apply_btn.click()
            time.sleep(1)

            # Fill common fields
            self.fill_common_fields()

            # Upload resume if available
            self.upload_resume()

            print("✅ LinkedIn Easy Apply filled. Review before submitting!")

        except Exception as e:
            print(f"❌ Error with LinkedIn Easy Apply: {e}")

    def fill_seek_application(self, job_url):
        """Fill Seek application"""
        print(f"📝 Opening Seek application: {job_url}")
        self.driver.get(job_url)
        time.sleep(2)

        try:
            # Click Apply button
            apply_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Apply')]"))
            )
            apply_btn.click()
            time.sleep(1)

            # Fill common fields
            self.fill_common_fields()

            # Upload resume
            self.upload_resume()

            print("✅ Seek application filled. Review before submitting!")

        except Exception as e:
            print(f"❌ Error with Seek application: {e}")

    def fill_generic_application(self, job_url):
        """Fill generic job application form"""
        print(f"📝 Opening application: {job_url}")
        self.driver.get(job_url)
        time.sleep(2)

        # Fill common fields
        self.fill_common_fields()

        # Try to upload resume
        self.upload_resume()

        print("✅ Generic application filled. Review before submitting!")

    def get_resume_summary(self):
        """Get formatted resume summary for text boxes"""
        return self.data['summary']

    def get_skills_list(self):
        """Get comma-separated skills"""
        all_skills = []
        for category, skills in self.data['skills'].items():
            if isinstance(skills, list):
                all_skills.extend(skills)
        return ', '.join(all_skills)

    def close(self):
        """Close browser"""
        if self.driver:
            self.driver.quit()


def demo():
    """Demo usage"""
    filler = ApplicationAutoFiller()
    filler.init_browser(headless=False)

    print("\n🤖 Auto-Fill Application System Ready!")
    print("\nYour information loaded:")
    print(f"   Name: {filler.data['personal_info']['name']}")
    print(f"   Email: {filler.data['personal_info']['email']}")
    print(f"   Phone: {filler.data['personal_info']['phone']}")
    print(f"   Skills: {filler.get_skills_list()[:100]}...")

    # Example: To use this, provide a job URL
    # filler.fill_generic_application("https://example.com/job-application")

    print("\n💡 Usage:")
    print("   filler.fill_linkedin_easy_apply('JOB_URL')")
    print("   filler.fill_seek_application('JOB_URL')")
    print("   filler.fill_generic_application('JOB_URL')")

    input("\nPress Enter to close browser...")
    filler.close()


if __name__ == "__main__":
    demo()
