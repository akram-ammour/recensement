from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
class Promo(models.Model):
    level = models.IntegerField(default=1,validators=[MinValueValidator(1), MaxValueValidator(5)],unique=True)
    notion_token = models.CharField(max_length=200,null=True,blank=True) 
    page_id = models.CharField(max_length=200,null=True,blank=True)
    def __str__(self):
        return str(self.level)
class Bde(models.Model):
    fullname = models.CharField(max_length=200,null=False,blank=False)
    promo = models.ForeignKey(Promo,on_delete=models.CASCADE)

    def __str__(self):
        return self.fullname