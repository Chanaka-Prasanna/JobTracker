import tkinter as tk
import ttkbootstrap as ttk

class SetupWindow:
    def __init__(self, settings_manager):
        self.settings_manager = settings_manager
        self.result = False
        
        # Create window
        self.window = tk.Toplevel()
        self.window.title("Initial Setup")
        self.window.geometry("500x400")
        
        # Make it modal
        self.window.transient(self.window.master)
        self.window.grab_set()
        
        self.create_widgets()
        
        # Center the window
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.window, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        # Welcome message
        ttk.Label(
            main_frame,
            text="Welcome to Job Application Tracker!",
            font=('TkDefaultFont', 14, 'bold')
        ).pack(pady=(0, 20))
        
        ttk.Label(
            main_frame,
            text="Please enter your name to get started:",
            font=('TkDefaultFont', 10)
        ).pack(pady=(0, 10))
        
        # Name entry
        self.name_var = tk.StringVar(value=self.settings_manager.get_user_name())
        name_entry = ttk.Entry(main_frame, textvariable=self.name_var, width=40)
        name_entry.pack(pady=(0, 20))
        
        # Job roles section
        ttk.Label(
            main_frame,
            text="Default job roles are configured. You can modify them later in Settings.",
            font=('TkDefaultFont', 10),
            wraplength=400
        ).pack(pady=(0, 10))
        
        # Create a frame for the roles list
        roles_frame = ttk.Frame(main_frame)
        roles_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(roles_frame)
        scrollbar.pack(side="right", fill="y")
        
        # Add listbox for roles
        self.roles_list = tk.Listbox(
            roles_frame,
            height=8,
            selectmode="multiple",
            yscrollcommand=scrollbar.set
        )
        self.roles_list.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.roles_list.yview)
        
        # Populate roles list
        for role in self.settings_manager.get_job_roles():
            self.roles_list.insert(tk.END, role)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(20, 0))
        
        ttk.Button(
            button_frame,
            text="Start Using Application",
            style="success.TButton",
            command=self.save_and_close
        ).pack(side="right", padx=5)
    
    def save_and_close(self):
        name = self.name_var.get().strip()
        if not name:
            ttk.messagebox.showwarning(
                "Name Required",
                "Please enter your name to continue."
            )
            return
        
        # Save settings
        self.settings_manager.update_user_name(name)
        
        self.result = True
        self.window.destroy()
    
    def show(self):
        self.window.wait_window()
        return self.result
