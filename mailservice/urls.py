# In urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'trains', views.TrainViewSet)
router.register(r'parcels', views.ParcelViewSet)
router.register(r'lines', views.LineViewSet)
router.register(r'bookings', views.BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('process-shipments/', views.ProcessShipmentsAPIView.as_view(), name='process-shipments'),
]
