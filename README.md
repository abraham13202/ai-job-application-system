# 🚀 AI Job Application System

**Automate your job search with AI-powered resume tailoring, cover letter generation, and application tracking.**

> A comprehensive tool to help students and job seekers worldwide find opportunities, tailor applications, and track their progress across multiple job platforms - all from a beautiful web interface!

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-blue)]()

---

## ✨ Features

### 🔍 **Web-Based Job Search** (NEW!)
- **No coding required!** Search for jobs directly from your browser
- Enter keywords, select platforms, and watch the magic happen
- Real-time progress tracking with live updates
- Automatically generates tailored resumes and cover letters for each job
- Works on **Seek, Indeed, and LinkedIn**

### 🎯 **Intelligent Resume Tailoring**
- Analyzes job descriptions automatically
- Matches your skills with job requirements
- Shows skill match percentage for each job
- Prioritizes relevant experience and projects
- Generates both JSON and formatted text versions

### ✍️ **Smart Cover Letter Generation**
- Creates personalized cover letters for each application
- Highlights your relevant experience
- Professional formatting
- Matches company culture and role requirements

### 📊 **Beautiful Web Dashboard**
- Track all applications in one place
- See statistics and analytics
- Filter and sort jobs by priority
- Export to CSV for spreadsheets
- **No terminal or coding knowledge needed!**

### 🌐 **Chrome Extension** (Optional)
- Save LinkedIn profiles manually
- Quick-add recruiters and hiring managers
- Track networking contacts

---

## 💻 Installation

### Quick Start (Recommended)

Choose your operating system:

<details>
<summary><b>🍎 macOS</b></summary>

```bash
# 1. Download the project
# Click "Code" → "Download ZIP" on GitHub, then extract it
# Or use git:
git clone https://github.com/abraham13202/ai-job-application-system.git
cd ai-job-application-system

# 2. Run the setup script
chmod +x setup.sh
./setup.sh

# 3. Start the web interface
source venv/bin/activate
python3 web_app.py

# 4. Open your browser to http://localhost:5000
```

**Done!** 🎉 The web interface will open automatically.

</details>

<details>
<summary><b>🪟 Windows</b></summary>

```powershell
# 1. Download the project
# Click "Code" → "Download ZIP" on GitHub, then extract it
# Or use git:
git clone https://github.com/abraham13202/ai-job-application-system.git
cd ai-job-application-system

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Edit your resume data
# Open resume_data.json in Notepad and add your information

# 5. Start the web interface
python web_app.py

# 6. Open your browser to http://localhost:5000
```

**Done!** 🎉

</details>

<details>
<summary><b>🐧 Linux</b></summary>

```bash
# 1. Download the project
git clone https://github.com/abraham13202/ai-job-application-system.git
cd ai-job-application-system

# 2. Run the setup script
chmod +x setup.sh
./setup.sh

# 3. Start the web interface
source venv/bin/activate
python3 web_app.py

# 4. Open your browser to http://localhost:5000
```

**Done!** 🎉

</details>

---

## 🚀 How to Use

### For Non-Technical Users (Easiest!)

1. **Install** using the instructions above
2. **Start the web app**: `python3 web_app.py` (or `python web_app.py` on Windows)
3. **Open browser** to http://localhost:5000
4. **Enter your job search keywords** in the search panel:
   ```
   data scientist intern
   software engineer graduate
   junior analyst
   ```
5. **Select platforms** (Seek, Indeed, LinkedIn)
6. **Click "Search Jobs"**
7. **Watch the progress bar** as it finds and processes jobs
8. **View results** - all jobs sorted by priority with tailored resumes!

**That's it!** No coding, no terminal commands, just a simple web interface.

### For Developers (Advanced)

<details>
<summary>Click to expand advanced usage</summary>

#### Command Line Interface

```bash
# Search for jobs
python3 comprehensive_search.py

# Interactive menu
python3 main.py
```

#### Python API

```python
from job_scraper import JobScraper
from resume_tailor import ResumeTailor

# Search for jobs
scraper = JobScraper()
jobs = scraper.scrape_seek("data scientist", "Sydney")

# Tailor resume
tailor = ResumeTailor()
result = tailor.generate_tailored_resume(
    job_description="...",
    job_title="Data Scientist",
    company_name="Google"
)
```

</details>

---

## ⚙️ Configuration

### Step 1: Add Your Resume Information

Edit `resume_data.json` with your details:

```json
{
  "name": "Your Name",
  "email": "your.email@example.com",
  "location": "Sydney, Australia",

  "education": [
    {
      "degree": "Bachelor of Computer Science",
      "institution": "University of Sydney",
      "graduation_date": "2024"
    }
  ],

  "skills": [
    "Python",
    "Machine Learning",
    "Data Analysis",
    "SQL"
  ],

  "experience": [
    {
      "title": "Software Engineering Intern",
      "company": "Tech Company",
      "start_date": "Jun 2023",
      "end_date": "Aug 2023",
      "responsibilities": [
        "Developed features using Python",
        "Collaborated with team of 5 engineers"
      ]
    }
  ]
}
```

### Step 2: Customize Search (Optional)

