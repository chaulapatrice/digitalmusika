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
        (MIDDLEMAN, 'Middleman'),
        (ADMIN, 'Administrator')
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

    phone = models.CharField(max_length=13)
    type = models.CharField(max_length=45, choices=TYPES)
    house_number = models.IntegerField()
    street = models.CharField(max_length=255)
    suburb = models.CharField(max_length=255)
    city = models.CharField(max_length=255, choices=CITIES)
    province = models.CharField(max_length=255, choices=PROVINCES)
    lat = models.DecimalField(max_digits=15, decimal_places=8, null=True, blank=True)
    lng = models.DecimalField(max_digits=15, decimal_places=8, null=True, blank=True)
    created_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
