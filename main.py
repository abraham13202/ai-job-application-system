"""
Job Application Automation System - Main Interface
Orchestrates all components: scraping, tailoring, cover letters, auto-fill, and tracking
"""

import sys
from job_scraper import JobScraper
from resume_tailor import ResumeTailor
from cover_letter_generator import CoverLetterGenerator
from application_tracker import ApplicationTracker
from auto_fill_application import ApplicationAutoFiller
import time

class JobApplicationSystem:
    def __init__(self):
        """Initialize all components"""
        self.scraper = JobScraper()
        self.tailor = ResumeTailor()
        self.cover_gen = CoverLetterGenerator()
        self.tracker = ApplicationTracker()
        self.auto_filler = None  # Initialize when needed

    def run_full_workflow(self, keywords="data scientist", location="Sydney"):
        """Run complete job application workflow"""

        print("\n" + "="*80)
        print("🚀 JOB APPLICATION AUTOMATION SYSTEM")
        print("="*80 + "\n")

        # Step 1: Scrape jobs
        print("📍 STEP 1: Scraping job listings...")
        print(f"   Keywords: {keywords}")
        print(f"   Location: {location}\n")

        self.scraper.scrape_seek(keywords, location)
        time.sleep(2)
        self.scraper.scrape_indeed(keywords, f"{location} NSW")

        jobs = self.scraper.get_jobs()

        if not jobs:
            print("❌ No jobs found. Try different keywords or locations.")
            return

        print(f"\n✅ Found {len(jobs)} jobs\n")

        # Step 2: Display jobs and let user select
        print("📋 AVAILABLE JOBS:")
        for i, job in enumerate(jobs[:10], 1):  # Show top 10
            print(f"\n{i}. {job['title']}")
            print(f"   Company: {job['company']}")
            print(f"   Location: {job['location']}")
            print(f"   Source: {job['source']}")
            print(f"   URL: {job['url'][:80]}...")

        # Save jobs
        self.scraper.save_to_json()

        print("\n" + "="*80)
        print("\n💡 Next Steps:")
        print("   1. Review jobs in: /Users/ABRAHAM/job_application_system/jobs.json")
        print("   2. Use apply_to_job() to apply to specific jobs")
        print("   3. View dashboard with tracker.display_dashboard()")

    def apply_to_job(self, job_title, company_name, job_description, job_url, auto_fill=False):
        """Apply to a specific job"""

        print(f"\n📝 Applying to: {job_title} at {company_name}")
        print("="*80 + "\n")

        # Step 1: Tailor resume
        print("🎯 Step 1: Tailoring resume...")
        tailored_resume = self.tailor.generate_tailored_resume(
            job_description=job_description,
            job_title=job_title,
            company_name=company_name
        )

        # Step 2: Generate cover letter
        print("\n✍️  Step 2: Generating cover letter...")
        cover_letter = self.cover_gen.generate_cover_letter(
            job_description=job_description,
            job_title=job_title,
            company_name=company_name
        )

        # Step 3: Track application
        print("\n📊 Step 3: Adding to tracker...")
        app_id = self.tracker.add_application(
            job_title=job_title,
            company=company_name,
            job_url=job_url,
            notes=f"Tailored resume and cover letter generated. Match: {tailored_resume['skill_match_analysis']['match_percentage']:.1f}%"
        )

        # Step 4: Auto-fill (optional)
        if auto_fill:
            print("\n🤖 Step 4: Auto-filling application...")
            print("⚠️  Note: This will open a browser. You must review and submit manually.")

            response = input("Continue with auto-fill? (y/n): ")
            if response.lower() == 'y':
                if not self.auto_filler:
                    self.auto_filler = ApplicationAutoFiller()
                    self.auto_filler.init_browser()

                self.auto_filler.fill_generic_application(job_url)

        print("\n" + "="*80)
        print(f"✅ Application #{app_id} prepared successfully!")
        print("\n📁 Generated files:")
        print("   • Tailored resume (JSON & TXT)")
        print("   • Custom cover letter")
        print("   • Application tracked in database")
        print("\n💡 Next: Review materials and submit application")
        print("="*80 + "\n")

    def quick_apply(self, job_index=0):
        """Quick apply to a job from scraped list"""
        jobs = self.scraper.get_jobs()

        if not jobs or job_index >= len(jobs):
            print("❌ Job not found. Run run_full_workflow() first.")
            return

        job = jobs[job_index]

        # For demo, use a generic job description
        # In real use, you'd fetch the full job description from the URL
        job_description = f"""
        {job['title']} position at {job['company']}.

        We are looking for a skilled data scientist with experience in:
        - Python, SQL, and machine learning
        - Data visualization and analytics
        - Building and deploying ML models
        - Strong communication skills
        """

        self.apply_to_job(
            job_title=job['title'],
            company_name=job['company'],
            job_description=job_description,
            job_url=job['url'],
            auto_fill=False
        )

    def show_dashboard(self):
        """Show application tracking dashboard"""
        self.tracker.display_dashboard()

    def cleanup(self):
        """Cleanup resources"""
        if self.auto_filler:
            self.auto_filler.close()


def main():
    """Main entry point"""
    system = JobApplicationSystem()

    print("\n" + "="*80)
    print("🤖 JOB APPLICATION AUTOMATION SYSTEM")
    print("="*80)
    print("\nWelcome! This system will help you:")
    print("  ✅ Scrape jobs from multiple sources")
    print("  ✅ Tailor your resume for each job")
    print("  ✅ Generate custom cover letters")
    print("  ✅ Auto-fill applications")
    print("  ✅ Track all your applications")
    print("\n" + "="*80 + "\n")

    # Interactive menu
    while True:
        print("\n📋 MAIN MENU")
        print("1. Search and scrape jobs")
        print("2. Apply to a job (with job description)")
        print("3. View application dashboard")
        print("4. Export applications to CSV")
        print("5. Exit")

        choice = input("\nSelect option (1-5): ").strip()

        if choice == '1':
            keywords = input("Job keywords (default: data scientist): ").strip() or "data scientist"
            location = input("Location (default: Sydney): ").strip() or "Sydney"
            system.run_full_workflow(keywords, location)

        elif choice == '2':
            job_title = input("Job title: ").strip()
            company = input("Company name: ").strip()
            job_url = input("Job URL: ").strip()
            print("\nPaste job description (end with empty line):")

            job_desc_lines = []
            while True:
                line = input()
                if not line:
                    break
                job_desc_lines.append(line)

            job_description = '\n'.join(job_desc_lines)

            auto_fill = input("\nAuto-fill application? (y/n): ").strip().lower() == 'y'

            system.apply_to_job(job_title, company, job_description, job_url, auto_fill)

        elif choice == '3':
            system.show_dashboard()

        elif choice == '4':
            system.tracker.export_to_csv()

        elif choice == '5':
            print("\n👋 Goodbye! Good luck with your applications!")
            system.cleanup()
            break

        else:
            print("❌ Invalid option. Please select 1-5.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Exiting... Goodbye!")
        sys.exit(0)
