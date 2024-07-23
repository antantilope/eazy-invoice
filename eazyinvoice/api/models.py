
import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class USERAPPS:
    USER_ACCESS_INVOICING = "invoicing"


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

    user_access = models.CharField(max_length=255)


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
    days_to_pay = models.PositiveSmallIntegerField(default=30)

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
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(blank=True, null=True, default=None)

    class Meta:
        unique_together = (
            'organization',
            'invoice_number',
        )

    def __str__(self):
        return "INV " + self.invoice_number

    @property
    def download_file_name(self):
        return f"invoice_{timezone.now().strftime('%Y%m%d_%H%M%S')}_{self.invoice_number}.pdf"


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
        return "Rate " + str(self.rate) + f" ({self.organization})"




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
