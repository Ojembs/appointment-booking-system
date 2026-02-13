from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from bookings.models import Booking
from specialists.models import Specialist


@login_required
def dashboard_view(request):
    user = request.user
    context = {"user": user}

    if user.role == 'patient':
        patient_bookings = Booking.objects.filter(
            patient=user.patient_profile
        ).select_related('specialist__user').order_by('-start_time')
        context['patient_bookings'] = patient_bookings

    elif user.role == 'specialist':
        specialist_bookings = Booking.objects.filter(
            specialist=user.specialist_profile
        ).select_related('patient__user').order_by('-start_time')
        context['specialist_bookings'] = specialist_bookings
        
        pending_count = specialist_bookings.filter(status='pending').count()
        context['pending_count'] = pending_count

    return render(request, "dashboard.html", context)
