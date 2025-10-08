import os
import sys
import json
import shutil
from pathlib import Path
import PyInstaller.__main__

def clean_build():
    """Clean up build directories"""
    dirs_to_clean = ['build', 'dist']
    files_to_clean = ['*.spec']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
    
    for pattern in files_to_clean:
        for file in Path('.').glob(pattern):
            file.unlink()

def ensure_data_files():
    """No-op: data files are created in the chosen storage directory by the app."""
    return

def build_app():
    """Build the application"""
    # Clean previous builds
    clean_build()
    
    # No pre-creation of data files in project root
    ensure_data_files()
    
    # PyInstaller arguments
    args = [
        'job_tracker.py',  # Your main script
        '--name=JobTracker',  # Name of the executable
        '--onefile',  # Create a single executable
        '--windowed',  # Don't show console window
        '--noconfirm',  # Replace output directory without confirmation
        '--clean',  # Clean PyInstaller cache
    ]
    
    # Add only static resources if any (e.g., icon)
    static_files = [
        'app.ico'
    ]
    
    for file in static_files:
        if os.path.exists(file):
            args.append(f'--add-data={file};.')
    
    # Run PyInstaller
    PyInstaller.__main__.run(args)
    
    # Create distribution folder
    dist_folder = "JobTracker_Distribution"
    if os.path.exists(dist_folder):
        shutil.rmtree(dist_folder)
    os.makedirs(dist_folder)
    
    # Copy executable
    shutil.copy2(os.path.join("dist", "JobTracker.exe"), dist_folder)
    
    # Do not include default data files in distribution; app will create them in chosen folder
    
    # Create README
    readme_content = """Job Application Tracker

This is a standalone application for tracking job applications. 

To use:
1. Double-click JobTracker.exe to start
2. No installation needed
3. Data is stored locally in your chosen folder (Settings → Storage Location)

Important:
- Your data is stored only on your computer; nothing is uploaded to any cloud.
- You can change where data is stored from within the app: Settings → Storage Location → Change Folder.
- If you keep the exe on your Desktop, consider creating a personal subfolder (e.g., Desktop\\MyJobTracker) and choose it to avoid files being created directly on the Desktop.
"""
    
    with open(os.path.join(dist_folder, "README.txt"), 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("\nBuild completed!")
    print(f"\nDistribution package created in: {dist_folder}")
    
    # Create release package
    release_version = "1.1.0"  # Update this for new releases
    release_folder = "release"
    if os.path.exists(release_folder):
        shutil.rmtree(release_folder)
    os.makedirs(release_folder)
    
    # Create release notes
    release_notes = f"""# Job Application Tracker v{release_version}

A desktop application to track job applications, especially useful for LinkedIn job posts.

## Features
- Track job applications with company name and job link
- Search through previous applications
- Basic statistics
- Modern user interface
- No installation needed - just unzip and run

## Installation
1. Download and extract the zip file
2. Run JobTracker.exe
3. Start tracking your job applications!

## System Requirements
- Windows 7 or later
- No additional software needed

## Important: Local data storage

- Your data is stored only on your computer; nothing is uploaded to any cloud service.
- When first run, choose where to store your data.
- To change the storage folder later, open the app and go to: Settings → Storage Location → Change Folder.
- If you plan to keep the exe on your Desktop, create a personal subfolder (e.g., `Desktop\\MyJobTracker`) and select it to avoid files being created directly on the Desktop.

## What's New in v{release_version}
- Storage location now fully respects your chosen folder; no files are created in the app root.
- Removed heavy plotting dependencies and graphs; kept lightweight basic stats.
- Significantly reduced executable size for faster downloads and updates.
"""
    
    with open(os.path.join(release_folder, "RELEASE_NOTES.md"), 'w', encoding='utf-8') as f:
        f.write(release_notes)
    
    # Create zip file
    shutil.make_archive(
        os.path.join(release_folder, f"JobTracker-v{release_version}-windows"),
        'zip',
        dist_folder
    )
    
    print("\nRelease package created!")
    print(f"Release files are in: {release_folder}")
    print("\nTo publish on GitHub:")
    print("1. Create a new repository on GitHub")
    print("2. Create a new release")
    print("3. Upload the zip file and copy-paste the release notes")

if __name__ == "__main__":
    build_app()
