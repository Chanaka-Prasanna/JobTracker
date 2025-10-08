# Job Application Tracker

A simple desktop application to track job applications, especially useful for LinkedIn job posts where application tracking isn't available.

## Features

- Search for previous job applications by job link or company name
- Add new job applications with company name and job link
- View detailed information for each application
- Copy job links with one click
- Delete individual or all records
- Modern UI with bootstrap styling
- Data stored locally in JSON format
- Record numbering and total count display

## For Users: Installing the Application

### Option 1: Using the Installer

1. Download the latest release from the releases page
2. Run the JobTracker.exe file
3. The application will create its data file in the same directory

### Option 2: Running from Source

1. Make sure you have Python 3.7+ installed
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python job_tracker.py
   ```

## For Developers: Building the Application

1. Install development requirements:

   ```
   pip install -r requirements.txt
   ```

2. Build the executable:

   ```
   python build.py
   ```

3. Find the executable in the `dist` directory

## Usage

1. Adding a Job Application:

   - Enter the company name
   - Enter the job link
   - Click "Add Job"

2. Searching Applications:

   - Enter the job link or company name
   - Select search type (by link or by company)
   - Click "Search" or "Show All" to see all records

3. Managing Records:
   - Click on any record to view full details
   - Use the "Copy Link" button in the details view
   - Delete individual records or use "Delete All"
   - See total record count at the top

## Data Storage

The application stores all data in a `job_data.json` file in the same directory as the application. This file is automatically created when you add your first job application.
