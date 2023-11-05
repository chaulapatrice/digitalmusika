from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    CUSTOMER = 'customer'
    PRODUCER = 'producer'
    MIDDLEMAN = 'middleman'
    ADMIN = 'admin'

    TYPES = (
        (CUSTOMER, 'Customer'),
        (PRODUCER, 'Producer'),
        (MIDDLEMAN, 'Middleman')
    )

    CITIES = (
        ('Harare', 'Harare'),
        ('Bulawayo', 'Bulawayo'),
        ('Chitungwiza', 'Chitungwiza'),
        ('Mutare', 'Mutare'),
        ('Gweru', 'Gweru'),
        ('Epworth', 'Epworth'),
        ('Kwekwe', 'Kwekwe'),
        ('Kadoma', 'Kadoma'),
        ('Masvingo', 'Masvingo'),
        ('Chinhoyi', 'Chinhoyi'),
        ('Marondera', 'Marondera'),
        ('Norton', 'Norton'),
        ('Chegutu', 'Chegutu'),
        ('Bindura', 'Bindura'),
        ('Beitbridge', 'Beitbridge'),
    )

    HARARE_PROVINCE = 'Harare'
    BULAWAYO_PROVINCE = 'Bulawayo'
    MANICALAND_PROVINCE = 'Manicaland'
    MASH_CENTRAL_PROVINCE = 'Mashonaland Central'
    MASH_EAST_PROVINCE = 'Mashonaland East'
    MASH_WEST_PROVINCE = 'Mashonaland West'
    MASVINGO_PROVINCE = 'Masvingo'
    MAT_NORTH_PROVINCE = 'Matabeleland North'
    MAT_SOUTH_PROVINCE = 'Matabeleland South'
    MIDLANDS_PROVINCE = 'Midlands'

    PROVINCES = (
        (HARARE_PROVINCE, 'Harare'),
        (BULAWAYO_PROVINCE, 'Bulawayo'),
        (MANICALAND_PROVINCE, 'Manicaland'),
        (MASH_CENTRAL_PROVINCE, 'Mashonaland Central'),
        (MASH_EAST_PROVINCE, 'Mashonaland East'),
        (MASH_WEST_PROVINCE, 'Mashonaland West'),
        (MASVINGO_PROVINCE, 'Masvingo'),
        (MAT_NORTH_PROVINCE, 'Matabeleland North'),
        (MAT_SOUTH_PROVINCE, 'Matabeleland South'),
        (MIDLANDS_PROVINCE, 'Midlands'),
    )

    phone = models.CharField(max_length=13, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    type = models.CharField(max_length=45, choices=TYPES, default=CUSTOMER)
    house_number = models.IntegerField(null=True)
    street = models.CharField(max_length=255, null=True)
    suburb = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, choices=CITIES, null=True)
    province = models.CharField(max_length=255, choices=PROVINCES, null=True)
    lat = models.DecimalField(
        max_digits=15, decimal_places=8, null=True, blank=True)
    lng = models.DecimalField(
        max_digits=15, decimal_places=8, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.first_name and self.last_name:
            return self.first_name + " " + self.last_name
        return self.username
