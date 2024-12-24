import datetime
import unittest
from unittest.mock import MagicMock


class TestLineMan(unittest.TestCase):

    def setUp(self):
        self.coupon = MagicMock()
        self.coupon.title = '50% discount coupon'
        self.coupon.has_used = False

        self.customer = MagicMock()
        self.customer.coupon = self.coupon
        self.customer.has_ordered = False

        self.coupon_customer = MagicMock()
        self.coupon_customer.customer = self.customer
        self.coupon_customer.coupon = self.coupon
        self.coupon_customer.created_at = datetime.date.today()
        self.coupon_customer.is_active = True

        self.coupon.set_status.side_effect = lambda: (
            setattr(self.coupon, 'show', self.coupon.title)
            if not self.customer.has_ordered and not self.customer.coupon.has_used and self.coupon_customer.is_active
            else setattr(self.coupon, 'show', None)
        )

        self.coupon_customer.set_expired.side_effect = lambda: (
            setattr(self.coupon_customer, 'is_active', True)
            if (self.coupon_customer.created_at - datetime.date.today()).days < 7
            else setattr(self.coupon_customer, 'is_active', False)
        )

    def test_new_customer(self):
        # New customer
        self.customer.has_ordered = False
        self.customer.coupon.set_status()
        self.assertEqual(self.customer.coupon.show, self.coupon.title)

        # Old customer
        self.customer.has_ordered = True
        self.customer.coupon.set_status()
        self.assertEqual(self.customer.coupon.show, None)

    def test_used_coupon(self):
        # Not used yet
        self.customer.coupon.has_used = False
        self.customer.coupon.set_status()
        self.assertEqual(self.customer.coupon.show, self.coupon.title)

        # Already used
        self.customer.coupon.has_used = True
        self.customer.coupon.set_status()
        self.assertEqual(self.customer.coupon.show, None)

    def test_expired_coupon(self):
        self.customer.coupon.has_used = False

        # Not over 7 days
        self.coupon_customer.created_at = datetime.date.today()
        self.coupon_customer.set_expired()
        self.assertEqual(self.coupon_customer.is_active, True)

        self.customer.coupon.set_status()
        self.assertEqual(self.customer.coupon.show, self.coupon.title)

        # Over 7 days
        self.coupon_customer.created_at = datetime.date.today() + datetime.timedelta(days=7)
        self.coupon_customer.set_expired()
        self.assertEqual(self.coupon_customer.is_active, False)

        self.customer.coupon.set_status()
        self.assertEqual(self.customer.coupon.show, None)

if __name__ == "__main__":
    unittest.main()
