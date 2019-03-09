# Generated by Django 2.1.7 on 2019-03-09 10:01

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0001_squashed_0021'),
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        ('home', '0007_auto_20190309_1434'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoSubmission',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('headline', models.CharField(blank=True, max_length=200, null=True)),
                ('intro_video_id', models.CharField(blank=True, max_length=50, null=True)),
                ('video_ids', wagtail.core.fields.StreamField([('video_ids', wagtail.core.blocks.StructBlock([('video_ids', wagtail.core.blocks.CharBlock())]))], blank=True, null=True)),
                ('background_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
