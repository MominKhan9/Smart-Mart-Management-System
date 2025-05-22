import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from controllers.admin_controller import AdminController

class AdminView:
    def __init__(self, master, login_window):
        self.master = master
        self.login_window = login_window
        self.controller = AdminController()
        
        # Set up main window
        self.master.title("Smart Mart Management System - Admin Dashboard")
        self.master.geometry("1000x600")
        self.master.configure(bg="#f0f0f0")
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Center window on screen
        self.center_window()
        
        # Create styles
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Arial", 12))
        self.style.configure("TButton", font=("Arial", 12))
        self.style.configure("Header.TLabel", font=("Arial", 24, "bold"), background="#f0f0f0")
        self.style.configure("Section.TLabel", font=("Arial", 16, "bold"), background="#f0f0f0")
        
        # Main container
        self.main_frame = ttk.Frame(self.master)
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Header
        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.pack(fill="x", pady=10)
        
        self.header_label = ttk.Label(self.header_frame, text="Admin Dashboard", style="Header.TLabel")
        self.header_label.pack(side="left", padx=10)
        
        self.logout_btn = ttk.Button(self.header_frame, text="Logout", command=self.logout)
        self.logout_btn.pack(side="right", padx=10)
        
        # Tab control
        self.tab_control = ttk.Notebook(self.main_frame)
        self.tab_control.pack(expand=True, fill="both", pady=10)
        
        # Cashier Management Tab
        self.cashier_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.cashier_tab, text="Cashier Management")
        self.setup_cashier_tab()
        
        # Product Management Tab
        self.product_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.product_tab, text="Product Management")
        self.setup_product_tab()
        
        # Footer
        self.footer_frame = ttk.Frame(self.main_frame)
        self.footer_frame.pack(fill="x", pady=10)
        
        self.footer_label = ttk.Label(self.footer_frame, text="© 2023 Smart Mart Management System", font=("Arial", 10))
        self.footer_label.pack(side="left", padx=10)

    def center_window(self):
        """Center the window on the screen"""
        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.master.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def setup_cashier_tab(self):
        """Set up the cashier management tab"""
        # Cashier management container
        self.cashier_container = ttk.Frame(self.cashier_tab)
        self.cashier_container.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Left panel - List of cashiers
        self.cashier_left_panel = ttk.LabelFrame(self.cashier_container, text="Cashier List")
        self.cashier_left_panel.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        
        # Cashier treeview
        self.cashier_treeview = ttk.Treeview(self.cashier_left_panel, columns=("Username", "Name"), show="headings")
        self.cashier_treeview.heading("Username", text="Username")
        self.cashier_treeview.heading("Name", text="Name")
        self.cashier_treeview.column("Username", width=150)
        self.cashier_treeview.column("Name", width=200)
        self.cashier_treeview.pack(expand=True, fill="both", padx=5, pady=5)
        
        # Vertical scrollbar
        self.cashier_scrollbar = ttk.Scrollbar(self.cashier_left_panel, orient="vertical", command=self.cashier_treeview.yview)
        self.cashier_scrollbar.pack(side="right", fill="y")
        self.cashier_treeview.configure(yscrollcommand=self.cashier_scrollbar.set)
        
        # Right panel - Cashier actions
        self.cashier_right_panel = ttk.LabelFrame(self.cashier_container, text="Cashier Actions")
        self.cashier_right_panel.pack(side="right", expand=True, fill="both", padx=5, pady=5)
        
        # Add cashier section
        self.add_cashier_frame = ttk.Frame(self.cashier_right_panel)
        self.add_cashier_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(self.add_cashier_frame, text="Add New Cashier", style="Section.TLabel").pack(anchor="w", pady=5)
        
        # Username
        ttk.Label(self.add_cashier_frame, text="Username:").pack(anchor="w", pady=2)
        self.cashier_username_var = tk.StringVar()
        ttk.Entry(self.add_cashier_frame, textvariable=self.cashier_username_var).pack(fill="x", pady=2)
        
        # Password
        ttk.Label(self.add_cashier_frame, text="Password:").pack(anchor="w", pady=2)
        self.cashier_password_var = tk.StringVar()
        ttk.Entry(self.add_cashier_frame, textvariable=self.cashier_password_var, show="*").pack(fill="x", pady=2)
        
        # Name
        ttk.Label(self.add_cashier_frame, text="Name:").pack(anchor="w", pady=2)
        self.cashier_name_var = tk.StringVar()
        ttk.Entry(self.add_cashier_frame, textvariable=self.cashier_name_var).pack(fill="x", pady=2)
        
        # Add button
        ttk.Button(self.add_cashier_frame, text="Add Cashier", command=self.add_cashier).pack(anchor="w", pady=10)
        
        # Separator
        ttk.Separator(self.cashier_right_panel, orient="horizontal").pack(fill="x", padx=10, pady=10)
        
        # Manage cashier section
        self.manage_cashier_frame = ttk.Frame(self.cashier_right_panel)
        self.manage_cashier_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(self.manage_cashier_frame, text="Manage Selected Cashier", style="Section.TLabel").pack(anchor="w", pady=5)
        
        # Update and delete buttons
        button_frame = ttk.Frame(self.manage_cashier_frame)
        button_frame.pack(fill="x", pady=10)
        
        ttk.Button(button_frame, text="Update Password", command=self.update_cashier_password).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Update Name", command=self.update_cashier_name).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Delete Cashier", command=self.delete_cashier).pack(side="left", padx=5)
        
        # Refresh cashier list
        ttk.Button(self.manage_cashier_frame, text="Refresh List", command=self.load_cashiers).pack(anchor="w", pady=10)
        
        # Load initial cashier list
        self.load_cashiers()

    def setup_product_tab(self):
        """Set up the product management tab"""
        # Product management container
        self.product_container = ttk.Frame(self.product_tab)
        self.product_container.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Top panel - Category selection
        self.category_frame = ttk.LabelFrame(self.product_container, text="Category")
        self.category_frame.pack(fill="x", padx=5, pady=5)
        
        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(self.category_frame, textvariable=self.category_var, state="readonly")
        self.category_dropdown.pack(side="left", padx=10, pady=10)
        
        ttk.Button(self.category_frame, text="Load Products", command=self.load_products).pack(side="left", padx=10, pady=10)
        ttk.Button(self.category_frame, text="Add New Category", command=self.add_category).pack(side="left", padx=10, pady=10)
        
        # Middle panel - Product list
        self.product_list_frame = ttk.LabelFrame(self.product_container, text="Products")
        self.product_list_frame.pack(expand=True, fill="both", padx=5, pady=5)
        
        # Product treeview
        self.product_treeview = ttk.Treeview(self.product_list_frame, 
                                             columns=("Name", "Price", "Stock"), 
                                             show="headings")
        self.product_treeview.heading("Name", text="Product Name")
        self.product_treeview.heading("Price", text="Price")
        self.product_treeview.heading("Stock", text="Stock")
        self.product_treeview.column("Name", width=200)
        self.product_treeview.column("Price", width=100)
        self.product_treeview.column("Stock", width=100)
        self.product_treeview.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        
        # Vertical scrollbar for product list
        self.product_scrollbar = ttk.Scrollbar(self.product_list_frame, orient="vertical", command=self.product_treeview.yview)
        self.product_scrollbar.pack(side="right", fill="y")
        self.product_treeview.configure(yscrollcommand=self.product_scrollbar.set)
        
        # Bottom panel - Product actions
        self.product_actions_frame = ttk.LabelFrame(self.product_container, text="Product Actions")
        self.product_actions_frame.pack(fill="x", padx=5, pady=5)
        
        # Add product section
        self.add_product_frame = ttk.Frame(self.product_actions_frame)
        self.add_product_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(self.add_product_frame, text="Add New Product", style="Section.TLabel").pack(anchor="w", pady=5)
        
        # Product fields
        fields_frame = ttk.Frame(self.add_product_frame)
        fields_frame.pack(fill="x", pady=5)
        
        # Name
        ttk.Label(fields_frame, text="Name:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.product_name_var = tk.StringVar()
        ttk.Entry(fields_frame, textvariable=self.product_name_var, width=20).grid(row=0, column=1, padx=5, pady=2)
        
        # Price
        ttk.Label(fields_frame, text="Price:").grid(row=0, column=2, sticky="w", padx=5, pady=2)
        self.product_price_var = tk.StringVar()
        ttk.Entry(fields_frame, textvariable=self.product_price_var, width=10).grid(row=0, column=3, padx=5, pady=2)
        
        # Stock
        ttk.Label(fields_frame, text="Stock:").grid(row=0, column=4, sticky="w", padx=5, pady=2)
        self.product_stock_var = tk.StringVar()
        ttk.Entry(fields_frame, textvariable=self.product_stock_var, width=10).grid(row=0, column=5, padx=5, pady=2)
        
        # Add product button
        ttk.Button(self.add_product_frame, text="Add Product", command=self.add_product).pack(anchor="w", pady=5)
        
        # Separator
        ttk.Separator(self.product_actions_frame, orient="horizontal").pack(fill="x", padx=10, pady=5)
        
        # Manage product section
        self.manage_product_frame = ttk.Frame(self.product_actions_frame)
        self.manage_product_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(self.manage_product_frame, text="Manage Selected Product", style="Section.TLabel").pack(anchor="w", pady=5)
        
        # Update and delete buttons
        button_frame = ttk.Frame(self.manage_product_frame)
        button_frame.pack(fill="x", pady=5)
        
        ttk.Button(button_frame, text="Update Price", command=self.update_product_price).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Update Stock", command=self.update_product_stock).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Delete Product", command=self.delete_product).pack(side="left", padx=5)
        
        # Load initial categories
        self.load_categories()

    def load_cashiers(self):
        """Load cashiers into the treeview"""
        # Clear existing items
        for item in self.cashier_treeview.get_children():
            self.cashier_treeview.delete(item)
        
        # Get cashiers from controller
        cashiers = self.controller.get_all_cashiers()
        
        # Add to treeview
        for cashier in cashiers:
            self.cashier_treeview.insert("", "end", values=(cashier["username"], cashier["name"]))

    def add_cashier(self):
        """Add a new cashier"""
        username = self.cashier_username_var.get()
        password = self.cashier_password_var.get()
        name = self.cashier_name_var.get()
        
        success, message = self.controller.add_cashier(username, password, name)
        
        if success:
            messagebox.showinfo("Success", message)
            # Clear form fields
            self.cashier_username_var.set("")
            self.cashier_password_var.set("")
            self.cashier_name_var.set("")
            # Refresh list
            self.load_cashiers()
        else:
            messagebox.showerror("Error", message)

    def update_cashier_password(self):
        """Update the selected cashier's password"""
        selected_item = self.cashier_treeview.selection()
        if not selected_item:
            messagebox.showerror("Error", "No cashier selected")
            return
            
        username = self.cashier_treeview.item(selected_item[0])["values"][0]
        
        # Prompt for new password
        new_password = simpledialog.askstring("Update Password", 
                                             f"Enter new password for {username}:", 
                                             show="*")
        
        if new_password:
            success, message = self.controller.update_cashier(username, password=new_password)
            
            if success:
                messagebox.showinfo("Success", message)
            else:
                messagebox.showerror("Error", message)

    def update_cashier_name(self):
        """Update the selected cashier's name"""
        selected_item = self.cashier_treeview.selection()
        if not selected_item:
            messagebox.showerror("Error", "No cashier selected")
            return
            
        username = self.cashier_treeview.item(selected_item[0])["values"][0]
        current_name = self.cashier_treeview.item(selected_item[0])["values"][1]
        
        # Prompt for new name
        new_name = simpledialog.askstring("Update Name", 
                                         f"Enter new name for {username}:", 
                                         initialvalue=current_name)
        
        if new_name:
            success, message = self.controller.update_cashier(username, name=new_name)
            
            if success:
                messagebox.showinfo("Success", message)
                # Refresh list
                self.load_cashiers()
            else:
                messagebox.showerror("Error", message)

    def delete_cashier(self):
        """Delete the selected cashier"""
        selected_item = self.cashier_treeview.selection()
        if not selected_item:
            messagebox.showerror("Error", "No cashier selected")
            return
            
        username = self.cashier_treeview.item(selected_item[0])["values"][0]
        
        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Delete", 
                                     f"Are you sure you want to delete cashier '{username}'?")
        
        if confirm:
            success, message = self.controller.delete_cashier(username)
            
            if success:
                messagebox.showinfo("Success", message)
                # Refresh list
                self.load_cashiers()
            else:
                messagebox.showerror("Error", message)

    def load_categories(self):
        """Load product categories into dropdown"""
        categories = self.controller.get_all_categories()
        self.category_dropdown["values"] = categories
        
        # Select first category if available
        if categories:
            self.category_dropdown.current(0)
            # Load products for the first category
            self.load_products()

    def add_category(self):
        """Add a new category"""
        new_category = simpledialog.askstring("New Category", "Enter new category name:")
        
        if new_category:
            # Check if category already exists
            existing_categories = self.controller.get_all_categories()
            if new_category in existing_categories:
                messagebox.showerror("Error", f"Category '{new_category}' already exists")
                return
                
            # Add a default product to create the category
            success, message = self.controller.add_product(new_category, "Sample Product", 0, 0)
            
            if success:
                messagebox.showinfo("Success", f"Category '{new_category}' created")
                # Refresh categories
                self.load_categories()
            else:
                messagebox.showerror("Error", "Failed to create category")

    def load_products(self):
        """Load products for selected category"""
        category = self.category_var.get()
        if not category:
            return
            
        # Clear existing items
        for item in self.product_treeview.get_children():
            self.product_treeview.delete(item)
        
        # Get products from controller
        products = self.controller.get_products_by_category(category)
        
        # Add to treeview
        for product in products:
            self.product_treeview.insert("", "end", values=(product["name"], product["price"], product["stock"]))

    def add_product(self):
        """Add a new product to the selected category"""
        category = self.category_var.get()
        name = self.product_name_var.get()
        price = self.product_price_var.get()
        stock = self.product_stock_var.get()
        
        success, message = self.controller.add_product(category, name, price, stock)
        
        if success:
            messagebox.showinfo("Success", message)
            # Clear form fields
            self.product_name_var.set("")
            self.product_price_var.set("")
            self.product_stock_var.set("")
            # Refresh list
            self.load_products()
        else:
            messagebox.showerror("Error", message)

    def update_product_price(self):
        """Update the selected product's price"""
        category = self.category_var.get()
        selected_item = self.product_treeview.selection()
        
        if not selected_item:
            messagebox.showerror("Error", "No product selected")
            return
            
        product_name = self.product_treeview.item(selected_item[0])["values"][0]
        current_price = self.product_treeview.item(selected_item[0])["values"][1]
        
        # Prompt for new price
        new_price = simpledialog.askfloat("Update Price", 
                                         f"Enter new price for {product_name}:", 
                                         initialvalue=current_price)
        
        if new_price is not None:
            success, message = self.controller.update_product(category, product_name, price=new_price)
            
            if success:
                messagebox.showinfo("Success", message)
                # Refresh list
                self.load_products()
            else:
                messagebox.showerror("Error", message)

    def update_product_stock(self):
        """Update the selected product's stock"""
        category = self.category_var.get()
        selected_item = self.product_treeview.selection()
        
        if not selected_item:
            messagebox.showerror("Error", "No product selected")
            return
            
        product_name = self.product_treeview.item(selected_item[0])["values"][0]
        current_stock = self.product_treeview.item(selected_item[0])["values"][2]
        
        # Prompt for new stock
        new_stock = simpledialog.askinteger("Update Stock", 
                                           f"Enter new stock for {product_name}:", 
                                           initialvalue=current_stock)
        
        if new_stock is not None:
            success, message = self.controller.update_product(category, product_name, stock=new_stock)
            
            if success:
                messagebox.showinfo("Success", message)
                # Refresh list
                self.load_products()
            else:
                messagebox.showerror("Error", message)

    def delete_product(self):
        """Delete the selected product"""
        category = self.category_var.get()
        selected_item = self.product_treeview.selection()
        
        if not selected_item:
            messagebox.showerror("Error", "No product selected")
            return
            
        product_name = self.product_treeview.item(selected_item[0])["values"][0]
        
        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Delete", 
                                     f"Are you sure you want to delete product '{product_name}'?")
        
        if confirm:
            success, message = self.controller.delete_product(category, product_name)
            
            if success:
                messagebox.showinfo("Success", message)
                # Refresh list
                self.load_products()
            else:
                messagebox.showerror("Error", message)

    def logout(self):
        """Logout and return to login screen"""
        self.master.destroy()
        self.login_window.deiconify()  # Show the login window again

    def on_close(self):
        """Handle window close event"""
        self.logout() 