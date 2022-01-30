
import uuid

from django.db import models
from django.contrib.auth import get_user_model


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserProfile(BaseModel):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    legal_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    address1 = models.TextField()
    address2 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default=None,
    )
    city = models.CharField(
        max_length=255,
    )
    state = models.CharField(
        max_length=2,
    )
    zipcode = models.CharField(
        max_length=24,
    )

    def __str__(self):
        return "UP " + self.user.username


class Organization(BaseModel):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    short_name = models.CharField(max_length=24)
    legal_name = models.CharField(max_length=255)
    attn = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default=None,
    )

    address1 = models.TextField()
    address2 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default=None,
    )
    city = models.CharField(
        max_length=255,
    )
    state = models.CharField(
        max_length=2,
    )
    zipcode = models.CharField(
        max_length=24,
    )

    def __str__(self):
        return "ORG " + self.short_name


class Invoice(BaseModel):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
    )
    issued_date = models.DateField()
    due_date = models.DateField()
    invoice_number = models.CharField(
        max_length=255,
    )

    class Meta:
        unique_together = (
            'organization',
            'invoice_number',
        )

    def __str__(self):
        return "INV " + self.invoice_number



class HourlyRate(BaseModel):
    rate = models.DecimalField(
        max_digits=6,
        decimal_places=2,
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "Rate " + str(self.rate)




class HoursEntry(BaseModel):
    date = models.DateField()
    rate = models.ForeignKey(
        HourlyRate,
        on_delete=models.CASCADE,
    )
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        default=None,
    )
    quantity = models.DecimalField(
        max_digits=6,
        decimal_places=2,
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default=None,
    )

    def __str__(self):
        return "Entry " + str(self.date)
