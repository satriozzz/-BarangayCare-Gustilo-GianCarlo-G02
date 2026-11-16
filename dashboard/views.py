from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def admin_dashboard(request):
    if request.user.role != 'ADMIN':
        return redirect('health_worker_dashboard')

    return render(request, 'dashboard/owner.html')


@login_required
def health_worker_dashboard(request):
    if request.user.role != 'HEALTH_WORKER':
        return redirect('admin_dashboard')

    return render(request, 'dashboard/staff.html')