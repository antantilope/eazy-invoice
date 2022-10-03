from django.contrib import admin

from icit.models import (
    IcitState,
    IcitMessage,
    DummyMachineToken,
)

admin.site.register(IcitState)
admin.site.register(IcitMessage)
admin.site.register(DummyMachineToken)

