import os
import datetime

class BillingModel:
    def __init__(self, file_path="data/bills.txt"):
        self.file_path = file_path
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.full_path = os.path.join(self.base_dir, file_path)
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(self.full_path), exist_ok=True)
        # Create bills.txt if it doesn't exist
        if not os.path.exists(self.full_path):
            with open(self.full_path, "w") as file:
                pass  # Create empty file

    def save_bill(self, bill_amount, payment_method):
        """Save a bill to the bills file"""
        try:
            # Get the next bill number
            bill_number = self.get_next_bill_number()
            
            # Format bill details
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            bill_details = f"Bill {bill_number}: {bill_amount} | {payment_method} | {timestamp}\n"
            
            # Save to file
            with open(self.full_path, "a") as file:
                file.write(bill_details)
                
            return bill_number
        except Exception as e:
            print(f"Error saving bill: {e}")
            return None

    def get_next_bill_number(self):
        """Get the next bill number by checking the last bill"""
        try:
            # If file doesn't exist or is empty, start with bill number 1
            if not os.path.exists(self.full_path) or os.path.getsize(self.full_path) == 0:
                return 1
                
            # Read the file and find the highest bill number
            highest_bill_number = 0
            with open(self.full_path, "r") as file:
                for line in file:
                    if line.startswith("Bill "):
                        # Extract bill number: "Bill X: amount"
                        parts = line.split(":", 1)
                        if len(parts) > 0:
                            try:
                                bill_num = int(parts[0].replace("Bill ", "").strip())
                                highest_bill_number = max(highest_bill_number, bill_num)
                            except ValueError:
                                continue
            
            # Return next bill number
            return highest_bill_number + 1
        except Exception as e:
            print(f"Error getting next bill number: {e}")
            return 1  # Default to 1 in case of error

    def get_all_bills(self):
        """Get all saved bills"""
        try:
            bills = []
            if not os.path.exists(self.full_path):
                return bills
                
            with open(self.full_path, "r") as file:
                for line in file:
                    line = line.strip()
                    if line:
                        bills.append(line)
            return bills
        except Exception as e:
            print(f"Error getting bills: {e}")
            return []

    def calculate_total(self, items, payment_method="Cash"):
        """Calculate the total bill amount with discount if applicable"""
        try:
            subtotal = sum(item["price"] * item["quantity"] for item in items)
            
            # Apply 10% discount for card payments
            if payment_method.lower() == "card":
                discount = subtotal * 0.1
                total = subtotal - discount
            else:
                discount = 0
                total = subtotal
                
            return {
                "subtotal": subtotal,
                "discount": discount,
                "total": total
            }
        except Exception as e:
            print(f"Error calculating total: {e}")
            return {
                "subtotal": 0,
                "discount": 0,
                "total": 0
            } 