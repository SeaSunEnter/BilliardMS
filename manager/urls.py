from django.urls import path
from . import views

app_name = 'manager'

urlpatterns = [
    # Authentication Routes
    path('', views.Index.as_view(), name='index'),
    path('register/', views.Register.as_view(), name='reg'),
    path('login/', views.LoginViewer.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('user/<int:pk>/update', views.UserUpdate.as_view(), name='user_update'),
    path('user/password_change', views.password_change, name='user_password_change'),

    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),

    # Employee Routes
    path('employee/', views.EmployeeAll.as_view(), name='employee_all'),
    path('employee/new/', views.EmployeeNew.as_view(), name='employee_new'),
    path('employee/<int:pk>/view/', views.EmployeeView.as_view(), name='employee_view'),
    path('employee/<int:pk>/update/', views.EmployeeUpdate.as_view(), name='employee_update'),
    path('employee/<int:pk>/delete/', views.EmployeeDelete.as_view(), name='employee_delete'),

    # Department Routes
    path('department/all/', views.DepartmentAll.as_view(), name='dept_all'),
    path('department/add/', views.DepartmentNew.as_view(), name='dept_new'),
    path('department/<int:pk>/update/', views.DepartmentUpdate.as_view(), name='dept_update'),

]
