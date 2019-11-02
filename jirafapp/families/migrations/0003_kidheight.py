# Generated by Django 2.2.6 on 2019-11-02 18:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('families', '0002_auto_20191029_0810'),
    ]

    operations = [
        migrations.CreateModel(
            name='KidHeight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created.', verbose_name='created at')),
                ('modified', models.DateTimeField(auto_now=True, help_text='Date time on which the object was last modified.', verbose_name='modified at')),
                ('height', models.DecimalField(decimal_places=3, max_digits=3, verbose_name='Height')),
                ('date_height', models.DateField(verbose_name='Date Heigth')),
                ('kid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='families.Kid')),
            ],
            options={
                'verbose_name': 'Altura Niño',
                'verbose_name_plural': 'Alturas de los Niño',
            },
        ),
    ]
