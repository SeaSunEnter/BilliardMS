# Generated by Django 4.2.3 on 2023-09-02 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tabler', '0003_tablebactiveassettmp_tablebactiveprocess_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tableb',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
