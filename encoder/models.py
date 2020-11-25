from django.db import models
SCHEMES = (
        ("Unipolar",'Unipolar'),
        ("NRZ-L",'NRZ-L'),
        ("NRZ-I",'NRZ-I'),
        ("Polar RZ",'Polar RZ'),
        ("Manchester",'Manchester'),
        ("Differential Manchester",'Differential Manchester'),
        ("AMI",'AMI'),
        )
SCRAMBLING = (
        ("None",'None'),
        ("B8ZS",'B8ZS'),
        ("HDB3",'HDB3'),
        )   
# Create your models here.
class Encoder(models.Model):
    custom = models.BooleanField(default=False,blank=True)
    custom_bits = models.CharField(max_length=256,blank=True)
    bit_size = models.IntegerField(blank=True)
    fixed_sequence = models.BooleanField(default=False,blank=True)
    fixed_size = models.IntegerField(blank=True)
    fixed_freq = models.IntegerField(blank=True)
    pos_logic = models.BooleanField(default=True,blank=True)
    scheme_choice = models.CharField(max_length=50,
                                    choices=SCHEMES,
                                    default="Unipolar")
    scrambling_choice = models.CharField(max_length=20,
                                        choices=SCRAMBLING,
                                        default="None",blank=True)