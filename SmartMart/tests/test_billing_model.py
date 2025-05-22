import sys
import os
import pytest
import tempfile
import shutil

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.billing_model import BillingModel

class TestBillingModel:
    """Test class for BillingModel"""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for test files"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        # Clean up after test
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def billing_model(self, temp_dir):
        """Create a BillingModel instance with a temporary file"""
        test_file = os.path.join(temp_dir, "bills.txt")
        model = BillingModel(test_file)
        return model
    
    def test_init_creates_file(self, billing_model, temp_dir):
        """Test that __init__ creates the bills file if it doesn't exist"""
        test_file = os.path.join(temp_dir, "bills.txt")
        assert os.path.exists(test_file)
    
    def test_get_next_bill_number_empty_file(self, billing_model):
        """Test that get_next_bill_number returns 1 for empty file"""
        result = billing_model.get_next_bill_number()
        assert result == 1
    
    def test_save_bill(self, billing_model):
        """Test that save_bill saves a bill correctly"""
        # Save a bill
        bill_number = billing_model.save_bill(100, "Cash")
        assert bill_number == 1
        
        # Check that the next bill number is incremented
        next_bill_number = billing_model.get_next_bill_number()
        assert next_bill_number == 2
        
        # Check that the bill was saved correctly
        bills = billing_model.get_all_bills()
        assert len(bills) == 1
        assert "Bill 1: 100" in bills[0]
        assert "Cash" in bills[0]
    
    def test_get_all_bills(self, billing_model):
        """Test that get_all_bills returns all bills"""
        # Save multiple bills
        billing_model.save_bill(100, "Cash")
        billing_model.save_bill(200, "Card")
        
        # Get all bills
        bills = billing_model.get_all_bills()
        
        # Check that both bills were retrieved
        assert len(bills) == 2
        assert any("Bill 1: 100" in bill for bill in bills)
        assert any("Bill 2: 200" in bill for bill in bills)
    
    def test_calculate_total_cash(self, billing_model):
        """Test calculating total for cash payment (no discount)"""
        items = [
            {"price": 100, "quantity": 2},
            {"price": 50, "quantity": 1}
        ]
        
        result = billing_model.calculate_total(items, "Cash")
        
        # Expected values
        expected_subtotal = 250  # (100 * 2) + (50 * 1)
        expected_discount = 0    # No discount for cash
        expected_total = 250     # No discount applied
        
        assert result["subtotal"] == expected_subtotal
        assert result["discount"] == expected_discount
        assert result["total"] == expected_total
    
    def test_calculate_total_card(self, billing_model):
        """Test calculating total for card payment (10% discount)"""
        items = [
            {"price": 100, "quantity": 2},
            {"price": 50, "quantity": 1}
        ]
        
        result = billing_model.calculate_total(items, "Card")
        
        # Expected values
        expected_subtotal = 250    # (100 * 2) + (50 * 1)
        expected_discount = 25     # 10% of 250
        expected_total = 225       # 250 - 25
        
        assert result["subtotal"] == expected_subtotal
        assert result["discount"] == expected_discount
        assert result["total"] == expected_total
    
    def test_calculate_total_empty_cart(self, billing_model):
        """Test calculating total for empty cart"""
        items = []
        
        result = billing_model.calculate_total(items, "Cash")
        
        assert result["subtotal"] == 0
        assert result["discount"] == 0
        assert result["total"] == 0 