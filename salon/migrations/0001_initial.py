# Generated by Django 2.2.2 on 2019-09-21 01:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sportclub', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalonModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_confirmed', models.BooleanField(default=False)),
                ('profit_percentage', models.FloatField()),
                ('company_discount_percentage', models.FloatField(default=0)),
                ('area', models.PositiveIntegerField()),
                ('floor_type', models.CharField(blank=True, max_length=264, null=True)),
                ('locker', models.BooleanField()),
                ('drinking_water', models.BooleanField()),
                ('parking_area', models.BooleanField()),
                ('shower', models.BooleanField()),
                ('safe_keeping', models.BooleanField()),
                ('changing_room', models.BooleanField()),
                ('buffet', models.BooleanField()),
                ('local_taxi', models.BooleanField()),
                ('wifi', models.BooleanField()),
                ('spectator_place', models.BooleanField()),
                ('air_conditioner', models.BooleanField()),
                ('ball_rent', models.BooleanField()),
                ('is_futsall', models.BooleanField()),
                ('is_volleyball', models.BooleanField()),
                ('is_football', models.BooleanField()),
                ('is_basketball', models.BooleanField()),
                ('is_handball', models.BooleanField()),
                ('six_to_twelve_sessions_discount', models.PositiveIntegerField(default=0)),
                ('more_than_twelve_sessions_discount', models.PositiveIntegerField(default=0)),
                ('more_than_24_sessions_discount', models.PositiveIntegerField(default=0)),
                ('sportclub', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='salons', to='sportclub.SportClubModel')),
            ],
        ),
        migrations.CreateModel(
            name='SalonPictureModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='sportclub/salon/picture')),
                ('salon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pictures', to='salon.SalonModel')),
            ],
        ),
    ]
