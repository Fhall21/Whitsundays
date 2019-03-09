# Generated by Django 2.1.7 on 2019-03-09 03:50

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        ('home', '0003_homepage_intro_video_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomFormSubmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form_data', models.TextField()),
                ('submit_time', models.DateTimeField(auto_now_add=True, verbose_name='submit time')),
                ('email', models.EmailField(max_length=100)),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.Page')),
            ],
            options={
                'verbose_name': 'form submission',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HomeFormField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('label', models.CharField(help_text='The label of the form field', max_length=255, verbose_name='label')),
                ('field_type', models.CharField(choices=[('singleline', 'Single line text'), ('multiline', 'Multi-line text'), ('email', 'Email'), ('number', 'Number'), ('url', 'URL'), ('checkbox', 'Checkbox'), ('checkboxes', 'Checkboxes'), ('dropdown', 'Drop down'), ('multiselect', 'Multiple select'), ('radio', 'Radio buttons'), ('date', 'Date'), ('datetime', 'Date/time'), ('hidden', 'Hidden field')], max_length=16, verbose_name='field type')),
                ('required', models.BooleanField(default=True, verbose_name='required')),
                ('choices', models.TextField(blank=True, help_text='Comma separated list of choices. Only applicable in checkboxes, radio and dropdown.', verbose_name='choices')),
                ('default_value', models.CharField(blank=True, help_text='Default value. Comma separated values supported for checkboxes.', max_length=255, verbose_name='default value')),
                ('help_text', models.CharField(blank=True, max_length=255, verbose_name='help text')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='homepage',
            name='from_address',
            field=models.CharField(blank=True, max_length=255, verbose_name='from address'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='subject',
            field=models.CharField(blank=True, max_length=255, verbose_name='subject'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='thank_you_text',
            field=wagtail.core.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='to_address',
            field=models.CharField(blank=True, help_text='Optional - form submissions will be emailed to these addresses. Separate multiple addresses by comma.', max_length=255, verbose_name='to address'),
        ),
        migrations.AddField(
            model_name='homeformfield',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='form_fields', to='home.HomePage'),
        ),
    ]
