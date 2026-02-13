from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from specialists.models import Specialist, Availability
from datetime import time

User = get_user_model()


class Command(BaseCommand):
    help = 'Create sample specialist data for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=5,
            help='Number of specialists to create (default: 5)'
        )

    def handle(self, *args, **options):
        count = options['count']
        
        sample_data = [
            {
                'username': 'dr_smith',
                'email': 'dr.smith@clinic.com',
                'first_name': 'John',
                'last_name': 'Smith',
                'specialty': 'Cardiology',
                'bio': 'Experienced cardiologist with 15+ years in practice. Specializing in preventive cardiology and heart disease management.',
                'availability': [
                    (0, time(9, 0), time(17, 0)),  # Monday
                    (1, time(9, 0), time(17, 0)),  # Tuesday
                    (2, time(9, 0), time(17, 0)),  # Wednesday
                    (4, time(9, 0), time(15, 0)),  # Friday
                ]
            },
            {
                'username': 'dr_johnson',
                'email': 'dr.johnson@clinic.com',
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'specialty': 'Dermatology',
                'bio': 'Board-certified dermatologist specializing in skin cancer prevention and cosmetic dermatology.',
                'availability': [
                    (1, time(10, 0), time(18, 0)),  # Tuesday
                    (2, time(10, 0), time(18, 0)),  # Wednesday
                    (3, time(10, 0), time(18, 0)),  # Thursday
                    (4, time(10, 0), time(16, 0)),  # Friday
                ]
            },
            {
                'username': 'dr_brown',
                'email': 'dr.brown@clinic.com',
                'first_name': 'Michael',
                'last_name': 'Brown',
                'specialty': 'Orthopedics',
                'bio': 'Orthopedic surgeon with expertise in sports medicine and joint replacement.',
                'availability': [
                    (0, time(8, 0), time(16, 0)),  # Monday
                    (2, time(8, 0), time(16, 0)),  # Wednesday
                    (4, time(8, 0), time(12, 0)),  # Friday
                ]
            },
            {
                'username': 'dr_davis',
                'email': 'dr.davis@clinic.com',
                'first_name': 'Emily',
                'last_name': 'Davis',
                'specialty': 'Pediatrics',
                'bio': 'Pediatrician dedicated to providing comprehensive healthcare for children from birth to adolescence.',
                'availability': [
                    (0, time(9, 0), time(17, 0)),  # Monday
                    (1, time(9, 0), time(17, 0)),  # Tuesday
                    (2, time(9, 0), time(17, 0)),  # Wednesday
                    (3, time(9, 0), time(17, 0)),  # Thursday
                    (4, time(9, 0), time(13, 0)),  # Friday
                ]
            },
            {
                'username': 'dr_wilson',
                'email': 'dr.wilson@clinic.com',
                'first_name': 'Robert',
                'last_name': 'Wilson',
                'specialty': 'Internal Medicine',
                'bio': 'Internal medicine physician focused on adult primary care and chronic disease management.',
                'availability': [
                    (1, time(8, 30), time(16, 30)),  # Tuesday
                    (3, time(8, 30), time(16, 30)),  # Thursday
                    (4, time(8, 30), time(14, 0)),   # Friday
                ]
            }
        ]

        created_count = 0
        for i, data in enumerate(sample_data[:count]):
            # Create user if doesn't exist
            user, user_created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'email': data['email'],
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'is_active': True,
                }
            )
            
            if user_created:
                user.set_password('testpass123')
                user.save()
                self.stdout.write(f"Created user: {user.username}")
            
            # Create specialist profile if doesn't exist
            specialist, spec_created = Specialist.objects.get_or_create(
                user=user,
                defaults={
                    'specialty': data['specialty'],
                    'bio': data['bio'],
                }
            )
            
            if spec_created:
                self.stdout.write(f"Created specialist: {specialist}")
                
                # Create availability slots
                for weekday, start_time, end_time in data['availability']:
                    Availability.objects.get_or_create(
                        specialist=specialist,
                        weekday=weekday,
                        start_time=start_time,
                        defaults={'end_time': end_time}
                    )
                
                created_count += 1
            else:
                self.stdout.write(f"Specialist already exists: {specialist}")
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} new specialists'
            )
        )