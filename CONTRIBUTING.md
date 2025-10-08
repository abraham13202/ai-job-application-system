# Contributing to AI Job Application System

First off, thank you for considering contributing! 🎉

This project was created to help students and job seekers worldwide, and we welcome contributions of all kinds.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)
- [Community](#community)

## 📜 Code of Conduct

This project and everyone participating in it is governed by respect, kindness, and professionalism. Be welcoming to newcomers, be patient with questions, and be respectful of differing viewpoints.

## 🤝 How Can I Contribute?

### 🐛 Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce**
- **Expected vs actual behavior**
- **Screenshots** (if applicable)
- **Environment details** (OS, Python version, etc.)

### 💡 Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear title**
- **Provide detailed description** of the proposed feature
- **Explain why this would be useful** to most users
- **List any alternatives** you've considered

### 🌍 Adding Support for New Countries

We'd love to support more job platforms globally! To add a new country:

1. Research popular job platforms in that country
2. Check their `robots.txt` and Terms of Service
3. Implement scraper in `job_scraper.py`
4. Add configuration options
5. Update documentation
6. Test thoroughly

### 📝 Improving Documentation

- Fix typos or clarify existing docs
- Add examples and tutorials
- Translate documentation to other languages
- Create video tutorials

### 🎨 Design Contributions

- Improve UI/UX of web dashboard
- Create better icons and graphics
- Design promotional materials
- Create demo videos/GIFs

## 🛠️ Development Setup

### 1. Fork and Clone

```bash
# Fork the repo on GitHub, then clone your fork
git clone https://github.com/YOUR-USERNAME/ai-job-application-system.git
cd ai-job-application-system
```

### 2. Set Up Environment

```bash
# Run the setup script
./setup.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### 4. Make Your Changes

- Write clear, commented code
- Follow the style guidelines below
- Test your changes thoroughly
- Update documentation as needed

### 5. Test

```bash
# Run the web app
python web_app.py

# Test job scraping
python comprehensive_search.py

# Test specific components
python -c "from job_scraper import JobScraper; s = JobScraper(); print('OK')"
```

## 🔄 Pull Request Process

1. **Update documentation** - Update README.md if you changed functionality
2. **Update changelog** - Add a brief note about your changes
3. **Test thoroughly** - Make sure everything works
4. **Create PR** with clear title and description:

```markdown
## What does this PR do?
Brief description of changes

## Why?
Explain the motivation

## How to test?
Steps to verify your changes work

## Screenshots (if applicable)
Add screenshots showing the changes
```

5. **Wait for review** - Maintainers will review your PR
6. **Address feedback** - Make requested changes if needed
7. **Celebrate!** 🎉 Your contribution will be merged

## 📐 Style Guidelines

### Python Code Style

- Follow [PEP 8](https://pep8.org/)
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and small
- Add comments for complex logic

```python
# Good example
def calculate_skill_match(job_skills: list, resume_skills: list) -> float:
    """
    Calculate percentage match between job requirements and resume skills.

    Args:
        job_skills: List of skills from job description
        resume_skills: List of skills from resume

    Returns:
        Percentage match as float (0-100)
    """
    matched = set(job_skills) & set(resume_skills)
    return (len(matched) / len(job_skills)) * 100 if job_skills else 0
```

### Commit Messages

Use clear, descriptive commit messages:

```bash
# Good
git commit -m "Add support for Glassdoor job scraping"
git commit -m "Fix skill matching algorithm for edge cases"
git commit -m "Update README with installation instructions"

# Bad
git commit -m "fix bug"
git commit -m "updates"
git commit -m "asdf"
```

### File Organization

```
job_application_system/
├── *.py              # Main Python modules
├── templates/        # HTML/email templates
├── chrome_extension/ # Browser extension files
├── docs/            # Documentation and screenshots
├── tests/           # Unit tests (coming soon)
└── README.md        # Main documentation
```

## 🌟 Areas We Need Help

### High Priority
- [ ] Add more job platform scrapers (Glassdoor, ZipRecruiter, etc.)
- [ ] Improve resume parsing and tailoring algorithms
- [ ] Add unit tests
- [ ] Better error handling and logging
- [ ] Performance optimizations

### Medium Priority
- [ ] Mobile app (React Native/Flutter)
- [ ] Email notifications
- [ ] Interview preparation module
- [ ] Salary insights and analytics
- [ ] LinkedIn API integration (official)

### Documentation
- [ ] Video tutorials
- [ ] Translations (Spanish, Hindi, Mandarin, etc.)
- [ ] More examples and use cases
- [ ] Troubleshooting guide
- [ ] Best practices guide

## 💬 Community

- **Discussions:** Use [GitHub Discussions](https://github.com/yourusername/ai-job-application-system/discussions) for questions
- **Issues:** Use [GitHub Issues](https://github.com/yourusername/ai-job-application-system/issues) for bugs and features
- **Discord:** [Join our Discord](https://discord.gg/your-link) (coming soon)

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

All contributors will be recognized in our [Contributors](https://github.com/yourusername/ai-job-application-system/graphs/contributors) page and README.

Thank you for making this project better! ❤️

---

**Questions?** Feel free to reach out by creating a discussion or issue.

Happy contributing! 🚀
