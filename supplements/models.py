from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from django.conf import settings # Add this import

class Supplement(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100, choices=[('Protein', 'Protein'), ('Creatine', 'Creatine'), ('Bars', 'Bars'), ('Pre-workout', 'Pre-workout')])
    stock_quantity = models.IntegerField(default=0)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Sale(models.Model):
    supplement = models.ForeignKey(Supplement, on_delete=models.CASCADE)
    # New field to log who sold it
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    buyer_name = models.CharField(max_length=200)
    buyer_contact = models.CharField(max_length=15)
    quantity_sold = models.IntegerField()
    sale_date = models.DateTimeField(default=timezone.now)
    total_profit = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        profit_per_unit = self.supplement.selling_price - self.supplement.purchase_price
        self.total_profit = profit_per_unit * self.quantity_sold
        self.supplement.stock_quantity -= self.quantity_sold
        self.supplement.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.supplement.name} sold to {self.buyer_name}"