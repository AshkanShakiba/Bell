from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import IncreaseRecord, SaleRecord


class IncreaseRecordModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.seller1 = get_user_model().objects.create_user(
            name="seller1",
            username="seller1",
            account_number="12345678",
            password="drowssap_one",
            is_confirmed=True,
        )
        cls.seller2 = get_user_model().objects.create_user(
            name="seller2",
            username="seller2",
            account_number="87654321",
            password="drowssap_two",
            is_confirmed=True,
        )

    def test_increase_record_model(self):
        # seller 1:
        IncreaseRecord.objects.create(
            amount=1000,
            seller=self.seller1,
        )
        self.assertEqual(self.seller1.credit, 1000)
        IncreaseRecord.objects.create(
            amount=10000,
            seller=self.seller1,
        )
        self.assertEqual(self.seller1.credit, 11000)
        # seller 2:
        IncreaseRecord.objects.create(
            amount=2000,
            seller=self.seller2,
        )
        self.assertEqual(self.seller2.credit, 2000)
        IncreaseRecord.objects.create(
            amount=20000,
            seller=self.seller2,
        )
        self.assertEqual(self.seller2.credit, 22000)


class SaleRecordModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.seller1 = get_user_model().objects.create_user(
            name="seller1",
            username="seller1",
            account_number="12345678",
            password="drowssap_one",
            is_confirmed=True,
            credit=10000,
        )
        cls.seller2 = get_user_model().objects.create_user(
            name="seller2",
            username="seller2",
            account_number="87654321",
            password="drowssap_two",
            is_confirmed=True,
            credit=1000,
        )

    def test_sale_record_model(self):
        # seller 1:
        SaleRecord.objects.create(
            amount=5000,
            seller=self.seller1,
            phone_number="09123456789",
        )
        self.assertEqual(self.seller1.credit, 5000)
        SaleRecord.objects.create(
            amount=2000,
            seller=self.seller1,
            phone_number="09123456789",
        )
        self.assertEqual(self.seller1.credit, 3000)
        SaleRecord.objects.create(
            amount=1000,
            seller=self.seller1,
            phone_number="09123456789",
        )
        self.assertEqual(self.seller1.credit, 2000)
        SaleRecord.objects.create(
            amount=500,
            seller=self.seller1,
            phone_number="09123456789",
        )
        self.assertEqual(self.seller1.credit, 1500)
        SaleRecord.objects.create(
            amount=200,
            seller=self.seller1,
            phone_number="09123456789",
        )
        self.assertEqual(self.seller1.credit, 1300)
        SaleRecord.objects.create(
            amount=100,
            seller=self.seller1,
            phone_number="09123456789",
        )
        self.assertEqual(self.seller1.credit, 1200)
        SaleRecord.objects.create(
            amount=50,
            seller=self.seller1,
            phone_number="09123456789",
        )
        self.assertEqual(self.seller1.credit, 1150)
        SaleRecord.objects.create(
            amount=20,
            seller=self.seller1,
            phone_number="09123456789",
        )
        self.assertEqual(self.seller1.credit, 1130)
        SaleRecord.objects.create(
            amount=10,
            seller=self.seller1,
            phone_number="09123456789",
        )
        self.assertEqual(self.seller1.credit, 1120)
        SaleRecord.objects.create(
            amount=5,
            seller=self.seller1,
            phone_number="09123456789",
        )
        self.assertEqual(self.seller1.credit, 1115)
        # seller 2:
        SaleRecord.objects.create(
            amount=15,
            seller=self.seller2,
            phone_number="09123456789",
        )
        self.assertEqual(self.seller2.credit, 985)
        SaleRecord.objects.create(
            amount=12,
            seller=self.seller2,
            phone_number="09123456789",
        )
        self.assertEqual(self.seller2.credit, 973)
        SaleRecord.objects.create(
            amount=43,
            seller=self.seller2,
            phone_number="09123456789",
        )
        self.assertEqual(self.seller2.credit, 930)
        SaleRecord.objects.create(
            amount=92,
            seller=self.seller2,
            phone_number="09123456789",
        )
        self.assertEqual(self.seller2.credit, 838)
        SaleRecord.objects.create(
            amount=101,
            seller=self.seller2,
            phone_number="09123456789",
        )
        self.assertEqual(self.seller2.credit, 737)
        SaleRecord.objects.create(
            amount=2,
            seller=self.seller2,
            phone_number="09123456789",
        )
        self.assertEqual(self.seller2.credit, 735)
        SaleRecord.objects.create(
            amount=87,
            seller=self.seller2,
            phone_number="09123456789",
        )
        self.assertEqual(self.seller2.credit, 648)
        SaleRecord.objects.create(
            amount=17,
            seller=self.seller2,
            phone_number="09123456789",
        )
        self.assertEqual(self.seller2.credit, 631)
        SaleRecord.objects.create(
            amount=67,
            seller=self.seller2,
            phone_number="09123456789",
        )
        self.assertEqual(self.seller2.credit, 564)
        SaleRecord.objects.create(
            amount=33,
            seller=self.seller2,
            phone_number="09123456789",
        )
        self.assertEqual(self.seller2.credit, 531)
