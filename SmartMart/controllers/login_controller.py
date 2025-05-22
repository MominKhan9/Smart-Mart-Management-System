import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.admin_model import AdminModel
from models.cashier_model import CashierModel

class LoginController:
    def __init__(self):
        self.admin_model = AdminModel()
        self.cashier_model = CashierModel()
        
    def login_admin(self, username, password):
        """Validate admin login credentials"""
        if not username or not password:
            return False, "Username and password cannot be empty"
        
        # Verify against admin.txt
        if self.admin_model.verify_admin(username, password):
            return True, "Admin login successful"
        else:
            return False, "Invalid admin credentials"
    
    def login_cashier(self, username, password):
        """Validate cashier login credentials"""
        if not username or not password:
            return False, "Username and password cannot be empty", ""
        
        # Verify against cashiers.txt
        success, cashier_name = self.cashier_model.verify_cashier(username, password)
        if success:
            return True, "Cashier login successful", cashier_name
        else:
            return False, "Invalid cashier credentials", "" 