import io
import unittest
from unittest.mock import patch
from banking_algorithm import deposit, withdrawal, check_balance, transfer

class TestBankingFunctions(unittest.TestCase):

    def setUp(self):
        # Set up any common resources or configurations needed for the tests
        pass

    def tearDown(self):
        # Clean up any resources after the tests
        pass

    def test_deposit(self):
        account_balances = {"12345": 1000}
        with patch("builtins.input", side_effect=["500"]):
            deposit(account_balances, "12345")
        self.assertEqual(account_balances["12345"], 1500)

    def test_deposit_negative(self):
        account_balances = {"12345": 1000}
        with patch("builtins.input", side_effect=["-500"]):
            deposit(account_balances, "12345")
        self.assertEqual(account_balances["12345"], 1000)

    def test_withdrawal(self):
        account_balances = {"12345": 100000}
        with patch("builtins.input", side_effect=["50000"]):
            withdrawal(account_balances, "12345")
        self.assertEqual(account_balances["12345"], 50000)

    def test_withdrawal_over_value(self):
        account_balances = {"12345": 100000}
        with patch("builtins.input", side_effect=["500000"]):
            withdrawal(account_balances, "12345")
        self.assertEqual(account_balances["12345"], 100000)

    def test_withdrawal_negative_value(self):
        account_balances = {"12345": 100000}
        with patch("builtins.input", side_effect=["-50000"]):
            withdrawal(account_balances, "12345")
        self.assertEqual(account_balances["12345"], 100000)


    def test_check_balance(self):
        account_balances = {"12345": 2500}
        with patch("builtins.input", side_effect=["12345"]):
            with unittest.mock.patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                check_balance(account_balances, "12345")
                output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "Your account balance is: $2500.00")

    def test_transfer(self):
        account_balances = {"sender": 500000, "receiver": 200000}
        account_credentials = {"sender": {"username": "sender_user"}, "receiver": {"username": "receiver_user"}}
        with patch("builtins.input", side_effect=["receiver", "1500"]):
            transfer(account_balances, account_credentials, "sender")
        self.assertEqual(account_balances["sender"], 2498)  # 5000 - 1500 - 2500(admin fee)
        self.assertEqual(account_balances["receiver"], 3500)  # 2000 + 1500

if __name__ == '__main__':
    unittest.main()
