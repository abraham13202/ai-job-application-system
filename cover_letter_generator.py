"""
Automated Cover Letter Generator
Creates tailored cover letters based on job description and your experience
"""

import json
from datetime import datetime
import re

class CoverLetterGenerator:
    def __init__(self, resume_data_path='/Users/ABRAHAM/job_application_system/resume_data.json'):
        """Initialize with resume data"""
        with open(resume_data_path, 'r') as f:
            self.data = json.load(f)

    def extract_key_requirements(self, job_description):
        """Extract key requirements from job description"""
        # Common requirement indicators
        requirement_patterns = [
            r'(?:require|requirement|must have|essential)[s]?:?\s*(.+)',
            r'(?:experience with|proficiency in|knowledge of)\s+(.+)',
            r'(?:strong|excellent|solid)\s+(?:understanding|knowledge|experience)\s+(?:of|in|with)\s+(.+)'
        ]

        requirements = []
        for pattern in requirement_patterns:
            matches = re.findall(pattern, job_description.lower(), re.MULTILINE)
            requirements.extend(matches)

        return requirements[:5]  # Top 5 requirements

    def match_experience_to_requirements(self, job_description):
        """Find relevant experience matching job requirements"""
        job_lower = job_description.lower()

        matched_experiences = []

        # Check work experience
        for exp in self.data['experience']:
            exp_text = ' '.join(exp['achievements']).lower()
            relevance_score = sum(1 for word in ['ml', 'machine learning', 'data', 'python', 'model', 'dashboard']
                                 if word in exp_text and word in job_lower)

            if relevance_score > 0:
                matched_experiences.append({
                    'type': 'work',
                    'title': exp['title'],
                    'company': exp['company'],
                    'achievement': exp['achievements'][0],  # Best achievement
                    'score': relevance_score
                })

        # Check projects
        for proj in self.data['projects']:
            proj_text = (proj['description'] + ' ' + ' '.join(proj.get('achievements', []))).lower()
            relevance_score = sum(1 for word in ['ml', 'machine learning', 'data', 'python', 'model', 'accuracy']
                                 if word in proj_text and word in job_lower)

            if relevance_score > 0:
                matched_experiences.append({
                    'type': 'project',
                    'name': proj['name'],
                    'achievement': proj.get('achievements', [proj['description']])[0],
                    'score': relevance_score
                })

        # Sort by relevance
        matched_experiences.sort(key=lambda x: x['score'], reverse=True)

        return matched_experiences[:3]  # Top 3 most relevant

    def generate_opening_paragraph(self, job_title, company_name):
        """Generate opening paragraph"""
        templates = [
            f"I am writing to express my strong interest in the {job_title} position at {company_name}. As a dynamic Computer Science graduate specializing in AI and Data Science, currently pursuing my Master's at the University of Sydney, I am excited about the opportunity to contribute to your data-driven initiatives.",

            f"With great enthusiasm, I am applying for the {job_title} role at {company_name}. My background in machine learning, data science, and hands-on experience developing AI solutions aligns perfectly with the requirements of this position.",

            f"I am excited to apply for the {job_title} position at {company_name}. Having successfully delivered machine learning solutions that improved efficiency by up to 40% in my previous role, I am confident in my ability to drive similar impactful results for your team."
        ]

        return templates[0]  # Use first template

    def generate_body_paragraphs(self, matched_experiences, job_title):
        """Generate body paragraphs highlighting relevant experience"""
        paragraphs = []

        # Paragraph about work experience
        work_exp = [exp for exp in matched_experiences if exp['type'] == 'work']
        if work_exp:
            exp = work_exp[0]
            paragraph = f"In my role as {exp['title']} at {exp['company']}, I {exp['achievement'].lower()} This experience has equipped me with practical skills in machine learning, data analysis, and delivering measurable business impact - capabilities that directly align with the {job_title} position."
            paragraphs.append(paragraph)

        # Paragraph about technical projects
        project_exp = [exp for exp in matched_experiences if exp['type'] == 'project']
        if project_exp:
            proj = project_exp[0]
            if len(project_exp) > 1:
                paragraph = f"My technical expertise is further demonstrated through projects such as {proj['name']}, where I {proj['achievement'].lower()} These projects showcase my ability to apply cutting-edge machine learning techniques to solve real-world problems."
            else:
                paragraph = f"I have also developed strong technical skills through my project work. For instance, in my {proj['name']} project, I {proj['achievement'].lower()} This demonstrates my capability to build and deploy effective ML solutions."
            paragraphs.append(paragraph)

        # Paragraph about skills and tools
        skills_paragraph = f"I bring proficiency in key technologies including Python, TensorFlow, PyTorch, and scikit-learn, along with strong data visualization skills using Tableau and Power BI. My AWS certification and experience with cloud platforms enable me to deploy scalable ML solutions in production environments."
        paragraphs.append(skills_paragraph)

        return paragraphs

    def generate_closing_paragraph(self, company_name):
        """Generate closing paragraph"""
        templates = [
            f"I am particularly drawn to {company_name} because of your commitment to innovation and data-driven decision making. I am eager to contribute my technical skills, analytical mindset, and collaborative approach to your team. I would welcome the opportunity to discuss how my background and enthusiasm can benefit your organization.",

            f"I am excited about the prospect of bringing my machine learning expertise and passion for data science to {company_name}. I am confident that my combination of technical skills and proven track record of delivering results would make me a valuable addition to your team. I look forward to the opportunity to discuss my application further.",

            f"Thank you for considering my application. I am enthusiastic about the opportunity to contribute to {company_name}'s success and would welcome the chance to discuss how my skills and experience align with your needs. I look forward to hearing from you."
        ]

        return templates[0]

    def generate_cover_letter(self, job_description, job_title, company_name, hiring_manager="Hiring Manager"):
        """Generate complete cover letter"""

        # Extract matched experiences
        matched_exp = self.match_experience_to_requirements(job_description)

        # Build cover letter
        personal = self.data['personal_info']

        # Header
        header = f"{personal['name']}\n"
        header += f"{personal['location']}\n"
        header += f"{personal['email']} | {personal['phone']}\n"
        header += f"LinkedIn: linkedin.com/in/{personal['linkedin']}\n\n"

        # Date and recipient
        today = datetime.now().strftime("%B %d, %Y")
        recipient = f"{today}\n\n"
        recipient += f"Dear {hiring_manager},\n\n"

        # Opening
        opening = self.generate_opening_paragraph(job_title, company_name) + "\n\n"

        # Body
        body_paragraphs = self.generate_body_paragraphs(matched_exp, job_title)
        body = "\n\n".join(body_paragraphs) + "\n\n"

        # Closing
        closing = self.generate_closing_paragraph(company_name) + "\n\n"
        closing += f"Sincerely,\n{personal['name']}"

        # Combine all parts
        cover_letter = header + recipient + opening + body + closing

        # Save to file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        # Clean company name for filename
        clean_company = company_name.replace(' ', '_').replace('/', '_').replace('|', '_')
        filename = f"/Users/ABRAHAM/job_application_system/cover_letter_{clean_company}_{timestamp}.txt"

        with open(filename, 'w') as f:
            f.write(cover_letter)

        print(f"\n✅ Cover letter generated: {filename}")

        return cover_letter

    def generate_multiple_versions(self, job_description, job_title, company_name):
        """Generate multiple cover letter versions"""
        versions = []

        # Version 1: Technical focus
        cl1 = self.generate_cover_letter(job_description, job_title, company_name)
        versions.append(('technical', cl1))

        # Version 2: Results focus (modify opening)
        # Version 3: Innovation focus

        return versions


def main():
    """Demo usage"""
    generator = CoverLetterGenerator()

    # Example job details
    job_description = """
    We are seeking a Data Scientist to join our team.

    Requirements:
    - Strong Python programming and ML experience
    - Experience with TensorFlow, PyTorch
    - Proven track record of deploying ML models
    - Data visualization skills (Tableau/Power BI)
    - Strong communication skills

    You will:
    - Build and deploy ML models
    - Analyze complex datasets
    - Create dashboards for stakeholders
    - Collaborate with cross-functional teams
    """

    job_title = "Data Scientist"
    company_name = "Tech Innovations Inc"

    print("✍️  Generating cover letter...\n")

    cover_letter = generator.generate_cover_letter(
        job_description=job_description,
        job_title=job_title,
        company_name=company_name,
        hiring_manager="Hiring Manager"
    )

    print("\n📄 Cover Letter Preview:")
    print("=" * 80)
    print(cover_letter[:500] + "...")
    print("=" * 80)


if __name__ == "__main__":
    main()
