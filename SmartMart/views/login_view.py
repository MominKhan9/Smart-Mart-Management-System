import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from controllers.login_controller import LoginController

class LoginView:
    def __init__(self, master):
        self.master = master
        self.controller = LoginController()
        
        # Set up main window
        self.master.title("Smart Mart Management System - Login")
        self.master.geometry("800x500")
        self.master.configure(bg="#f0f0f0")
        
        # Center window on screen
        self.center_window()
        
        # Create styles
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Arial", 12))
        self.style.configure("TButton", font=("Arial", 12))
        self.style.configure("Header.TLabel", font=("Arial", 24, "bold"), background="#f0f0f0")
        self.style.configure("Role.TLabel", font=("Arial", 14, "bold"), background="#f0f0f0")
        
        # Logo and header
        self.header_frame = ttk.Frame(self.master)
        self.header_frame.pack(pady=30)
        
        self.header_label = ttk.Label(self.header_frame, text="Smart Mart Management System", style="Header.TLabel")
        self.header_label.pack()
        
        # Tab control for Admin/Cashier login
        self.tab_control = ttk.Notebook(self.master)
        self.tab_control.pack(expand=1, fill="both", padx=50, pady=20)
        
        # Admin login tab
        self.admin_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.admin_tab, text="Admin Login")
        self.setup_admin_login()
        
        # Cashier login tab
        self.cashier_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.cashier_tab, text="Cashier Login")
        self.setup_cashier_login()
        
        # Footer
        self.footer_frame = ttk.Frame(self.master)
        self.footer_frame.pack(pady=20)
        
        self.footer_label = ttk.Label(self.footer_frame, text="© 2023 Smart Mart Management System", font=("Arial", 10))
        self.footer_label.pack()

    def center_window(self):
        """Center the window on the screen"""
        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.master.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def setup_admin_login(self):
        """Set up the admin login form"""
        self.admin_frame = ttk.Frame(self.admin_tab)
        self.admin_frame.pack(expand=True, fill="both", padx=50, pady=20)
        
        # Admin login form
        self.admin_label = ttk.Label(self.admin_frame, text="Admin Login", style="Role.TLabel")
        self.admin_label.pack(pady=10)
        
        # Username
        self.username_frame = ttk.Frame(self.admin_frame)
        self.username_frame.pack(fill="x", pady=10)
        
        self.username_label = ttk.Label(self.username_frame, text="Username:", width=15, anchor="e")
        self.username_label.pack(side="left", padx=5)
        
        self.admin_username_var = tk.StringVar()
        self.admin_username_entry = ttk.Entry(self.username_frame, textvariable=self.admin_username_var, width=25)
        self.admin_username_entry.pack(side="left", padx=5)
        
        # Password
        self.password_frame = ttk.Frame(self.admin_frame)
        self.password_frame.pack(fill="x", pady=10)
        
        self.password_label = ttk.Label(self.password_frame, text="Password:", width=15, anchor="e")
        self.password_label.pack(side="left", padx=5)
        
        self.admin_password_var = tk.StringVar()
        self.admin_password_entry = ttk.Entry(self.password_frame, textvariable=self.admin_password_var, show="*", width=25)
        self.admin_password_entry.pack(side="left", padx=5)
        
        # Login button
        self.admin_login_btn = ttk.Button(self.admin_frame, text="Login", command=self.admin_login)
        self.admin_login_btn.pack(pady=20)

    def setup_cashier_login(self):
        """Set up the cashier login form"""
        self.cashier_frame = ttk.Frame(self.cashier_tab)
        self.cashier_frame.pack(expand=True, fill="both", padx=50, pady=20)
        
        # Cashier login form
        self.cashier_label = ttk.Label(self.cashier_frame, text="Cashier Login", style="Role.TLabel")
        self.cashier_label.pack(pady=10)
        
        # Username
        self.cashier_username_frame = ttk.Frame(self.cashier_frame)
        self.cashier_username_frame.pack(fill="x", pady=10)
        
        self.cashier_username_label = ttk.Label(self.cashier_username_frame, text="Username:", width=15, anchor="e")
        self.cashier_username_label.pack(side="left", padx=5)
        
        self.cashier_username_var = tk.StringVar()
        self.cashier_username_entry = ttk.Entry(self.cashier_username_frame, textvariable=self.cashier_username_var, width=25)
        self.cashier_username_entry.pack(side="left", padx=5)
        
        # Password
        self.cashier_password_frame = ttk.Frame(self.cashier_frame)
        self.cashier_password_frame.pack(fill="x", pady=10)
        
        self.cashier_password_label = ttk.Label(self.cashier_password_frame, text="Password:", width=15, anchor="e")
        self.cashier_password_label.pack(side="left", padx=5)
        
        self.cashier_password_var = tk.StringVar()
        self.cashier_password_entry = ttk.Entry(self.cashier_password_frame, textvariable=self.cashier_password_var, show="*", width=25)
        self.cashier_password_entry.pack(side="left", padx=5)
        
        # Login button
        self.cashier_login_btn = ttk.Button(self.cashier_frame, text="Login", command=self.cashier_login)
        self.cashier_login_btn.pack(pady=20)

    def admin_login(self):
        """Handle admin login button click"""
        username = self.admin_username_var.get()
        password = self.admin_password_var.get()
        
        success, message = self.controller.login_admin(username, password)
        
        if success:
            messagebox.showinfo("Login Successful", message)
            self.master.withdraw()  # Hide the login window
            self.open_admin_dashboard()
        else:
            messagebox.showerror("Login Failed", message)

    def cashier_login(self):
        """Handle cashier login button click"""
        username = self.cashier_username_var.get()
        password = self.cashier_password_var.get()
        
        success, message, cashier_name = self.controller.login_cashier(username, password)
        
        if success:
            messagebox.showinfo("Login Successful", message)
            self.master.withdraw()  # Hide the login window
            self.open_cashier_panel(username, cashier_name)
        else:
            messagebox.showerror("Login Failed", message)

    def open_admin_dashboard(self):
        """Open the admin dashboard window"""
        admin_window = tk.Toplevel(self.master)
        # Import here to avoid circular import
        from views.admin_view import AdminView
        AdminView(admin_window, self.master)

    def open_cashier_panel(self, username, cashier_name):
        """Open the cashier panel window"""
        cashier_window = tk.Toplevel(self.master)
        # Import here to avoid circular import
        from views.cashier_view import CashierView
        CashierView(cashier_window, self.master, username, cashier_name) 