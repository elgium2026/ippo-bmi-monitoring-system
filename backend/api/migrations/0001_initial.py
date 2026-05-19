# Generated for the initial Render deployment.

import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('rank', models.CharField(choices=[('PBGEN', 'PBGEN'), ('PCOL', 'PCOL'), ('PLTCOL', 'PLTCOL'), ('PMAJ', 'PMAJ'), ('PCPT', 'PCPT'), ('PLT', 'PLT'), ('PEMS', 'PEMS'), ('PCMS', 'PCMS'), ('PSMS', 'PSMS'), ('PMSg', 'PMSg'), ('PSSg', 'PSSg'), ('PCpl', 'PCpl'), ('Pat', 'Pat'), ('NUP', 'NUP')], max_length=15)),
                ('rank_classification', models.CharField(choices=[('PCO', 'PCO'), ('PNCO', 'PNCO'), ('NUP', 'NUP')], max_length=10)),
                ('middle_name', models.CharField(blank=True, max_length=100)),
                ('qualifier', models.CharField(blank=True, max_length=30)),
                ('birthdate', models.DateField(blank=True, null=True)),
                ('unit', models.CharField(choices=[('PHQ', 'PHQ'), ('1st IPMFC', '1st IPMFC'), ('2nd IPMFC', '2nd IPMFC'), ('Aguinaldo MPS', 'Aguinaldo MPS'), ('Alfonso Lista MPS', 'Alfonso Lista MPS'), ('Asipulo MPS', 'Asipulo MPS'), ('Banaue MPS', 'Banaue MPS'), ('Hingyon MPS', 'Hingyon MPS'), ('Hungduan MPS', 'Hungduan MPS'), ('Kiangan MPS', 'Kiangan MPS'), ('Lagawe MPS', 'Lagawe MPS'), ('Lamut MPS', 'Lamut MPS'), ('Mayoyao MPS', 'Mayoyao MPS'), ('Tinoc MPS', 'Tinoc MPS'), ('Other Units (Please Specify)', 'Other Units (Please Specify)')], max_length=50)),
                ('unit_other', models.CharField(blank=True, max_length=100)),
                ('sex', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=10)),
                ('weight_kg', models.FloatField(blank=True, null=True)),
                ('height_cm', models.FloatField(blank=True, null=True)),
                ('waist_cm', models.FloatField(blank=True, null=True)),
                ('hip_cm', models.FloatField(blank=True, null=True)),
                ('wrist_cm', models.FloatField(blank=True, null=True)),
                ('must_change_password', models.BooleanField(default=True)),
                ('admin_totp_secret', models.CharField(blank=True, max_length=128, null=True)),
                ('is_personnel', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LoginHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150)),
                ('action', models.CharField(max_length=80)),
                ('success', models.BooleanField(default=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]
