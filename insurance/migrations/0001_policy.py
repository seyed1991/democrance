# Generated by Django 3.2.8 on 2021-10-19 20:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('policy_type', models.IntegerField(choices=[(1, 'Personal Accident'), (2, 'Earthquake')], db_index=True, verbose_name='Policy Type')),
                ('premium', models.IntegerField(verbose_name='Premium')),
                ('cover', models.IntegerField(verbose_name='Cover')),
                ('state', models.IntegerField(choices=[(1, 'New'), (2, 'Quoted'), (3, 'Active')], db_index=True, verbose_name='Policy State')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='policies', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
