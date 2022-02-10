# Generated by Django 2.2.24 on 2022-02-10 14:07

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('firstname', models.CharField(max_length=30)),
                ('lastname', models.CharField(max_length=30)),
                ('username', models.CharField(max_length=20, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('sector', models.CharField(blank=True, choices=[('INFO', 'Informatique'), ('PHOT', 'Photonique'), ('SNUM', 'Systèmes numériques'), ('IMR', 'IMR')], help_text='Donne moi ta filière bro', max_length=4)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('klax_coins', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Bets',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('bet_name', models.CharField(max_length=256, unique=True)),
                ('win_rate', models.DecimalField(decimal_places=2, default=1.0, max_digits=4)),
                ('win_vote', models.IntegerField(default=0)),
                ('win_gains', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('draw_rate', models.DecimalField(decimal_places=2, default=1.0, max_digits=4)),
                ('draw_vote', models.IntegerField(default=0)),
                ('draw_gains', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('lose_rate', models.DecimalField(decimal_places=2, default=1.0, max_digits=4)),
                ('lose_vote', models.IntegerField(default=0)),
                ('lose_gains', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('ended', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='StoreBets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(blank=True, choices=[('W', 'Win'), ('D', 'Draw'), ('L', 'Lose')], help_text='Which result for the bet', max_length=1)),
                ('gains', models.DecimalField(decimal_places=2, default=1.0, max_digits=12)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('is_combined', models.BooleanField(default=False)),
                ('id_combined', models.IntegerField(null=True)),
                ('bet_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main_app.Bets')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
