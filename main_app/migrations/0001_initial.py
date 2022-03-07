# Generated by Django 4.0.2 on 2022-03-07 14:08

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
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
                ('klax_coins', models.DecimalField(decimal_places=2, default=100.0, max_digits=12)),
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
            name='Allos',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('allo_type', models.CharField(blank=True, choices=[('A', 'Bières'), ('B', 'Goûter'), ('C', "P'tit dej"), ('D', 'Ménage'), ('E', 'Car wash'), ('F', 'Le klaxeur fou'), ('G', 'Cuisine'), ('H', 'Courses')], help_text='Which type of allo', max_length=1)),
                ('start_date', models.DateTimeField(help_text='YYYY-MM-DD HH:MM:SS')),
                ('end_date', models.DateTimeField(help_text='YYYY-MM-DD HH:MM:SS')),
                ('description', models.CharField(max_length=1024)),
                ('cost', models.DecimalField(decimal_places=2, default=1.0, max_digits=12)),
                ('visible', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Bets',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('bet_name', models.CharField(max_length=256, unique=True)),
                ('win_rate', models.DecimalField(decimal_places=2, default=2.0, max_digits=4)),
                ('win_vote', models.IntegerField(default=0)),
                ('win_gains', models.DecimalField(decimal_places=2, default=1.0, max_digits=12)),
                ('win_name', models.CharField(default='Oui', max_length=128)),
                ('lose_rate', models.DecimalField(decimal_places=2, default=2.0, max_digits=4)),
                ('lose_vote', models.IntegerField(default=0)),
                ('lose_gains', models.DecimalField(decimal_places=2, default=1.0, max_digits=12)),
                ('lose_name', models.CharField(default='Non', max_length=128)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('ended', models.DateTimeField(help_text='YYYY-MM-DD HH:MM:SS')),
                ('visible', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('event_name', models.CharField(max_length=256, unique=True)),
                ('event_description', models.CharField(max_length=1024)),
                ('event_type', models.CharField(blank=True, choices=[('A', 'Annonce'), ('B', 'Prévention'), ('C', "Ker'mess"), ('D', 'Soirée'), ('E', '12 Travaux du Klax')], help_text='Which type of event', max_length=1)),
                ('event_date', models.DateTimeField(help_text='YYYY-MM-DD HH:MM:SS')),
                ('attendees_number', models.IntegerField(default=0)),
                ('max_attendees', models.IntegerField(null=True)),
                ('associated_bet', models.BooleanField(default=False)),
                ('associated_html', models.BooleanField(default=False)),
                ('visible', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='StoreBets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(blank=True, choices=[('W', 'Win'), ('L', 'Lose')], help_text='Which result for the bet', max_length=1)),
                ('gains', models.DecimalField(decimal_places=2, default=1.0, max_digits=12)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('bet_rate', models.DecimalField(decimal_places=2, default=1.0, max_digits=4)),
                ('blocked_bet', models.BooleanField(default=False)),
                ('bet_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.bets')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EventsRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.event')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AllosUserCounters',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('biere', models.IntegerField(default=1)),
                ('gouter', models.IntegerField(default=0)),
                ('ptitdej', models.IntegerField(default=0)),
                ('menage', models.IntegerField(default=0)),
                ('car_wash', models.IntegerField(default=1)),
                ('klax', models.IntegerField(default=0)),
                ('cuisine', models.IntegerField(default=0)),
                ('courses', models.IntegerField(default=0)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AllosRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(help_text='YYYY-MM-DD HH:MM:SS')),
                ('take_over', models.BooleanField(default=False)),
                ('made', models.BooleanField(default=False)),
                ('staff_id', models.IntegerField(default=0)),
                ('allo_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.allos')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
