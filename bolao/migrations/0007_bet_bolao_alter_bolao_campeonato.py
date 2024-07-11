# Generated by Django 5.0.7 on 2024-07-11 01:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bolao', '0006_alter_game_final_score1_alter_game_final_score2'),
    ]

    operations = [
        migrations.AddField(
            model_name='bet',
            name='bolao',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='bolao.bolao'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bolao',
            name='campeonato',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bolao', to='bolao.campeonato'),
        ),
    ]
