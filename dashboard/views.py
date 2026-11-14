
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test


def role_required(role):
    def check_role(user):
        return user.is_authenticated and user.role == role
    return user_passes_test(check_role, login_url='login', redirect_field_name=None)


@login_required
def owner_dashboard(request):
    if request.user.role != 'OWNER':
        return redirect('staff_dashboard' if request.user.role == 'STAFF' else 'mechanic_dashboard')
    return render(request, 'dashboard/owner.html')


@login_required
def staff_dashboard(request):
    if request.user.role != 'STAFF':
        if request.user.role == 'OWNER':
            return redirect('owner_dashboard')
        return redirect('mechanic_dashboard')
    return render(request, 'dashboard/staff.html')


@login_required
def mechanic_dashboard(request):
    if request.user.role != 'MECHANIC':
        if request.user.role == 'OWNER':
            return redirect('owner_dashboard')
        return redirect('staff_dashboard')
    return render(request, 'dashboard/mechanic.html')
