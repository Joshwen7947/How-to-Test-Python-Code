import pytest  
from unittest.mock import patch  
import sys  
import os  

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import OrderProcessing


@pytest.fixture
def order_system():
    """
    Pytest fixture to create a new instance of OrderProcessing.
    This ensures a fresh OrderProcessing instance for each test, 
    preventing data contamination between test cases.
    """
    return OrderProcessing()


class TestOrderProcessing:
    """Test class for OrderProcessing - Contains all unit tests."""

    def test_create_order(self, order_system):
        """
        Test case for creating a valid order.
        Ensures the order is created with the correct amount and status.
        """
        order = order_system.create_order(101, 50)  # Create order with ID 101 and amount 50
        assert order["amount"] == 50  # Ensure the amount is stored correctly
        assert order["status"] == "pending"  # Ensure the initial status is "pending"

    @pytest.mark.parametrize("order_id, amount, expected_exception", [
        (102, 100, None),        # Valid order, no exception expected
        (102, -50, ValueError),  # Negative amount should raise ValueError
        (102, 0, ValueError),    # Zero amount should also raise ValueError
    ])
    def test_create_order_scenarios(self, order_system, order_id, amount, expected_exception):
        """
        Test multiple scenarios for order creation using parametrization.
        - If an exception is expected, assert that it is raised.
        - Otherwise, verify that the order is created successfully.
        """
        if expected_exception:
            with pytest.raises(expected_exception):  # Expect ValueError for invalid amounts
                order_system.create_order(order_id, amount)
        else:
            order = order_system.create_order(order_id, amount)  # Create a valid order
            assert order["amount"] == amount  # Verify amount is correctly stored

    def test_get_order_status(self, order_system):
        """
        Test retrieving the status of an order.
        - Ensures the status is "pending" right after order creation.
        - Ensures a non-existent order returns "not found".
        """
        order_system.create_order(103, 75)  # Create order with ID 103
        assert order_system.get_order_status(103) == "pending"  # Newly created orders should be pending
        assert order_system.get_order_status(999) == "not found"  # Non-existent order should return "not found"

    @pytest.mark.skip(reason="Payment processing is slow, skipping for now")
    def test_process_payment(self, order_system):
        """
        Test the payment processing function.
        - Skipped due to the 1-second delay in processing.
        - Ensures that the function returns either True or False (since payment is randomized).
        """
        order_system.create_order(104, 200)  # Create an order
        assert order_system.process_payment(104) in [True, False]  # Payment can be successful or failed

    @pytest.mark.slow  # Marked as a slow test, useful for running only when needed
    def test_slow_payment_processing(self, order_system):
        """
        Test the actual payment processing flow.
        - Verifies that payment status changes to either "paid" or "failed".
        """
        order_system.create_order(105, 150)  # Create an order
        result = order_system.process_payment(105)  # Process payment
        assert result in [True, False]  # Ensure result is either True or False
        assert order_system.get_order_status(105) in ["paid", "failed"]  # Order should have updated status

    def test_mocked_payment_processing(self, order_system):
        """
        Test payment processing with a mocked random.choice function.
        - Mocks the payment outcome to always return True (successful payment).
        - Ensures that the order status is updated correctly.
        """
        order_system.create_order(106, 300)  # Create an order

        # Patch the random.choice function to always return True (force successful payment)
        with patch("main.random.choice", return_value=True):  
            assert order_system.process_payment(106) is True  # Payment should succeed
            assert order_system.get_order_status(106) == "paid"  # Order status should be updated to "paid"
