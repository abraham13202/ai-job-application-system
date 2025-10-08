"""
Job Application System - Web Interface
Flask web application for managing job applications
"""

from flask import Flask, render_template, jsonify, request, send_file
import json
import os
import threading
import time
from application_tracker import ApplicationTracker
from resume_tailor import ResumeTailor
from cover_letter_generator import CoverLetterGenerator
from job_scraper import JobScraper

# Base directory - use current working directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Global variable to track search status
search_status = {
    'running': False,
    'progress': 0,
    'message': '',
    'total_jobs': 0
}

app = Flask(__name__)

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/dashboard')
def get_dashboard():
    """Get dashboard statistics"""
    tracker = ApplicationTracker()
    stats = tracker.get_statistics()
    return jsonify(stats)

@app.route('/api/applications')
def get_applications():
    """Get all applications"""
    tracker = ApplicationTracker()

    # Load application info from both batch folders
    batch_dirs = [
        os.path.join(BASE_DIR, 'applications_batch'),
        os.path.join(BASE_DIR, 'applications_comprehensive')
    ]
    applications = []

    for batch_dir in batch_dirs:
        if os.path.exists(batch_dir):
            for company_folder in os.listdir(batch_dir):
                folder_path = os.path.join(batch_dir, company_folder)
                if os.path.isdir(folder_path):
                    info_file = os.path.join(folder_path, 'application_info.json')
                    if os.path.exists(info_file):
                        with open(info_file, 'r') as f:
                            app_info = json.load(f)
                            app_info['folder'] = os.path.join(os.path.basename(batch_dir), company_folder)

                            # Add priority score if not present
                            if 'priority_score' not in app_info:
                                app_info['priority_score'] = calculate_priority_score(app_info)

                            applications.append(app_info)

    # Sort by priority score (highest first)
    applications.sort(key=lambda x: x.get('priority_score', 0), reverse=True)

    return jsonify(applications)

def calculate_priority_score(job):
    """Calculate priority score for a job"""
    score = 0
    title = job.get('job_title', '').lower()
    company = job.get('company', '').lower()

    # HIGH PRIORITY KEYWORDS
    if any(keyword in title for keyword in ['intern', 'internship', 'graduate', 'entry level', 'junior', 'undergraduate']):
        score += 20

    # TOP COMPANIES
    top_companies = ['google', 'microsoft', 'tiktok', 'meta', 'amazon', 'apple', 'atlassian', 'canva', 'ey', 'deloitte']
    if any(top_company in company for top_company in top_companies):
        score += 50

    # RELEVANT ROLES
    if any(role in title for role in ['data scientist', 'data analyst', 'machine learning', 'ml engineer', 'java developer']):
        score += 15

    # PENALTY: Senior roles
    if any(word in title for word in ['senior', 'lead', 'principal', 'staff']):
        score -= 30

    return max(0, score)

@app.route('/api/application/<path:company_folder>')
def get_application_details(company_folder):
    """Get details for a specific application"""
    folder_path = os.path.join(BASE_DIR, company_folder)

    if not os.path.exists(folder_path):
        return jsonify({'error': 'Application not found'}), 404

    # Load application info
    info_file = os.path.join(folder_path, 'application_info.json')
    with open(info_file, 'r') as f:
        app_info = json.load(f)

    # Load resume
    resume_files = [f for f in os.listdir(folder_path) if f.startswith('resume_') and f.endswith('.txt')]
    resume_content = ''
    if resume_files:
        with open(os.path.join(folder_path, resume_files[0]), 'r') as f:
            resume_content = f.read()

    # Load cover letter
    cover_files = [f for f in os.listdir(folder_path) if f.startswith('cover_letter_') and f.endswith('.txt')]
    cover_content = ''
    if cover_files:
        with open(os.path.join(folder_path, cover_files[0]), 'r') as f:
            cover_content = f.read()

    return jsonify({
        'info': app_info,
        'resume': resume_content,
        'cover_letter': cover_content
    })

