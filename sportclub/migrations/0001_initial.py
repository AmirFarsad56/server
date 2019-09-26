# Generated by Django 2.2.2 on 2019-09-21 01:20

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SportClubModel',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='sportclubs', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('region', models.CharField(max_length=264)),
                ('phone_number', models.CharField(max_length=20, unique=True)),
                ('serial_number', models.IntegerField(unique=True)),
                ('company_phone_number', models.CharField(max_length=20)),
                ('sportclub_name', models.CharField(max_length=264)),
                ('address', models.TextField()),
                ('location', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('info', models.TextField(blank=True, null=True)),
                ('picture', models.ImageField(default='sportclub/default/coverpicture.png', upload_to='sportclub/coverpicture')),
                ('terms_and_conditions', models.TextField(blank=True, null=True)),
                ('bankaccount_ownername', models.CharField(blank=True, max_length=300, null=True)),
                ('bankaccount_accountnumber', models.CharField(blank=True, max_length=30, null=True)),
                ('bankaccount_cardnumber', models.CharField(blank=True, max_length=30, null=True)),
                ('bankaccount_bankname', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]
