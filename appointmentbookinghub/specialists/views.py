from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Specialist, Availability
from bookings.models import Booking


@login_required
def specialist_list_view(request):
    specialists = Specialist.objects.select_related('user').all()
    
    context = {
        'specialists': specialists,
        'user': request.user
    }
    
    return render(request, 'specialists/specialist_list.html', context)


@login_required 
def specialist_detail_view(request, specialist_id):
    specialist = get_object_or_404(Specialist, id=specialist_id)
    
    availabilities = Availability.objects.filter(specialist=specialist).order_by('weekday', 'start_time')
    
    context = {
        'specialist': specialist,
        'availabilities': availabilities,
        'user': request.user
    }
    
    return render(request, 'specialists/specialist_detail.html', context)


@login_required
def specialist_calendar_view(request, specialist_id):
    specialist = get_object_or_404(Specialist, id=specialist_id)
    date_str = request.GET.get('date', timezone.now().date().isoformat())
    
    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        selected_date = timezone.now().date()
    
    weekday = selected_date.weekday() 
    
    availabilities = Availability.objects.filter(
        specialist=specialist, 
        weekday=weekday
    )
    
    existing_bookings = Booking.objects.filter(
        specialist=specialist,
        start_time__date=selected_date,
        status__in=['pending', 'confirmed']
    )
    
    available_slots = []
    for availability in availabilities:
        current_time = timezone.make_aware(
            datetime.combine(selected_date, availability.start_time),
            timezone.get_current_timezone()
        )
        end_time = timezone.make_aware(
            datetime.combine(selected_date, availability.end_time),
            timezone.get_current_timezone()
        )
        
        while current_time < end_time:
            slot_end = current_time + timedelta(minutes=60)

            is_available = True
            for booking in existing_bookings:
                if booking.start_time < slot_end and booking.end_time > current_time:
                    is_available = False
                    break

            if is_available:
                available_slots.append({
                    'start_time': current_time.isoformat(),
                    'display_time': current_time.strftime('%I:%M %p'),
                    'end_time': slot_end.isoformat()
                })

            current_time = slot_end

    
    context = {
        'specialist': specialist,
        'date': selected_date,
        'available_slots': available_slots
    }
    
    return render(request, 'specialists/partials/available_slots.html', context)