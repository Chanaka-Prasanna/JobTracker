# Job Application Tracker

A desktop application to track job applications, especially useful for LinkedIn job posts where application tracking isn't available.

![Job Tracker Screenshot](screenshots/main.png)

## Download

👉 [Download Latest Release](../../releases/latest)

Just download, unzip, and run! No installation needed.

## Features

- Track job applications with company name and job link
- Search through previous applications
- View basic application statistics
- Modern user interface with dark mode support
- No installation needed - portable application
- Data stored locally for privacy

## For Users

1. Go to [Releases](../../releases)
2. Download the latest `JobTracker-vX.X.X-windows.zip`
3. Extract the zip file
4. Run `JobTracker.exe`
5. Start tracking your applications!

## Important: Local data storage

- Your data is stored only on your computer; nothing is uploaded to any cloud service.
- Default location: the same folder as `JobTracker.exe` (portable app behavior).
- You can change where data is stored from within the app: Settings → Storage Location → Change Folder.
- Tip: If you keep the exe on your Desktop, consider creating a personal subfolder (e.g., `Desktop\\MyJobTracker`) and choose it. Otherwise, `settings.json` and `job_data.json` will be created directly on the Desktop.

## For Developers

### Requirements

- Python 3.7+
- Required packages in requirements.txt

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/YourUsername/JobTracker.git
cd JobTracker

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run in Development Mode

```bash
python job_tracker.py
```

### Build Executable

```bash
python build.py
```

The executable and distribution package will be created in the `JobTracker_Distribution` folder.

## License

MIT License - feel free to use and modify!
