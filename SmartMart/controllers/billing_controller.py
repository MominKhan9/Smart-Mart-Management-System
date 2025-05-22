import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.billing_model import BillingModel
from models.product_model import ProductModel

class BillingController:
    def __init__(self):
        self.billing_model = BillingModel()
        self.product_model = ProductModel()
        self.cart = []  # List to store items added to cart
    
    def get_all_categories(self):
        """Get all product categories"""
        return self.product_model.get_all_categories()
    
    def get_products_by_category(self, category):
        """Get all products in a category"""
        if not category:
            return []
        return self.product_model.get_products_by_category(category)
    
    def add_to_cart(self, category, product_name, price, quantity=1):
        """Add an item to the cart"""
        if not category or not product_name or price <= 0 or quantity <= 0:
            return False, "Invalid product details"
        
        # Check product stock
        products = self.product_model.get_products_by_category(category)
        product = next((p for p in products if p["name"] == product_name), None)
        
        if not product:
            return False, f"Product '{product_name}' not found"
            
        if product["stock"] < quantity:
            return False, f"Not enough stock for '{product_name}'. Available: {product['stock']}"
        
        # Check if product already in cart
        for item in self.cart:
            if item["category"] == category and item["name"] == product_name:
                if item["quantity"] + quantity > product["stock"]:
                    return False, f"Not enough stock for '{product_name}'. Available: {product['stock']}"
                # Update quantity if already in cart
                item["quantity"] += quantity
                return True, f"Updated quantity of '{product_name}' in cart"
        
        # Add new item to cart
        self.cart.append({
            "category": category,
            "name": product_name,
            "price": price,
            "quantity": quantity
        })
        
        return True, f"Added '{product_name}' to cart"
    
    def update_cart_item(self, index, quantity):
        """Update quantity of an item in the cart"""
        if index < 0 or index >= len(self.cart) or quantity <= 0:
            return False, "Invalid item index or quantity"
        
        item = self.cart[index]
        
        # Check product stock
        products = self.product_model.get_products_by_category(item["category"])
        product = next((p for p in products if p["name"] == item["name"]), None)
        
        if not product:
            return False, f"Product '{item['name']}' not found"
            
        if product["stock"] < quantity:
            return False, f"Not enough stock for '{item['name']}'. Available: {product['stock']}"
        
        # Update quantity
        self.cart[index]["quantity"] = quantity
        
        return True, f"Updated quantity of '{item['name']}' in cart"
    
    def remove_from_cart(self, index):
        """Remove an item from the cart"""
        if index < 0 or index >= len(self.cart):
            return False, "Invalid item index"
        
        item_name = self.cart[index]["name"]
        del self.cart[index]
        
        return True, f"Removed '{item_name}' from cart"
    
    def get_cart(self):
        """Get all items in the cart"""
        return self.cart
    
    def clear_cart(self):
        """Clear all items from the cart"""
        self.cart = []
        return True, "Cart cleared"
    
    def calculate_bill(self, payment_method="Cash"):
        """Calculate the bill total with discount if applicable"""
        return self.billing_model.calculate_total(self.cart, payment_method)
    
    def checkout(self, payment_method="Cash"):
        """Process the checkout and save the bill"""
        if not self.cart:
            return False, "Cart is empty", None
        
        # Calculate bill total
        bill_data = self.calculate_bill(payment_method)
        
        # Save bill to file
        bill_number = self.billing_model.save_bill(bill_data["total"], payment_method)
        
        if bill_number is None:
            return False, "Failed to save bill", None
        
        # Update product stock
        for item in self.cart:
            self.product_model.decrease_stock(
                item["category"],
                item["name"],
                item["quantity"]
            )
        
        # Clear cart after successful checkout
        old_cart = self.cart.copy()
        self.clear_cart()
        
        return True, f"Bill #{bill_number} created successfully", {
            "bill_number": bill_number,
            "items": old_cart,
            "bill_data": bill_data
        } 