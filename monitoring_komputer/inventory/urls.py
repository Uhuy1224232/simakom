from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import KomputerViewSet, MonitoringStatusViewSet, RiwayatKerusakanViewSet, RiwayatPerawatanViewSet, KomponenViewSet, UserViewSet

router = DefaultRouter()
router.register(r'komputer', KomputerViewSet)
router.register(r'monitoring_status', MonitoringStatusViewSet)
router.register(r'riwayat_kerusakan', RiwayatKerusakanViewSet)
router.register(r'riwayat_perawatan', RiwayatPerawatanViewSet)
router.register(r'komponen', KomponenViewSet) # Tambahkan ini
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]