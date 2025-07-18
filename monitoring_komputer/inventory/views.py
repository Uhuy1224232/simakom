# simakom/monitoring_komputer/inventory/views.py

from rest_framework import viewsets
# Hapus impor duplikat dan gabungkan
from rest_framework.permissions import IsAuthenticated, IsAdminUser # Pastikan keduanya terimpor
from django.contrib.auth.models import User # Pastikan model User terimpor

# Pastikan SEMUA serializer diimpor di SATU baris ini
from .serializers import (
    KomputerSerializer,
    MonitoringStatusSerializer,
    RiwayatKerusakanSerializer,
    RiwayatPerawatanSerializer,
    KomponenSerializer,
    UserSerializer # <--- PASTIKAN UserSerializer ADA DI SINI SEKARANG!
)

# Impor model aplikasi Anda
from .models import Komputer, MonitoringStatus, RiwayatKerusakan, RiwayatPerawatan, Komponen

# Pindahkan UserViewSet ke bawah agar UserSerializer sudah diimpor saat didefinisikan
# Urutan class ViewSet tidak masalah, tapi impor harus di atas semua definisi class

class KomputerViewSet(viewsets.ModelViewSet):
    queryset = Komputer.objects.all()
    serializer_class = KomputerSerializer
    permission_classes = [IsAuthenticated]

class MonitoringStatusViewSet(viewsets.ModelViewSet):
    queryset = MonitoringStatus.objects.all()
    serializer_class = MonitoringStatusSerializer
    permission_classes = [IsAuthenticated]

class RiwayatKerusakanViewSet(viewsets.ModelViewSet):
    queryset = RiwayatKerusakan.objects.all()
    serializer_class = RiwayatKerusakanSerializer
    permission_classes = [IsAuthenticated]

class RiwayatPerawatanViewSet(viewsets.ModelViewSet):
    queryset = RiwayatPerawatan.objects.all()
    serializer_class = RiwayatPerawatanSerializer
    permission_classes = [IsAuthenticated]

class KomponenViewSet(viewsets.ModelViewSet):
    queryset = Komponen.objects.all()
    serializer_class = KomponenSerializer
    permission_classes = [IsAuthenticated]

# Pindahkan UserViewSet ke posisi yang lebih logis (setelah semua impor)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer # Sekarang UserSerializer sudah diimpor
    permission_classes = [IsAdminUser]
    # Jika Anda ingin user terautentikasi biasa bisa melihat daftar, tapi admin bisa CRUD:
    # def get_permissions(self):
    #     if self.action in ['list', 'retrieve']:
    #         permission_classes = [IsAuthenticated]
    #     else:
    #         permission_classes = [IsAdminUser]
    #     return [permission() for permission in permission_classes]