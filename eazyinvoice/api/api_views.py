
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from api.models import Organization, HourlyRate, HoursEntry
from api.api_forms import (
    NewHoursEntryForm,
)
from api.services import invoice_lib


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_hours_entry(request, orgId: str):
    org = get_object_or_404(Organization, id=orgId, user=request.user)
    form = NewHoursEntryForm(request.data)
    if not form.is_valid():
        return Response(form.errors, status.HTTP_400_BAD_REQUEST)
    if form.cleaned_data['ord_id'] != orgId:
        return Response("org id mismatch", status.HTTP_400_BAD_REQUEST)
    rate = get_object_or_404(
        HourlyRate,
        id=form.cleaned_data['rate_id'],
        organization=org,
    )

    HoursEntry.objects.create(
        date=form.cleaned_data['date'],
        rate=rate,
        invoice=None,
        quantity=form.cleaned_data['quantity'],
        description=form.cleaned_data.get('description'),
    )

    return Response({}, status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_hours_entry(request, orgId: str, entryId: str):
    org = get_object_or_404(Organization, id=orgId, user=request.user)
    entry = get_object_or_404(HoursEntry, id=entryId, rate__organization=org)
    if entry.invoice is not None:
        return Response(
            "entry already assigned to invoice",
            status.HTTP_400_BAD_REQUEST,
        )
    entry.delete()
    return Response({}, status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_invoice(request, orgId: str):
    org = get_object_or_404(Organization, id=orgId, user=request.user)
    entries = HoursEntry.objects.filter(
        rate__organization=org,
        invoice__isnull=True,
    ).order_by("date", "created_at")

    if not entries.exists():
        return Response(
            "no hour entries to assign",
            status.HTTP_400_BAD_REQUEST,
        )

    invoice = invoice_lib.create_invoice_for_entries(org, entries)
    return Response({'id': invoice.id}, status.HTTP_201_CREATED)
