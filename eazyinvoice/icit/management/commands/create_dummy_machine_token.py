

from django.core.management.base import BaseCommand
from django.core.management.utils import get_random_secret_key
from django.db import transaction


from icit.models import DummyMachineToken
from icit.services import create_md5_hash


class Command(BaseCommand):

    @transaction.atomic
    def handle(self, *args, **options):

        DummyMachineToken.objects.all().delete()

        new_key = get_random_secret_key()
        DummyMachineToken.objects.create(
            token_hash=create_md5_hash(new_key)
        )

        print(f"new key\n\n{new_key}\n\n")