@app.route('/api/download/<path:company_folder>/<file_type>')
def download_file(company_folder, file_type):
    """Download resume or cover letter"""
    folder_path = os.path.join(BASE_DIR, company_folder)

    if file_type == 'resume':
        files = [f for f in os.listdir(folder_path) if f.startswith('resume_') and f.endswith('.txt')]
    elif file_type == 'cover_letter':
        files = [f for f in os.listdir(folder_path) if f.startswith('cover_letter_') and f.endswith('.txt')]
    else:
        return jsonify({'error': 'Invalid file type'}), 400

    if files:
        return send_file(os.path.join(folder_path, files[0]), as_attachment=True)

    return jsonify({'error': 'File not found'}), 404

@app.route('/api/jobs')
def get_jobs():
    """Get scraped jobs"""
    jobs_file = os.path.join(BASE_DIR, 'jobs.json')
    if os.path.exists(jobs_file):
        with open(jobs_file, 'r') as f:
            jobs = json.load(f)
        return jsonify(jobs)
    return jsonify([])

@app.route('/api/update_status', methods=['POST'])
def update_status():
    """Update application status"""
    data = request.json
    tracker = ApplicationTracker()

    # Find application by company name
    for app in tracker.applications:
        if app['company'] == data.get('company'):
            tracker.update_status(app['id'], data.get('status'), data.get('notes', ''))
            return jsonify({'success': True})

    return jsonify({'error': 'Application not found'}), 404

@app.route('/api/mark_applied', methods=['POST'])
def mark_applied():
    """Mark an application as applied when link is clicked"""
    data = request.json
    company = data.get('company')
    job_title = data.get('job_title')

    # Update the application_info.json file
    batch_dirs = [
        os.path.join(BASE_DIR, 'applications_batch'),
        os.path.join(BASE_DIR, 'applications_comprehensive')
    ]

    for batch_dir in batch_dirs:
        if os.path.exists(batch_dir):
            for company_folder in os.listdir(batch_dir):
                folder_path = os.path.join(batch_dir, company_folder)
                if os.path.isdir(folder_path):
                    info_file = os.path.join(folder_path, 'application_info.json')
                    if os.path.exists(info_file):
                        with open(info_file, 'r') as f:
                            app_info = json.load(f)

                        if app_info.get('company') == company and app_info.get('job_title') == job_title:
                            # Mark as applied
                            app_info['status'] = 'Applied'
                            app_info['applied_date'] = request.json.get('timestamp')

                            with open(info_file, 'w') as f:
                                json.dump(app_info, f, indent=2)

                            return jsonify({'success': True})

    return jsonify({'success': False, 'error': 'Application not found'}), 404

@app.route('/api/search_jobs', methods=['POST'])
def search_jobs():
    """Trigger new job search"""
    global search_status

    if search_status['running']:
        return jsonify({'error': 'Search already in progress'}), 400

    data = request.json
    keywords = data.get('keywords', [])
    location = data.get('location', 'Sydney')
    country = data.get('country', 'australia')
    platforms = data.get('platforms', ['seek', 'indeed', 'linkedin'])
    clear_old = data.get('clear_old', False)

    if not keywords:
        return jsonify({'error': 'Please provide at least one keyword'}), 400

    # Start search in background thread
    thread = threading.Thread(target=run_job_search, args=(keywords, location, country, platforms, clear_old))
    thread.daemon = True
    thread.start()

    return jsonify({'success': True, 'message': 'Job search started'})

@app.route('/api/search_status')
def get_search_status():
    """Get current search status"""
    return jsonify(search_status)

