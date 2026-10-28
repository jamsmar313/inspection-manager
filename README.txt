INSPECTION EDITING UPDATE — EXISTING DJANGO PROJECT

This update adds a new forms.py and edit.html, plus instructions to add a view and URL.
It does NOT replace your existing views.py, urls.py, models.py or database.

1. BACK UP YOUR PROJECT, ESPECIALLY db.sqlite3.
2. Copy inspections/forms.py to your project's inspections/forms.py.
3. Copy inspections/templates/inspections/edit.html to the same location in your project.
4. Append this code to the END of inspections/views.py:

from django.contrib import messages
from django.shortcuts import redirect
from .forms import InspectionForm

@login_required
def job_edit(request, pk):
    job = get_object_or_404(company_queryset(request.user), pk=pk)
    if request.method == 'POST':
        form = InspectionForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inspection updated successfully.')
            return redirect('job_detail', pk=job.pk)
    else:
        form = InspectionForm(instance=job)
    return render(request, 'inspections/edit.html', {'job': job, 'form': form})

5. Inside urlpatterns in config/urls.py add:

    path('jobs/<int:pk>/edit/', views.job_edit, name='job_edit'),

6. In inspections/templates/inspections/detail.html, add a link near the top:

    <a class="btn btn-primary" href="{% url 'job_edit' job.pk %}">Edit inspection</a>

7. Run: python manage.py check
8. Restart server and open a job; click Edit inspection.

NOTES:
- Existing import URL and import code remain untouched.
- This form does not edit the job number or company.
- This form requires a logged-in user who belongs to the job's company.
- Django's timezone settings may affect displayed appointment times.
- There are no database migrations for this update.
