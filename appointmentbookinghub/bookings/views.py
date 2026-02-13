from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from datetime import datetime, timedelta
from .models import Booking
from specialists.models import Specialist
from patients.models import Patient
import json


@login_required
@require_http_methods(["GET"])
def booking_confirmation_view(request):
    if request.user.role != 'patient':
        return HttpResponse("Only patients can book appointments", status=403)
    
    try:
        specialist_id = request.GET.get('specialist_id')
        start_time_str = request.GET.get('start_time')
        end_time_str = request.GET.get('end_time')
        
        if not all([specialist_id, start_time_str, end_time_str]):
            return HttpResponse("Missing booking information", status=400)
        
        specialist = get_object_or_404(Specialist, id=specialist_id)
        
        # Parse datetime strings
        start_time = datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
        end_time = datetime.fromisoformat(end_time_str.replace('Z', '+00:00'))
        
        context = {
            'specialist': specialist,
            'start_time': start_time,
            'end_time': end_time,
            'start_time_iso': start_time.isoformat(),
            'end_time_iso': end_time.isoformat(),
        }
        
        return render(request, 'bookings/partials/booking_confirmation.html', context)
        
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=400)


@login_required
@require_http_methods(["POST"])
def create_booking_view(request):
    if request.user.role != 'patient':
        return HttpResponse("Only patients can create bookings", status=403)
    
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST
        
        specialist_id = data.get('specialist_id')
        start_time_str = data.get('start_time')
        end_time_str = data.get('end_time')
        
        if not all([specialist_id, start_time_str, end_time_str]):
            return render(request, 'bookings/booking_result.html', {
                'success': False,
                'message': 'Missing required booking information.'
            })
        
        specialist = get_object_or_404(Specialist, id=specialist_id)
        patient = request.user.patient_profile
        
        start_time = datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
        end_time = datetime.fromisoformat(end_time_str.replace('Z', '+00:00'))
        
        conflicting_bookings = Booking.objects.filter(
            specialist=specialist,
            start_time__lt=end_time,
            end_time__gt=start_time,
            status__in=['pending', 'confirmed']
        ).exists()
        
        if conflicting_bookings:
            return render(request, 'bookings/booking_result.html', {
                'success': False,
                'message': 'This time slot is no longer available. Please select a different time.'
            })
        
        booking = Booking.objects.create(
            patient=patient,
            specialist=specialist,
            start_time=start_time,
            end_time=end_time,
            status='pending'
        )
        
        return render(request, 'bookings/booking_result.html', {
            'success': True,
            'message': 'Your appointment has been booked successfully!',
            'booking': booking
        })
        
    except Exception as e:
        return render(request, 'bookings/booking_result.html', {
            'success': False,
            'message': f'An error occurred while booking your appointment: {str(e)}'
        })


@login_required
@require_http_methods(["POST"])
def confirm_booking_view(request, booking_id):
    if request.user.role != 'specialist':
        return HttpResponse("Only specialists can confirm bookings", status=403)
    
    booking = get_object_or_404(Booking, id=booking_id, specialist=request.user.specialist_profile)
    booking.status = 'confirmed'
    booking.save()
    
    return render(request, 'bookings/booking_row.html', {'booking': booking})


@login_required
@require_http_methods(["POST"])
def cancel_booking_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.user.role == 'specialist':
        if booking.specialist != request.user.specialist_profile:
            return HttpResponse("Unauthorized", status=403)
    elif request.user.role == 'patient':
        if booking.patient != request.user.patient_profile:
            return HttpResponse("Unauthorized", status=403)
    else:
        return HttpResponse("Unauthorized", status=403)
    
    booking.status = 'cancelled'
    booking.save()
    
    return render(request, 'bookings/booking_row.html', {'booking': booking})
