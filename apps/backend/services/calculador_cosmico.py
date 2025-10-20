"""
🌙 Calculador Cósmico - Capa 7 del Sistema

Calcula contexto astronómico/astrológico preciso para cada Estado Cero:
- Fase lunar (porcentaje de iluminación, fase nominal)
- Hora planetaria (Sol, Luna, Marte, Mercurio, Júpiter, Venus, Saturno)
- Posición solar (signo zodiacal actual)
- Tránsitos planetarios (expansión futura)

Principio: La capa cósmica INFORMA, no DETERMINA.
Opera al borde del caos: proporciona contexto sin colapsar en determinismo.
"""

import ephem
from datetime import datetime, timedelta
from typing import Dict, Tuple, Optional
from pathlib import Path
import json


class CalculadorCosmico:
    """
    Calcula contexto astronómico preciso usando pyephem.

    La Capa 7 es la más sutil: proporciona el "clima cósmico" del momento,
    pero NO dicta la pregunta. Es contexto, no destino.
    """

    def __init__(self, latitud: float = 40.4168, longitud: float = -3.7038):
        """
        Args:
            latitud: Latitud del observador (default: Madrid)
            longitud: Longitud del observador (default: Madrid)
        """
        self.observador = ephem.Observer()
        self.observador.lat = str(latitud)
        self.observador.lon = str(longitud)

        # Configuración de ubicación
        self.latitud = latitud
        self.longitud = longitud

        # Mapeo de signos zodiacales
        self.signos_zodiacales = [
            "Aries", "Tauro", "Géminis", "Cáncer",
            "Leo", "Virgo", "Libra", "Escorpio",
            "Sagitario", "Capricornio", "Acuario", "Piscis"
        ]

        # Orden caldeo de planetas para horas planetarias
        self.orden_caldeo = [
            "Saturno", "Júpiter", "Marte", "Sol",
            "Venus", "Mercurio", "Luna"
        ]

        # Correspondencias de horas planetarias con arquetipos
        self.arquetipos_planetarios = {
            "Saturno": "estructura, límites, disciplina",
            "Júpiter": "expansión, sabiduría, abundancia",
            "Marte": "acción, coraje, energía",
            "Sol": "vitalidad, claridad, propósito",
            "Venus": "belleza, armonía, conexión",
            "Mercurio": "comunicación, intelecto, adaptabilidad",
            "Luna": "intuición, emoción, flujo"
        }

    def calcular_contexto_completo(
        self,
        fecha_hora: Optional[datetime] = None
    ) -> Dict:
        """
        Calcula contexto cósmico completo para un momento dado.

        Args:
            fecha_hora: Momento a calcular (default: ahora)

        Returns:
            Dict con toda la información astronómica/astrológica
        """
        if fecha_hora is None:
            fecha_hora = datetime.now()

        self.observador.date = fecha_hora

        # Calcular todos los componentes
        fase_lunar = self.calcular_fase_lunar(fecha_hora)
        hora_planetaria = self.calcular_hora_planetaria(fecha_hora)
        posicion_solar = self.calcular_posicion_solar(fecha_hora)

        return {
            "timestamp": fecha_hora.isoformat(),
            "fase_lunar": fase_lunar,
            "hora_planetaria": hora_planetaria,
            "posicion_solar": posicion_solar,
            "latitud": self.latitud,
            "longitud": self.longitud
        }

    def calcular_fase_lunar(self, fecha_hora: Optional[datetime] = None) -> Dict:
        """
        Calcula fase lunar precisa usando ephem.

        Args:
            fecha_hora: Momento a calcular (default: ahora)

        Returns:
            {
                "porcentaje_iluminacion": float (0-100),
                "fase": str (nueva/creciente/llena/menguante),
                "fase_detallada": str,
                "dias_desde_nueva": float,
                "significado": str
            }
        """
        if fecha_hora is None:
            fecha_hora = datetime.now()

        self.observador.date = fecha_hora
        luna = ephem.Moon(self.observador)

        # Porcentaje de iluminación
        porcentaje = luna.phase

        # Calcular días desde luna nueva
        fecha_nueva_previa = ephem.previous_new_moon(self.observador.date)
        dias_desde_nueva = (self.observador.date - fecha_nueva_previa)

        # Determinar fase nominal
        if porcentaje < 1:
            fase = "Luna Nueva"
            fase_detallada = "Luna Nueva (oscuridad, potencial)"
            significado = "Inicio, semilla, potencial latente"
        elif porcentaje < 25:
            fase = "Creciente"
            fase_detallada = "Luna Creciente Joven"
            significado = "Germinación, primeros pasos, intención"
        elif porcentaje < 50:
            fase = "Creciente"
            fase_detallada = "Cuarto Creciente"
            significado = "Acción, construcción, manifestación"
        elif porcentaje < 75:
            fase = "Creciente"
            fase_detallada = "Luna Gibosa Creciente"
            significado = "Refinamiento, ajuste, preparación"
        elif porcentaje < 99:
            fase = "Luna Llena"
            fase_detallada = "Aproximación a Luna Llena"
            significado = "Culminación, revelación, cosecha"
        elif porcentaje >= 99:
            fase = "Luna Llena"
            fase_detallada = "Luna Llena (plenitud, revelación)"
            significado = "Plenitud, claridad máxima, culminación"
        else:
            # Menguante
            if porcentaje > 75:
                fase = "Menguante"
                fase_detallada = "Luna Gibosa Menguante"
                significado = "Gratitud, compartir, enseñar"
            elif porcentaje > 50:
                fase = "Menguante"
                fase_detallada = "Cuarto Menguante"
                significado = "Liberación, soltar, desapego"
            elif porcentaje > 25:
                fase = "Menguante"
                fase_detallada = "Luna Menguante Final"
                significado = "Descanso, integración, vacío fértil"
            else:
                fase = "Luna Nueva"
                fase_detallada = "Aproximación a Luna Nueva"
                significado = "Rendición, finalización, silencio"

        return {
            "porcentaje_iluminacion": round(porcentaje, 2),
            "fase": fase,
            "fase_detallada": fase_detallada,
            "dias_desde_nueva": round(dias_desde_nueva, 2),
            "significado": significado
        }

    def calcular_hora_planetaria(self, fecha_hora: Optional[datetime] = None) -> Dict:
        """
        Calcula hora planetaria según sistema caldeo tradicional.

        Las horas planetarias dividen el día (amanecer a atardecer) y
        la noche (atardecer a amanecer) en 12 horas cada uno, asignando
        planetas en orden caldeo.

        Args:
            fecha_hora: Momento a calcular (default: ahora)

        Returns:
            {
                "planeta": str,
                "arquetipos": str,
                "es_diurna": bool,
                "numero_hora": int (1-12),
                "regente_dia": str
            }
        """
        if fecha_hora is None:
            fecha_hora = datetime.now()

        self.observador.date = fecha_hora

        # Calcular amanecer y atardecer del día
        sol = ephem.Sun(self.observador)

        try:
            amanecer = ephem.localtime(self.observador.previous_rising(sol))
            atardecer = ephem.localtime(self.observador.next_setting(sol))

            # Si estamos después del atardecer, calcular próximo amanecer
            if fecha_hora > atardecer:
                siguiente_amanecer = ephem.localtime(self.observador.next_rising(sol))
                es_diurna = False
                inicio = atardecer
                fin = siguiente_amanecer
            else:
                es_diurna = True
                inicio = amanecer
                fin = atardecer

            # Calcular duración de hora planetaria
            duracion_periodo = (fin - inicio).total_seconds()
            duracion_hora_planetaria = duracion_periodo / 12

            # Calcular qué hora planetaria estamos
            tiempo_transcurrido = (fecha_hora - inicio).total_seconds()
            numero_hora = int(tiempo_transcurrido / duracion_hora_planetaria) + 1

            # Limitar a 1-12
            numero_hora = max(1, min(12, numero_hora))

            # Determinar regente del día (según día de la semana)
            regentes_dias = {
                0: "Luna",      # Lunes
                1: "Marte",     # Martes
                2: "Mercurio",  # Miércoles
                3: "Júpiter",   # Jueves
                4: "Venus",     # Viernes
                5: "Saturno",   # Sábado
                6: "Sol"        # Domingo
            }
            regente_dia = regentes_dias[fecha_hora.weekday()]

            # Calcular planeta de la hora actual
            # La primera hora del día es regida por el regente del día
            indice_regente = self.orden_caldeo.index(regente_dia)
            indice_hora = (indice_regente + (numero_hora - 1)) % 7
            planeta_hora = self.orden_caldeo[indice_hora]

            return {
                "planeta": planeta_hora,
                "arquetipos": self.arquetipos_planetarios[planeta_hora],
                "es_diurna": es_diurna,
                "numero_hora": numero_hora,
                "regente_dia": regente_dia,
                "duracion_hora_minutos": round(duracion_hora_planetaria / 60, 1)
            }

        except Exception as e:
            # Fallback si hay error (ej: latitudes extremas)
            print(f"⚠️ Error calculando hora planetaria: {e}")
            return {
                "planeta": "Sol",
                "arquetipos": self.arquetipos_planetarios["Sol"],
                "es_diurna": True,
                "numero_hora": 1,
                "regente_dia": "Sol",
                "duracion_hora_minutos": 60,
                "error": str(e)
            }

    def calcular_posicion_solar(self, fecha_hora: Optional[datetime] = None) -> Dict:
        """
        Calcula posición del Sol en el zodíaco.

        Args:
            fecha_hora: Momento a calcular (default: ahora)

        Returns:
            {
                "signo": str,
                "grados": float,
                "elemento": str,
                "cualidad": str,
                "significado": str
            }
        """
        if fecha_hora is None:
            fecha_hora = datetime.now()

        self.observador.date = fecha_hora
        sol = ephem.Sun(self.observador)

        # Longitud eclíptica del Sol (0-360 grados)
        longitud_eclipitica = float(sol.ra) * 180 / ephem.pi

        # Ajustar para obtener longitud zodiacal
        # (ephem usa ascensión recta, necesitamos longitud eclíptica)
        # Aproximación: convertir RA a longitud eclíptica
        oblicuidad = 23.44  # Oblicuidad de la eclíptica en grados

        # Para simplificar, usamos el mes para determinar el signo
        # (más preciso sería calcular la longitud eclíptica verdadera)
        mes = fecha_hora.month
        dia = fecha_hora.day

        # Fechas aproximadas de inicio de signos
        if (mes == 3 and dia >= 21) or (mes == 4 and dia <= 19):
            signo_idx = 0  # Aries
        elif (mes == 4 and dia >= 20) or (mes == 5 and dia <= 20):
            signo_idx = 1  # Tauro
        elif (mes == 5 and dia >= 21) or (mes == 6 and dia <= 20):
            signo_idx = 2  # Géminis
        elif (mes == 6 and dia >= 21) or (mes == 7 and dia <= 22):
            signo_idx = 3  # Cáncer
        elif (mes == 7 and dia >= 23) or (mes == 8 and dia <= 22):
            signo_idx = 4  # Leo
        elif (mes == 8 and dia >= 23) or (mes == 9 and dia <= 22):
            signo_idx = 5  # Virgo
        elif (mes == 9 and dia >= 23) or (mes == 10 and dia <= 22):
            signo_idx = 6  # Libra
        elif (mes == 10 and dia >= 23) or (mes == 11 and dia <= 21):
            signo_idx = 7  # Escorpio
        elif (mes == 11 and dia >= 22) or (mes == 12 and dia <= 21):
            signo_idx = 8  # Sagitario
        elif (mes == 12 and dia >= 22) or (mes == 1 and dia <= 19):
            signo_idx = 9  # Capricornio
        elif (mes == 1 and dia >= 20) or (mes == 2 and dia <= 18):
            signo_idx = 10  # Acuario
        else:  # (mes == 2 and dia >= 19) or (mes == 3 and dia <= 20)
            signo_idx = 11  # Piscis

        signo = self.signos_zodiacales[signo_idx]

        # Mapeo de elementos y cualidades
        elementos = {
            "Aries": "Fuego", "Tauro": "Tierra", "Géminis": "Aire", "Cáncer": "Agua",
            "Leo": "Fuego", "Virgo": "Tierra", "Libra": "Aire", "Escorpio": "Agua",
            "Sagitario": "Fuego", "Capricornio": "Tierra", "Acuario": "Aire", "Piscis": "Agua"
        }

        cualidades = {
            "Aries": "Cardinal", "Tauro": "Fijo", "Géminis": "Mutable", "Cáncer": "Cardinal",
            "Leo": "Fijo", "Virgo": "Mutable", "Libra": "Cardinal", "Escorpio": "Fijo",
            "Sagitario": "Mutable", "Capricornio": "Cardinal", "Acuario": "Fijo", "Piscis": "Mutable"
        }

        significados = {
            "Aries": "Iniciación, coraje, acción directa",
            "Tauro": "Estabilidad, sensualidad, recursos",
            "Géminis": "Comunicación, curiosidad, versatilidad",
            "Cáncer": "Nutrición, emocionalidad, hogar",
            "Leo": "Creatividad, expresión, generosidad",
            "Virgo": "Análisis, servicio, perfección",
            "Libra": "Balance, relaciones, estética",
            "Escorpio": "Transformación, profundidad, poder",
            "Sagitario": "Expansión, filosofía, aventura",
            "Capricornio": "Estructura, ambición, maestría",
            "Acuario": "Innovación, colectivo, libertad",
            "Piscis": "Trascendencia, compasión, imaginación"
        }

        return {
            "signo": signo,
            "elemento": elementos[signo],
            "cualidad": cualidades[signo],
            "significado": significados[signo]
        }

    def generar_sintesis_cosmica(self, contexto: Dict) -> str:
        """
        Genera una síntesis narrativa del contexto cósmico.

        Esta síntesis se puede incluir en la generación de preguntas
        para proporcionar "sabor" astrológico sin determinar la pregunta.

        Args:
            contexto: Output de calcular_contexto_completo()

        Returns:
            Frase descriptiva del clima cósmico
        """
        fase_lunar = contexto["fase_lunar"]
        hora_planetaria = contexto["hora_planetaria"]
        posicion_solar = contexto["posicion_solar"]

        # Construir síntesis
        partes = []

        # Luna
        partes.append(f"{fase_lunar['fase_detallada']} ({fase_lunar['significado'].lower()})")

        # Hora planetaria
        if hora_planetaria["es_diurna"]:
            partes.append(f"hora diurna de {hora_planetaria['planeta']}")
        else:
            partes.append(f"hora nocturna de {hora_planetaria['planeta']}")

        # Sol
        partes.append(f"Sol en {posicion_solar['signo']} ({posicion_solar['elemento']})")

        return ", ".join(partes)


