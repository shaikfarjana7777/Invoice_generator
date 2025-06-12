from django.db import models

# Create your models here.
class Client(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    address=models.TextField()
    
    def __str__(self):
        return self.name
    
class Invoice(models.Model):
    client=models.ForeignKey(Client,related_name='items',on_delete=models.CASCADE)    
    date=models.DateField(auto_now_add=True)
    due_date=models.DateField()
    notes=models.TextField(blank=True)
     
    def __str__(self):
        return f"Invoice #{self.id}-{self.client.name}"
    
class InvoiceItem(models.Model):
    invoice=models.ForeignKey(Invoice,related_name='items',on_delete=models.CASCADE)    
    description=models.CharField(max_length=300)
    quantity=models.PositiveIntegerField()
    price=models.DecimalField(max_digits=10,decimal_places=2)

    def total(self):
        return self.quantity * self.price  

    def __str__(self):
        return f"{self.description} - {self.total()}"