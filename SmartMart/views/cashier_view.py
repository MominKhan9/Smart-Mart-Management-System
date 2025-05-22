import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from controllers.billing_controller import BillingController

class CashierView:
    def __init__(self, master, login_window, username, cashier_name):
        self.master = master
        self.login_window = login_window
        self.username = username
        self.cashier_name = cashier_name
        self.controller = BillingController()
        
        # Set up main window
        self.master.title("Smart Mart Management System - Cashier Panel")
        self.master.geometry("1100x700")
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
        self.style.configure("Cart.TLabel", background="#fafafa")
        self.style.configure("Total.TLabel", font=("Arial", 14, "bold"), background="#f0f0f0")
        
        # Main container
        self.main_frame = ttk.Frame(self.master)
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Header
        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.pack(fill="x", pady=10)
        
        self.header_label = ttk.Label(self.header_frame, text=f"Cashier Panel - {cashier_name}", style="Header.TLabel")
        self.header_label.pack(side="left", padx=10)
        
        self.logout_btn = ttk.Button(self.header_frame, text="Logout", command=self.logout)
        self.logout_btn.pack(side="right", padx=10)
        
        # Split view into left (products) and right (cart)
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(expand=True, fill="both", pady=10)
        
        # Left panel - Products
        self.products_frame = ttk.LabelFrame(self.content_frame, text="Products")
        self.products_frame.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        self.setup_products_panel()
        
        # Right panel - Cart
        self.cart_frame = ttk.LabelFrame(self.content_frame, text="Shopping Cart")
        self.cart_frame.pack(side="right", expand=True, fill="both", padx=5, pady=5)
        self.setup_cart_panel()
        
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

    def setup_products_panel(self):
        """Set up the products browsing panel"""
        # Category selection
        self.categories_frame = ttk.Frame(self.products_frame)
        self.categories_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(self.categories_frame, text="Select Category:").pack(side="left", padx=5)
        
        # Category dropdown
        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(self.categories_frame, textvariable=self.category_var, state="readonly", width=20)
        self.category_dropdown.pack(side="left", padx=5)
        self.category_dropdown.bind("<<ComboboxSelected>>", lambda e: self.load_products())
        
        # Load categories
        categories = self.controller.get_all_categories()
        self.category_dropdown["values"] = categories
        
        # Select first category if available
        if categories:
            self.category_dropdown.current(0)
        
        # Products list
        self.products_list_frame = ttk.Frame(self.products_frame)
        self.products_list_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Product treeview
        self.columns = ("Name", "Price", "Stock")
        self.products_treeview = ttk.Treeview(self.products_list_frame, columns=self.columns, show="headings")
        self.products_treeview.heading("Name", text="Product Name")
        self.products_treeview.heading("Price", text="Price")
        self.products_treeview.heading("Stock", text="Available")
        self.products_treeview.column("Name", width=200)
        self.products_treeview.column("Price", width=100)
        self.products_treeview.column("Stock", width=100)
        self.products_treeview.pack(side="left", expand=True, fill="both")
        
        # Scrollbar for products
        products_scrollbar = ttk.Scrollbar(self.products_list_frame, orient="vertical", command=self.products_treeview.yview)
        products_scrollbar.pack(side="right", fill="y")
        self.products_treeview.configure(yscrollcommand=products_scrollbar.set)
        
        # Add to cart panel
        self.add_to_cart_frame = ttk.Frame(self.products_frame)
        self.add_to_cart_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(self.add_to_cart_frame, text="Quantity:").pack(side="left", padx=5)
        
        # Quantity spinner
        self.quantity_var = tk.IntVar(value=1)
        quantity_spinner = ttk.Spinbox(self.add_to_cart_frame, from_=1, to=100, textvariable=self.quantity_var, width=5)
        quantity_spinner.pack(side="left", padx=5)
        
        # Add to cart button
        ttk.Button(self.add_to_cart_frame, text="Add to Cart", command=self.add_to_cart).pack(side="left", padx=10)
        
        # Load initial products
        self.load_products()

    def setup_cart_panel(self):
        """Set up the shopping cart panel"""
        # Cart items list
        self.cart_list_frame = ttk.Frame(self.cart_frame)
        self.cart_list_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Cart treeview
        self.cart_columns = ("Product", "Price", "Quantity", "Total")
        self.cart_treeview = ttk.Treeview(self.cart_list_frame, columns=self.cart_columns, show="headings")
        self.cart_treeview.heading("Product", text="Product")
        self.cart_treeview.heading("Price", text="Unit Price")
        self.cart_treeview.heading("Quantity", text="Quantity")
        self.cart_treeview.heading("Total", text="Total")
        self.cart_treeview.column("Product", width=180)
        self.cart_treeview.column("Price", width=100)
        self.cart_treeview.column("Quantity", width=80)
        self.cart_treeview.column("Total", width=100)
        self.cart_treeview.pack(side="left", expand=True, fill="both")
        
        # Scrollbar for cart
        cart_scrollbar = ttk.Scrollbar(self.cart_list_frame, orient="vertical", command=self.cart_treeview.yview)
        cart_scrollbar.pack(side="right", fill="y")
        self.cart_treeview.configure(yscrollcommand=cart_scrollbar.set)
        
        # Cart actions frame
        self.cart_actions_frame = ttk.Frame(self.cart_frame)
        self.cart_actions_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(self.cart_actions_frame, text="Remove Selected", command=self.remove_from_cart).pack(side="left", padx=5)
        ttk.Button(self.cart_actions_frame, text="Update Quantity", command=self.update_cart_item).pack(side="left", padx=5)
        ttk.Button(self.cart_actions_frame, text="Clear Cart", command=self.clear_cart).pack(side="left", padx=5)
        
        # Cart totals frame
        self.totals_frame = ttk.Frame(self.cart_frame)
        self.totals_frame.pack(fill="x", padx=10, pady=10)
        
        # Subtotal
        subtotal_frame = ttk.Frame(self.totals_frame)
        subtotal_frame.pack(fill="x", pady=5)
        ttk.Label(subtotal_frame, text="Subtotal:").pack(side="left")
        self.subtotal_var = tk.StringVar(value="₹ 0.00")
        ttk.Label(subtotal_frame, textvariable=self.subtotal_var, style="Total.TLabel").pack(side="right")
        
        # Discount
        discount_frame = ttk.Frame(self.totals_frame)
        discount_frame.pack(fill="x", pady=5)
        ttk.Label(discount_frame, text="Discount:").pack(side="left")
        self.discount_var = tk.StringVar(value="₹ 0.00")
        ttk.Label(discount_frame, textvariable=self.discount_var, style="Total.TLabel").pack(side="right")
        
        # Total
        total_frame = ttk.Frame(self.totals_frame)
        total_frame.pack(fill="x", pady=5)
        ttk.Label(total_frame, text="Total:").pack(side="left")
        self.total_var = tk.StringVar(value="₹ 0.00")
        ttk.Label(total_frame, textvariable=self.total_var, style="Total.TLabel").pack(side="right")
        
        # Payment method
        payment_frame = ttk.LabelFrame(self.cart_frame, text="Payment Method")
        payment_frame.pack(fill="x", padx=10, pady=10)
        
        self.payment_var = tk.StringVar(value="Cash")
        ttk.Radiobutton(payment_frame, text="Cash", variable=self.payment_var, value="Cash", 
                       command=self.update_totals).pack(side="left", padx=10, pady=5)
        ttk.Radiobutton(payment_frame, text="Card (10% discount)", variable=self.payment_var, 
                       value="Card", command=self.update_totals).pack(side="left", padx=10, pady=5)
        
        # Checkout button
        checkout_frame = ttk.Frame(self.cart_frame)
        checkout_frame.pack(fill="x", padx=10, pady=10)
        
        checkout_button = ttk.Button(checkout_frame, text="Process Payment", command=self.process_payment)
        checkout_button.pack(pady=10, fill="x")

    def load_products(self):
        """Load products for the selected category"""
        category = self.category_var.get()
        
        if not category:
            return
        
        # Clear current products
        for item in self.products_treeview.get_children():
            self.products_treeview.delete(item)
        
        # Get products from controller
        products = self.controller.get_products_by_category(category)
        
        # Add products to treeview
        for product in products:
            self.products_treeview.insert("", "end", values=(
                product["name"],
                f"₹{product['price']:.2f}",
                product["stock"]
            ))

    def add_to_cart(self):
        """Add selected product to cart"""
        selected_item = self.products_treeview.selection()
        
        if not selected_item:
            messagebox.showerror("Error", "No product selected")
            return
        
        # Get product details
        product_values = self.products_treeview.item(selected_item[0])["values"]
        product_name = product_values[0]
        # Remove currency symbol and convert to float
        price = float(product_values[1].replace("₹", ""))
        available_stock = int(product_values[2])
        
        # Get quantity
        quantity = self.quantity_var.get()
        
        if quantity <= 0:
            messagebox.showerror("Error", "Quantity must be greater than zero")
            return
            
        if quantity > available_stock:
            messagebox.showerror("Error", f"Not enough stock. Available: {available_stock}")
            return
        
        # Add to cart using controller
        category = self.category_var.get()
        success, message = self.controller.add_to_cart(category, product_name, price, quantity)
        
        if success:
            # Update cart display
            self.update_cart_display()
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)

    def update_cart_display(self):
        """Update the cart treeview with current cart items"""
        # Clear current cart display
        for item in self.cart_treeview.get_children():
            self.cart_treeview.delete(item)
        
        # Get cart items from controller
        cart_items = self.controller.get_cart()
        
        # Add items to cart treeview
        for i, item in enumerate(cart_items):
            self.cart_treeview.insert("", "end", values=(
                item["name"],
                f"₹{item['price']:.2f}",
                item["quantity"],
                f"₹{item['price'] * item['quantity']:.2f}"
            ))
        
        # Update totals
        self.update_totals()

    def update_totals(self):
        """Update the cart totals based on current items"""
        payment_method = self.payment_var.get()
        bill_data = self.controller.calculate_bill(payment_method)
        
        # Update totals display
        self.subtotal_var.set(f"₹ {bill_data['subtotal']:.2f}")
        self.discount_var.set(f"₹ {bill_data['discount']:.2f}")
        self.total_var.set(f"₹ {bill_data['total']:.2f}")

    def remove_from_cart(self):
        """Remove selected item from cart"""
        selected_item = self.cart_treeview.selection()
        
        if not selected_item:
            messagebox.showerror("Error", "No cart item selected")
            return
        
        # Get item index
        index = self.cart_treeview.index(selected_item[0])
        
        # Remove from cart
        success, message = self.controller.remove_from_cart(index)
        
        if success:
            # Update cart display
            self.update_cart_display()
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)

    def update_cart_item(self):
        """Update the quantity of selected cart item"""
        selected_item = self.cart_treeview.selection()
        
        if not selected_item:
            messagebox.showerror("Error", "No cart item selected")
            return
        
        # Get item index
        index = self.cart_treeview.index(selected_item[0])
        
        # Get current quantity
        current_quantity = int(self.cart_treeview.item(selected_item[0])["values"][2])
        
        # Ask for new quantity
        new_quantity = tk.simpledialog.askinteger("Update Quantity", 
                                               "Enter new quantity:", 
                                               initialvalue=current_quantity,
                                               minvalue=1)
        
        if new_quantity is None:
            return  # User canceled
            
        # Update cart item
        success, message = self.controller.update_cart_item(index, new_quantity)
        
        if success:
            # Update cart display
            self.update_cart_display()
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)

    def clear_cart(self):
        """Clear all items from cart"""
        if not self.controller.get_cart():
            messagebox.showinfo("Info", "Cart is already empty")
            return
            
        # Confirm before clearing
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to clear the cart?")
        
        if confirm:
            self.controller.clear_cart()
            # Update cart display
            self.update_cart_display()
            messagebox.showinfo("Success", "Cart cleared")

    def process_payment(self):
        """Process payment and complete the sale"""
        cart_items = self.controller.get_cart()
        
        if not cart_items:
            messagebox.showerror("Error", "Cart is empty")
            return
            
        payment_method = self.payment_var.get()
        
        # Confirm checkout
        bill_data = self.controller.calculate_bill(payment_method)
        confirm_message = (
            f"Payment Method: {payment_method}\n"
            f"Subtotal: ₹ {bill_data['subtotal']:.2f}\n"
            f"Discount: ₹ {bill_data['discount']:.2f}\n"
            f"Total: ₹ {bill_data['total']:.2f}\n\n"
            f"Proceed with payment?"
        )
        
        confirm = messagebox.askyesno("Confirm Payment", confirm_message)
        
        if confirm:
            success, message, bill_info = self.controller.checkout(payment_method)
            
            if success:
                # Show bill details
                self.show_bill(bill_info)
                # Refresh product list to update stock
                self.load_products()
            else:
                messagebox.showerror("Error", message)

    def show_bill(self, bill_info):
        """Show bill details in a popup window"""
        bill_window = tk.Toplevel(self.master)
        bill_window.title("Bill Receipt")
        bill_window.geometry("400x500")
        bill_window.configure(bg="#ffffff")
        
        # Center the window
        bill_window.update_idletasks()
        width = bill_window.winfo_width()
        height = bill_window.winfo_height()
        x = (bill_window.winfo_screenwidth() // 2) - (width // 2)
        y = (bill_window.winfo_screenheight() // 2) - (height // 2)
        bill_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        
        # Bill content
        main_frame = ttk.Frame(bill_window)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Header
        ttk.Label(main_frame, text="Smart Mart", font=("Arial", 16, "bold")).pack(pady=5)
        ttk.Label(main_frame, text="Sales Receipt", font=("Arial", 14)).pack(pady=5)
        ttk.Label(main_frame, text=f"Bill #{bill_info['bill_number']}").pack(pady=5)
        ttk.Label(main_frame, text=f"Cashier: {self.cashier_name}").pack(pady=5)
        
        # Separator
        ttk.Separator(main_frame, orient="horizontal").pack(fill="x", pady=10)
        
        # Items
        items_frame = ttk.Frame(main_frame)
        items_frame.pack(fill="x", pady=10)
        
        ttk.Label(items_frame, text="Item", width=20, font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w")
        ttk.Label(items_frame, text="Price", width=8, font=("Arial", 10, "bold")).grid(row=0, column=1)
        ttk.Label(items_frame, text="Qty", width=5, font=("Arial", 10, "bold")).grid(row=0, column=2)
        ttk.Label(items_frame, text="Total", width=10, font=("Arial", 10, "bold")).grid(row=0, column=3)
        
        # Add items
        for i, item in enumerate(bill_info["items"]):
            ttk.Label(items_frame, text=item["name"], width=20).grid(row=i+1, column=0, sticky="w")
            ttk.Label(items_frame, text=f"₹{item['price']:.2f}", width=8).grid(row=i+1, column=1)
            ttk.Label(items_frame, text=str(item["quantity"]), width=5).grid(row=i+1, column=2)
            ttk.Label(items_frame, text=f"₹{item['price'] * item['quantity']:.2f}", width=10).grid(row=i+1, column=3)
        
        # Separator
        ttk.Separator(main_frame, orient="horizontal").pack(fill="x", pady=10)
        
        # Totals
        totals_frame = ttk.Frame(main_frame)
        totals_frame.pack(fill="x", pady=10)
        
        # Subtotal
        ttk.Label(totals_frame, text="Subtotal:").grid(row=0, column=0, sticky="w", padx=5)
        ttk.Label(totals_frame, text=f"₹{bill_info['bill_data']['subtotal']:.2f}").grid(row=0, column=1, sticky="e")
        
        # Discount
        ttk.Label(totals_frame, text="Discount:").grid(row=1, column=0, sticky="w", padx=5)
        ttk.Label(totals_frame, text=f"₹{bill_info['bill_data']['discount']:.2f}").grid(row=1, column=1, sticky="e")
        
        # Total
        ttk.Label(totals_frame, text="Total:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w", padx=5)
        ttk.Label(totals_frame, text=f"₹{bill_info['bill_data']['total']:.2f}", 
                 font=("Arial", 10, "bold")).grid(row=2, column=1, sticky="e")
        
        # Close button
        ttk.Button(main_frame, text="Close", command=bill_window.destroy).pack(pady=10)

    def logout(self):
        """Logout and return to login screen"""
        if self.controller.get_cart():
            confirm = messagebox.askyesno("Confirm Logout", 
                                        "You have items in your cart. Are you sure you want to logout?")
            if not confirm:
                return
                
        self.master.destroy()
        self.login_window.deiconify()  # Show the login window again

    def on_close(self):
        """Handle window close event"""
        self.logout() 