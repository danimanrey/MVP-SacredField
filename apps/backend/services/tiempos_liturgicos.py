from __future__ import annotations

from datetime import datetime, timedelta, date
import pytz
from praytimes import PrayTimes

from models.schemas import (
    TiemposRezoDia, TiempoRezo, VerificacionMomento, ProximoEstadoCero, MomentoLiturgico
)


class CalculadorTiemposLiturgicos:
    """
    Cálculos PRECISOS de tiempos litúrgicos usando astronomía real.
    
    Usa PrayTimes para calcular momentos exactos de oración basados en:
    - Posición del sol (amanecer, mediodía, ocaso)
    - Latitud y longitud
    - Método de cálculo (MWL, ISNA, etc.)
    """

    def __init__(self, latitud: float, longitud: float, timezone: str = "Europe/Madrid"):
        self.latitud = latitud
        self.longitud = longitud
        self.timezone = pytz.timezone(timezone)
        
        # Configurar PrayTimes con método MWL (Muslim World League)
        self.pt = PrayTimes('MWL')

    def _hoy(self):
        return datetime.now(self.timezone)

    def calcular_tiempos_hoy(self, dia: date | None = None) -> TiemposRezoDia:
        """
        Calcula tiempos PRECISOS de oración para un día específico.
        
        Momentos calculados astronómicamente:
        - Fajr: Amanecer astronómico (sol a -18°)
        - Sunrise: Salida del sol visible
        - Dhuhr: Mediodía solar (sol en cénit)
        - Asr: Tarde (sombra = objeto + su longitud)
        - Maghrib: Ocaso (sol toca horizonte)
        - Isha: Noche (sol a -17°)
        """
        
        fecha = dia or self._hoy().date()
        
        # Calcular tiempos con PrayTimes
        # Formato: (año, mes, día), (lat, lon), offset_timezone
        # Obtener offset de timezone (ej: +2 para CEST)
        dt_ref = self.timezone.localize(datetime(fecha.year, fecha.month, fecha.day, 12, 0))
        offset_hours = dt_ref.utcoffset().total_seconds() / 3600
        
        tiempos = self.pt.getTimes(
            (fecha.year, fecha.month, fecha.day),
            (self.latitud, self.longitud),
            offset_hours
        )
        
        # Convertir strings de tiempo a datetime con timezone
        def parse_tiempo(tiempo_str: str) -> datetime:
            """Convierte '06:46' a datetime con timezone"""
            hora, minuto = map(int, tiempo_str.split(':'))
            dt = datetime(fecha.year, fecha.month, fecha.day, hora, minuto)
            return self.timezone.localize(dt)
        
        # Crear objetos TiempoRezo con ventanas precisas
        def crear_tiempo_rezo(inicio_str: str, fin_str: str = None, duracion_ventana: int = 30) -> TiempoRezo:
            """
            Crea objeto TiempoRezo con:
            - inicio: Momento exacto astronómico
            - fin: Siguiente tiempo de oración (o inicio + duracion_ventana)
            - ventana_estado_cero: inicio + duracion_ventana
            """
            inicio = parse_tiempo(inicio_str)
            
            if fin_str:
                fin = parse_tiempo(fin_str)
            else:
                fin = inicio + timedelta(minutes=duracion_ventana)
            
            return TiempoRezo(
                inicio=inicio,
                fin=fin,
                ventana_estado_cero=inicio + timedelta(minutes=duracion_ventana)
            )
        
        # Construir tiempos precisos del día
        return TiemposRezoDia(
            fecha=fecha,
            
            # Fajr: Desde amanecer astronómico hasta salida del sol
            fajr=crear_tiempo_rezo(
                tiempos['fajr'],       # Inicio: Amanecer astronómico (ej: 06:46)
                tiempos['sunrise'],    # Fin: Salida del sol visible (ej: 08:19)
                30                     # Ventana Estado Cero: 30 min desde inicio
            ),
            
            # Dhuhr: Desde mediodía solar hasta Asr
            dhuhr=crear_tiempo_rezo(
                tiempos['dhuhr'],      # Inicio: Mediodía solar (ej: 14:02)
                tiempos['asr'],        # Fin: Asr (ej: 17:13)
                30
            ),
            
            # Asr: Desde tarde hasta Maghrib
            asr=crear_tiempo_rezo(
                tiempos['asr'],        # Inicio: Tarde (ej: 17:13)
                tiempos['maghrib'],    # Fin: Ocaso (ej: 19:43)
                30
            ),
            
            # Maghrib: Desde ocaso hasta Isha
            maghrib=crear_tiempo_rezo(
                tiempos['maghrib'],    # Inicio: Ocaso (ej: 19:43)
                tiempos['isha'],       # Fin: Noche (ej: 21:09)
                30
            ),
            
            # Isha: Desde noche hasta medianoche
            isha=crear_tiempo_rezo(
                tiempos['isha'],       # Inicio: Noche (ej: 21:09)
                tiempos['midnight'],   # Fin: Medianoche (ej: 01:25)
                30
            )
        )

    def verificar_momento_estado_cero(self, permitir_fuera_ventana: bool = False) -> VerificacionMomento:
        """
        Verifica si AHORA es momento de Estado Cero.
        
        Args:
            permitir_fuera_ventana: Si True, permite acceso fuera de ventana (para recuperar)
        
        Retorna:
        - es_momento: True si estamos en ventana válida
        - momento: Qué momento litúrgico es
        - minutos_restantes: Cuánto queda de la ventana
        - fuera_de_ventana: True si pasó el tiempo pero permitir_fuera_ventana=True
        """
        ahora = self._hoy()
        tiempos = self.calcular_tiempos_hoy()
        
        # Verificar si estamos DENTRO de alguna ventana activa
        for momento in ["fajr", "dhuhr", "asr", "maghrib", "isha"]:
            t = getattr(tiempos, momento)
            
            # Verificar si estamos en la ventana de este momento
            if t.inicio <= ahora <= t.fin:
                minutos = int((t.fin - ahora).total_seconds() // 60)
                return VerificacionMomento(
                    es_momento=True,
                    momento=MomentoLiturgico(momento),
                    ventana_inicio=t.inicio,
                    ventana_fin=t.fin,
                    minutos_restantes=minutos
                )
        
        # Si permitir_fuera_ventana=True, verificar si PASÓ alguna ventana hoy
        if permitir_fuera_ventana:
            for momento in ["maghrib", "isha", "asr", "dhuhr", "fajr"]:  # Orden inverso (más reciente primero)
                t = getattr(tiempos, momento)
                
                # Si ya pasó la ventana de este momento hoy
                if ahora > t.fin:
                    return VerificacionMomento(
                        es_momento=True,  # Permitir acceso
                        momento=MomentoLiturgico(momento),
                        ventana_inicio=t.inicio,
                        ventana_fin=t.fin,
                        minutos_restantes=0,  # Ya pasó
                        fuera_de_ventana=True
                    )
        
        # No estamos en ninguna ventana, calcular próximo
        prox = self.proximo_estado_cero()
        return VerificacionMomento(
            es_momento=False, 
            momento=prox.momento, 
            ventana_inicio=None,
            ventana_fin=None,
            minutos_restantes=None
        )

    def proximo_estado_cero(self) -> ProximoEstadoCero:
        """
        Calcula el próximo momento de Estado Cero.
        
        Retorna:
        - momento: Qué momento litúrgico viene
        - hora: Hora exacta de inicio
        - countdown: Tiempo restante (ej: "2h 45m")
        """
        ahora = self._hoy()
        tiempos = self.calcular_tiempos_hoy()
        
        # Buscar próximo momento hoy
        candidatos = []
        for momento in ["fajr", "dhuhr", "asr", "maghrib", "isha"]:
            t = getattr(tiempos, momento)
            if t.inicio > ahora:
                candidatos.append((MomentoLiturgico(momento), t.inicio))
        
        # Si no hay más hoy, siguiente es Fajr de mañana
        if not candidatos:
            manana = (ahora + timedelta(days=1)).date()
            t_manana = self.calcular_tiempos_hoy(manana)
            delta = t_manana.fajr.inicio - ahora
            horas = int(delta.total_seconds() // 3600)
            minutos = int((delta.total_seconds() % 3600) // 60)
            countdown = f"{horas}h {minutos}m"
            return ProximoEstadoCero(
                momento=MomentoLiturgico.FAJR, 
                hora=t_manana.fajr.inicio, 
                countdown=countdown
            )
        
        # Ordenar por hora y tomar el primero
        candidatos.sort(key=lambda x: x[1])
        momento, hora = candidatos[0]
        
        # Calcular countdown
        delta = hora - ahora
        horas = int(delta.total_seconds() // 3600)
        minutos = int((delta.total_seconds() % 3600) // 60)
        countdown = f"{horas}h {minutos}m"
        
        return ProximoEstadoCero(momento=momento, hora=hora, countdown=countdown)

    def momento_actual(self) -> MomentoLiturgico:
        """
        Determina en qué momento litúrgico estamos AHORA.
        
        Si no estamos en ninguna ventana de Estado Cero,
        retorna el momento del día según posición solar:
        - Antes de Fajr → Noche (considera como Isha)
        - Fajr-Dhuhr → Fajr
        - Dhuhr-Asr → Dhuhr
        - Asr-Maghrib → Asr
        - Maghrib-Isha → Maghrib
        - Después de Isha → Isha
        """
        ahora = self._hoy()
        tiempos = self.calcular_tiempos_hoy()
        
        # Verificar ventanas de Estado Cero primero
        ver = self.verificar_momento_estado_cero()
        if ver.es_momento:
            return ver.momento
        
        # Si no estamos en ventana, determinar momento del día
        if ahora < tiempos.fajr.inicio:
            return MomentoLiturgico.ISHA  # Noche
        elif ahora < tiempos.dhuhr.inicio:
            return MomentoLiturgico.FAJR
        elif ahora < tiempos.asr.inicio:
            return MomentoLiturgico.DHUHR
        elif ahora < tiempos.maghrib.inicio:
            return MomentoLiturgico.ASR
        elif ahora < tiempos.isha.inicio:
            return MomentoLiturgico.MAGHRIB
        else:
            return MomentoLiturgico.ISHA
    
    def obtener_tiempos_formato_legible(self, dia: date = None) -> dict:
        """
        Retorna tiempos en formato legible para mostrar al usuario.
        
        Ejemplo:
        {
            "fajr": {
                "inicio": "06:46",
                "fin": "08:19",
                "ventana_completa": "06:46 - 08:19 (1h 33m)"
            },
            ...
        }
        """
        tiempos = self.calcular_tiempos_hoy(dia)
        
        def formatear(t: TiempoRezo) -> dict:
            duracion = t.fin - t.inicio
            horas = int(duracion.total_seconds() // 3600)
            minutos = int((duracion.total_seconds() % 3600) // 60)
            
            return {
                "inicio": t.inicio.strftime("%H:%M"),
                "fin": t.fin.strftime("%H:%M"),
                "ventana_completa": f"{t.inicio.strftime('%H:%M')} - {t.fin.strftime('%H:%M')} ({horas}h {minutos}m)" if horas > 0 else f"{t.inicio.strftime('%H:%M')} - {t.fin.strftime('%H:%M')} ({minutos}m)",
                "estado_cero_recomendado": t.inicio.strftime("%H:%M")
            }
        
        return {
            "fecha": tiempos.fecha.strftime("%Y-%m-%d"),
            "fajr": formatear(tiempos.fajr),
            "dhuhr": formatear(tiempos.dhuhr),
            "asr": formatear(tiempos.asr),
            "maghrib": formatear(tiempos.maghrib),
            "isha": formatear(tiempos.isha)
        }
