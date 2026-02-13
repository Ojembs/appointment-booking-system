# Appointment Booking System

A Django-based appointment booking system that allows patients to book appointments with medical specialists. The system features role-based authentication, real-time availability checking, and a modern HTMX-powered frontend.

## Features Implemented

### Core Booking Flow
- **Patient Registration & Authentication**: Role-based user system (patients and specialists)
- **Specialist Directory**: Browse available specialists with their specialties and profiles
- **Real-time Calendar**: Dynamic availability checking with conflict prevention
- **Two-step Booking Process**: Select time slot → Confirm details → Create booking
- **Booking Management**: View, confirm, and cancel appointments

### Technical Features
- **HTMX Integration**: Dynamic frontend updates without page refreshes
- **Timezone-aware Scheduling**: Proper handling of date/time comparisons
- **Availability System**: Weekly recurring schedules with flexible time slots
- **Conflict Prevention**: Real-time checking for overlapping appointments
- **Responsive UI**: Modern design using DaisyUI and Tailwind CSS

### User Roles
- **Patients**: Browse specialists, book appointments, view their bookings
- **Specialists**: View their bookings, manage availability, confirm/cancel appointments

## Project Structure

```
appointmentbookinghub/
├── config/                 # Django project settings
├── accounts/              # User authentication and profiles
├── patients/              # Patient-specific models and views
├── specialists/           # Specialist profiles and availability
├── bookings/              # Appointment booking system
└── dashboard/             # User dashboards
```

## Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd appointmentbookinghub
```

### 2. Install Dependencies

```bash
pip install django
```

### 3. Database Setup

Run migrations to create the database:

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

### 4. Create Sample Data

Use the management command to populate the system with sample specialists:

```bash
# Create 5 sample specialists (default)
python3 manage.py create_sample_specialists

# Create custom number of specialists
python3 manage.py create_sample_specialists --count=10
```

This command creates:
- User accounts for specialists (username: dr_smith, dr_johnson, etc.)
- Specialist profiles with different specialties
- Weekly availability schedules
- Default password: `testpass123` for all sample users

### 5. Create Admin User (Optional)

```bash
python3 manage.py createsuperuser
```

### 6. Run the Server

```bash
python3 manage.py runserver
```

Visit `http://127.0.0.1:8000` to access the application.

## Usage Guide

### For Patients

1. **Register**: Create a patient account at `/register`
2. **Browse Specialists**: View available specialists and their profiles
3. **Book Appointment**: 
   - Select a specialist
   - Choose an available date
   - Pick a time slot
   - Confirm booking details
4. **Manage Bookings**: View and cancel your appointments

### For Specialists

1. **Register**: Create a specialist account (or use sample data)
2. **Dashboard**: View incoming appointment requests
3. **Manage Bookings**: Confirm or cancel appointments
4. **Availability**: (Future feature) Manage your schedule

## Management Commands

### Create Sample Specialists

```bash
python3 manage.py create_sample_specialists [--count=N]
```

**Options:**
- `--count`: Number of specialists to create (default: 5)

**What it creates:**
- Dr. John Smith (Cardiology) - Available Mon/Tue/Wed/Fri
- Dr. Sarah Johnson (Dermatology) - Available Tue/Wed/Thu/Fri
- Dr. Michael Brown (Orthopedics) - Available Mon/Wed/Fri
- Dr. Emily Davis (Pediatrics) - Available Mon-Fri
- Dr. Robert Wilson (Internal Medicine) - Available Tue/Thu/Fri

**Sample Login Credentials:**
- Username: `dr_smith`, `dr_johnson`, `dr_brown`, `dr_davis`, `dr_wilson`
- Password: `testpass123`
- Role: specialist

## Development

### Project Architecture

- **Models**: User → Patient/Specialist → Booking → Availability
- **Views**: Function-based views with HTMX support
- **Templates**: DaisyUI components with responsive design
- **URL Structure**: App-based routing with namespaces

### Key Files

- `specialists/views.py` - Calendar and availability logic
- `bookings/views.py` - Booking creation and management
- `specialists/management/commands/create_sample_specialists.py` - Data generation
- `templates/` - HTMX-powered frontend templates

### Testing the Booking Flow

1. Run `python3 manage.py create_sample_specialists`
2. Create a patient account via `/register`
3. Navigate to `/specialists/` to browse specialists
4. Click on a specialist to view their profile
5. Select a date to see available time slots
6. Click a time slot to see booking confirmation
7. Confirm the booking to create the appointment

## API Endpoints

- `GET /specialists/` - List all specialists
- `GET /specialists/<id>/` - Specialist detail and booking interface
- `GET /specialists/<id>/calendar?date=YYYY-MM-DD` - Available time slots
- `GET /bookings/confirm-booking/` - Booking confirmation form
- `POST /bookings/create/` - Create new booking
- `POST /bookings/<id>/confirm/` - Confirm existing booking
- `POST /bookings/<id>/cancel/` - Cancel booking

## Troubleshooting

### Common Issues

1. **CSRF Token Missing**: HTMX requests include CSRF tokens automatically via JavaScript configuration
2. **Timezone Errors**: All datetime objects are timezone-aware using Django's timezone utilities
3. **Migration Issues**: Run `python3 manage.py makemigrations` before `migrate`
4. **Sample Data**: Use the management command to quickly populate test data

### Database Reset

To start fresh:
```bash
rm db.sqlite3
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py create_sample_specialists
```
