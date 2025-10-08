"""
Resume Tailoring System
Customizes resume based on job description using keyword matching and AI
"""

import json
import re
from collections import Counter
from datetime import datetime
import os

class ResumeTailor:
    def __init__(self, resume_data_path=None):
        """Initialize with resume data"""
        if resume_data_path is None:
            # Use path relative to this file
            base_dir = os.path.dirname(os.path.abspath(__file__))
            resume_data_path = os.path.join(base_dir, 'resume_data.json')
        """Initialize with resume data"""
        with open(resume_data_path, 'r') as f:
            self.data = json.load(f)

    def extract_keywords(self, text):
        """Extract keywords from job description"""
        # Convert to lowercase
        text = text.lower()

        # Common data science keywords
        tech_keywords = [
            'python', 'r', 'sql', 'java', 'c++', 'scala',
            'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'xgboost',
            'pandas', 'numpy', 'matplotlib', 'seaborn',
            'machine learning', 'deep learning', 'neural network',
            'nlp', 'computer vision', 'reinforcement learning',
            'data visualization', 'tableau', 'power bi',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes',
            'spark', 'hadoop', 'airflow',
            'statistics', 'a/b testing', 'hypothesis testing',
            'regression', 'classification', 'clustering',
            'time series', 'forecasting', 'recommendation system',
            'api', 'rest', 'microservices',
            'git', 'ci/cd', 'agile', 'scrum'
        ]

        found_keywords = []
        for keyword in tech_keywords:
            if keyword in text:
                found_keywords.append(keyword)

        return found_keywords

    def match_skills(self, job_description):
        """Match your skills with job requirements"""
        job_keywords = set(self.extract_keywords(job_description))

        # Get your skills
        your_skills = set()
        for category, skills in self.data['skills'].items():
            if isinstance(skills, list):
                your_skills.update([s.lower() for s in skills])

        # Also check techniques
        if 'techniques' in self.data['skills']:
            your_skills.update([t.lower() for t in self.data['skills']['techniques']])

        # Find matches
        matched_skills = job_keywords.intersection(your_skills)
        missing_skills = job_keywords - your_skills

        return {
            'matched': list(matched_skills),
            'missing': list(missing_skills),
            'match_percentage': (len(matched_skills) / len(job_keywords) * 100) if job_keywords else 0
        }

    def prioritize_experience(self, job_description):
        """Reorder experience based on relevance to job"""
        job_keywords = self.extract_keywords(job_description)

        experience_scores = []
        for exp in self.data['experience']:
            # Calculate relevance score
            exp_text = ' '.join(exp['achievements']).lower() + ' ' + exp['title'].lower()
            score = sum(1 for keyword in job_keywords if keyword in exp_text)

            experience_scores.append({
                'experience': exp,
                'score': score
            })

        # Sort by score (descending)
        experience_scores.sort(key=lambda x: x['score'], reverse=True)

        return [item['experience'] for item in experience_scores]

    def prioritize_projects(self, job_description):
        """Select and reorder projects based on relevance"""
        job_keywords = self.extract_keywords(job_description)

        project_scores = []
        for proj in self.data['projects']:
            # Calculate relevance score
            proj_text = (proj['description'] + ' ' + ' '.join(proj.get('achievements', []))).lower()
            proj_text += ' ' + ' '.join(proj.get('technologies', [])).lower()

            score = sum(1 for keyword in job_keywords if keyword in proj_text)

            project_scores.append({
                'project': proj,
                'score': score
            })

        # Sort by score (descending)
        project_scores.sort(key=lambda x: x['score'], reverse=True)

        # Return top 3-4 most relevant projects
        return [item['project'] for item in project_scores[:4]]

    def customize_summary(self, job_title, company_name=None):
        """Customize professional summary for specific role"""
        base_summary = self.data['summary']

        # Add job-specific intro if provided
        if company_name:
            custom_intro = f"Motivated Data Scientist seeking to contribute to {company_name}'s data-driven initiatives. "
        else:
            custom_intro = f"Results-driven {job_title} with proven expertise in machine learning and data analysis. "

        # Combine
        return custom_intro + base_summary

    def generate_tailored_resume(self, job_description, job_title, company_name=None, output_format='text'):
        """Generate a tailored resume"""

        # Analyze job description
        skill_match = self.match_skills(job_description)
        print(f"\n📊 Skill Match: {skill_match['match_percentage']:.1f}%")
        print(f"   ✅ Matched skills: {', '.join(skill_match['matched'][:10])}")
        if skill_match['missing']:
            print(f"   ⚠️  Missing skills: {', '.join(skill_match['missing'][:5])}")

        # Prioritize content
        prioritized_experience = self.prioritize_experience(job_description)
        prioritized_projects = self.prioritize_projects(job_description)

        # Create tailored resume data
        tailored = {
            'personal_info': self.data['personal_info'],
            'summary': self.customize_summary(job_title, company_name),
            'education': self.data['education'],
            'experience': prioritized_experience,
            'projects': prioritized_projects,
            'skills': self.data['skills'],
            'certifications': self.data['certifications'],
            'skill_match_analysis': skill_match
        }

        # Save tailored version
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(base_dir, f"tailored_resume_{timestamp}.json")

        with open(filename, 'w') as f:
            json.dump(tailored, f, indent=2)

        print(f"\n✅ Tailored resume saved: {filename}")

        # Generate text version
        if output_format == 'text':
            base_dir = os.path.dirname(os.path.abspath(__file__))
            text_filename = os.path.join(base_dir, f"tailored_resume_{timestamp}.txt")
            self._generate_text_resume(tailored, text_filename, job_title, company_name)

        return tailored

    def _generate_text_resume(self, tailored_data, filename, job_title, company_name):
        """Generate text version of tailored resume"""

        with open(filename, 'w') as f:
            # Header
            personal = tailored_data['personal_info']
            f.write(f"{personal['name']}\n")
            f.write(f"{personal['location']} | {personal['phone']} | {personal['email']}\n")
            f.write(f"LinkedIn: linkedin.com/in/{personal['linkedin']} | GitHub: github.com/{personal['github']}\n")
            f.write(f"Visa Status: {personal['visa_status']}\n")
            f.write("\n" + "="*80 + "\n\n")

            # Summary
            f.write("PROFESSIONAL SUMMARY\n")
            f.write("-" * 80 + "\n")
            f.write(f"{tailored_data['summary']}\n\n")

            # Skills (prioritized)
            f.write("TECHNICAL SKILLS\n")
            f.write("-" * 80 + "\n")
            for category, skills in tailored_data['skills'].items():
                if isinstance(skills, list):
                    category_name = category.replace('_', ' ').title()
                    f.write(f"{category_name}: {', '.join(skills)}\n")
            f.write("\n")

            # Experience
            f.write("PROFESSIONAL EXPERIENCE\n")
            f.write("-" * 80 + "\n")
            for exp in tailored_data['experience']:
                f.write(f"{exp['title']} | {exp['company']}\n")
                f.write(f"{exp['dates']} | {exp['location']}\n")
                for achievement in exp['achievements']:
                    f.write(f"  • {achievement}\n")
                f.write("\n")

            # Projects
            f.write("KEY PROJECTS\n")
            f.write("-" * 80 + "\n")
            for proj in tailored_data['projects']:
                f.write(f"{proj['name']}\n")
                if 'url' in proj:
                    f.write(f"{proj['url']}\n")
                f.write(f"{proj['description']}\n")
                if 'achievements' in proj:
                    for achievement in proj['achievements']:
                        f.write(f"  • {achievement}\n")
                f.write(f"Technologies: {', '.join(proj.get('technologies', []))}\n\n")

            # Education
            f.write("EDUCATION\n")
            f.write("-" * 80 + "\n")
            for edu in tailored_data['education']:
                f.write(f"{edu['degree']} | {edu['institution']}\n")
                f.write(f"{edu['dates']}\n\n")

            # Certifications
            f.write("CERTIFICATIONS\n")
            f.write("-" * 80 + "\n")
            for cert in tailored_data['certifications']:
                f.write(f"  • {cert}\n")

        print(f"✅ Text resume saved: {filename}")


def main():
    """Demo usage"""
    tailor = ResumeTailor()

    # Example job description
    job_description = """
    Data Scientist position at leading tech company.

    Requirements:
    - Strong Python programming skills
    - Experience with TensorFlow and PyTorch
    - Knowledge of NLP and Computer Vision
    - Proficiency in SQL and data visualization (Tableau/Power BI)
    - Experience with AWS cloud platform
    - Strong machine learning fundamentals
    - Experience building recommendation systems

    Responsibilities:
    - Develop ML models for production
    - Analyze large datasets
    - Create dashboards and reports
    - Collaborate with engineering teams
    """

    job_title = "Data Scientist"
    company_name = "Tech Corp"

    print("🎯 Tailoring resume for job...")
    tailored = tailor.generate_tailored_resume(job_description, job_title, company_name)

    print("\n✅ Resume tailoring complete!")


if __name__ == "__main__":
    main()
