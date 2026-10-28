import calendar
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from .models import Inspection


def _jobs(user):
    return Inspection.objects.filter(company__memberships__user=user).distinct()


@login_required
def calendar_view(request):
    today = timezone.localdate()
    try:
        year = int(request.GET.get('year', today.year))
        month = int(request.GET.get('month', today.month))
        first = date(year, month, 1)
    except (ValueError, TypeError):
        first = today.replace(day=1)
    next_first = (first.replace(day=28) + timedelta(days=4)).replace(day=1)
    previous = first - timedelta(days=1)
    jobs = _jobs(request.user).filter(
        scheduled_at__date__gte=first,
        scheduled_at__date__lt=next_first,
    ).order_by('scheduled_at', 'job_number')
    by_day = {}
    for job in jobs:
        day = timezone.localtime(job.scheduled_at).date()
        by_day.setdefault(day, []).append(job)
    weeks = [
        [{'date': day, 'jobs': by_day.get(day, []), 'current_month': day.month == first.month, 'today': day == today}
         for day in week]
        for week in calendar.Calendar(firstweekday=6).monthdatescalendar(first.year, first.month)
    ]
    return render(request, 'inspections/calendar.html', {
        'weeks': weeks, 'month_label': first.strftime('%B %Y'),
        'prev_year': previous.year, 'prev_month': previous.month,
        'next_year': next_first.year, 'next_month': next_first.month,
    })


@login_required
def worklist_view(request):
    today = timezone.localdate()
    qs = _jobs(request.user)
    today_jobs = qs.filter(scheduled_at__date=today).order_by('scheduled_at')
    overdue = qs.filter(next_action_date__lt=today).exclude(status__iexact='Paid').order_by('next_action_date')
    calls = qs.filter(status__in=['New', 'Call Needed', 'CALL', 'Call']).order_by('date_assigned', 'job_number')
    reports = qs.filter(inspection_complete_date__isnull=False, report_submitted_date__isnull=True).order_by('inspection_complete_date')
    payments = qs.filter(report_submitted_date__isnull=False, paid=False).order_by('report_submitted_date')
    return render(request, 'inspections/worklist.html', {
        'today': today, 'today_jobs': today_jobs[:100], 'overdue': overdue[:100],
        'calls': calls[:100], 'reports': reports[:100], 'payments': payments[:100],
    })