@app.route('/api/clear_jobs', methods=['POST'])
def clear_jobs():
    """Clear all saved jobs"""
    try:
        import shutil

        # Clear both application folders
        folders_to_clear = [
            os.path.join(BASE_DIR, 'applications_batch'),
            os.path.join(BASE_DIR, 'applications_comprehensive')
        ]

        for folder in folders_to_clear:
            if os.path.exists(folder):
                shutil.rmtree(folder)
                os.makedirs(folder, exist_ok=True)

        return jsonify({'success': True, 'message': 'All jobs cleared'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def run_job_search(keywords, location, country, platforms, clear_old):
    """Run job search in background"""
    global search_status

    try:
        search_status['running'] = True
        search_status['progress'] = 0
        search_status['message'] = 'Initializing search...'
        search_status['total_jobs'] = 0

        # Clear old jobs if requested
        if clear_old:
            search_status['message'] = 'Clearing old jobs...'
            import shutil
            comp_dir = os.path.join(BASE_DIR, 'applications_comprehensive')
            if os.path.exists(comp_dir):
                for item in os.listdir(comp_dir):
                    item_path = os.path.join(comp_dir, item)
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)

        # Initialize scraper
        scraper = JobScraper()
        tailor = ResumeTailor()
        cover_gen = CoverLetterGenerator()
        tracker = ApplicationTracker()

        # Supported platforms
        supported_platforms = {'seek', 'indeed', 'linkedin', 'naukri', 'monster', 'glassdoor', 'reed', 'totaljobs'}
        unsupported = [p for p in platforms if p not in supported_platforms]

        # Filter to only supported platforms
        supported = [p for p in platforms if p in supported_platforms]

        total_searches = len(keywords) * len(supported)
        current_search = 0

        # Show message about unsupported platforms
        if unsupported:
            search_status['message'] = f'Note: {", ".join(unsupported)} scrapers coming soon! Searching with: {", ".join(supported)}'
            time.sleep(2)

        # Search each keyword on each platform
        for keyword in keywords:
            for platform in supported:
                current_search += 1
                search_status['progress'] = int((current_search / total_searches) * 50)  # 50% for searching
                search_status['message'] = f'Searching {platform.title()} for "{keyword}"...'

                try:
                    if platform == 'seek':
                        # Seek is Australia-only
                        if country == 'australia':
                            scraper.scrape_seek(keyword, location)
                    elif platform == 'indeed':
                        # Pass country to Indeed scraper
                        scraper.scrape_indeed(keyword, location, country)
                    elif platform == 'linkedin':
                        # Pass country to LinkedIn scraper
                        scraper.scrape_linkedin(keyword, location, country)
                    elif platform == 'naukri':
                        # Naukri is India-focused
                        scraper.scrape_naukri(keyword, location, country)
                    elif platform == 'monster':
                        # Monster for USA and other countries
                        scraper.scrape_monster(keyword, location, country)
                    elif platform == 'glassdoor':
                        # Glassdoor for USA
                        scraper.scrape_glassdoor(keyword, location, country)
                    elif platform == 'reed':
                        # Reed for UK
                        scraper.scrape_reed(keyword, location, country)
                    elif platform == 'totaljobs':
                        # TotalJobs for UK
                        scraper.scrape_totaljobs(keyword, location, country)
                    time.sleep(2)  # Be respectful with requests
                except Exception as e:
                    print(f"Error scraping {platform}: {e}")

        # Get unique jobs
        jobs = scraper.get_jobs()
        unique_jobs = []
        seen_urls = set()
        for job in jobs:
            if job['url'] not in seen_urls:
                unique_jobs.append(job)
                seen_urls.add(job['url'])

        search_status['total_jobs'] = len(unique_jobs)
        search_status['message'] = f'Found {len(unique_jobs)} jobs! Preparing applications...'

        # Save jobs
        scraper.jobs = unique_jobs
        scraper.save_to_json(os.path.join(BASE_DIR, 'jobs_comprehensive.json'))
        scraper.save_to_csv(os.path.join(BASE_DIR, 'jobs_comprehensive.csv'))

        # Prepare applications
        output_dir = os.path.join(BASE_DIR, 'applications_comprehensive')
        os.makedirs(output_dir, exist_ok=True)

        for i, job in enumerate(unique_jobs):
            search_status['progress'] = 50 + int(((i + 1) / len(unique_jobs)) * 50)  # 50-100% for processing
            search_status['message'] = f'Processing {i+1}/{len(unique_jobs)}: {job["title"]} at {job["company"]}'

            try:
                # Create company folder
                company_folder = os.path.join(output_dir, f"{job['company'].replace('/', '_').replace('|', '_')}_{i+1}")
                os.makedirs(company_folder, exist_ok=True)

                # Create job description
                job_desc = create_job_description(job)

                # Tailor resume
                tailored_resume = tailor.generate_tailored_resume(
                    job_description=job_desc,
                    job_title=job['title'],
                    company_name=job['company'],
                    output_format='text'
                )

                # Move files
                import glob
                latest_resume = max(glob.glob(os.path.join(BASE_DIR, 'tailored_resume_*.txt')),
                                   key=os.path.getctime, default=None)
                if latest_resume:
                    os.rename(latest_resume, os.path.join(company_folder, f"resume_{job['company'].replace('/', '_')}.txt"))

                latest_resume_json = max(glob.glob(os.path.join(BASE_DIR, 'tailored_resume_*.json')),
                                        key=os.path.getctime, default=None)
                if latest_resume_json:
                    os.rename(latest_resume_json, os.path.join(company_folder, f"resume_{job['company'].replace('/', '_')}.json"))

                # Generate cover letter
                cover_letter = cover_gen.generate_cover_letter(
                    job_description=job_desc,
                    job_title=job['title'],
                    company_name=job['company']
                )

                latest_cover = max(glob.glob(os.path.join(BASE_DIR, 'cover_letter_*.txt')),
                                  key=os.path.getctime, default=None)
                if latest_cover:
                    os.rename(latest_cover, os.path.join(company_folder, f"cover_letter_{job['company'].replace('/', '_')}.txt"))

                # Save application info
                app_info = {
                    'job_title': job['title'],
                    'company': job['company'],
                    'location': job['location'],
                    'url': job['url'],
                    'source': job['source'],
                    'skill_match': f"{tailored_resume['skill_match_analysis']['match_percentage']:.1f}%",
                    'matched_skills': tailored_resume['skill_match_analysis']['matched'],
                    'status': 'Ready to Apply',
                    'priority_score': calculate_priority_score({'job_title': job['title'], 'company': job['company']})
                }

                with open(os.path.join(company_folder, 'application_info.json'), 'w') as f:
                    json.dump(app_info, f, indent=2)

            except Exception as e:
                print(f"Error processing {job['title']}: {e}")

        search_status['progress'] = 100
        search_status['message'] = f'Complete! Found and processed {len(unique_jobs)} jobs.'
        time.sleep(3)  # Keep message visible

    except Exception as e:
        search_status['message'] = f'Error: {str(e)}'
        print(f"Search error: {e}")
    finally:
        search_status['running'] = False

def create_job_description(job):
    """Create a generic job description based on title"""
    title_lower = job['title'].lower()

    if 'data scientist' in title_lower or 'data science' in title_lower:
        return f"{job['title']} at {job['company']} - Data Science role requiring Python, ML, SQL skills"
    elif 'data analyst' in title_lower:
        return f"{job['title']} at {job['company']} - Data Analytics role requiring SQL, Python, Tableau"
    elif 'java' in title_lower or 'software' in title_lower:
        return f"{job['title']} at {job['company']} - Software Development role requiring Java, SQL, APIs"
    elif 'machine learning' in title_lower or 'ml' in title_lower:
        return f"{job['title']} at {job['company']} - ML/AI role requiring Python, TensorFlow, PyTorch"
    else:
        return f"{job['title']} at {job['company']} - Technical role requiring programming and problem-solving skills"

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)

    print("\n" + "="*80)
    print("🌐 JOB APPLICATION WEB INTERFACE")
    print("="*80)
    print("\n📍 Open your browser and go to:")
    print("   http://localhost:5000")
    print("\n⚠️  Press Ctrl+C to stop the server")
    print("="*80 + "\n")

    app.run(debug=True, port=5000)
