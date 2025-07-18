# Generated by Django 5.2 on 2025-06-02 21:23

import JARVIS.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JARVIS', '0002_chatmessage_chatsession_document_embedding_and_more'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='embedding',
            name='JARVIS_embe_documen_a8ed03_idx',
        ),
        migrations.AlterField(
            model_name='document',
            name='file',
            field=models.FileField(upload_to='documents/', validators=[JARVIS.models.validate_pdf_file]),
        ),
        migrations.AlterField(
            model_name='embedding',
            name='vector',
            field=models.JSONField(validators=[JARVIS.models.validate_embedding_dimension]),
        ),
    ]
