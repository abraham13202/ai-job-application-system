"""
Batch Application Preparation
Prepares tailored resumes and cover letters for all scraped jobs
"""

import json
from resume_tailor import ResumeTailor
from cover_letter_generator import CoverLetterGenerator
from application_tracker import ApplicationTracker
import time
import os

def batch_prepare_applications():
    """Prepare application materials for all jobs"""

    # Load jobs
    with open('/Users/ABRAHAM/job_application_system/jobs.json', 'r') as f:
        jobs = json.load(f)

    tailor = ResumeTailor()
    cover_gen = CoverLetterGenerator()
    tracker = ApplicationTracker()

    print("\n" + "="*80)
    print(f"🚀 BATCH APPLICATION PREPARATION - {len(jobs)} JOBS")
    print("="*80 + "\n")

    # Create output directory
    output_dir = '/Users/ABRAHAM/job_application_system/applications_batch'
    os.makedirs(output_dir, exist_ok=True)

    for i, job in enumerate(jobs, 1):
        print(f"\n📝 [{i}/{len(jobs)}] Preparing: {job['title']} at {job['company']}")
        print("-" * 80)

        # Create company folder
        company_folder = os.path.join(output_dir, job['company'].replace('/', '_'))
        os.makedirs(company_folder, exist_ok=True)

        # Generic job description (since we can't scrape full descriptions automatically)
        # In real use, you'd fetch the actual job description from the URL
        generic_job_desc = f"""
        {job['title']} position at {job['company']} in {job['location']}.

        We are seeking a talented professional with:
        - Strong Python and data science skills
        - Experience with machine learning frameworks (TensorFlow, PyTorch)
        - Data visualization expertise (Tableau, Power BI)
        - Knowledge of SQL and databases
        - Cloud platform experience (AWS preferred)
        - Excellent analytical and problem-solving skills

        Responsibilities include:
        - Building and deploying ML models
        - Analyzing complex datasets
        - Creating dashboards and reports
        - Collaborating with cross-functional teams
        """

        # Tailor resume
        print("  🎯 Tailoring resume...")
        tailored_resume = tailor.generate_tailored_resume(
            job_description=generic_job_desc,
            job_title=job['title'],
            company_name=job['company'],
            output_format='text'
        )

        # Move tailored files to company folder
        import glob
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
        cover_letter = cover_gen.generate_cover_letter(
            job_description=generic_job_desc,
            job_title=job['title'],
            company_name=job['company']
        )

        # Move cover letter to company folder
        latest_cover = max(glob.glob('/Users/ABRAHAM/job_application_system/cover_letter_*.txt'),
                          key=os.path.getctime)
        os.rename(latest_cover,
                 os.path.join(company_folder, f"cover_letter_{job['company'].replace('/', '_')}.txt"))

        # Create application info file
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
        tracker.add_application(
            job_title=job['title'],
            company=job['company'],
            job_url=job['url'],
            location=job['location'],
            status='Prepared',
            notes=f"Skill match: {tailored_resume['skill_match_analysis']['match_percentage']:.1f}%"
        )

        print(f"  ✅ Complete! Saved to: {company_folder}")
        time.sleep(0.5)  # Brief pause

    print("\n" + "="*80)
    print("🎉 BATCH PREPARATION COMPLETE!")
    print("="*80)
    print(f"\n📁 All materials saved to: {output_dir}/")
    print("\n📊 Summary:")
    print(f"   • {len(jobs)} jobs processed")
    print(f"   • {len(jobs)} tailored resumes created")
    print(f"   • {len(jobs)} cover letters generated")
    print(f"   • All tracked in application dashboard")

    print("\n📋 Next Steps:")
    print("   1. Review materials in: applications_batch/")
    print("   2. For each job:")
    print("      - Visit the job URL")
    print("      - Upload the tailored resume")
    print("      - Copy/paste the cover letter")
    print("      - Submit application")
    print("   3. Update status in tracker after submission")

    print("\n💡 View dashboard:")
    print("   python3 -c \"from application_tracker import ApplicationTracker; ApplicationTracker().display_dashboard()\"")
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    batch_prepare_applications()
