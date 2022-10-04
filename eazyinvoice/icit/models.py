
import uuid

from django.db import models
from django.contrib.auth import get_user_model


class IcitState(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    should_be_logged_in = models.BooleanField()


class IcitMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    message = models.TextField()


class DummyMachineToken(models.Model):
    token_hash = models.TextField()
