import json
import os
from datetime import datetime
from pathlib import Path

class SettingsManager:
    def __init__(self, app_dir: str):
        # The folder where the executable (or script) resides
        self.app_dir = app_dir

        # Defaults
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

        # Paths: primary settings file lives next to the app; we also mirror to the chosen data directory
        self.app_settings_path = os.path.join(self.app_dir, 'settings.json')
        self.settings_path = self.app_settings_path
        self.settings = self.load_settings()

        # Determine data directory (default to app_dir if not set); also compute user-facing settings path
        self.data_directory = self.settings.get('data_directory') or self.app_dir
        self.user_settings_path = os.path.join(self.data_directory, 'settings.json')
        self.data_path = os.path.join(self.data_directory, 'job_data.json')
    
    def load_settings(self):
        """Load settings from settings.json next to the app, or create defaults."""
        try:
            with open(self.app_settings_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            settings = {
                "user_name": "",
                "job_roles": self.default_roles.copy(),
                # Store only the chosen data directory here if changed by user later
            }
            Path(self.app_dir).mkdir(parents=True, exist_ok=True)
            with open(self.app_settings_path, 'w') as f:
                json.dump(settings, f, indent=4)
            return settings
    
    def save_settings(self, settings=None):
        """Save settings to settings.json in app folder."""
        if settings is not None:
            self.settings = settings
        Path(self.app_dir).mkdir(parents=True, exist_ok=True)
        # Write to app folder settings (authoritative for remembering data_directory)
        with open(self.app_settings_path, 'w') as f:
            json.dump(self.settings, f, indent=4)
        # Also mirror to the user-selected directory (for user's visibility/backups)
        try:
            Path(self.data_directory).mkdir(parents=True, exist_ok=True)
            with open(self.user_settings_path, 'w') as f:
                json.dump(self.settings, f, indent=4)
        except Exception:
            # If mirroring fails (e.g., permissions), ignore and keep primary settings
            pass
    
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
        return not os.path.exists(self.settings_path) or not self.get_user_name()

    def get_creation_date(self):
        """Get the date when settings were first created"""
        return datetime.fromisoformat(self.settings.get('created_date', datetime.now().isoformat()))

    # -------------------- Storage paths management --------------------
    def get_settings_file_path(self) -> str:
        # Prefer returning the user-visible settings path
        return self.user_settings_path

    def get_data_file_path(self) -> str:
        return self.data_path

    def get_storage_directory(self) -> str:
        return self.data_directory

    def set_storage_directory(self, directory_path: str):
        """Change the storage directory for job_data.json only.
        The authoritative settings.json remains next to the app.
        The chosen directory is stored inside settings.json (field: data_directory).
        """
        directory_path = os.path.abspath(directory_path)
        Path(directory_path).mkdir(parents=True, exist_ok=True)

        old_data_path = self.data_path
        old_user_settings_path = getattr(self, 'user_settings_path', os.path.join(self.data_directory, 'settings.json'))

        self.data_directory = directory_path
        self.user_settings_path = os.path.join(self.data_directory, 'settings.json')
        self.data_path = os.path.join(self.data_directory, 'job_data.json')

        # Persist new directory in settings and write to both locations
        self.settings['data_directory'] = self.data_directory
        self.save_settings()

        # Migrate data: if old exists and new doesn't, copy contents
        try:
            if os.path.exists(old_data_path) and not os.path.exists(self.data_path):
                with open(old_data_path, 'r') as f:
                    data = f.read()
                with open(self.data_path, 'w') as f:
                    f.write(data)
        except Exception:
            pass

        # Ensure a settings.json exists in the chosen directory (already written by save_settings)
        # Note: No pointer file is created. Settings remain in app folder.
