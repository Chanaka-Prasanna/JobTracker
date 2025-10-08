import json
import os
from datetime import datetime
from pathlib import Path

class SettingsManager:
    def __init__(self):
        self.settings_file = "settings.json"
        self.default_roles = [
            "Software Engineer",
            "Associate Software Engineer",
            "Software Engineer Intern",
            "ML Engineer",
            "AI Engineer",
            "Associate ML Engineer",
            "Associate AI Engineer",
            "Data Scientist",
            "ML Intern",
            "AI Intern",
            "Data Science Intern"
        ]
        self.settings = self.load_settings()
    
    def load_settings(self):
        """Load settings from file or create with default roles if not exists"""
        try:
            with open(self.settings_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Create settings with default roles
            settings = {
                "user_name": "",
                "job_roles": self.default_roles.copy()  # Use copy to avoid reference issues
            }
            # Save settings
            self.save_settings(settings)
            return settings
    
    def save_settings(self, settings=None):
        """Save settings to file"""
        if settings is not None:
            self.settings = settings
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f, indent=4)
    
    def update_user_name(self, name):
        """Update user name in settings"""
        self.settings['user_name'] = name
        self.save_settings()
    
    def get_user_name(self):
        """Get user name from settings"""
        return self.settings.get('user_name', '')
    
    def get_job_roles(self):
        """Get list of job roles"""
        return self.settings.get('job_roles', [])
    
    def update_job_roles(self, roles):
        """Update job roles list"""
        self.settings['job_roles'] = roles
        self.save_settings()
    
    def add_job_role(self, role):
        """Add a new job role"""
        if role not in self.settings['job_roles']:
            self.settings['job_roles'].append(role)
            self.save_settings()
    
    def remove_job_role(self, role):
        """Remove a job role"""
        if role in self.settings['job_roles']:
            self.settings['job_roles'].remove(role)
            self.save_settings()
    
    def is_first_run(self):
        """Check if this is the first run of the application"""
        return not os.path.exists(self.settings_file) or not self.get_user_name()

    def get_creation_date(self):
        """Get the date when settings were first created"""
        return datetime.fromisoformat(self.settings.get('created_date', datetime.now().isoformat()))
