
from api.tests.base import BaseTest


class TestHoursEntry(BaseTest):

    def test_user_can_create_hours_entry_for_own_org(self):
        self.login_user()

    def test_user_cant_create_hours_entry_for_another_users_org(self):
        self.login_user()

    def test_user_can_delete_hours_entry_for_own_org(self):
        self.login_user()

    def test_user_cant_delete_hours_entry_for_another_users_entry(self):
        self.login_user()

    def test_user_cant_delete_hours_entry_if_already_assigned_to_invoice(self):
        self.login_user()
