from django.contrib import admin

from app.models import (
    UserProfile,
    Organization,
    Invoice,
    HourlyRate,
    HoursEntry,
)

admin.site.register(UserProfile)
admin.site.register(Organization)
admin.site.register(Invoice)
admin.site.register(HourlyRate)
admin.site.register(HoursEntry)
