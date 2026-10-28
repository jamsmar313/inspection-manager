from datetime import date
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Inspection


@login_required
@require_POST
def quick_action(request, pk):
    # Scope changes to companies this user belongs to.
    job = get_object_or_404(
        Inspection.objects.filter(company__memberships__user=request.user).distinct(),
        pk=pk,
    )
    action = request.POST.get('action', '')
    if action == 'followup':
        value = request.POST.get('next_action_date', '')
        try:
            followup_date = date.fromisoformat(value)
        except ValueError:
            messages.error(request, 'Please enter a valid follow-up date.')
        else:
            job.next_action_date = followup_date
            job.save(update_fields=['next_action_date', 'updated_at'])
            messages.success(request, f'Follow-up saved for job #{job.job_number}.')
    elif action == 'inspected':
        if request.POST.get('confirm') != 'yes':
            messages.error(request, 'Confirmation required to mark inspected.')
        elif job.inspection_complete_date:
            messages.info(request, f'Job #{job.job_number} was already marked inspected.')
        else:
            job.inspection_complete_date = timezone.localdate()
            job.status = 'Inspected'
            job.save(update_fields=['inspection_complete_date', 'status', 'updated_at'])
            messages.success(request, f'Job #{job.job_number} marked inspected.')
    elif action == 'submitted':
        if request.POST.get('confirm') != 'yes':
            messages.error(request, 'Confirmation required to mark submitted.')
        elif not job.inspection_complete_date:
            messages.error(request, 'Mark this inspection completed before submitting its report.')
        elif job.report_submitted_date:
            messages.info(request, f'Job #{job.job_number} was already submitted.')
        else:
            job.report_submitted_date = timezone.localdate()
            job.status = 'Submitted'
            job.save(update_fields=['report_submitted_date', 'status', 'updated_at'])
            messages.success(request, f'Job #{job.job_number} marked submitted.')
    else:
        messages.error(request, 'Unknown quick action.')
    return redirect('worklist')
