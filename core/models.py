from django.db import models

class MarketingPlan(models.Model):
    business_name = models.CharField(max_length=255)
    strengths = models.TextField(null=True, blank=True)
    weaknesses = models.TextField(null=True, blank=True)
    opportunities = models.TextField(null=True, blank=True)
    threats = models.TextField(null=True, blank=True)
    pestel_data = models.TextField(null=True, blank=True)
    marketing_mix_4p = models.TextField(null=True, blank=True)
    marketing_mix_4c = models.TextField(null=True, blank=True)
    target_audience = models.TextField(null=True, blank=True)
    generated_strategy = models.TextField() # ეს არ უნდა იყოს null
    created_at = models.DateTimeField(auto_now_add=True)