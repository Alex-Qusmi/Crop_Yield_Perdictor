# dashboard/models.py
from django.db import models

class MarketPrice(models.Model):
    crop = models.CharField(max_length=100)
    variety = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2) # Price per quintal
    mandi = models.CharField(max_length=100, default="Dehradun") # e.g., Dehradun, Nainital
    trend = models.CharField(
        max_length=10, 
        choices=[('UP', 'Up'), ('DOWN', 'Down'), ('STABLE', 'Stable'), ('HIGH', 'High Demand')],
        default='STABLE'
    )
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.crop} ({self.variety}) - ₹{self.price} in {self.mandi}"

class FeaturedCrop(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    tag = models.CharField(max_length=50) # e.g., "High Profit", "Market Window"
    image_search_term = models.CharField(max_length=100) # e.g., "saffron,farm"
    district = models.CharField(max_length=100, blank=True, null=True, help_text="Leave blank for a 'general' crop")

    def __str__(self):
        return self.name