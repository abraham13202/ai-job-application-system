# 🚀 AI Job Application System

**Automate your job search with AI-powered resume tailoring, cover letter generation, and application tracking.**

> A comprehensive tool to help students and job seekers find opportunities, tailor applications, and track their progress across multiple job platforms.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

---

## Features

### 1. Job Scraping
- Scrapes jobs from **Seek**, **Indeed**, and **LinkedIn**
- Filters by keywords and location
- Saves results to JSON/CSV

### 2. Resume Tailoring
- Analyzes job descriptions
- Matches your skills with requirements
- Prioritizes relevant experience and projects
- Generates customized resume (JSON + TXT)
- Shows skill match percentage

### 3. Cover Letter Generation
- Creates tailored cover letters automatically
- Highlights relevant experience
- Matches job requirements
- Professional formatting

### 4. Auto-Fill Applications
- Uses Selenium to auto-fill forms
- Supports LinkedIn Easy Apply, Seek, and generic forms
- Uploads resume automatically
- **Note**: You must review and submit manually

### 5. Application Tracking
- Dashboard with statistics
- Track application status
- Follow-up reminders
- Export to CSV

## Setup

### 1. Install Dependencies

```bash
cd /Users/ABRAHAM/job_application_system
pip install -r requirements.txt
```

### 2. Install Chrome WebDriver (for auto-fill)

```bash
# macOS with Homebrew
brew install chromedriver

# Or download from: https://chromedriver.chromium.org/
```

### 3. Your Resume Data

Your resume is already loaded in `resume_data.json`. Update it if needed.

## Usage

### Option 1: Interactive Mode

```bash
python main.py
```

Follow the menu to:
1. Search and scrape jobs
2. Apply to jobs
3. View dashboard
4. Export applications

### Option 2: Individual Components

#### Scrape Jobs
```python
from job_scraper import JobScraper

scraper = JobScraper()
scraper.scrape_seek("data scientist", "Sydney")
scraper.scrape_indeed("data scientist", "Sydney NSW")
scraper.save_to_json()
```

#### Tailor Resume
```python
from resume_tailor import ResumeTailor

tailor = ResumeTailor()
job_description = "..." # Paste job description

tailored = tailor.generate_tailored_resume(
    job_description=job_description,
    job_title="Data Scientist",
    company_name="Google"
)
```

#### Generate Cover Letter
```python
from cover_letter_generator import CoverLetterGenerator

gen = CoverLetterGenerator()
cover_letter = gen.generate_cover_letter(
    job_description=job_description,
    job_title="Data Scientist",
    company_name="Google"
)
```

#### Track Applications
```python
from application_tracker import ApplicationTracker

tracker = ApplicationTracker()
tracker.add_application(
    job_title="Data Scientist",
    company="Google",
    job_url="https://...",
    notes="Applied via referral"
)

tracker.display_dashboard()
```

#### Auto-Fill Application
```python
from auto_fill_application import ApplicationAutoFiller

filler = ApplicationAutoFiller()
filler.init_browser()
filler.fill_generic_application("JOB_URL")
# Review and submit manually
filler.close()
```

### Option 3: Complete Workflow

```python
from main import JobApplicationSystem

system = JobApplicationSystem()

# 1. Search jobs
system.run_full_workflow("data scientist", "Sydney")

# 2. Apply to specific job
job_description = "..." # Full job description
system.apply_to_job(
    job_title="Senior Data Scientist",
    company_name="Atlassian",
    job_description=job_description,
    job_url="https://...",
    auto_fill=True  # Optional
)

# 3. View dashboard
system.show_dashboard()
```

## Files Generated

- `jobs.json` - Scraped jobs
- `jobs.csv` - Scraped jobs (CSV)
- `tailored_resume_TIMESTAMP.json` - Tailored resume data
- `tailored_resume_TIMESTAMP.txt` - Tailored resume (text)
- `cover_letter_COMPANY_TIMESTAMP.txt` - Cover letter
- `applications.json` - Application tracker database
- `applications.csv` - Exported applications

## Important Notes

### ⚠️ Web Scraping
- Job sites may block scraping or require login
- LinkedIn heavily restricts scraping (consider using API)
- Be respectful with request frequency
- Some sites may require Selenium for dynamic content

### 🤖 Auto-Fill
- **Always review** before submitting
- You are responsible for application accuracy
- Some sites have anti-bot measures
- Manual review ensures quality

### 🔒 Privacy
- Resume data is stored locally only
- No data is sent to external servers
- You control all submissions

### ✅ Best Practices
1. Review all generated content before use
2. Customize cover letters further for important roles
3. Track follow-ups and responses
4. Update resume_data.json regularly
5. Backup your applications.json

## Workflow Example

```bash
# 1. Search for jobs
python main.py
# Select option 1, enter "data scientist" and "Sydney"

# 2. Review scraped jobs
cat jobs.json

# 3. Apply to a job
python main.py
# Select option 2, provide job details

# 4. Check generated files
ls -la tailored_resume_*.txt
ls -la cover_letter_*.txt

# 5. View dashboard
python main.py
# Select option 3

# 6. Export for spreadsheet
python main.py
# Select option 4
```

## Troubleshooting

### ChromeDriver Issues
```bash
# Check Chrome version
google-chrome --version

# Install matching ChromeDriver version
brew install chromedriver
```

### Scraping Blocked
- Try with longer delays between requests
- Use VPN or different IP
- Consider using official APIs
- Selenium may work better for some sites

### Import Errors
```bash
pip install --upgrade -r requirements.txt
```

## Future Enhancements

- [ ] LinkedIn API integration
- [ ] Email notifications for responses
- [ ] Interview scheduler
- [ ] Salary tracker
- [ ] Network analysis (who works where)
- [ ] Job recommendation based on skills
- [ ] Browser extension for one-click apply

## License

Personal use only. Respect terms of service for job sites.

## Support

For issues or questions:
1. Check job site's robots.txt
2. Verify ChromeDriver installation
3. Update dependencies
4. Review error messages

---

**Good luck with your job search! 🚀**
