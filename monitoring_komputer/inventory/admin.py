from django.contrib import admin
from .models import Komputer, RiwayatPerawatan, RiwayatKerusakan, MonitoringStatus, Komponen #, PerawatanKomponen (jika sudah ada)

@admin.register(Komputer)
class KomputerAdmin(admin.ModelAdmin):
    list_display = ('dal_code', 'machine_name', 'location', 'is_online', 'last_ping_time', 'machine_condition')
    list_filter = ('is_online', 'location', 'machine_condition', 'acquisition_year', 'group_name')
    search_fields = ('dal_code', 'machine_name', 'location', 'operator_name')
    # Menjadikan last_ping_time read-only di form admin agar tidak diedit manual
    readonly_fields = ('last_ping_time', 'is_online',)

admin.site.register(MonitoringStatus)
admin.site.register(RiwayatPerawatan)
admin.site.register(RiwayatKerusakan)
admin.site.register(Komponen)
# Jika Anda menggunakan decorator untuk RiwayatPerawatanAdmin, jangan daftarkan lagi di sini.
# admin.site.register(RiwayatPerawatan)
# Jika Anda punya model PerawatanKomponen:
# admin.site.register(PerawatanKomponen)