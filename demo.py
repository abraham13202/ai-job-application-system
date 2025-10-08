"""
Quick Demo of Job Application System
"""

from job_scraper import JobScraper
from resume_tailor import ResumeTailor
from cover_letter_generator import CoverLetterGenerator
from application_tracker import ApplicationTracker

def demo():
    print("\n" + "="*80)
    print("🚀 JOB APPLICATION SYSTEM - DEMO")
    print("="*80 + "\n")

    # Demo 1: Job Scraping
    print("📍 DEMO 1: Job Scraping")
    print("-" * 80)
    scraper = JobScraper()
    print("Scraping jobs for 'Data Scientist' in 'Sydney'...\n")

    scraper.scrape_seek("data scientist", "Sydney")
    scraper.save_to_json()

    jobs = scraper.get_jobs()
    print(f"\n✅ Found {len(jobs)} jobs")

    if jobs:
        print("\nSample jobs:")
        for job in jobs[:3]:
            print(f"  • {job['title']} at {job['company']}")

    print("\n" + "="*80 + "\n")

    # Demo 2: Resume Tailoring
    print("🎯 DEMO 2: Resume Tailoring")
    print("-" * 80)

    tailor = ResumeTailor()

    sample_job_desc = """
    Senior Data Scientist position.

    Requirements:
    - Strong Python and SQL skills
    - Experience with TensorFlow and PyTorch
    - Knowledge of NLP and Computer Vision
    - Tableau/Power BI for visualization
    - AWS cloud platform experience
    - Machine learning model deployment
    """

    print("Tailoring resume for sample job...\n")
    tailored = tailor.generate_tailored_resume(
        job_description=sample_job_desc,
        job_title="Senior Data Scientist",
        company_name="Tech Corp"
    )

    print("\n" + "="*80 + "\n")

    # Demo 3: Cover Letter Generation
    print("✍️  DEMO 3: Cover Letter Generation")
    print("-" * 80)

    gen = CoverLetterGenerator()
    print("Generating cover letter for sample job...\n")

    cover_letter = gen.generate_cover_letter(
        job_description=sample_job_desc,
        job_title="Senior Data Scientist",
        company_name="Tech Corp"
    )

    print("\nPreview (first 300 chars):")
    print("-" * 80)
    print(cover_letter[:300] + "...")

    print("\n" + "="*80 + "\n")

    # Demo 4: Application Tracking
    print("📊 DEMO 4: Application Tracking Dashboard")
    print("-" * 80)

    tracker = ApplicationTracker()

    # Add sample applications if empty
    if len(tracker.applications) == 0:
        print("Adding sample applications...\n")
        tracker.add_application(
            job_title="Data Scientist",
            company="Google",
            job_url="https://careers.google.com/jobs/123",
            notes="Applied via referral"
        )
        tracker.add_application(
            job_title="ML Engineer",
            company="Atlassian",
            job_url="https://atlassian.com/careers/456",
            notes="Strong match"
        )

    tracker.display_dashboard()

    print("\n" + "="*80 + "\n")
    print("✅ DEMO COMPLETE!")
    print("\nGenerated files in: /Users/ABRAHAM/job_application_system/")
    print("\nNext steps:")
    print("  1. Review: jobs.json (scraped jobs)")
    print("  2. Review: tailored_resume_*.txt (customized resume)")
    print("  3. Review: cover_letter_*.txt (cover letter)")
    print("  4. Review: applications.json (tracked applications)")
    print("\nTo use interactively: python3 main.py")
    print("="*80 + "\n")


if __name__ == "__main__":
    demo()
