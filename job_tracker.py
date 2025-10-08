import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledFrame
import json
import os
import sys
from datetime import datetime
import pyperclip  # For copying to clipboard
from PIL import Image, ImageTk
from stats_manager import StatsManager
from settings_manager import SettingsManager

class JobTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Job Application Tracker")
        self.root.geometry("1000x700")
        
        # Get the application directory
        if getattr(sys, 'frozen', False):
            self.app_dir = os.path.dirname(sys.executable)
        else:
            self.app_dir = os.path.dirname(os.path.abspath(__file__))
            
        self.data_file = os.path.join(self.app_dir, 'job_data.json')
        self.settings_manager = SettingsManager()
        self.load_data()
        
        # Initialize stats manager
        self.stats_manager = StatsManager(self.jobs, self.settings_manager)
        
        self.create_widgets()
        # Show all records when app starts
        self.show_all_records()
        
    def load_data(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    self.jobs = json.load(f)
            else:
                self.jobs = []
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {str(e)}")
            self.jobs = []
            
    def save_data(self):
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.jobs, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Error saving data: {str(e)}")
            
    def create_widgets(self):
        # Create greeting frame
        greeting_frame = ttk.Frame(self.root)
        greeting_frame.pack(fill="x", padx=10, pady=(10,5))
        
        # User greeting
        user_name = self.settings_manager.get_user_name()
        greeting_text = f"Welcome back, {user_name}!" if user_name else "Welcome to Job Application Tracker!"
        greeting_label = ttk.Label(greeting_frame, text=greeting_text, 
                                 font=('TkDefaultFont', 12, 'bold'))
        greeting_label.pack(side="left")
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Main tab
        self.main_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.main_tab, text="Applications")
        
        # Stats tab
        self.stats_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.stats_tab, text="Statistics")
        
        # Settings tab
        self.settings_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_tab, text="Settings")
        
        self.create_main_tab()
        self.create_stats_tab()
        self.create_settings_tab()
        
    def create_stats_tab(self):
        """Create the statistics tab with graphs and analytics"""
        # Create main container
        stats_container = ScrolledFrame(self.stats_tab, autohide=True)
        stats_container.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Basic Stats Section
        basic_stats_frame = ttk.LabelFrame(stats_container, text="Overview", padding=10)
        basic_stats_frame.pack(fill="x", padx=5, pady=5)
        
        # Stats labels
        self.total_apps_label = ttk.Label(basic_stats_frame, text="Total Applications: 0")
        self.total_apps_label.pack(anchor="w", pady=2)
        
        self.unique_companies_label = ttk.Label(basic_stats_frame, text="Unique Companies: 0")
        self.unique_companies_label.pack(anchor="w", pady=2)
        
        self.daily_rate_label = ttk.Label(basic_stats_frame, text="Daily Application Rate: 0")
        self.daily_rate_label.pack(anchor="w", pady=2)
        
        # Applications by Role Section
        roles_frame = ttk.LabelFrame(stats_container, text="Applications by Role", padding=10)
        roles_frame.pack(fill="x", padx=5, pady=5)
        
        self.roles_tree = ttk.Treeview(roles_frame, columns=("role", "count"), show="headings", height=6)
        self.roles_tree.heading("role", text="Role")
        self.roles_tree.heading("count", text="Applications")
        self.roles_tree.pack(fill="x", pady=5)
        
        # Graphs Section
        graphs_frame = ttk.LabelFrame(stats_container, text="Application Trends", padding=10)
        graphs_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Daily Applications Graph
        self.daily_graph_label = ttk.Label(graphs_frame, text="Daily Applications")
        self.daily_graph_label.pack(pady=5)
        
        self.daily_graph = ttk.Label(graphs_frame)
        self.daily_graph.pack(pady=5)
        
        # Role Distribution Graph
        self.role_graph_label = ttk.Label(graphs_frame, text="Role Distribution")
        self.role_graph_label.pack(pady=5)
        
        self.role_graph = ttk.Label(graphs_frame)
        self.role_graph.pack(pady=5)
        
        # Refresh button
        ttk.Button(stats_container, text="Refresh Statistics", 
                  command=self.refresh_statistics,
                  style="info.TButton").pack(pady=10)
        
        # Initial statistics update
        self.refresh_statistics()
    
    def create_settings_tab(self):
        """Create the settings tab for managing user preferences"""
        # Create main container
        settings_container = ScrolledFrame(self.settings_tab, autohide=True)
        settings_container.pack(fill="both", expand=True, padx=10, pady=5)
        
        # User Settings Section
        user_frame = ttk.LabelFrame(settings_container, text="User Settings", padding=10)
        user_frame.pack(fill="x", padx=5, pady=5)
        
        # User Name
        ttk.Label(user_frame, text="Your Name:").grid(row=0, column=0, padx=5, pady=5)
        self.settings_name_var = tk.StringVar(value=self.settings_manager.get_user_name())
        name_entry = ttk.Entry(user_frame, textvariable=self.settings_name_var, width=40)
        name_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
        
        # Job Roles Section
        roles_frame = ttk.LabelFrame(settings_container, text="Job Roles", padding=10)
        roles_frame.pack(fill="x", padx=5, pady=5)
        
        # Existing Roles List
        roles_list_frame = ttk.Frame(roles_frame)
        roles_list_frame.pack(fill="x", pady=5)
        
        # Roles listbox with scrollbar
        roles_scroll = ttk.Scrollbar(roles_list_frame)
        roles_scroll.pack(side="right", fill="y")
        
        self.roles_listbox = tk.Listbox(roles_list_frame, height=8, 
                                      yscrollcommand=roles_scroll.set)
        self.roles_listbox.pack(side="left", fill="both", expand=True)
        roles_scroll.config(command=self.roles_listbox.yview)
        
        # Populate roles list
        for role in self.settings_manager.get_job_roles():
            self.roles_listbox.insert(tk.END, role)
        
        # Add/Remove Roles
        roles_button_frame = ttk.Frame(roles_frame)
        roles_button_frame.pack(fill="x", pady=5)
        
        self.new_role_var = tk.StringVar()
        new_role_entry = ttk.Entry(roles_button_frame, 
                                 textvariable=self.new_role_var, width=30)
        new_role_entry.pack(side="left", padx=5)
        
        ttk.Button(roles_button_frame, text="Add Role",
                  command=self.add_job_role,
                  style="info.TButton").pack(side="left", padx=5)
        
        ttk.Button(roles_button_frame, text="Remove Selected",
                  command=self.remove_job_role,
                  style="danger.TButton").pack(side="left", padx=5)
        
        # Save Settings Button
        ttk.Button(settings_container, text="Save Settings",
                  command=self.save_settings,
                  style="success.TButton").pack(pady=20)
    
    def add_job_role(self):
        """Add a new job role to settings"""
        new_role = self.new_role_var.get().strip()
        if not new_role:
            messagebox.showwarning("Warning", "Please enter a role name")
            return
            
        if new_role in self.settings_manager.get_job_roles():
            messagebox.showwarning("Warning", "This role already exists")
            return
            
        self.settings_manager.add_job_role(new_role)
        self.roles_listbox.insert(tk.END, new_role)
        self.new_role_var.set("")
    
    def remove_job_role(self):
        """Remove selected job role from settings"""
        selection = self.roles_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a role to remove")
            return
            
        role = self.roles_listbox.get(selection[0])
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to remove the role '{role}'?"):
            self.settings_manager.remove_job_role(role)
            self.roles_listbox.delete(selection[0])
    
    def save_settings(self):
        """Save user settings"""
        name = self.settings_name_var.get().strip()
        self.settings_manager.update_user_name(name)
        
        # Update greeting
        greeting_text = f"Welcome back, {name}!" if name else "Welcome to Job Application Tracker!"
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Label):
                        child.config(text=greeting_text)
                        break
                break
        
        messagebox.showinfo("Success", "Settings saved successfully!")
    
    def refresh_statistics(self):
        """Update all statistics and graphs"""
        # Update stats manager with current data
        self.stats_manager = StatsManager(self.jobs, self.settings_manager)
        
        # Get basic stats
        stats = self.stats_manager.get_basic_stats()
        
        # Update labels
        self.total_apps_label.config(text=f"Total Applications: {stats['total_applications']}")
        self.unique_companies_label.config(text=f"Unique Companies: {stats['unique_companies']}")
        self.daily_rate_label.config(text=f"Daily Application Rate: {stats['daily_rate']:.1f}")
        
        # Update roles tree
        self.roles_tree.delete(*self.roles_tree.get_children())
        for role, count in stats['applications_by_role'].items():
            self.roles_tree.insert("", "end", values=(role, count))
        
        # Update graphs
        daily_plot = self.stats_manager.generate_daily_applications_plot()
        if daily_plot:
            daily_img = ImageTk.PhotoImage(Image.open(daily_plot))
            self.daily_graph.configure(image=daily_img)
            self.daily_graph.image = daily_img
        
        roles_plot = self.stats_manager.generate_roles_pie_chart()
        if roles_plot:
            roles_img = ImageTk.PhotoImage(Image.open(roles_plot))
            self.role_graph.configure(image=roles_img)
            self.role_graph.image = roles_img
    
    def create_main_tab(self):
        # Search Frame
        search_frame = ttk.LabelFrame(self.main_tab, text="Search Job Applications", padding=10)
        search_frame.pack(fill="x", padx=10, pady=5)
        
        # Search Entry
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=50)
        search_entry.pack(side="left", padx=5)
        
        # Search Type
        self.search_type = tk.StringVar(value="link")
        ttk.Radiobutton(search_frame, text="Search by Link", variable=self.search_type, 
                       value="link").pack(side="left", padx=5)
        ttk.Radiobutton(search_frame, text="Search by Company", variable=self.search_type, 
                       value="company").pack(side="left", padx=5)
        
        # Search Button
        ttk.Button(search_frame, text="Search", command=self.search_job, 
                  style="primary.TButton").pack(side="left", padx=5)
        
        # Home Button
        ttk.Button(search_frame, text="Show All", command=self.show_all_records,
                  style="info.TButton").pack(side="left", padx=5)
        
        # Add Application Button
        add_button = ttk.Button(self.main_tab, text="Add New Application", 
                              command=self.show_add_job_dialog,
                              style="success.TButton")
        add_button.pack(padx=10, pady=5)
        
        # Results Frame
        result_frame = ttk.LabelFrame(self.main_tab, text="Job Applications", padding=10)
        result_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Top Info Frame
        top_frame = ttk.Frame(result_frame)
        top_frame.pack(fill="x", pady=(0, 5))
        
        # Record counter
        self.record_count_label = ttk.Label(top_frame, text="Total Records: 0", 
                                          font=('TkDefaultFont', 10))
        self.record_count_label.pack(side="left")
        
        # Delete All Button
        ttk.Button(top_frame, text="Delete All Records", 
                  command=self.delete_all_records,
                  style="danger.TButton").pack(side="right")
        
        # Results Canvas and Scrollbar
        canvas_frame = ttk.Frame(result_frame)
        canvas_frame.pack(fill="both", expand=True)
        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)
        
        canvas = tk.Canvas(canvas_frame)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        self.results_frame = ttk.Frame(canvas)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Grid scrollbar and canvas
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Create window in canvas
        self.canvas_window = canvas.create_window((0, 0), window=self.results_frame, anchor="nw")
        
        # Configure canvas scrolling
        def configure_scroll(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            # Update the canvas window width to match the canvas
            canvas.itemconfig(self.canvas_window, width=canvas.winfo_width())
        
        self.results_frame.bind("<Configure>", configure_scroll)
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(self.canvas_window, width=canvas.winfo_width()))
        
        # Bind mouse wheel
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
    def delete_record(self, job_link):
        """Delete a single record by its job link"""
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this job application?"):
            self.jobs = [job for job in self.jobs if job['link'] != job_link]
            self.save_data()
            self.show_all_records()
    
    def delete_all_records(self):
        """Delete all records after confirmation"""
        if not self.jobs:
            messagebox.showinfo("Info", "No records to delete.")
            return
            
        if messagebox.askyesno("Confirm Delete All", 
                              "Are you sure you want to delete ALL job applications?\nThis action cannot be undone!"):
            self.jobs = []
            self.save_data()
            self.show_all_records()
    
    def show_details(self, job):
        """Show detailed view in a popup window"""
        detail_window = tk.Toplevel(self.root)
        detail_window.title(f"Job Details - {job['company']}")
        detail_window.geometry("600x400")
        
        # Make the window modal
        detail_window.transient(self.root)
        detail_window.grab_set()
        
        # Content frame
        content_frame = ttk.Frame(detail_window, padding=20)
        content_frame.pack(fill="both", expand=True)
        
        # Company details
        ttk.Label(content_frame, text="Company:", 
                 font=('TkDefaultFont', 12, 'bold')).pack(anchor="w", pady=(0,5))
        company_frame = ttk.Frame(content_frame)
        company_frame.pack(fill="x", pady=(0,20))
        ttk.Label(company_frame, text=job['company'], 
                 font=('TkDefaultFont', 11)).pack(side="left")
        
        # Link details
        ttk.Label(content_frame, text="Job Link:", 
                 font=('TkDefaultFont', 12, 'bold')).pack(anchor="w", pady=(0,5))
        link_frame = ttk.Frame(content_frame)
        link_frame.pack(fill="x", pady=(0,20))
        link_text = ttk.Label(link_frame, text=job['link'], 
                          wraplength=550, cursor="hand2")
        link_text.pack(side="left", fill="x", expand=True)
        
        def copy_link():
            pyperclip.copy(job['link'])
            copy_btn.configure(text="Copied!", style="success.TButton")
            detail_window.after(1500, lambda: copy_btn.configure(text="Copy Link", style="info.TButton"))
            
        copy_btn = ttk.Button(content_frame, text="Copy Link", style="info.TButton",
                          command=copy_link)
        copy_btn.pack(pady=20)
        
        # Close button
        ttk.Button(content_frame, text="Close", 
                  command=detail_window.destroy).pack(pady=10)
        
        # Center the window
        detail_window.update_idletasks()
        width = detail_window.winfo_width()
        height = detail_window.winfo_height()
        x = (detail_window.winfo_screenwidth() // 2) - (width // 2)
        y = (detail_window.winfo_screenheight() // 2) - (height // 2)
        detail_window.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_record_frame(self, job, parent_frame, index=None):
        """Create a frame for a single record with delete button"""
        record_frame = ttk.Frame(parent_frame)
        record_frame.pack(fill="x", padx=5, pady=5)
        
        # Add a border around each record
        record_border = ttk.LabelFrame(record_frame, text="")
        record_border.pack(fill="x", padx=2, pady=2)
        
        # Content frame
        content_frame = ttk.Frame(record_border)
        content_frame.pack(fill="x", padx=10, pady=5)
        
        # Record number
        number_frame = ttk.Frame(content_frame, width=50)
        number_frame.pack(side="left", padx=(0, 10))
        number_frame.pack_propagate(False)  # Keep fixed width
        ttk.Label(number_frame, text=f"#{index}", 
                 font=('TkDefaultFont', 10, 'bold')).pack(anchor="center")

        # Left side: Company and truncated link
        info_frame = ttk.Frame(content_frame)
        info_frame.pack(side="left", fill="x", expand=True)
        
        company_label = ttk.Label(info_frame, text=f"Company: {job['company']}", 
                                font=('TkDefaultFont', 10, 'bold'))
        company_label.pack(anchor="w")
        
        # Truncate link if it's too long
        link_text = job['link']
        if len(link_text) > 60:
            link_text = link_text[:57] + "..."
        link_label = ttk.Label(info_frame, text=f"Job Link: {link_text}")
        link_label.pack(anchor="w")
        
        # Make the entire info frame clickable
        for widget in [company_label, link_label, info_frame]:
            widget.bind("<Button-1>", lambda e, j=job: self.show_details(j))
            widget.bind("<Enter>", lambda e, w=widget: w.configure(cursor="hand2"))
            widget.bind("<Leave>", lambda e, w=widget: w.configure(cursor=""))
        
        # Right side: Buttons
        button_frame = ttk.Frame(content_frame)
        button_frame.pack(side="right", padx=(10,0))
        
        # View Details button
        ttk.Button(button_frame, text="View Details", style="info.TButton",
                  command=lambda j=job: self.show_details(j)).pack(side="left", padx=5)
        
        # Delete button
        ttk.Button(button_frame, text="Delete", style="danger.TButton",
                  command=lambda l=job['link']: self.delete_record(l)).pack(side="left")
    
    def clear_results_frame(self):
        """Clear all widgets from results frame"""
        for widget in self.results_frame.winfo_children():
            widget.destroy()
    
    def update_record_count(self, count=None):
        """Update the record count label"""
        if count is None:
            count = len(self.jobs)
        self.record_count_label.configure(text=f"Total Records: {count}")
    
    def show_all_records(self):
        self.search_var.set("")  # Clear search field
        self.clear_results_frame()
        
        if not self.jobs:
            ttk.Label(self.results_frame, 
                     text="No job applications recorded yet.",
                     padding=20).pack()
            self.update_record_count(0)
            return
            
        for index, job in enumerate(self.jobs, 1):
            self.create_record_frame(job, self.results_frame, index)
        
        self.update_record_count()
    
    def search_job(self):
        search_term = self.search_var.get().strip()
        if not search_term:
            self.show_all_records()  # If search is empty, show all records
            return
            
        self.clear_results_frame()
        found = False
        found_count = 0
        
        for index, job in enumerate(self.jobs, 1):
            if self.search_type.get() == "link":
                # Exact match for links (after stripping spaces)
                if search_term.lower().strip() == job['link'].lower().strip():
                    self.create_record_frame(job, self.results_frame, found_count + 1)
                    found = True
                    found_count += 1
            else:
                # Partial match for company names
                if search_term.lower() in job['company'].lower():
                    self.create_record_frame(job, self.results_frame, found_count + 1)
                    found = True
                    found_count += 1
        
        self.update_record_count(found_count)
                
        if not found:
            ttk.Label(self.results_frame, 
                     text="No matching applications found.\nClick 'Show All' to view all records.",
                     padding=20).pack()
            
    def show_add_job_dialog(self):
        """Show popup dialog for adding new job application"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Job Application")
        dialog.geometry("600x400")
        
        # Make the window modal
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Create main frame
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        # Company Name
        ttk.Label(main_frame, text="Company Name:", 
                 font=('TkDefaultFont', 10)).pack(anchor="w", pady=(0,5))
        company_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=company_var, width=50).pack(fill="x", pady=(0,15))
        
        # Job Link
        ttk.Label(main_frame, text="Job Link:", 
                 font=('TkDefaultFont', 10)).pack(anchor="w", pady=(0,5))
        link_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=link_var, width=50).pack(fill="x", pady=(0,15))
        
        # Job Role
        ttk.Label(main_frame, text="Role:", 
                 font=('TkDefaultFont', 10)).pack(anchor="w", pady=(0,5))
        role_var = tk.StringVar()
        role_combo = ttk.Combobox(main_frame, textvariable=role_var, 
                                width=47, state="readonly")
        role_combo['values'] = self.settings_manager.get_job_roles()
        role_combo.pack(fill="x", pady=(0,15))
        
        # Current Date (display only)
        current_date = datetime.now().strftime('%Y-%m-%d')
        ttk.Label(main_frame, text="Application Date:", 
                 font=('TkDefaultFont', 10)).pack(anchor="w", pady=(0,5))
        ttk.Label(main_frame, text=current_date,
                 font=('TkDefaultFont', 10, 'bold')).pack(anchor="w", pady=(0,20))
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(20,0))
        
        ttk.Button(button_frame, text="Cancel",
                  command=dialog.destroy).pack(side="right", padx=5)
        
        def save_job():
            company = company_var.get().strip()
            link = link_var.get().strip()
            role = role_var.get().strip()
            
            if not company or not link or not role:
                messagebox.showwarning("Warning", "Please fill in all fields")
                return
            
            if self.add_job(company, link, role, current_date):
                dialog.destroy()  # Only close if add_job was successful
        
        ttk.Button(button_frame, text="Save",
                  command=save_job,
                  style="success.TButton").pack(side="right", padx=5)
        
        # Center the window
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')
    
    def add_job(self, company, link, role, date):
        """Add a new job application"""
        # Strip spaces from link before checking
        link = link.strip()
        
        # Check if job already exists
        for job in self.jobs:
            if job['link'].lower().strip() == link.lower():
                messagebox.showwarning("Warning", "This job link already exists in the tracker")
                return False  # Return False to indicate failure
                
        self.jobs.append({
            'company': company.strip(),  # Strip spaces from all text fields
            'link': link,
            'role': role.strip(),
            'applied_date': date
        })
        
        self.save_data()
        messagebox.showinfo("Success", "Job application added successfully!")
        self.show_all_records()  # Refresh the display to show all records including the new one
        self.update_record_count()  # Update the record counter
        self.refresh_statistics()  # Update statistics tab
        return True  # Return True to indicate success

def main():
    root = ttk.Window(themename="cosmo")
    app = JobTracker(root)
    root.mainloop()

if __name__ == "__main__":
    main()
