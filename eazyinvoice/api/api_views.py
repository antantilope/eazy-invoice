import csv

from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from api.models import Organization, HourlyRate, HoursEntry, Invoice
from api.api_forms import (
    NewHoursEntryForm,
    RunQueryForm
)
from api.services import invoice_lib, notification_lib


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

    notification_lib.send_admin_alert(
        "New hour entry created for " + org.short_name
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
    notification_lib.send_admin_alert(
        "Hours entry deleted: " + entryId
    )
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
    notification_lib.send_admin_alert(
        "New invoice created: " + invoice.invoice_number
    )
    return Response({'id': invoice.id}, status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_invoice(request, orgId: str, invoiceId: str):
    org = get_object_or_404(Organization, id=orgId, user=request.user)
    invoice = get_object_or_404(
        Invoice,
        organization=org,
        id=invoiceId,
    )
    invoice.delete()
    notification_lib.send_admin_alert(
        "Invoice deleted: " + invoiceId
    )
    return Response({}, status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_invoice_paid(request, orgId: str, invoiceId: str):
    org = get_object_or_404(Organization, id=orgId, user=request.user)
    invoice = get_object_or_404(
        Invoice,
        organization=org,
        id=invoiceId,
        is_paid=False,
    )
    invoice.is_paid = True
    invoice.paid_at = timezone.now()
    invoice.save(update_fields=['is_paid', 'paid_at'])
    return Response({}, status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def run_query(request):
    print(request.data)
    form = RunQueryForm(request.data)
    if not form.is_valid():
        return Response(form.errors, status.HTTP_400_BAD_REQUEST)

    org_ids = []
    for org in form.cleaned_data['organizations']:
        if org.user != request.user:
            return Response("", status.HTTP_404_NOT_FOUND)
        org_ids.append(org.id)

    if not len(org_ids):
        return Response("no orgs selected", status.HTTP_400_BAD_REQUEST)

    invoice_paid_start_date = form.cleaned_data.get('invoice_paid_start_date')
    invoice_paid_end_date = form.cleaned_data.get('invoice_paid_end_date')
    is_paid = form.cleaned_data.get('is_paid', False)

    now_ts = timezone.now().strftime('%Y%m%d_%H%M%S')
    resp = HttpResponse(status=status.HTTP_200_OK)
    resp['Content-Type'] = 'text/csv'
    resp['Content-Disposition'] = f'attachment; filename="query_{now_ts}.csv"'

    writer = csv.writer(resp)
    for row in invoice_lib.get_invoice_csv_rows(
        org_ids, is_paid, invoice_paid_start_date, invoice_paid_end_date
    ):
        writer.writerow(row)
    return resp
