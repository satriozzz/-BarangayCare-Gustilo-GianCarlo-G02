
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404

from .models import Patient, PatientVisit
from .forms import PatientForm, PatientVisitForm


def get_accessible_patients(user):
    if user.role == 'ADMIN':
        return Patient.objects.all()

    if user.role == 'HEALTH_WORKER':
        return Patient.objects.filter(created_by=user)

    raise PermissionDenied


def get_accessible_visits(user):
    if user.role == 'ADMIN':
        return PatientVisit.objects.all()

    if user.role == 'HEALTH_WORKER':
        return PatientVisit.objects.filter(created_by=user)

    raise PermissionDenied


# =========================
# PATIENT MANAGEMENT
# =========================

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
        'search_query': search_query
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


# =========================
# PATIENT VISIT MANAGEMENT
# =========================

@login_required
def visit_list(request):
    visits = get_accessible_visits(request.user).select_related('patient')

    return render(request, 'patients/visit_list.html', {
        'visits': visits
    })


@login_required
def visit_create(request):
    get_accessible_visits(request.user)

    if request.method == 'POST':
        form = PatientVisitForm(request.POST, user=request.user)

        if form.is_valid():
            visit = form.save(commit=False)
            visit.created_by = request.user
            visit.save()

            messages.success(request, 'Patient visit recorded successfully.')
            return redirect('visit_list')
    else:
        form = PatientVisitForm(user=request.user)

    return render(request, 'patients/visit_form.html', {
        'form': form,
        'title': 'Record Patient Visit'
    })


@login_required
def visit_detail(request, pk):
    visit = get_object_or_404(
        get_accessible_visits(request.user).select_related('patient', 'created_by'),
        pk=pk
    )
    return render(request, 'patients/visit_detail.html', {'visit': visit})

@login_required
def visit_update(request, pk):
    visit = get_object_or_404(
        get_accessible_visits(request.user),
        pk=pk
    )

    if request.method == 'POST':
        form = PatientVisitForm(
            request.POST,
            instance=visit,
            user=request.user
        )

        if form.is_valid():
            form.save()
            messages.success(request, 'Patient visit updated successfully.')
            return redirect('visit_detail', pk=visit.pk)
    else:
        form = PatientVisitForm(
            instance=visit,
            user=request.user
        )

    return render(request, 'patients/visit_form.html', {
        'form': form,
        'title': 'Edit Patient Visit'
    })


@login_required
def visit_delete(request, pk):
    visit = get_object_or_404(
        get_accessible_visits(request.user).select_related('patient'),
        pk=pk
    )

    if request.method == 'POST':
        visit.delete()
        messages.success(request, 'Patient visit deleted successfully.')
        return redirect('visit_list')

    return render(request, 'patients/visit_confirm_delete.html', {
        'visit': visit
    })
