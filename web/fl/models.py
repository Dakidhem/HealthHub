from django.db import models

# Create your models here.
class FlResults(models.Model):

    ALGO_CHOICES = (
        ('Pneumonia', 'Pneumonia'),
        ('Multiclass', 'Multiclass'),
    )

    date = models.DateTimeField(auto_now_add = True)
    logs= models.TextField(blank=True, null = True)
    min_client = models.IntegerField(default=2)
    num_round = models.IntegerField(default=2)
    algo = models.CharField(max_length=10, choices=ALGO_CHOICES, default=ALGO_CHOICES[0][0])

    class Meta:
        db_table = "FlResults"