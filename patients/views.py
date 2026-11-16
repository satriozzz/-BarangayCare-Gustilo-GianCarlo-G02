
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.db import models

from .models import Patient
from .forms import PatientForm


def get_accessible_patients(user):
    if user.role == 'ADMIN':
        return Patient.objects.all()

    if user.role == 'HEALTH_WORKER':
        return Patient.objects.filter(created_by=user)

    raise PermissionDenied


@login_required
def patient_list(request):
    patients = get_accessible_patients(request.user)

    search_query = request.GET.get('search', '').strip()

    if search_query:
        patients = patients.filter(
            models.Q(first_name__icontains=search_query) |
            models.Q(middle_name__icontains=search_query) |
            models.Q(last_name__icontains=search_query)
        )

    return render(request, 'patients/patient_list.html', {
        'patients': patients,
        'search_query': search_query,
    })


@login_required
def patient_create(request):
    get_accessible_patients(request.user)

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
    patient = get_object_or_404(
        get_accessible_patients(request.user),
        pk=pk
    )

    return render(request, 'patients/patient_detail.html', {
        'patient': patient
    })


@login_required
def patient_update(request, pk):
    patient = get_object_or_404(
        get_accessible_patients(request.user),
        pk=pk
    )

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
    patient = get_object_or_404(
        get_accessible_patients(request.user),
        pk=pk
    )

    if request.method == 'POST':
        patient.delete()
        messages.success(request, 'Patient record deleted successfully.')
        return redirect('patient_list')

    return render(request, 'patients/patient_confirm_delete.html', {
        'patient': patient
    })
