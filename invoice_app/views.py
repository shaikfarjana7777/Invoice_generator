from django.shortcuts import HttpResponse,render, redirect, get_object_or_404
from .forms import ClientForm, InvoiceForm, InvoiceItemForm
from .models import Client, Invoice, InvoiceItem
from django.template.loader import get_template
from django.forms import modelformset_factory
from django.templatetags.static import static
from django.http import HttpResponse
from django.conf import settings
from weasyprint import HTML




from datetime import date

# Create your views here.

def home(request):
    return render(request, 'home.html')


def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('add_invoice') 
    else:
        form = ClientForm()
    return render(request, 'add_client.html', {'form': form})


def add_invoice(request):
    InvoiceItemFormSet = modelformset_factory(InvoiceItem, form=InvoiceItemForm, extra=1)

    if request.method == 'POST':
        invoice_form = InvoiceForm(request.POST)
        formset = InvoiceItemFormSet(request.POST, queryset=InvoiceItem.objects.none())

        if invoice_form.is_valid() and formset.is_valid():
            invoice = invoice_form.save()
            for form in formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                    item = form.save(commit=False)
                    item.invoice = invoice
                    item.save()

            return redirect('invoice_detail', pk=invoice.pk)

        else:
            
            print("Invoice Form Errors:", invoice_form.errors)
            for form in formset:
                print("Formset error:", form.errors)
    else:
        invoice_form = InvoiceForm()
        formset = InvoiceItemFormSet(queryset=InvoiceItem.objects.none())

    return render(request, 'add_invoice.html', {
        'invoice_form': invoice_form,
        'formset': formset
    })


   
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    client = invoice.client
    items = invoice.items.all()  

    total_amount = sum(item.total() for item in items)

    return render(request, 'invoice_detail.html', {
        'invoice': invoice,
        'client': client,
        'items': items,
        'total': total_amount,
        'today': date.today(),  

    })


def invoice_detail_pdf(request, pk):
    try:
        invoice = Invoice.objects.get(pk=pk)
        client = invoice.client
        items = invoice.items.all()
        total = sum(item.total() for item in items)

        logo_path = request.build_absolute_uri(static('images/Web Design.png'))

        template = get_template('invoice_pdf.html')
        html_string = template.render({
            'invoice': invoice,
            'client': client,
            'items': items,
            'total': total,
            'today': date.today(),
            'request': request,
            'logo_path': logo_path,
        })

        html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
        pdf_file = html.write_pdf()

        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.pk}.pdf"'
        return response

    except Exception as e:
        return HttpResponse(f"<h1>Error generating PDF</h1><p>{e}</p>", status=500)
