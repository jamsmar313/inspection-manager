from django import forms
from .models import Inspection


class InspectionForm(forms.ModelForm):
    scheduled_at = forms.SplitDateTimeField(
        required=False,
        widget=forms.SplitDateTimeWidget(
            date_attrs={'type': 'date', 'class': 'form-control'},
            time_attrs={'type': 'time', 'class': 'form-control'},
        ),
    )

    class Meta:
        model = Inspection
        fields = [
            'insured_name', 'property_address', 'town', 'area', 'phone',
            'policy_number', 'insurance_carrier', 'inspection_company',
            'date_assigned', 'job_fee', 'status', 'scheduled_at',
            'inspection_complete_date', 'report_submitted_date',
            'paid', 'payment_date', 'next_action_date',
            'contact_notes', 'general_notes', 'field_notes',
        ]
        widgets = {
            'date_assigned': forms.DateInput(attrs={'type': 'date'}),
            'inspection_complete_date': forms.DateInput(attrs={'type': 'date'}),
            'report_submitted_date': forms.DateInput(attrs={'type': 'date'}),
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
            'next_action_date': forms.DateInput(attrs={'type': 'date'}),
            'contact_notes': forms.Textarea(attrs={'rows': 3}),
            'general_notes': forms.Textarea(attrs={'rows': 3}),
            'field_notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            elif isinstance(field.widget, forms.SplitDateTimeWidget):
                continue
            else:
                field.widget.attrs['class'] = 'form-control'
