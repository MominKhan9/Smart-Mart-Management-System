import os

class AdminModel:
    def __init__(self, file_path="data/admin.txt"):
        self.file_path = file_path
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.full_path = os.path.join(self.base_dir, file_path)
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(self.full_path), exist_ok=True)
        # Create admin.txt with default credentials if it doesn't exist
        if not os.path.exists(self.full_path):
            with open(self.full_path, "w") as file:
                # Default admin credentials: username:password
                file.write("admin:admin123")

    def verify_admin(self, username, password):
        """Verify admin credentials"""
        try:
            with open(self.full_path, "r") as file:
                credentials = file.read().strip()
                stored_username, stored_password = credentials.split(":")
                return username == stored_username and password == stored_password
        except Exception as e:
            print(f"Error verifying admin: {e}")
            return False 