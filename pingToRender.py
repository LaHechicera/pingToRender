import requests
import time
from datetime import datetime

# ---------- CONFIGURACIÓN ----------
URL = "https://tu-app.onrender.com"  # <-- cambia esto por la URL real de tu backend
INTERVALO_SEGUNDOS = 600             # 10 minutos

HORA_INICIO_NOCHE = 23   # a partir de las 23:00 deja de hacer ping
HORA_FIN_NOCHE = 7       # vuelve a hacer ping a partir de las 07:00
# ------------------------------------


def es_horario_nocturno() -> bool:
    """Devuelve True si la hora actual cae dentro del rango nocturno."""
    ahora = datetime.now().hour

    if HORA_INICIO_NOCHE > HORA_FIN_NOCHE:
        # El rango cruza la medianoche (ej: 23:00 -> 07:00)
        return ahora >= HORA_INICIO_NOCHE or ahora < HORA_FIN_NOCHE
    else:
        # Rango que no cruza medianoche (ej: 01:00 -> 06:00)
        return HORA_INICIO_NOCHE <= ahora < HORA_FIN_NOCHE


def despertar_backend():
    try:
        respuesta = requests.get(URL, timeout=10)
        print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Ping enviado - Status: {respuesta.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Error al hacer ping: {e}")


def main():
    print("Iniciando script de mantenimiento activo del backend...")
    print(f"Horario de descanso: {HORA_INICIO_NOCHE}:00 - {HORA_FIN_NOCHE}:00")

    while True:
        if es_horario_nocturno():
            print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Horario nocturno, se omite el ping.")
        else:
            despertar_backend()

        time.sleep(INTERVALO_SEGUNDOS)


if __name__ == "__main__":
    main()