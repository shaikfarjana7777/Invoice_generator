from django import forms
from .models import Client, InvoiceItem,Invoice

class ClientForm(forms.ModelForm):
    class Meta:
        model=Client
        fields=['name','email','address']


class InvoiceForm(forms.ModelForm):
    class Meta:
        model=Invoice
        fields=['client','due_date','notes']        

        widgets = {
            'due_date': forms.DateInput(attrs={
                'placeholder': 'yyyy-mm-dd',
                'type': 'date', 
                'style': 'width: 200px; padding: 6px; border-radius: 6px;'
            }),
            'notes': forms.Textarea(attrs={
                'rows': 3,
                'cols': 40,
                'style': 'font-size: 14px; width: 100%; border-radius: 8px; padding: 8px;'
            })
        }
class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model=InvoiceItem
        fields=['description','quantity','price']        