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

        # Paths: base settings file may live next to the app; user settings live in the chosen data directory
        self.app_settings_path = os.path.join(self.app_dir, 'settings.json')
        # AppData pointer to remember chosen directory across app moves
        self.appdata_config_dir = os.path.join(os.getenv('APPDATA', self.app_dir), 'JobTracker')
        self.appdata_config_path = os.path.join(self.appdata_config_dir, 'config.json')

        # Load base settings from app folder if present (do not create)
        self.settings = self.load_settings()

        # Resolve data directory: prefer AppData pointer, then settings, then app directory
        pointed_directory = self._load_pointed_directory()
        self.data_directory = pointed_directory or self.settings.get('data_directory') or self.app_dir

        # Compute user-facing paths in chosen data directory
        self.user_settings_path = os.path.join(self.data_directory, 'settings.json')
        self.data_path = os.path.join(self.data_directory, 'job_data.json')

        # Prefer settings from the chosen directory if present
        try:
            if os.path.exists(self.user_settings_path):
                with open(self.user_settings_path, 'r') as f:
                    self.settings = json.load(f)
        except Exception:
            # If reading chosen settings fails, keep existing self.settings
            pass
    
    def load_settings(self):
        """Load settings from settings.json next to the app, or create defaults."""
        try:
            with open(self.app_settings_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Do not auto-create any files; return defaults only
            return {
                "user_name": "",
                "job_roles": self.default_roles.copy(),
                # data_directory will be set after user chooses
            }
    
    def save_settings(self, settings=None):
        """Save settings to settings.json in the chosen data directory."""
        if settings is not None:
            self.settings = settings
        # Ensure chosen data directory exists
        if not getattr(self, 'data_directory', None):
            # If no data directory yet, default to app folder until user selects
            self.data_directory = self.app_dir
            self.user_settings_path = os.path.join(self.data_directory, 'settings.json')
        Path(self.data_directory).mkdir(parents=True, exist_ok=True)
        with open(self.user_settings_path, 'w') as f:
            json.dump(self.settings, f, indent=4)
        # Persist pointer so app can find the chosen folder even if moved
        self._save_pointed_directory(self.data_directory)
    
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
        return not os.path.exists(self.user_settings_path) or not self.get_user_name()

    def get_creation_date(self):
        """Get the date when settings were first created"""
        return datetime.fromisoformat(self.settings.get('created_date', datetime.now().isoformat()))

    # -------------------- Storage paths management --------------------
    def get_settings_file_path(self) -> str:
        # Always use settings.json in the chosen storage directory
        return self.user_settings_path

    def get_data_file_path(self) -> str:
        return self.data_path

    def get_storage_directory(self) -> str:
        return self.data_directory

    def set_storage_directory(self, directory_path: str):
        """Change the storage directory.
        Both settings.json and job_data.json will be stored only in the chosen directory.
        The chosen directory is stored inside settings.json (field: data_directory).
        """
        directory_path = os.path.abspath(directory_path)
        Path(directory_path).mkdir(parents=True, exist_ok=True)

        old_data_path = self.data_path
        old_user_settings_path = getattr(self, 'user_settings_path', os.path.join(self.data_directory, 'settings.json'))

        self.data_directory = directory_path
        self.user_settings_path = os.path.join(self.data_directory, 'settings.json')
        self.data_path = os.path.join(self.data_directory, 'job_data.json')

        # Persist new directory in settings and write to chosen location
        self.settings['data_directory'] = self.data_directory
        self.save_settings()
        # Update pointer as well
        self._save_pointed_directory(self.data_directory)

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
        # Ensure job_data.json exists if it wasn't migrated
        if not os.path.exists(self.data_path):
            with open(self.data_path, 'w') as f:
                f.write('[]')
        # Files are not created in the app root once a storage directory is chosen.

    # -------------------- Internal helpers --------------------
    def _load_pointed_directory(self):
        try:
            with open(self.appdata_config_path, 'r') as f:
                cfg = json.load(f)
            directory = cfg.get('data_directory')
            if directory and os.path.isdir(directory):
                return directory
        except Exception:
            return None
        return None

    def _save_pointed_directory(self, directory_path: str):
        try:
            Path(self.appdata_config_dir).mkdir(parents=True, exist_ok=True)
            with open(self.appdata_config_path, 'w') as f:
                json.dump({'data_directory': directory_path}, f, indent=2)
        except Exception:
            # Ignore pointer write failures; app can still use current session paths
            pass
