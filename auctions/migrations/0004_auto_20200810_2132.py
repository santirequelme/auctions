# Generated by Django 3.0.7 on 2020-08-10 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20200810_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(blank=True, choices=[('No Category', ' No Category'), ('Home', 'Home'), ('Toys', 'Toys'), ('Tech', 'Tech'), ('Sport', 'Sport'), ('Pet', 'Pet'), ('Other', 'Other')], default='No Category', max_length=64),
        ),
    ]
