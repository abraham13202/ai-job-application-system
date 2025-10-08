"""
Application Tracking Dashboard
Track and manage all your job applications with analytics
"""

import json
import pandas as pd
from datetime import datetime
import os

class ApplicationTracker:
    def __init__(self, db_path='/Users/ABRAHAM/job_application_system/applications.json'):
        """Initialize tracker with database"""
        self.db_path = db_path

        # Load existing applications or create new
        if os.path.exists(db_path):
            with open(db_path, 'r') as f:
                self.applications = json.load(f)
        else:
            self.applications = []

    def add_application(self, job_title, company, job_url, location="Sydney, Australia",
                       status="Applied", date_applied=None, notes=""):
        """Add new job application"""

        if date_applied is None:
            date_applied = datetime.now().strftime('%Y-%m-%d')

        application = {
            'id': len(self.applications) + 1,
            'job_title': job_title,
            'company': company,
            'location': location,
            'job_url': job_url,
            'status': status,
            'date_applied': date_applied,
            'date_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'notes': notes,
            'follow_up_date': None,
            'resume_version': None,
            'cover_letter_version': None
        }

        self.applications.append(application)
        self.save()

        print(f"✅ Added application: {job_title} at {company}")
        return application['id']

    def update_status(self, app_id, new_status, notes=""):
        """Update application status"""
        for app in self.applications:
            if app['id'] == app_id:
                app['status'] = new_status
                app['date_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if notes:
                    app['notes'] += f"\n{datetime.now().strftime('%Y-%m-%d')}: {notes}"
                self.save()
                print(f"✅ Updated #{app_id} to: {new_status}")
                return True

        print(f"❌ Application #{app_id} not found")
        return False

    def add_follow_up(self, app_id, follow_up_date, notes=""):
        """Add follow-up reminder"""
        for app in self.applications:
            if app['id'] == app_id:
                app['follow_up_date'] = follow_up_date
                if notes:
                    app['notes'] += f"\nFollow-up scheduled for {follow_up_date}: {notes}"
                self.save()
                print(f"✅ Follow-up added for #{app_id} on {follow_up_date}")
                return True

        return False

    def get_applications_by_status(self, status):
        """Get all applications with specific status"""
        return [app for app in self.applications if app['status'] == status]

    def get_pending_followups(self):
        """Get applications needing follow-up"""
        today = datetime.now().strftime('%Y-%m-%d')
        pending = [app for app in self.applications
                  if app['follow_up_date'] and app['follow_up_date'] <= today]
        return pending

    def get_statistics(self):
        """Get application statistics"""
        if not self.applications:
            return {
                'total': 0,
                'by_status': {},
                'by_company': {},
                'response_rate': 0
            }

        df = pd.DataFrame(self.applications)

        stats = {
            'total': len(self.applications),
            'by_status': df['status'].value_counts().to_dict(),
            'by_company': df['company'].value_counts().to_dict(),
            'recent_applications': len(df[df['date_applied'] >=
                (datetime.now() - pd.Timedelta(days=7)).strftime('%Y-%m-%d')]),
        }

        # Calculate response rate
        responded = len(df[df['status'].isin(['Interview Scheduled', 'Offer', 'Rejected'])])
        stats['response_rate'] = (responded / len(df) * 100) if len(df) > 0 else 0

        return stats

    def search_applications(self, keyword):
        """Search applications by keyword"""
        keyword_lower = keyword.lower()
        results = [
            app for app in self.applications
            if keyword_lower in app['job_title'].lower() or
               keyword_lower in app['company'].lower() or
               keyword_lower in app.get('notes', '').lower()
        ]
        return results

    def export_to_csv(self, filename='/Users/ABRAHAM/job_application_system/applications.csv'):
        """Export applications to CSV"""
        if self.applications:
            df = pd.DataFrame(self.applications)
            df.to_csv(filename, index=False)
            print(f"✅ Exported to {filename}")
        else:
            print("⚠️  No applications to export")

    def save(self):
        """Save applications to JSON"""
        with open(self.db_path, 'w') as f:
            json.dump(self.applications, f, indent=2)

    def display_dashboard(self):
        """Display application dashboard"""
        stats = self.get_statistics()

        print("\n" + "="*80)
        print("📊 JOB APPLICATION DASHBOARD")
        print("="*80)

        print(f"\n📈 STATISTICS")
        print(f"   Total Applications: {stats['total']}")
        print(f"   Recent (Last 7 days): {stats.get('recent_applications', 0)}")
        print(f"   Response Rate: {stats['response_rate']:.1f}%")

        print(f"\n📋 BY STATUS")
        for status, count in stats['by_status'].items():
            print(f"   {status}: {count}")

        print(f"\n🏢 TOP COMPANIES")
        for company, count in list(stats['by_company'].items())[:5]:
            print(f"   {company}: {count}")

        # Show pending follow-ups
        pending = self.get_pending_followups()
        if pending:
            print(f"\n⏰ PENDING FOLLOW-UPS ({len(pending)})")
            for app in pending:
                print(f"   #{app['id']}: {app['job_title']} at {app['company']} - {app['follow_up_date']}")

        # Show recent applications
        recent = sorted(self.applications, key=lambda x: x['date_applied'], reverse=True)[:5]
        print(f"\n📅 RECENT APPLICATIONS")
        for app in recent:
            status_emoji = {
                'Applied': '📤',
                'Interview Scheduled': '📞',
                'Rejected': '❌',
                'Offer': '🎉',
                'Withdrawn': '⏸️'
            }.get(app['status'], '📋')
            print(f"   {status_emoji} {app['job_title']} at {app['company']} - {app['status']} ({app['date_applied']})")

        print("\n" + "="*80 + "\n")

    def list_all(self):
        """List all applications"""
        if not self.applications:
            print("No applications yet.")
            return

        print("\n📋 ALL APPLICATIONS\n")
        for app in self.applications:
            print(f"#{app['id']}: {app['job_title']} at {app['company']}")
            print(f"   Status: {app['status']} | Applied: {app['date_applied']}")
            print(f"   URL: {app['job_url']}")
            if app['notes']:
                print(f"   Notes: {app['notes'][:100]}...")
            print()


def main():
    """Demo usage"""
    tracker = ApplicationTracker()

    # Example: Add some applications
    if len(tracker.applications) == 0:
        print("Adding sample applications...\n")

        tracker.add_application(
            job_title="Senior Data Scientist",
            company="Google",
            job_url="https://careers.google.com/jobs/123",
            location="Sydney, Australia",
            notes="Great company culture, ML focus"
        )

        tracker.add_application(
            job_title="Machine Learning Engineer",
            company="Atlassian",
            job_url="https://atlassian.com/careers/456",
            location="Sydney, Australia",
            notes="Referred by John"
        )

        tracker.add_application(
            job_title="Data Scientist",
            company="Canva",
            job_url="https://canva.com/careers/789",
            location="Sydney, Australia"
        )

    # Display dashboard
    tracker.display_dashboard()

    # Example operations
    print("\n💡 Available Operations:")
    print("   tracker.add_application(title, company, url)")
    print("   tracker.update_status(app_id, 'Interview Scheduled')")
    print("   tracker.add_follow_up(app_id, '2025-10-15')")
    print("   tracker.search_applications('data scientist')")
    print("   tracker.export_to_csv()")


if __name__ == "__main__":
    main()
