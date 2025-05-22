import os

class ProductModel:
    def __init__(self, file_path="data/products.txt"):
        self.file_path = file_path
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.full_path = os.path.join(self.base_dir, file_path)
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(self.full_path), exist_ok=True)
        # Create products.txt with default categories and products if it doesn't exist
        if not os.path.exists(self.full_path):
            self._create_default_products()

    def _create_default_products(self):
        """Create default categories and products"""
        default_products = {
            "Groceries": [
                {"name": "Rice", "price": 120, "stock": 50},
                {"name": "Wheat Flour", "price": 80, "stock": 40},
                {"name": "Sugar", "price": 60, "stock": 30},
                {"name": "Salt", "price": 20, "stock": 100},
                {"name": "Cooking Oil", "price": 220, "stock": 25},
                {"name": "Milk", "price": 90, "stock": 20},
                {"name": "Eggs", "price": 120, "stock": 50},
                {"name": "Bread", "price": 40, "stock": 30},
                {"name": "Lentils", "price": 75, "stock": 45},
                {"name": "Tea Leaves", "price": 150, "stock": 15}
            ],
            "Electronics": [
                {"name": "Headphones", "price": 1500, "stock": 10},
                {"name": "Phone Charger", "price": 500, "stock": 20},
                {"name": "USB Drive", "price": 800, "stock": 15},
                {"name": "Mouse", "price": 600, "stock": 12},
                {"name": "Keyboard", "price": 1200, "stock": 8},
                {"name": "Power Bank", "price": 2000, "stock": 10},
                {"name": "Memory Card", "price": 700, "stock": 25},
                {"name": "Webcam", "price": 1800, "stock": 5},
                {"name": "Speakers", "price": 1600, "stock": 7},
                {"name": "HDMI Cable", "price": 300, "stock": 30}
            ],
            "Clothing": [
                {"name": "T-Shirt", "price": 500, "stock": 30},
                {"name": "Jeans", "price": 1200, "stock": 20},
                {"name": "Socks", "price": 150, "stock": 50},
                {"name": "Cap", "price": 250, "stock": 25},
                {"name": "Jacket", "price": 2000, "stock": 10},
                {"name": "Sweater", "price": 800, "stock": 15},
                {"name": "Formal Shirt", "price": 900, "stock": 12},
                {"name": "Track Pants", "price": 700, "stock": 18},
                {"name": "Shorts", "price": 400, "stock": 22},
                {"name": "Scarf", "price": 300, "stock": 20}
            ],
            "Household": [
                {"name": "Soap", "price": 40, "stock": 100},
                {"name": "Detergent", "price": 150, "stock": 50},
                {"name": "Toothpaste", "price": 90, "stock": 60},
                {"name": "Shampoo", "price": 180, "stock": 40},
                {"name": "Toilet Paper", "price": 120, "stock": 80},
                {"name": "Dish Soap", "price": 70, "stock": 45},
                {"name": "Air Freshener", "price": 110, "stock": 30},
                {"name": "Light Bulbs", "price": 60, "stock": 50},
                {"name": "Tissues", "price": 50, "stock": 70},
                {"name": "Hand Sanitizer", "price": 85, "stock": 55}
            ],
            "Stationery": [
                {"name": "Notebook", "price": 50, "stock": 100},
                {"name": "Pen", "price": 20, "stock": 200},
                {"name": "Pencil", "price": 10, "stock": 150},
                {"name": "Eraser", "price": 15, "stock": 100},
                {"name": "Ruler", "price": 25, "stock": 80},
                {"name": "Glue", "price": 30, "stock": 60},
                {"name": "Scissors", "price": 45, "stock": 40},
                {"name": "Stapler", "price": 75, "stock": 30},
                {"name": "Tape", "price": 35, "stock": 70},
                {"name": "File Folder", "price": 40, "stock": 50}
            ]
        }

        with open(self.full_path, "w") as file:
            for category, products in default_products.items():
                for product in products:
                    # Format: category:name:price:stock
                    file.write(f"{category}:{product['name']}:{product['price']}:{product['stock']}\n")

    def get_all_categories(self):
        """Get all unique categories"""
        try:
            categories = set()
            with open(self.full_path, "r") as file:
                for line in file:
                    line = line.strip()
                    if line:
                        parts = line.split(":", 1)
                        if parts:
                            categories.add(parts[0])
            return sorted(list(categories))
        except Exception as e:
            print(f"Error getting categories: {e}")
            return []

    def get_products_by_category(self, category):
        """Get all products for a specific category"""
        try:
            products = []
            with open(self.full_path, "r") as file:
                for line in file:
                    line = line.strip()
                    if line:
                        parts = line.split(":")
                        if len(parts) >= 4 and parts[0] == category:
                            products.append({
                                "category": parts[0],
                                "name": parts[1],
                                "price": float(parts[2]),
                                "stock": int(parts[3])
                            })
            return products
        except Exception as e:
            print(f"Error getting products by category: {e}")
            return []

    def get_all_products(self):
        """Get all products from all categories"""
        try:
            products = []
            with open(self.full_path, "r") as file:
                for line in file:
                    line = line.strip()
                    if line:
                        parts = line.split(":")
                        if len(parts) >= 4:
                            products.append({
                                "category": parts[0],
                                "name": parts[1],
                                "price": float(parts[2]),
                                "stock": int(parts[3])
                            })
            return products
        except Exception as e:
            print(f"Error getting all products: {e}")
            return []

    def add_product(self, category, name, price, stock):
        """Add a new product"""
        try:
            # Check if product already exists
            products = self.get_all_products()
            for product in products:
                if product["category"] == category and product["name"] == name:
                    return False  # Product already exists

            # Add new product
            with open(self.full_path, "a") as file:
                file.write(f"{category}:{name}:{price}:{stock}\n")
            return True
        except Exception as e:
            print(f"Error adding product: {e}")
            return False

    def update_product(self, category, name, price=None, stock=None):
        """Update an existing product's price or stock"""
        try:
            products = self.get_all_products()
            found = False
            updated_content = ""

            for product in products:
                if product["category"] == category and product["name"] == name:
                    found = True
                    # Update price and/or stock if provided
                    updated_price = price if price is not None else product["price"]
                    updated_stock = stock if stock is not None else product["stock"]
                    updated_content += f"{category}:{name}:{updated_price}:{updated_stock}\n"
                else:
                    updated_content += f"{product['category']}:{product['name']}:{product['price']}:{product['stock']}\n"

            if found:
                with open(self.full_path, "w") as file:
                    file.write(updated_content)
                return True
            return False  # Product not found
        except Exception as e:
            print(f"Error updating product: {e}")
            return False

    def delete_product(self, category, name):
        """Delete a product"""
        try:
            products = self.get_all_products()
            found = False
            updated_content = ""

            for product in products:
                if product["category"] == category and product["name"] == name:
                    found = True
                else:
                    updated_content += f"{product['category']}:{product['name']}:{product['price']}:{product['stock']}\n"

            if found:
                with open(self.full_path, "w") as file:
                    file.write(updated_content)
                return True
            return False  # Product not found
        except Exception as e:
            print(f"Error deleting product: {e}")
            return False

    def decrease_stock(self, category, name, quantity):
        """Decrease stock of a product when purchased"""
        try:
            products = self.get_all_products()
            found = False
            updated_content = ""

            for product in products:
                if product["category"] == category and product["name"] == name:
                    found = True
                    if product["stock"] >= quantity:
                        updated_stock = product["stock"] - quantity
                        updated_content += f"{category}:{name}:{product['price']}:{updated_stock}\n"
                    else:
                        # Not enough stock
                        return False
                else:
                    updated_content += f"{product['category']}:{product['name']}:{product['price']}:{product['stock']}\n"

            if found:
                with open(self.full_path, "w") as file:
                    file.write(updated_content)
                return True
            return False  # Product not found
        except Exception as e:
            print(f"Error decreasing stock: {e}")
            return False 