"""
Comprehensive Job Search
Search for multiple job types across LinkedIn, Indeed, and Seek
Focus on entry-level, internships, part-time, casual positions
"""

from job_scraper import JobScraper
from resume_tailor import ResumeTailor
from cover_letter_generator import CoverLetterGenerator
from application_tracker import ApplicationTracker
import time
import os
import json
import glob

class ComprehensiveJobSearch:
    def __init__(self):
        self.scraper = JobScraper()
        self.tailor = ResumeTailor()
        self.cover_gen = CoverLetterGenerator()
        self.tracker = ApplicationTracker()
        self.all_jobs = []

    def search_all_positions(self):
        """Search for all relevant positions"""

        # Job search configurations
        searches = [
            # Data Science roles
            {"keywords": "data scientist intern", "location": "Sydney"},
            {"keywords": "data scientist graduate", "location": "Sydney"},
            {"keywords": "junior data scientist", "location": "Sydney"},
            {"keywords": "entry level data scientist", "location": "Sydney"},

            # Data Analytics roles
            {"keywords": "data analyst intern", "location": "Sydney"},
            {"keywords": "data analyst graduate", "location": "Sydney"},
            {"keywords": "junior data analyst", "location": "Sydney"},
            {"keywords": "entry level data analyst", "location": "Sydney"},
            {"keywords": "data analytics part time", "location": "Sydney"},

            # Software Developer (Java) roles
            {"keywords": "java developer graduate", "location": "Sydney"},
            {"keywords": "junior java developer", "location": "Sydney"},
            {"keywords": "java developer intern", "location": "Sydney"},
            {"keywords": "software engineer graduate", "location": "Sydney"},
            {"keywords": "backend developer java", "location": "Sydney"},

            # ML/AI roles
            {"keywords": "machine learning intern", "location": "Sydney"},
            {"keywords": "AI engineer graduate", "location": "Sydney"},
            {"keywords": "junior ML engineer", "location": "Sydney"},

            # Technical Writing
            {"keywords": "technical writer", "location": "Sydney"},
            {"keywords": "technical documentation", "location": "Sydney"},

            # Research roles
            {"keywords": "research assistant data", "location": "Sydney"},
            {"keywords": "research analyst", "location": "Sydney"},

            # Part-time/Casual
            {"keywords": "data part time", "location": "Sydney"},
            {"keywords": "python developer casual", "location": "Sydney"},
        ]

        print("\n" + "="*80)
        print("🔍 COMPREHENSIVE JOB SEARCH")
        print("="*80 + "\n")

        for i, search in enumerate(searches, 1):
            print(f"\n[{i}/{len(searches)}] Searching: {search['keywords']} in {search['location']}")
            print("-" * 80)

            # Search on all platforms
            print("  📍 Searching Seek...")
            self.scraper.scrape_seek(search['keywords'], search['location'])
            time.sleep(2)

            print("  📍 Searching Indeed...")
            self.scraper.scrape_indeed(search['keywords'], f"{search['location']} NSW")
            time.sleep(2)

            print("  📍 Searching LinkedIn...")
            self.scraper.scrape_linkedin(search['keywords'], search['location'])
            time.sleep(2)

        # Get all unique jobs
        jobs = self.scraper.get_jobs()

        # Remove duplicates based on URL
        unique_jobs = []
        seen_urls = set()
        for job in jobs:
            if job['url'] not in seen_urls:
                unique_jobs.append(job)
                seen_urls.add(job['url'])

        self.all_jobs = unique_jobs

        print("\n" + "="*80)
        print(f"✅ Search Complete! Found {len(self.all_jobs)} unique jobs")
        print("="*80 + "\n")

        # Save jobs
        self.scraper.jobs = self.all_jobs
        self.scraper.save_to_json('/Users/ABRAHAM/job_application_system/jobs_comprehensive.json')
        self.scraper.save_to_csv('/Users/ABRAHAM/job_application_system/jobs_comprehensive.csv')

        return self.all_jobs

    def prepare_all_applications(self):
        """Prepare application materials for all jobs"""

        if not self.all_jobs:
            print("No jobs to process. Run search_all_positions() first.")
            return

        print("\n" + "="*80)
        print(f"📝 PREPARING {len(self.all_jobs)} APPLICATIONS")
        print("="*80 + "\n")

        # Create output directory
        output_dir = '/Users/ABRAHAM/job_application_system/applications_comprehensive'
        os.makedirs(output_dir, exist_ok=True)

        for i, job in enumerate(self.all_jobs, 1):
            print(f"\n[{i}/{len(self.all_jobs)}] {job['title']} at {job['company']}")
            print("-" * 80)

            # Create company folder
            company_folder = os.path.join(output_dir,
                f"{job['company'].replace('/', '_').replace('|', '_')}_{i}")
            os.makedirs(company_folder, exist_ok=True)

            # Create job-specific description
            job_desc = self._create_job_description(job)

            try:
                # Tailor resume
                print("  🎯 Tailoring resume...")
                tailored_resume = self.tailor.generate_tailored_resume(
                    job_description=job_desc,
                    job_title=job['title'],
                    company_name=job['company'],
                    output_format='text'
                )

                # Move tailored files
                latest_resume = max(glob.glob('/Users/ABRAHAM/job_application_system/tailored_resume_*.txt'),
                                   key=os.path.getctime)
                os.rename(latest_resume,
                         os.path.join(company_folder, f"resume_{job['company'].replace('/', '_')}.txt"))

                latest_resume_json = max(glob.glob('/Users/ABRAHAM/job_application_system/tailored_resume_*.json'),
                                        key=os.path.getctime)
                os.rename(latest_resume_json,
                         os.path.join(company_folder, f"resume_{job['company'].replace('/', '_')}.json"))

                # Generate cover letter
                print("  ✍️  Generating cover letter...")
                cover_letter = self.cover_gen.generate_cover_letter(
                    job_description=job_desc,
                    job_title=job['title'],
                    company_name=job['company']
                )

                # Move cover letter
                latest_cover = max(glob.glob('/Users/ABRAHAM/job_application_system/cover_letter_*.txt'),
                                  key=os.path.getctime)
                os.rename(latest_cover,
                         os.path.join(company_folder, f"cover_letter_{job['company'].replace('/', '_')}.txt"))

                # Create application info
                app_info = {
                    'job_title': job['title'],
                    'company': job['company'],
                    'location': job['location'],
                    'url': job['url'],
                    'source': job['source'],
                    'skill_match': f"{tailored_resume['skill_match_analysis']['match_percentage']:.1f}%",
                    'matched_skills': tailored_resume['skill_match_analysis']['matched'],
                    'status': 'Ready to Apply'
                }

                with open(os.path.join(company_folder, 'application_info.json'), 'w') as f:
                    json.dump(app_info, f, indent=2)

                # Track in system
                self.tracker.add_application(
                    job_title=job['title'],
                    company=job['company'],
                    job_url=job['url'],
                    location=job['location'],
                    status='Prepared',
                    notes=f"Skill match: {tailored_resume['skill_match_analysis']['match_percentage']:.1f}%. Source: {job['source']}"
                )

                print(f"  ✅ Complete!")

            except Exception as e:
                print(f"  ❌ Error: {e}")
                continue

            time.sleep(0.3)

        print("\n" + "="*80)
        print("🎉 ALL APPLICATIONS PREPARED!")
        print("="*80)
        print(f"\n📁 Saved to: {output_dir}/")
        print(f"📊 Total: {len(self.all_jobs)} applications ready")
        print("\n💡 Refresh the web interface to see new applications")
        print("="*80 + "\n")

    def _create_job_description(self, job):
        """Create a job description based on job title"""
        title_lower = job['title'].lower()

        # Determine job type
        if 'data scientist' in title_lower or 'data science' in title_lower:
            return f"""
            {job['title']} position at {job['company']} in {job['location']}.

            We are seeking a talented Data Scientist with:
            - Strong Python programming skills
            - Experience with machine learning frameworks (TensorFlow, PyTorch, scikit-learn)
            - Data analysis and visualization (Tableau, Power BI, Matplotlib)
            - SQL and database knowledge
            - Statistical analysis and modeling
            - Strong problem-solving abilities

            Responsibilities:
            - Build and deploy ML models
            - Analyze complex datasets
            - Create data visualizations and dashboards
            - Collaborate with cross-functional teams
            - Present insights to stakeholders
            """

        elif 'data analyst' in title_lower:
            return f"""
            {job['title']} position at {job['company']} in {job['location']}.

            We are seeking a Data Analyst with:
            - Proficiency in SQL and data querying
            - Data visualization tools (Tableau, Power BI)
            - Python or R for data analysis
            - Statistical analysis skills
            - Excel and spreadsheet expertise
            - Strong communication skills

            Responsibilities:
            - Analyze business data and trends
            - Create reports and dashboards
            - Identify insights and recommendations
            - Support data-driven decision making
            """

        elif 'java' in title_lower or 'software' in title_lower or 'backend' in title_lower:
            return f"""
            {job['title']} position at {job['company']} in {job['location']}.

            We are seeking a Software Developer with:
            - Strong Java programming skills
            - Object-oriented programming expertise
            - Spring Boot framework experience
            - Database knowledge (SQL)
            - REST API development
            - Problem-solving abilities

            Responsibilities:
            - Develop backend applications
            - Write clean, maintainable code
            - Participate in code reviews
            - Collaborate with team members
            - Debug and optimize applications
            """

        elif 'machine learning' in title_lower or 'ml engineer' in title_lower or 'ai' in title_lower:
            return f"""
            {job['title']} position at {job['company']} in {job['location']}.

            We are seeking an ML/AI professional with:
            - Strong Python skills
            - Deep learning frameworks (TensorFlow, PyTorch)
            - Machine learning algorithms
            - Model deployment experience
            - NLP or Computer Vision knowledge
            - Research mindset

            Responsibilities:
            - Develop ML models and algorithms
            - Train and optimize models
            - Deploy models to production
            - Research new techniques
            - Collaborate on AI projects
            """

        elif 'technical writer' in title_lower or 'documentation' in title_lower:
            return f"""
            {job['title']} position at {job['company']} in {job['location']}.

            We are seeking a Technical Writer with:
            - Excellent written communication
            - Technical background (CS, Engineering)
            - Documentation tools expertise
            - Ability to explain complex concepts
            - Attention to detail
            - Collaboration skills

            Responsibilities:
            - Create technical documentation
            - Write user guides and API docs
            - Maintain documentation systems
            - Work with developers and product teams
            """

        else:
            # Generic technical role
            return f"""
            {job['title']} position at {job['company']} in {job['location']}.

            We are seeking a technical professional with:
            - Strong programming skills (Python, Java)
            - Data analysis capabilities
            - Problem-solving mindset
            - Collaboration abilities
            - Continuous learning attitude
            - Technical communication skills

            Responsibilities:
            - Work on technical projects
            - Analyze and solve problems
            - Collaborate with teams
            - Contribute to product development
            """


def main():
    """Run comprehensive search and prepare applications"""
    search = ComprehensiveJobSearch()

    print("\n🚀 Starting comprehensive job search...")
    print("   Will search for:")
    print("   ✅ Data Science (intern, graduate, junior, entry-level)")
    print("   ✅ Data Analytics (all levels, part-time)")
    print("   ✅ Software Development (Java, backend)")
    print("   ✅ Machine Learning / AI")
    print("   ✅ Technical Writing")
    print("   ✅ Research positions")
    print("\n   Across: Seek, Indeed, LinkedIn")
    print("\n" + "="*80 + "\n")

    # Search for jobs
    jobs = search.search_all_positions()

    # Prepare applications
    if jobs:
        search.prepare_all_applications()
    else:
        print("No jobs found. Try adjusting search parameters.")


if __name__ == "__main__":
    main()
