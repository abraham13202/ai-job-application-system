"""
Smart Job Prioritization
Filters and ranks jobs based on quality and fit
"""

import json
import re

class JobPrioritizer:
    def __init__(self, jobs_file='/Users/ABRAHAM/job_application_system/jobs_comprehensive.json'):
        with open(jobs_file, 'r') as f:
            self.jobs = json.load(f)

    def score_job(self, job):
        """Score a job based on various factors"""
        score = 0
        title = job['title'].lower()
        company = job['company'].lower()

        # HIGH PRIORITY KEYWORDS (20 points each)
        high_priority = [
            'intern', 'internship', 'graduate', 'entry level', 'junior',
            'undergraduate', 'student', 'vacationer', 'trainee'
        ]
        for keyword in high_priority:
            if keyword in title:
                score += 20
                break

        # TOP COMPANIES (50 points)
        top_companies = [
            'google', 'microsoft', 'tiktok', 'meta', 'amazon', 'apple',
            'atlassian', 'canva', 'ey', 'deloitte', 'pwc', 'kpmg',
            'commonwealth bank', 'westpac', 'anz', 'nab',
            'qantas', 'telstra', 'optus'
        ]
        for top_company in top_companies:
            if top_company in company:
                score += 50
                break

        # RELEVANT ROLES (15 points each)
        relevant_roles = [
            'data scientist', 'data analyst', 'machine learning',
            'ml engineer', 'ai engineer', 'research', 'java developer',
            'backend', 'python developer'
        ]
        for role in relevant_roles:
            if role in title:
                score += 15
                break

        # BONUS: Part-time/Casual/Flexible (10 points)
        if any(word in title for word in ['part time', 'casual', 'flexible', 'remote']):
            score += 10

        # BONUS: Sydney location (5 points)
        if 'sydney' in job['location'].lower():
            score += 5

        # PENALTY: Senior/Lead roles (-30 points)
        if any(word in title for word in ['senior', 'lead', 'principal', 'staff', 'head of']):
            score -= 30

        # PENALTY: Requires years of experience (-20 points)
        if any(word in title for word in ['5+', '3+', '10+', 'experienced']):
            score -= 20

        # BONUS: Source diversity
        if job['source'] == 'LinkedIn':
            score += 3
        elif job['source'] == 'Indeed':
            score += 2

        return max(0, score)  # Don't go negative

    def categorize_jobs(self):
        """Categorize jobs into tiers"""
        scored_jobs = []
        for job in self.jobs:
            score = self.score_job(job)
            job['priority_score'] = score
            scored_jobs.append(job)

        # Sort by score
        scored_jobs.sort(key=lambda x: x['priority_score'], reverse=True)

        # Categorize
        tier_1 = [j for j in scored_jobs if j['priority_score'] >= 60]  # Must apply
        tier_2 = [j for j in scored_jobs if 30 <= j['priority_score'] < 60]  # Should apply
        tier_3 = [j for j in scored_jobs if 10 <= j['priority_score'] < 30]  # Nice to have
        tier_4 = [j for j in scored_jobs if j['priority_score'] < 10]  # Low priority

        return {
            'tier_1_must_apply': tier_1,
            'tier_2_should_apply': tier_2,
            'tier_3_nice_to_have': tier_3,
            'tier_4_low_priority': tier_4
        }

    def get_top_recommendations(self, limit=50):
        """Get top N job recommendations"""
        tiers = self.categorize_jobs()

        print("\n" + "="*80)
        print("🎯 SMART JOB PRIORITIZATION")
        print("="*80 + "\n")

        print(f"📊 BREAKDOWN:")
        print(f"   🔥 Tier 1 (MUST APPLY): {len(tiers['tier_1_must_apply'])} jobs")
        print(f"   ⭐ Tier 2 (SHOULD APPLY): {len(tiers['tier_2_should_apply'])} jobs")
        print(f"   ✨ Tier 3 (NICE TO HAVE): {len(tiers['tier_3_nice_to_have'])} jobs")
        print(f"   📋 Tier 4 (LOW PRIORITY): {len(tiers['tier_4_low_priority'])} jobs")

        # Recommend focus
        tier_1_count = len(tiers['tier_1_must_apply'])
        tier_2_count = len(tiers['tier_2_should_apply'])

        print(f"\n💡 RECOMMENDATION:")
        if tier_1_count <= 50:
            print(f"   Focus on ALL {tier_1_count} Tier 1 jobs")
            remaining = 50 - tier_1_count
            print(f"   + Top {remaining} Tier 2 jobs")
            print(f"   = {min(50, tier_1_count + tier_2_count)} total applications")
        else:
            print(f"   Focus on TOP {limit} Tier 1 jobs only")

        print("\n" + "="*80 + "\n")

        # Show Tier 1 jobs
        print("🔥 TIER 1 - MUST APPLY (Top Priority)")
        print("-" * 80)
        for i, job in enumerate(tiers['tier_1_must_apply'][:30], 1):
            print(f"{i:2d}. [{job['priority_score']:3d} pts] {job['title']}")
            print(f"    {job['company']} | {job['location']} | {job['source']}")
            print(f"    {job['url'][:80]}...")
            print()

        if len(tiers['tier_1_must_apply']) > 30:
            print(f"    ... and {len(tiers['tier_1_must_apply']) - 30} more Tier 1 jobs\n")

        # Save prioritized list
        output = {
            'tier_1_must_apply': tiers['tier_1_must_apply'],
            'tier_2_should_apply': tiers['tier_2_should_apply'][:50],
            'summary': {
                'total_jobs': len(self.jobs),
                'tier_1_count': len(tiers['tier_1_must_apply']),
                'tier_2_count': len(tiers['tier_2_should_apply']),
                'recommended_focus': min(50, tier_1_count + tier_2_count)
            }
        }

        with open('/Users/ABRAHAM/job_application_system/prioritized_jobs.json', 'w') as f:
            json.dump(output, f, indent=2)

        print(f"✅ Prioritized list saved to: prioritized_jobs.json")
        print(f"\n🎯 Focus on: {output['summary']['recommended_focus']} applications")
        print("   This is manageable and high-quality!")
        print("="*80 + "\n")

        return output

    def create_filtered_applications(self, tier='tier_1'):
        """Create application materials only for high-priority jobs"""
        from resume_tailor import ResumeTailor
        from cover_letter_generator import CoverLetterGenerator
        import os
        import glob

        tiers = self.categorize_jobs()
        jobs_to_apply = tiers[f'{tier}_must_apply'] if tier == 'tier_1' else tiers['tier_1_must_apply'] + tiers['tier_2_should_apply'][:20]

        print(f"\n🎯 Creating applications for {len(jobs_to_apply)} prioritized jobs...")

        tailor = ResumeTailor()
        cover_gen = CoverLetterGenerator()

        output_dir = f'/Users/ABRAHAM/job_application_system/applications_priority'
        os.makedirs(output_dir, exist_ok=True)

        for i, job in enumerate(jobs_to_apply, 1):
            print(f"\n[{i}/{len(jobs_to_apply)}] {job['title']} at {job['company']} (Score: {job['priority_score']})")

            # Create folder
            company_folder = os.path.join(output_dir, f"{i:03d}_{job['company'].replace('/', '_')}")
            os.makedirs(company_folder, exist_ok=True)

            # Create job description
            job_desc = self._create_job_description(job)

            try:
                # Tailor resume
                tailored_resume = tailor.generate_tailored_resume(
                    job_description=job_desc,
                    job_title=job['title'],
                    company_name=job['company'],
                    output_format='text'
                )

                # Move files
                latest_resume = max(glob.glob('/Users/ABRAHAM/job_application_system/tailored_resume_*.txt'),
                                   key=os.path.getctime)
                os.rename(latest_resume, os.path.join(company_folder, 'resume.txt'))

                latest_resume_json = max(glob.glob('/Users/ABRAHAM/job_application_system/tailored_resume_*.json'),
                                        key=os.path.getctime)
                os.rename(latest_resume_json, os.path.join(company_folder, 'resume.json'))

                # Generate cover letter
                cover_letter = cover_gen.generate_cover_letter(
                    job_description=job_desc,
                    job_title=job['title'],
                    company_name=job['company']
                )

                latest_cover = max(glob.glob('/Users/ABRAHAM/job_application_system/cover_letter_*.txt'),
                                  key=os.path.getctime)
                os.rename(latest_cover, os.path.join(company_folder, 'cover_letter.txt'))

                # Save info
                app_info = {
                    'priority_score': job['priority_score'],
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

                print(f"  ✅ Complete!")

            except Exception as e:
                print(f"  ❌ Error: {e}")

        print(f"\n✅ Created {len(jobs_to_apply)} priority applications!")

    def _create_job_description(self, job):
        """Create job description based on title"""
        title = job['title'].lower()

        if 'data scientist' in title or 'data science' in title:
            return f"{job['title']} at {job['company']}. Seeking candidate with Python, ML, data analysis skills."
        elif 'data analyst' in title:
            return f"{job['title']} at {job['company']}. Seeking candidate with SQL, Tableau, Excel, data visualization."
        elif 'java' in title or 'software' in title:
            return f"{job['title']} at {job['company']}. Seeking candidate with Java, Spring Boot, backend development."
        else:
            return f"{job['title']} at {job['company']}. Technical role requiring programming and analytical skills."


def main():
    prioritizer = JobPrioritizer()
    recommendations = prioritizer.get_top_recommendations(limit=50)

    print("\n💡 NEXT STEPS:")
    print("1. Focus on Tier 1 jobs (highest quality matches)")
    print("2. Apply to 5-10 jobs per day for better quality")
    print("3. Customize cover letters for top companies")
    print("4. Track applications in the web interface")
    print("\n⚡ Quality > Quantity!")


if __name__ == "__main__":
    main()
