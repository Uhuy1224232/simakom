# inventory/tasks.py
import platform
import subprocess
from django.utils import timezone
from .models import Komputer
from celery import shared_task


@shared_task
def check_computer_status_task():
    """
    Celery task untuk melakukan ping ke setiap komputer yang terdaftar
    dan memperbarui status online serta waktu ping terakhir.
    """
    print("Mulai menjalankan task check_computer_status_task...")
    computers = Komputer.objects.all()

    # Tentukan parameter ping berdasarkan OS
    param = '-n 1' if platform.system().lower() == 'windows' else '-c 1'

    for komputer in computers:
        # Pastikan dal_code ada dan tidak kosong
        if not komputer.dal_code:
            print(f"Skipping computer {komputer.machine_name} due to missing dal_code.")
            continue

        command = ['ping', param, komputer.dal_code]
        is_reachable = False
        try:
            # timeout=1: Beri waktu 1 detik untuk ping. Jika lebih, anggap gagal.
            # capture_output=True: Ambil output dan error
            # text=True: Dekode output sebagai teks
            result = subprocess.run(command, capture_output=True, text=True, timeout=1)

            # Kode kembali 0 menandakan sukses.
            # Periksa juga output untuk pesan keberhasilan spesifik OS jika diperlukan
            # Tapi returncode == 0 sudah cukup andal untuk sebagian besar kasus.
            if result.returncode == 0:
                is_reachable = True
            else:
                # Print error output jika ping gagal
                print(f"Ping to {komputer.dal_code} failed with code {result.returncode}: {result.stderr.strip()}")

        except subprocess.TimeoutExpired:
            print(f"Ping to {komputer.dal_code} timed out.")
            is_reachable = False
        except FileNotFoundError:
            print(f"Error: 'ping' command not found. Please ensure ping utility is installed and in your PATH.")
            is_reachable = False # Anggap offline jika utilitas ping tidak ada
        except Exception as e:
            print(f"An unexpected error occurred while pinging {komputer.dal_code}: {e}")
            is_reachable = False

        # Update status komputer di database
        komputer.is_online = is_reachable
        komputer.last_ping_time = timezone.now()
        komputer.save()
        print(f"Komputer {komputer.machine_name} ({komputer.dal_code}) status: {'Online' if is_reachable else 'Offline'}")

    print("Selesai menjalankan task check_computer_status_task.")