# Generated by Django 2.1.3 on 2019-02-08 10:29

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import education.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BoughtCourses',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CostUnit',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('unit_id', models.PositiveSmallIntegerField(choices=[(1, 'Rial'), (2, 'Dollor'), (3, 'Euro')], default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(blank=True, db_index=True, null=True, unique=True)),
                ('title', models.CharField(blank=True, max_length=511, null=True)),
                ('rate', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)])),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Course',
                'verbose_name_plural': 'Courses',
                'db_table': 'education_course',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='CourseBody',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('percent', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)])),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(blank=True, db_index=True, null=True, unique=True)),
                ('online_or_workshop', models.BooleanField(default=True)),
                ('cost', models.DecimalField(decimal_places=3, max_digits=10)),
                ('unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='education.CostUnit')),
            ],
        ),
        migrations.CreateModel(
            name='WorkshopFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=education.models.workshop_file_directory_path)),
            ],
        ),
        migrations.CreateModel(
            name='DateDiscount',
            fields=[
                ('discount_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='education.Discount')),
                ('start_date', models.DateField(help_text='Start Day of the Discount')),
                ('end_date', models.DateField(blank=True, help_text='End Day of the Discount', null=True)),
            ],
            bases=('education.discount',),
        ),
        migrations.CreateModel(
            name='PersonalDiscount',
            fields=[
                ('discount_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='education.Discount')),
                ('coupon_text', models.CharField(max_length=15)),
                ('start_date', models.DateField(blank=True, help_text='Start Day of the Discount', null=True)),
                ('end_date', models.DateField(blank=True, help_text='End Day of the Discount', null=True)),
                ('person', models.ForeignKey(on_delete=models.SET(education.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
            bases=('education.discount',),
        ),
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('course_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='education.Course')),
                ('city', models.CharField(max_length=255)),
                ('start_date', models.DateField(help_text='Start Day of the Workshop')),
                ('end_date', models.DateField(blank=True, help_text='End Day of the Workshop', null=True)),
                ('start_time', models.TimeField(help_text='Start Time of the Workshop')),
                ('end_time', models.TimeField(blank=True, help_text='End Time of the Workshop', null=True)),
            ],
            bases=('education.course',),
        ),
        migrations.AddField(
            model_name='discount',
            name='price',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='education.Price'),
        ),
        migrations.AddField(
            model_name='course',
            name='body',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='education.CourseBody'),
        ),
        migrations.AddField(
            model_name='course',
            name='instructor',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.SET(education.models.get_sentinel_user), to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='price',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='education.Price'),
        ),
        migrations.CreateModel(
            name='RaceDiscount',
            fields=[
                ('datediscount_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='education.DateDiscount')),
                ('coupon_text', models.CharField(blank=True, max_length=15, null=True)),
                ('limit', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)])),
            ],
            bases=('education.datediscount',),
        ),
        migrations.AddField(
            model_name='workshopfile',
            name='workshop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.Workshop'),
        ),
    ]