The web interface lets you customize:
- **Keywords**: Enter any job titles you're looking for
- **Location**: Change from Sydney to your city
- **Platforms**: Select which job sites to search

---

## 🌍 Supported Countries & Job Platforms

### Currently Configured
- 🇦🇺 **Australia**: Seek, Indeed, LinkedIn
- 🇺🇸 **USA**: Indeed, LinkedIn (add Glassdoor easily!)
- 🇬🇧 **UK**: Indeed, LinkedIn (add Reed easily!)
- 🇨🇦 **Canada**: Indeed, LinkedIn

### Want Your Country?
It's easy to add! Just update the location in the web interface. The scrapers work globally!

---

## 📱 Chrome Extension (Optional)

For tracking LinkedIn contacts manually:

1. Open Chrome → `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select the `chrome_extension` folder
5. Visit LinkedIn profiles and click the extension icon to save contacts

---

## 🎓 Perfect for Students!

### ✅ Why Students Love This Tool

- **Save Time**: Instead of spending hours searching, let the tool find jobs for you
- **Better Applications**: Tailored resumes match each job's requirements
- **Stay Organized**: Track all applications in one dashboard
- **Learn Faster**: See what skills employers are looking for
- **No Coding**: Use the web interface - no programming knowledge needed!

### 📚 Great for:
- Computer Science students
- Data Science students
- Engineering students
- Business students
- Anyone looking for their first job!

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md)

**Ways to help:**
- Add support for more job platforms
- Improve resume tailoring algorithm
- Add translations for other languages
- Create video tutorials
- Report bugs and suggest features

---

## ❓ FAQ

<details>
<summary><b>Do I need to know programming to use this?</b></summary>

**No!** Just follow the installation instructions, start the web app, and use the browser interface. No coding required!

</details>

<details>
<summary><b>Will this work on my computer?</b></summary>

**Yes!** Works on Windows, macOS, and Linux. Just need Python 3.8 or higher.

</details>

<details>
<summary><b>Is web scraping legal?</b></summary>

For personal use, yes. Always check each website's Terms of Service and `robots.txt`. Be respectful with request rates. This tool is for personal job searching only.

</details>

<details>
<summary><b>Will I get banned from LinkedIn?</b></summary>

The tool doesn't automate LinkedIn actions. It only saves profiles you manually visit via the Chrome extension. No automation = no risk!

</details>

<details>
<summary><b>How accurate is the skill matching?</b></summary>

The algorithm analyzes keywords and calculates overlap between your skills and job requirements. It's quite accurate but always review the results yourself!

</details>

<details>
<summary><b>Can I customize the resume and cover letter templates?</b></summary>

Yes! Edit the template files in the `templates/` folder or modify the generation logic in `resume_tailor.py` and `cover_letter_generator.py`.

</details>

<details>
<summary><b>Is my data safe?</b></summary>

**100% yes!** Everything is stored locally on your computer. No data is sent to external servers. You control everything.

</details>

<details>
<summary><b>Can I use this for non-technical jobs?</b></summary>

Absolutely! Just update your `resume_data.json` with your experience and skills, then search for any type of job. Works for marketing, finance, nursing, teaching, etc.

</details>

---

## 🛠️ Troubleshooting

<details>
<summary><b>Python not found</b></summary>

**macOS/Linux:**
```bash
# Install Python 3.8+
brew install python3  # macOS
sudo apt install python3  # Linux
```

**Windows:**
Download from [python.org](https://www.python.org/downloads/)

</details>

<details>
<summary><b>Module not found errors</b></summary>

Make sure you're in the virtual environment:

```bash
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate

# Then reinstall
pip install -r requirements.txt
```

</details>

<details>
<summary><b>Port 5000 already in use</b></summary>

Change the port in `web_app.py`:
```python
app.run(debug=True, port=5001)  # Change to 5001 or any other port
```

</details>

<details>
<summary><b>No jobs found</b></summary>

- Try different keywords
- Check your internet connection
- Some job sites may block scraping (use VPN or try later)
- LinkedIn requires login for most features

</details>

---

## 📄 License

MIT License - See [LICENSE](LICENSE)

**TL;DR:** Free to use, modify, and share. Just keep the license notice.

---

## 🙏 Acknowledgments

- Built with Python, Flask, BeautifulSoup, and Selenium
- Created to help students worldwide find their dream jobs
- Inspired by the struggles of job hunting during university

---

## 💖 Support

If this tool helped you land a job, please:
- ⭐ Star this repository
- 📢 Share with other job seekers
- 💬 Share your success story in [Discussions](https://github.com/abraham13202/ai-job-application-system/discussions)

---

## 📞 Get Help

- **Issues**: [GitHub Issues](https://github.com/abraham13202/ai-job-application-system/issues)
- **Questions**: [GitHub Discussions](https://github.com/abraham13202/ai-job-application-system/discussions)
- **Email**: abrahamkuriakosevit@gmail.com

---

**Made with ❤️ for students worldwide**

*Good luck with your job search! You've got this!* 🚀

---

## 🎯 Quick Links

- [Installation](#-installation)
- [How to Use](#-how-to-use)
- [Configuration](#️-configuration)
- [FAQ](#-faq)
- [Contributing](CONTRIBUTING.md)
- [License](LICENSE)


