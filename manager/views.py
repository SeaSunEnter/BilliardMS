import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, resolve_url, reverse
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model, logout
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView

from manager.forms import RegistrationForm, UserUpdateForm, LoginForm, SetPasswordForm, EmployeeForm, DepartmentForm
from manager.models import LoginLogs, Employee, Department
from tabler.models import TableB, TableBActive


# Create your views here.

class Index(TemplateView):
    template_name = 'manager/home/home.html'


# Authentication
class Register(CreateView):
    model = get_user_model()
    form_class = RegistrationForm
    template_name = 'manager/registrations/register.html'
    success_url = reverse_lazy('manager:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logs'] = LoginLogs.objects.all()
        return context


class LoginViewer(LoginView):
    model = get_user_model()
    form_class = LoginForm
    template_name = 'manager/registrations/login.html'

    def get_success_url(self):
        if self.request.user.is_authenticated:
            cur_user = self.request.user
            LoginLogs.objects.create(user=cur_user)

        url = resolve_url('manager:dashboard')
        return url


class LogoutView(View):

    def get(self, request):
        logout(self.request)
        return redirect('manager:login', permanent=True)


class UserUpdate(UpdateView):
    model = get_user_model()
    form_class = UserUpdateForm
    template_name = 'manager/registrations/user_update.html'

    def get_success_url(self):
        url = resolve_url('manager:dashboard')
        return url


@login_required
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect('manager:login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'manager/registrations/user_pass_change.html', {'form': form})


# Main Board
class Dashboard(LoginRequiredMixin, ListView):
    template_name = 'manager/dashboard/index.html'
    model = get_user_model()
    login_url = 'manager:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['admin_count'] = get_user_model().objects.all().count()
        context['TableBs'] = TableB.objects.all()
        context['TableBActives'] = TableBActive.objects.all()
        return context


# Department views
class DepartmentAll(LoginRequiredMixin, ListView):
    template_name = 'manager/department/index.html'
    login_url = 'manager:login'
    model = get_user_model()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['admin_count'] = get_user_model().objects.all().count()
        context['departments'] = Department.objects.order_by('id')
        return context


"""
  def get_queryset(self):
    queryset = Employee.objects.filter(department=self.kwargs['pk'])
    return queryset
"""


class DepartmentNew(LoginRequiredMixin, CreateView):
    template_name = 'manager/department/create.html'
    model = Department
    form_class = DepartmentForm
    login_url = 'manager:login'
    success_url = reverse_lazy('manager:dept_all')


class DepartmentUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'manager/department/edit.html'
    model = Department
    form_class = DepartmentForm
    login_url = 'manager:login'
    success_url = reverse_lazy('manager:dept_all')


# Employee's Controller
class EmployeeNew(LoginRequiredMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'manager/employee/create.html'
    login_url = 'manager:login'
    success_url = reverse_lazy('manager:employee_all')


class EmployeeAll(LoginRequiredMixin, ListView):
    template_name = 'manager/employee/overview.html'
    model = Employee
    login_url = 'manager:login'
    context_object_name = 'employees'
    paginate_by = 5


class EmployeeView(LoginRequiredMixin, DetailView):
    queryset = Employee.objects.select_related('department')
    template_name = 'manager/employee/single.html'
    context_object_name = 'employee'
    login_url = 'manager:login'


"""
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    try:
      query = Kin.objects.get(employee=self.object.pk)
      context["kin"] = query
      return context
    except ObjectDoesNotExist:
      return context
"""


class EmployeeUpdate(LoginRequiredMixin, UpdateView):
    model = Employee
    template_name = 'manager/employee/edit.html'
    form_class = EmployeeForm
    login_url = 'manager:login'

    # success_url = reverse_lazy('manager:employee_all')
    def get_success_url(self):
        return reverse('manager:employee_view', kwargs={'pk': self.kwargs['pk']})


class EmployeeDelete(LoginRequiredMixin, DeleteView):
    pass
