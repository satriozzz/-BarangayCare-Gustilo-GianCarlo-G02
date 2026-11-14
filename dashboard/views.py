
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test


@login_required
@user_passes_test(lambda user: user.role == 'OWNER')
def owner_dashboard(request):
    return render(request, 'dashboard/owner.html')


@login_required
@user_passes_test(lambda user: user.role == 'STAFF')
def staff_dashboard(request):
    return render(request, 'dashboard/staff.html')


@login_required
@user_passes_test(lambda user: user.role == 'MECHANIC')
def mechanic_dashboard(request):
    return render(request, 'dashboard/mechanic.html')
