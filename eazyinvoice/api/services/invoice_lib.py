
from datetime import timedelta
from decimal import Decimal
from io import StringIO
import os
from typing import List, Dict

from django.utils.html import escape
from django.db import transaction
from django.db.models import QuerySet
from django.utils import timezone
from django.conf import settings
import pdfkit

from api.models import HoursEntry, Organization, Invoice
from api.services import tmp_lib

def round_dec(val: Decimal) -> Decimal:
    return val.quantize(Decimal("0.00"))


def get_next_invoice_number(org: Organization) -> str:
    # format is `<ORG.SHORT_NAME>_<YEAR>_<COUNTER>`
    this_year = timezone.now().year
    invoices_numbers = list(Invoice
        .objects
        .filter(
            organization=org,
            created_at__year__gte=this_year,
            invoice_number__startswith=f"{org.short_name.lower()}_{this_year}_",
        )
        .order_by("-created_at")
        [:5]
        .values_list("invoice_number", flat=True)
    )
    if len(invoices_numbers):
        next_counter = max(
            int(inv_num.split("_")[-1])
            for inv_num in invoices_numbers
        ) + 1
    else:
        next_counter = 1

    return f"{org.short_name.replace(' ', '').lower()}_{this_year}_{next_counter}"


@transaction.atomic
def create_invoice_for_entries(
    org: Organization,
    entries: QuerySet,
) -> Invoice:
    invoice_number = get_next_invoice_number(org)

    invoice = Invoice.objects.create(
        organization=org,
        issued_date=timezone.now().date(),
        due_date=(timezone.now().date() + timedelta(days=org.days_to_pay)),
        invoice_number=invoice_number,
    )
    entries.update(invoice=invoice)
    return invoice


def get_created_invoices_data(org: Organization) -> List[Dict]:
    invoices = (Invoice
        .objects
        .filter(organization=org)
        .order_by("-created_at")
        [:20]
    )
    entries = (HoursEntry
        .objects
        .filter(invoice__in=invoices)
        .order_by("-invoice__created_at", "-created_at")
        .values("invoice_id", "rate__rate", "quantity")
    )
    data = []
    for inv in invoices:
        entries_this_inv = [e for e in entries if e['invoice_id'] == inv.id]
        entries_this_inv_ct = len(entries_this_inv)
        if not entries_this_inv_ct:
            continue

        total_amount = round_dec(sum(
            e['rate__rate'] * e['quantity']
            for e in entries_this_inv
        ))
        data.append({
            'id': inv.id,
            'invoice_number': inv.invoice_number,
            'total_amount': total_amount,
            'issued_date': inv.issued_date,
            'due_date': inv.due_date,
        })
    return data


def create_invoice_pdf(invoice: Invoice) -> bytes:
    htmlFp = create_invoice_html(invoice)
    html_path = tmp_lib.get_new_tmp_file_name("html")
    with open(html_path, "w") as f:
        f.write(htmlFp.read())
    options = {
        'page-size': 'A4',
        'disable-smart-shrinking': True,
        'margin-top': '0.25in',
        'margin-right': '0.30in',
        'margin-left': '0.30in',
        'margin-bottom': '0.25in',
    }
    data = pdfkit.from_file(
        html_path,
        output_path=None,
        options=options,
        css=settings.INVOICE_CSS_PATH,
    )
    os.remove(html_path)
    return data


def create_invoice_html(invoice: Invoice) -> StringIO:
    org = invoice.organization
    user_profile = org.user.userprofile

    html = StringIO()
    html.write('<html>')
    html.write('<head>')
    # html.write('<style>body { font-family:arial; margin:10px; }</style>')
    html.write('</head>')
    html.write('<body>')
    html.write(f'<div><strong><em>INVOICE</em></strong> #{escape(invoice.invoice_number)}</div>')

    # Payee section
    html.write('<div class="mb-4 section">')
    html.write(f'<div>{escape(user_profile.legal_name)}</div>')
    html.write(f'<div>{escape(user_profile.email)}</div>')
    html.write(f'<div>{escape(user_profile.phone_number)}</div>')
    html.write(f'<div>{escape(user_profile.address1)}')
    if user_profile.address2:
        html.write(f', {escape(user_profile.address2)}')
    html.write('</div>')
    html.write(f"<div>{escape(user_profile.city)}, {escape(user_profile.state)} {escape(user_profile.zipcode)}</div>")
    html.write('</div>')

    # Invoice details section
    html.write('<div class="mb-4 section">')
    html.write(f'<div><strong>Invoice #</strong> {escape(invoice.invoice_number)}</div>')
    html.write(f'<div><strong>Date</strong> {escape(invoice.issued_date.strftime("%b %d %Y"))}</div>')
    html.write(f'<div><strong>Due Date</strong> {escape(invoice.due_date.strftime("%b %d %Y"))}</div>')
    html.write('</div>')

    # Invoice payer section
    html.write('<div class="mb-12 section">')
    html.write(f'<div><strong>Bill To:</strong> {escape(org.legal_name)}')
    if org.attn:
        html.write(f', ATTN: {escape(org.attn)}')
    html.write('</div>')
    html.write(f'<div>{escape(org.address1)}')
    if org.address2:
        html.write(f', {escape(org.address2)}')
    html.write('</div>')
    html.write(f"<div>{escape(org.city)}, {escape(org.state)} {escape(org.zipcode)}</div>")
    html.write('</div>')

    # Details Section
    entries = HoursEntry.objects.filter(invoice=invoice).order_by("-created_at")
    html.write('<div class="mb-12">')
    html.write('<div class="mb-4">HOURLY DETAILS</div>')
    html.write('<table><tr><th>Date</th><th>Description</th><th>Quantity</th><th>Rate</th><th>Total</th></tr>')
    total_hours = Decimal(0)
    total_amount = Decimal(0)
    for entry in entries:
        html.write("<tr>")
        total = round_dec(entry.quantity * entry.rate.rate)
        date = entry.date.strftime("%b %d %Y")
        html.write(f'<td>{escape(date)}</td>')
        html.write(f'<td>{escape(entry.description[:38] if entry.description else "")}</td>')
        html.write(f'<td>{escape(entry.quantity)}</td>')
        html.write(f'<td>$ {escape(entry.rate.rate)}</td>')
        html.write(f'<td>$ {escape(total)}</td>')
        html.write("</tr>")

        total_hours += entry.quantity
        total_amount += total

    total_hours = round_dec(total_hours)
    total_amount = round_dec(total_amount)
    avg_rate = round_dec(total_amount / total_hours)
    html.write(
        f'<tr class="total-row"><td><strong>TOTAL</strong></td><td></td><td>{escape(total_hours)}</td><td>$ {escape(avg_rate)}</td><td class="highlight">$ {escape(total_amount)}</td></tr>'
    )
    html.write('</table></div>')

    # Add bottom message.
    html.write('<div class="mb-4"><em>Please reach out if you have any questions.</em></div>')

    # Close off file.
    html.write('</body>')
    html.write('</html>')
    html.seek(0)
    return html
