import random  
import time  

class OrderProcessing:
    """
    A class to handle order creation, payment processing, and order status retrieval.
    This simulates an order processing system where payments can either succeed or fail.
    """

    def __init__(self):
        self.orders = {}  # Dictionary to hold all orders.

    def create_order(self, order_id, amount):
        """
        Creates a new order with a specified order ID and amount.

        Args:
            order_id (str): A unique identifier for the order.
            amount (float): The amount to be paid for the order.

        Returns:
            dict: The newly created order containing amount and initial status.

        Raises:
            ValueError: If the order ID already exists or if the amount is not positive.
        """
        if order_id in self.orders:
            raise ValueError("Order ID already exists")

        if amount <= 0:
            raise ValueError("Order amount must be positive")
        
        self.orders[order_id] = {"amount": amount, "status": "pending"}
        return self.orders[order_id]

    def process_payment(self, order_id):
        """
        Simulates payment processing for an order.

        Args:
            order_id (str): The unique identifier for the order.

        Returns:
            bool: True if payment succeeds, False if it fails.

        Raises:
            ValueError: If the order ID is not found in the system.
        """
        if order_id not in self.orders:
            raise ValueError("Order not found")

        time.sleep(1)  #

        # Randomly determine if the payment succeeds or fails (50% chance each).
        if random.choice([True, False]):  # Randomly selects True (success) or False (failure).
            self.orders[order_id]["status"] = "paid"  # Update order status to 'paid' on success.
            return True  # Indicate successful payment.
        else:
            self.orders[order_id]["status"] = "failed"  # Update order status to 'failed' on failure.
            return False  # Indicate failed payment.

    def get_order_status(self, order_id):
        """
        Retrieves the current status of an order.

        Args:
            order_id (str): The unique identifier for the order.

        Returns:
            str: The status of the order. If the order is not found, returns 'not found'.
        """
        return self.orders.get(order_id, {}).get("status", "not found")
