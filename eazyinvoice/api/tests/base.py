
from django.test import TestCase
from django.test import Client as TestClient
from django.contrib.auth import get_user_model

from api.models import UserProfile


User = get_user_model()

class BaseTest(TestCase):

    PASSWORD_FACTORY = "password-yo"
    USER_NAME = "foobar"
    OTHER_USER_NAME = "foobar2"

    def login_user(self):
        self.client.force_login(self.user)

    def login_other_user(self):
        self.client.force_login(self.other_user)

    def logout(self):
        self.client.logout()


    def setUp(self):
        self.client = TestClient()

        self.user = User.objects.create_user(
            username=self.USER_NAME,
            email=f'{self.USER_NAME}@mail.com',
            password=self.PASSWORD_FACTORY
        )
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            legal_name="Foo Barius",
            phone_number="(555) 777-1234",
            email=f'{self.USER_NAME}@mail.com',
            address1="123 Main Street",
            address2="Apt 4A",
            city="Scottsdale",
            state="AZ",
            zipcode="83994",
        )

        self.other_user = User.objects.create_user(
            username=self.OTHER_USER_NAME,
            email=f'{self.OTHER_USER_NAME}@mail.com',
            password=self.PASSWORD_FACTORY
        )
        self.user_other_profile = UserProfile.objects.create(
            user=self.other_user,
            legal_name="Lorum Ipsum",
            phone_number="(336) 744-2255",
            email=f'{self.OTHER_USER_NAME}@mail.com',
            address1="47 Derpton Way",
            address2=None,
            city="Austin",
            state="TX",
            zipcode="76544",
        )