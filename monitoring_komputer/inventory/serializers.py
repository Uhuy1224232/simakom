# simakom/monitoring_komputer/inventory/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User # Impor model User
from .models import Komputer, MonitoringStatus, RiwayatKerusakan, RiwayatPerawatan, Komponen

# Letakkan UserSerializer bersama serializer lainnya untuk konsistensi
class UserSerializer(serializers.ModelSerializer):
    # Tambahkan password sebagai write-only field untuk pembuatan user baru atau perubahan password.
    # required=False saat edit, agar password tidak wajib diisi jika tidak ingin diubah.
    password = serializers.CharField(write_only=True, required=False) #

    class Meta:
        model = User
        # Tambahkan 'password' ke daftar fields yang akan diekspos (tapi sebagai write-only)
        fields = ['id', 'username', 'email', 'is_staff', 'is_active', 'date_joined', 'password']
        # 'id' dan 'date_joined' adalah read-only fields.
        # 'username' juga disarankan read_only_fields jika Anda tidak ingin mengizinkan perubahan username setelah dibuat.
        read_only_fields = ['id', 'date_joined'] #

    # Metode untuk membuat user baru (penting untuk hashing password)
    def create(self, validated_data): #
        # Ekstrak password dari data yang divalidasi
        password = validated_data.pop('password', None)
        # Buat user baru tanpa password dulu
        user = User.objects.create(**validated_data) #
        if password is not None:
            user.set_password(password) # Hashing password
            user.save() # Simpan user dengan password yang di-hash
        return user

    # Metode untuk mengupdate user (jika password juga mau diupdate)
    def update(self, instance, validated_data): #
        # Perbarui field lainnya
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value) # Hashing password baru jika diberikan
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

class KomputerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Komputer
        fields = '__all__' # Ini akan otomatis menyertakan last_ping_time dan is_online


class MonitoringStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringStatus
        fields = '__all__'

class RiwayatKerusakanSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiwayatKerusakan
        fields = '__all__'

class RiwayatPerawatanSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiwayatPerawatan
        fields = '__all__'

class KomponenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Komponen
        fields = '__all__'