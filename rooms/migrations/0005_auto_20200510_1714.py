# Generated by Django 3.0.6 on 2020-05-10 08:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0004_auto_20200510_1652'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Amenitiy',
            new_name='Amenity',
        ),
        migrations.AlterField(
            model_name='photo',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='rooms.Room'),
        ),
        migrations.AlterField(
            model_name='room',
            name='room_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='room_types', to='rooms.RoomType'),
        ),
    ]
