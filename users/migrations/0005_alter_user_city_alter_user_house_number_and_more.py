# Generated by Django 4.2.4 on 2023-11-04 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='city',
            field=models.CharField(choices=[('Harare', 'Harare'), ('Bulawayo', 'Bulawayo'), ('Chitungwiza', 'Chitungwiza'), ('Mutare', 'Mutare'), ('Gweru', 'Gweru'), ('Epworth', 'Epworth'), ('Kwekwe', 'Kwekwe'), ('Kadoma', 'Kadoma'), ('Masvingo', 'Masvingo'), ('Chinhoyi', 'Chinhoyi'), ('Marondera', 'Marondera'), ('Norton', 'Norton'), ('Chegutu', 'Chegutu'), ('Bindura', 'Bindura'), ('Beitbridge', 'Beitbridge')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='house_number',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=13, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='province',
            field=models.CharField(choices=[('Harare', 'Harare'), ('Bulawayo', 'Bulawayo'), ('Manicaland', 'Manicaland'), ('Mashonaland Central', 'Mashonaland Central'), ('Mashonaland East', 'Mashonaland East'), ('Mashonaland West', 'Mashonaland West'), ('Masvingo', 'Masvingo'), ('Matabeleland North', 'Matabeleland North'), ('Matabeleland South', 'Matabeleland South'), ('Midlands', 'Midlands')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='street',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='suburb',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='type',
            field=models.CharField(choices=[('customer', 'Customer'), ('producer', 'Producer'), ('middleman', 'Middleman'), ('admin', 'Administrator')], default='customer', max_length=45),
        ),
    ]
