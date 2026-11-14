from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, ProfileUpdateForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(
            self.request, 
            'Your account has been created successfully!')
        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.role == 'OWNER':
            return reverse_lazy('owner_dashboard')
        elif user.role == 'STAFF':
            return reverse_lazy('staff_dashboard')
        elif user.role == 'MECHANIC':
            return reverse_lazy('mechanic_dashboard')

        return reverse_lazy('login')  


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

# PROFILE VIEW
@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')


# PROFILE EDIT VIEW
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
