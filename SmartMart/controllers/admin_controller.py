import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.cashier_model import CashierModel
from models.product_model import ProductModel

class AdminController:
    def __init__(self):
        self.cashier_model = CashierModel()
        self.product_model = ProductModel()
    
    # Cashier management methods
    def get_all_cashiers(self):
        """Get all cashiers for display"""
        return self.cashier_model.get_all_cashiers()
    
    def add_cashier(self, username, password, name):
        """Add a new cashier"""
        if not username or not password or not name:
            return False, "All fields are required"
        
        # Validate input
        if len(username) < 3:
            return False, "Username must be at least 3 characters"
        if len(password) < 6:
            return False, "Password must be at least 6 characters"
        
        # Add cashier
        success = self.cashier_model.add_cashier(username, password, name)
        if success:
            return True, f"Cashier '{username}' added successfully"
        else:
            return False, f"Cashier with username '{username}' already exists"
    
    def update_cashier(self, username, password=None, name=None):
        """Update cashier details"""
        if not username:
            return False, "Username is required"
        
        # Validate input if provided
        if password and len(password) < 6:
            return False, "Password must be at least 6 characters"
        
        # Update cashier
        success = self.cashier_model.update_cashier(username, password, name)
        if success:
            return True, f"Cashier '{username}' updated successfully"
        else:
            return False, f"Cashier with username '{username}' not found"
    
    def delete_cashier(self, username):
        """Delete a cashier"""
        if not username:
            return False, "Username is required"
        
        # Delete cashier
        success = self.cashier_model.delete_cashier(username)
        if success:
            return True, f"Cashier '{username}' deleted successfully"
        else:
            return False, f"Cashier with username '{username}' not found"
    
    # Product management methods
    def get_all_categories(self):
        """Get all product categories"""
        return self.product_model.get_all_categories()
    
    def get_products_by_category(self, category):
        """Get all products in a category"""
        if not category:
            return []
        return self.product_model.get_products_by_category(category)
    
    def add_product(self, category, name, price, stock):
        """Add a new product"""
        if not category or not name:
            return False, "Category and name are required"
        
        # Validate input
        try:
            price = float(price)
            if price <= 0:
                return False, "Price must be greater than zero"
        except ValueError:
            return False, "Price must be a valid number"
            
        try:
            stock = int(stock)
            if stock < 0:
                return False, "Stock cannot be negative"
        except ValueError:
            return False, "Stock must be a valid integer"
        
        # Add product
        success = self.product_model.add_product(category, name, price, stock)
        if success:
            return True, f"Product '{name}' added successfully"
        else:
            return False, f"Product '{name}' already exists in category '{category}'"
    
    def update_product(self, category, name, price=None, stock=None):
        """Update an existing product"""
        if not category or not name:
            return False, "Category and name are required"
        
        # Validate input if provided
        if price is not None:
            try:
                price = float(price)
                if price <= 0:
                    return False, "Price must be greater than zero"
            except ValueError:
                return False, "Price must be a valid number"
                
        if stock is not None:
            try:
                stock = int(stock)
                if stock < 0:
                    return False, "Stock cannot be negative"
            except ValueError:
                return False, "Stock must be a valid integer"
        
        # Update product
        success = self.product_model.update_product(category, name, price, stock)
        if success:
            return True, f"Product '{name}' updated successfully"
        else:
            return False, f"Product '{name}' not found in category '{category}'"
    
    def delete_product(self, category, name):
        """Delete a product"""
        if not category or not name:
            return False, "Category and name are required"
        
        # Delete product
        success = self.product_model.delete_product(category, name)
        if success:
            return True, f"Product '{name}' deleted successfully"
        else:
            return False, f"Product '{name}' not found in category '{category}'" 