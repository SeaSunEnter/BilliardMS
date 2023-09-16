from django.urls import path
from . import views

app_name = 'tabler'

urlpatterns = [
    # TableBType Routes
    path('tablebtype/', views.TableBTypeAll.as_view(), name='tab_type_all'),
    path('tablebtype/add/', views.TableBTypeNew.as_view(), name='tab_type_new'),
    path('tablebtype/<int:pk>/update/', views.TableBTypeUpdate.as_view(), name='tab_type_update'),

    # TableB Routes
    path('tableb/', views.TableBAll.as_view(), name='tab_all'),
    path('tableb/new/', views.TableBNew.as_view(), name='tab_new'),
    path('tableb/<int:pk>/view/', views.TableBView.as_view(), name='tab_view'),
    path('tableb/<int:pk>/update/', views.TableBUpdate.as_view(), name='tab_update'),
    path('tableb/<int:pk>/delete/', views.TableBDelete.as_view(), name='tab_delete'),

    path('tablebactive/<int:pk>/new/', views.TableBActiveNew.as_view(), name='tab_act_new'),
    path('tablebactive/<int:pk>/ok/', views.TableBActiveOK.as_view(), name='tab_act_ok'),
    path('tablebactive/<int:pk>/order/', views.TableBActOrder.as_view(), name='tab_act_order'),
    path('tablebactive/<int:pk>/split/', views.TableBActSplit.as_view(), name='tab_act_split'),
    path('tablebactive/<int:pk>/askfinish/', views.TableBActAskFinish.as_view(), name='tab_act_ask_finish'),
    path('tablebactive/<int:pk>/finish/', views.TableBActFinish.as_view(), name='tab_act_finish'),
]
