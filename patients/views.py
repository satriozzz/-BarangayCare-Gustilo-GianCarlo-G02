from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Patient
from .forms import PatientForm


@login_required
def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patients/patient_list.html', {
        'patients': patients
    })


@login_required
def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.created_by = request.user
            patient.save()
            messages.success(request, 'Patient registered successfully.')
            return redirect('patient_list')
    else:
        form = PatientForm()

    return render(request, 'patients/patient_form.html', {
        'form': form,
        'title': 'Register Patient'
    })


@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, 'patients/patient_detail.html', {
        'patient': patient
    })


@login_required
def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk)

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient record updated successfully.')
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = PatientForm(instance=patient)

    return render(request, 'patients/patient_form.html', {
        'form': form,
        'title': 'Edit Patient'
    })


@login_required
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)

    if request.method == 'POST':
        patient.delete()
        messages.success(request, 'Patient record deleted successfully.')
        return redirect('patient_list')

    return render(request, 'patients/patient_confirm_delete.html', {
        'patient': patient
    })