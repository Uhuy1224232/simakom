# inventory/models.py
from django.db import models
from django.utils import timezone

# inventory/models.py
class Komputer(models.Model):
    sap_code = models.CharField(max_length=100, null=True, blank=True)
    dal_code = models.CharField(max_length=100, unique=True)
    inventory_code = models.CharField(max_length=100, null=True, blank=True)
    machine_name = models.CharField(max_length=255)
    acquisition_year = models.IntegerField()
    location = models.CharField(max_length=255)
    cost_center = models.CharField(max_length=100, null=True, blank=True)
    operator_name = models.CharField(max_length=100)
    MACHINE_CONDITION_CHOICES = [
        ('A', 'Baik Sekali'),
        ('B', 'Baik'),
        ('C', 'Kurang Baik'),
        ('D', 'Rusak'),
    ]
    machine_condition = models.CharField(max_length=50, choices=MACHINE_CONDITION_CHOICES, default='B')
    group_id = models.IntegerField()
    group_name = models.CharField(max_length=100)

    # Kolom dari model Komputer Anda sebelumnya yang tidak ada di CSV komputer.csv
    # Penanggung_jawab, spesifikasi, status_aset, status_pinjaman, tanggal_masuk
    # Anda perlu memutuskan apakah akan mempertahankan ini, menghapusnya, atau menyesuaikannya.
    # Untuk menyesuaikan dengan CSV, saya akan menghapusnya.
    # Jika Anda ingin mempertahankannya, pertimbangkan apakah mereka bisa null atau tidak.
    # Misalnya:
    # penanggung_jawab = models.CharField(max_length=100, null=True, blank=True)
    # spesifikasi = models.TextField(null=True, blank=True)
    # status_aset = models.CharField(max_length=50, null=True, blank=True)
    # status_pinjaman = models.CharField(max_length=50, null=True, blank=True)
    # tanggal_masuk = models.DateField(null=True, blank=True)

    last_ping_time = models.DateTimeField(null=True, blank=True)
    is_online = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Komputer"
        verbose_name_plural = "Komputer"

    def __str__(self):
        return f"{self.machine_name} ({self.dal_code})"

# ---------- MODEL BARU: Komponen ----------
class Komponen(models.Model):
    matgroup_id = models.IntegerField() # int64 di CSV
    material_id = models.CharField(max_length=100, unique=True) # Diasumsikan unik
    material_name = models.CharField(max_length=255)
    price = models.IntegerField() # int64 di CSV
    price_reference = models.CharField(max_length=255)
    safety_stock = models.IntegerField() # int64 di CSV
    unit = models.CharField(max_length=50)
    type_id = models.IntegerField(null=True, blank=True) # float64, ada null
    is_disposable = models.BooleanField(default=False) # int64 (1/0) di CSV, gunakan BooleanField
    label = models.CharField(max_length=255, null=True, blank=True) # Ada null di data
    cat_id = models.IntegerField() # int64 di CSV
    # sloc_id = models.FloatField(null=True, blank=True) # Semua null di data, mungkin tidak perlu disimpan?
    group_id = models.IntegerField() # int64 di CSV
    stock = models.IntegerField() # int64 di CSV
    broken_stock = models.IntegerField() # int64 di CSV
    types = models.CharField(max_length=100, null=True, blank=True) # Ada null di data
    cat_name = models.CharField(max_length=100)
    # cat_logo = models.FloatField(null=True, blank=True) # Semua null di data, mungkin tidak perlu disimpan?

    class Meta:
        verbose_name = "Komponen"
        verbose_name_plural = "Komponen"

    def __str__(self):
        return self.material_name

# Model-model yang berhubungan dengan Komputer (tidak berubah, sesuaikan Foreign Key jika Anda mengganti PK Komputer)
# Jika Anda mempertahankan Komputer.id sebagai PK, tidak ada perubahan di sini.
class RiwayatPerawatan(models.Model):
    komputer = models.ForeignKey(Komputer, on_delete=models.CASCADE, related_name='riwayat_perawatan')
    tanggal = models.DateField()
    deskripsi = models.TextField()

    def __str__(self):
        return f"Perawatan {self.komputer.machine_name} - {self.tanggal}"

class RiwayatKerusakan(models.Model):
    komputer = models.ForeignKey(Komputer, on_delete=models.CASCADE, related_name='riwayat_kerusakan')
    tanggal = models.DateField()
    deskripsi = models.TextField()

    def __str__(self):
        return f"Kerusakan {self.komputer.machine_name} - {self.tanggal}"

class MonitoringStatus(models.Model):
    komputer = models.ForeignKey(Komputer, on_delete=models.CASCADE, related_name='monitoring_status')
    waktu = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=100, default='unknown')

    def __str__(self):
        return f"{self.komputer.machine_name} - {self.status} @ {self.waktu}"