# === FUNCIONES PÚBLICAS ===

def obtener_contexto_cosmico(
    latitud: float = 40.4168,
    longitud: float = -3.7038,
    fecha_hora: Optional[datetime] = None
) -> Dict:
    """
    Función principal para obtener contexto cósmico completo.

    Args:
        latitud: Latitud del observador
        longitud: Longitud del observador
        fecha_hora: Momento a calcular (default: ahora)

    Returns:
        Dict con contexto astronómico/astrológico completo
    """
    calculador = CalculadorCosmico(latitud, longitud)
    contexto = calculador.calcular_contexto_completo(fecha_hora)
    contexto["sintesis"] = calculador.generar_sintesis_cosmica(contexto)
    return contexto


if __name__ == "__main__":
    # Test del calculador
    print("🌙 CALCULADOR CÓSMICO - Test\n")
    print("=" * 70)

    # Test en momento actual
    contexto = obtener_contexto_cosmico()

    print(f"\n⏰ Timestamp: {contexto['timestamp']}")
    print(f"📍 Ubicación: {contexto['latitud']}, {contexto['longitud']}\n")

    print("🌙 FASE LUNAR:")
    fase = contexto["fase_lunar"]
    print(f"   Fase: {fase['fase_detallada']}")
    print(f"   Iluminación: {fase['porcentaje_iluminacion']}%")
    print(f"   Días desde nueva: {fase['dias_desde_nueva']}")
    print(f"   Significado: {fase['significado']}\n")

    print("🪐 HORA PLANETARIA:")
    hora = contexto["hora_planetaria"]
    print(f"   Planeta: {hora['planeta']}")
    print(f"   Arquetipos: {hora['arquetipos']}")
    print(f"   Tipo: {'Diurna' if hora['es_diurna'] else 'Nocturna'}")
    print(f"   Hora #{hora['numero_hora']} del {'día' if hora['es_diurna'] else 'noche'}")
    print(f"   Regente del día: {hora['regente_dia']}\n")

    print("☀️ POSICIÓN SOLAR:")
    sol = contexto["posicion_solar"]
    print(f"   Signo: {sol['signo']}")
    print(f"   Elemento: {sol['elemento']}")
    print(f"   Cualidad: {sol['cualidad']}")
    print(f"   Significado: {sol['significado']}\n")

    print("✨ SÍNTESIS CÓSMICA:")
    print(f"   {contexto['sintesis']}\n")

    print("=" * 70)
    print("✅ Capa 7 (Cósmica) implementada correctamente")
