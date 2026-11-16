from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ProfileUpdateForm, CustomAuthenticationForm


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = CustomAuthenticationForm

    def get_success_url(self):
        user = self.request.user

        if user.role == 'ADMIN':
            return reverse_lazy('admin_dashboard')
        elif user.role == 'HEALTH_WORKER':
            return reverse_lazy('health_worker_dashboard')

        return reverse_lazy('login')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')


@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(
        request,
        'accounts/profile_edit.html',
        {'form': form}
    )