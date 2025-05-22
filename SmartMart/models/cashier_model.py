import os

class CashierModel:
    def __init__(self, file_path="data/cashiers.txt"):
        self.file_path = file_path
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.full_path = os.path.join(self.base_dir, file_path)
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(self.full_path), exist_ok=True)
        # Create cashiers.txt if it doesn't exist
        if not os.path.exists(self.full_path):
            with open(self.full_path, "w") as file:
                # Default cashiers: username:password:name
                file.write("cashier1:pass123:John Doe\n")
                file.write("cashier2:pass456:Jane Smith\n")
                file.write("cashier3:pass789:Mike Johnson\n")

    def get_all_cashiers(self):
        """Get all cashiers from file"""
        try:
            cashiers = []
            with open(self.full_path, "r") as file:
                for line in file:
                    line = line.strip()
                    if line:
                        username, password, name = line.split(":", 2)
                        cashiers.append({"username": username, "password": password, "name": name})
            return cashiers
        except Exception as e:
            print(f"Error getting cashiers: {e}")
            return []

    def verify_cashier(self, username, password):
        """Verify cashier credentials"""
        try:
            with open(self.full_path, "r") as file:
                for line in file:
                    line = line.strip()
                    if line:
                        parts = line.split(":", 2)
                        if len(parts) >= 2:
                            stored_username, stored_password = parts[0], parts[1]
                            if username == stored_username and password == stored_password:
                                return True, parts[2] if len(parts) > 2 else ""
            return False, ""
        except Exception as e:
            print(f"Error verifying cashier: {e}")
            return False, ""

    def add_cashier(self, username, password, name):
        """Add a new cashier"""
        try:
            # Check if username already exists
            cashiers = self.get_all_cashiers()
            for cashier in cashiers:
                if cashier["username"] == username:
                    return False  # Username already exists

            # Add new cashier
            with open(self.full_path, "a") as file:
                file.write(f"{username}:{password}:{name}\n")
            return True
        except Exception as e:
            print(f"Error adding cashier: {e}")
            return False

    def update_cashier(self, username, password=None, name=None):
        """Update an existing cashier"""
        try:
            cashiers = self.get_all_cashiers()
            found = False
            updated_content = ""

            for cashier in cashiers:
                if cashier["username"] == username:
                    found = True
                    # Update password and/or name if provided
                    updated_password = password if password else cashier["password"]
                    updated_name = name if name else cashier["name"]
                    updated_content += f"{username}:{updated_password}:{updated_name}\n"
                else:
                    updated_content += f"{cashier['username']}:{cashier['password']}:{cashier['name']}\n"

            if found:
                with open(self.full_path, "w") as file:
                    file.write(updated_content)
                return True
            return False  # Cashier not found
        except Exception as e:
            print(f"Error updating cashier: {e}")
            return False

    def delete_cashier(self, username):
        """Delete a cashier by username"""
        try:
            cashiers = self.get_all_cashiers()
            found = False
            updated_content = ""

            for cashier in cashiers:
                if cashier["username"] == username:
                    found = True
                else:
                    updated_content += f"{cashier['username']}:{cashier['password']}:{cashier['name']}\n"

            if found:
                with open(self.full_path, "w") as file:
                    file.write(updated_content)
                return True
            return False  # Cashier not found
        except Exception as e:
            print(f"Error deleting cashier: {e}")
            return False 