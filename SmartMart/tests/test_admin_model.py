import sys
import os
import pytest
import tempfile
import shutil

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.admin_model import AdminModel

class TestAdminModel:
    """Test class for AdminModel"""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for test files"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        # Clean up after test
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def admin_model(self, temp_dir):
        """Create an AdminModel instance with a temporary file"""
        test_file = os.path.join(temp_dir, "admin.txt")
        model = AdminModel(test_file)
        return model
    
    def test_init_creates_file(self, admin_model, temp_dir):
        """Test that __init__ creates the admin file if it doesn't exist"""
        test_file = os.path.join(temp_dir, "admin.txt")
        assert os.path.exists(test_file)
        
        # Check default admin credentials
        with open(test_file, "r") as file:
            content = file.read().strip()
            assert content == "admin:admin123"
    
    def test_verify_admin_valid_credentials(self, admin_model):
        """Test that verify_admin returns True for valid credentials"""
        result = admin_model.verify_admin("admin", "admin123")
        assert result is True
    
    def test_verify_admin_invalid_username(self, admin_model):
        """Test that verify_admin returns False for invalid username"""
        result = admin_model.verify_admin("invalid", "admin123")
        assert result is False
    
    def test_verify_admin_invalid_password(self, admin_model):
        """Test that verify_admin returns False for invalid password"""
        result = admin_model.verify_admin("admin", "invalid")
        assert result is False
    
    def test_verify_admin_empty_credentials(self, admin_model):
        """Test that verify_admin returns False for empty credentials"""
        result = admin_model.verify_admin("", "")
        assert result is False 