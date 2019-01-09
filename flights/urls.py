from django.urls import path
from . import views

app_name = 'flights'

urlpatterns = [
    path('', views.FlightsListView.as_view(), name='list'),
    path('<int:pk>/<slug:slug>/', views.FlightDetailView.as_view(), name='detail'),
    path('mine', views.MineOrders.as_view(), name='mine'),

    path('flight/create/', views.CreateFlight.as_view(), name='create'),
    path('flight/<int:pk>/edit', views.EditFlight.as_view(), name='edit'),
    path('flight<int:pk>/delete', views.DeleteFlight.as_view(), name='delete'),
]