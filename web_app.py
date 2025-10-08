"""
Job Application System - Web Interface
Flask web application for managing job applications
"""

from flask import Flask, render_template, jsonify, request, send_file
import json
import os
from application_tracker import ApplicationTracker
from resume_tailor import ResumeTailor
from cover_letter_generator import CoverLetterGenerator
from job_scraper import JobScraper

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
        '/Users/ABRAHAM/job_application_system/applications_batch',
        '/Users/ABRAHAM/job_application_system/applications_comprehensive'
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
    base_dir = '/Users/ABRAHAM/job_application_system'
    folder_path = os.path.join(base_dir, company_folder)

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
    base_dir = '/Users/ABRAHAM/job_application_system'
    folder_path = os.path.join(base_dir, company_folder)

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
    jobs_file = '/Users/ABRAHAM/job_application_system/jobs.json'
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
        '/Users/ABRAHAM/job_application_system/applications_batch',
        '/Users/ABRAHAM/job_application_system/applications_comprehensive'
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
