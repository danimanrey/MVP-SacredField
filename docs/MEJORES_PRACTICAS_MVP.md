# 🕌 Mejores Prácticas para Iterar el MVP - Estado Cero

## 📋 **Filosofía de Iteración**

El Campo Sagrado opera **al borde del caos** - esto significa que el desarrollo también debe ser orgánico, emergente y respetar los ritmos naturales.

---

## 🎯 **Principios de Desarrollo**

### 1. **Menos es Más (Minimalismo Sacral)**
- ✅ **3 preguntas** en vez de 6
- ✅ **Un flujo**, no múltiples caminos
- ✅ **Claridad visual**, no sobrecarga

**Regla de Oro**: Si no puedes explicarlo en una frase, simplifica.

### 2. **Feedback Inmediato del Cuerpo**
- El usuario debe **sentir** la respuesta correcta
- Botones grandes y táctiles
- Animaciones que respiran (no que distraen)
- Colores que evocan estados (expansión = verde, contracción = rosa)

### 3. **Contexto sobre Configuración**
- El sistema **debe inferir** antes de preguntar
- Usa el momento litúrgico (isha = sin comida)
- Aprende del perfil personal
- Adapta según energía y contexto

---

## 🔄 **Ciclo de Iteración Recomendado**

### **Fase 1: Observar** (Estado Cero personal)
1. Usa el sistema TÚ MISMO durante 5 días
2. Anota en Obsidian:
   - ¿Qué preguntas te confundieron?
   - ¿Cuándo sentiste fricción?
   - ¿Qué te hizo sonreír?

### **Fase 2: Simplificar** (Eliminar peso)
1. Identifica el paso más pesado
2. Pregunta: "¿Esto es esencial AHORA?"
3. Si no → muévelo a v0.2.0

**Ejemplo**:
- ❌ 6 preguntas → ✅ 3 preguntas
- ❌ Chat genérico → ✅ Chat contextual
- ❌ Intensidad 1-10 → ✅ Visual orgánico

### **Fase 3: Pulir** (Estética emergente)
1. Mejora UN aspecto visual cada iteración:
   - Animación de entrada
   - Paleta de color
   - Tipografía
   - Espaciado

2. No todo de golpe - respira entre cambios

### **Fase 4: Validar** (Prueba real)
1. Comparte con 1-2 personas de confianza
2. Observa SIN explicar
3. Si tienen que preguntar "¿cómo funciona esto?" → simplifica

---

## 🎨 **Guía de Diseño Visual**

### **Paleta Beige Cálida** (Implementada)
```css
--fondo-app: #F5F1E8;        /* Beige papel */
--fondo-card: #FEFCF6;       /* Crema cálido */
--color-primario: #8B6F47;   /* Terracota oscuro */
--color-acento: #E8B86D;     /* Ámbar suave */
```

### **Animaciones Orgánicas**
- `cubic-bezier(0.4, 0, 0.2, 1)` para transiciones suaves
- 300-600ms de duración (no más)
- `scale` para entrada, `fly` para transiciones
- Evita `bounce` - usa `cubicOut`

### **Espaciado Respiratorio**
```css
padding: 2rem;        /* Contenedores */
gap: 1.5rem;          /* Entre elementos */
margin-bottom: 3rem;  /* Secciones */
```

---

## 🧪 **Testing del MVP**

### **Test de los 3 Minutos**
El usuario debe poder:
1. Entender qué es (10 seg)
2. Iniciar Estado Cero (30 seg)
3. Completar las 3 preguntas (2 min)
4. Ver dirección emergente (20 seg)

**Si tarda más → hay fricción.**

### **Test de la Abuela**
Si tu abuela no entiende qué hacer:
- Los botones son muy pequeños
- El texto es muy técnico
- Hay demasiadas opciones

### **Test del Cuerpo**
Después de usar el sistema:
- ¿Te sientes más claro? ✅
- ¿Te sientes más ansioso? ❌
- ¿Te sientes indiferente? ❌ (necesita más impacto)

---

## 📊 **Métricas que Importan**

### **NO midas**:
- ❌ Tiempo en pantalla
- ❌ Clicks totales
- ❌ Páginas visitadas

### **SÍ mide**:
- ✅ ¿Completaron el Estado Cero?
- ✅ ¿Volvieron al día siguiente?
- ✅ ¿La dirección emergente fue accionable?
- ✅ ¿Cuántos Estados Cero completan por semana?

**Meta MVP**: 3 Estados Cero/semana durante 2 semanas = producto validado

---

## 🛠️ **Stack de Herramientas para Iterar**

### **Diseño Rápido**
1. **Figma** o papel + lápiz
2. Sketch del flujo ANTES de codear
3. Usa componentes existentes

### **Testing Local**
```bash
# Backend
cd backend && source venv/bin/activate && python run.py

# Frontend
cd frontend && npm run dev

# Ver logs en tiempo real
tail -f /tmp/campo-sagrado-backend.log
```

### **Debugging Efectivo**
1. Usa el navegador en modo incógnito
2. Abre DevTools → Network para ver llamadas API
3. Console.log estratégico (no spam)

---

## 🚀 **Roadmap Sugerido para Estado Cero**

### **v0.1.1 - Actual** ✅
- [x] 3 preguntas esenciales
- [x] Paleta beige cálida
- [x] UI mejorada y dinámica
- [x] Corrección de errores

### **v0.1.2 - Refinamiento** (Próximo)
- [ ] Añadir sonidos sutiles (expansión/contracción)
- [ ] Mejorar transición entre preguntas
- [ ] Guardar respuestas en Obsidian automáticamente
- [ ] Notificación nativa 5 min antes del Estado Cero

### **v0.2.0 - Integración** (Futuro)
- [ ] Conectar con el Espejo Sagrado
- [ ] Generar plan del día basado en respuestas
- [ ] Análisis semanal de patrones sacrales
- [ ] Compartir dirección emergente con pareja

---

## 💡 **Preguntas para Cada Iteración**

Antes de cambiar CUALQUIER cosa, pregúntate:

1. **¿Esto simplifica o complica?**
   - Si complica → descarta

2. **¿Esto respeta el ritmo del usuario?**
   - Si le hace ir más rápido de lo natural → descarta

3. **¿Esto honra la autoridad sacral?**
   - Si le dice qué hacer (en vez de preguntar) → descarta

4. **¿Esto es esencial AHORA?**
   - Si puede esperar a v0.2 → pospón

---

## 🌱 **Filosofía de Código**

### **Escribir para Humanos**
```python
# ❌ Malo
def fq(c):
    return [q for q in generate(c) if validate(q)]

# ✅ Bueno
def formular_preguntas_sacrales(contexto):
    """Genera 3 preguntas binarias que honran la autoridad sacral"""
    preguntas = generar_preguntas_contextuales(contexto)
    return filtrar_preguntas_apropiadas(preguntas)
```

### **Comentarios que Cuentan Historias**
```typescript
// ✅ Este delay permite que el usuario procese la pregunta
// antes de ver las opciones - respeta el ritmo sacral
setTimeout(() => mostrarOpciones(), 300);
```

### **Commit Messages Significativos**
```bash
# ❌ Malo
git commit -m "fix"

# ✅ Bueno
git commit -m "Reduce preguntas de 6 a 3 para minimizar fatiga de decisión"
```

---

## 🎭 **Anti-Patrones a Evitar**

### **1. Sobrecarga de Opciones**
❌ "¿Quieres modo claro/oscuro/sepia/auto?"
✅ Beige cálido por defecto. Punto.

### **2. Onboarding Extenso**
❌ 5 pantallas explicando cómo funciona
✅ Una frase + descubrimiento por uso

### **3. Gamificación Forzada**
❌ "¡Ganaste 10 puntos sacrales! 🏆"
✅ Progreso natural y orgánico

### **4. Análisis Excesivo**
❌ "Gráfica de tu energía sacral en los últimos 90 días"
✅ Resumen simple: "Esta semana respondiste expansión 8/9 veces"

---

## 🧘 **Ritual de Desarrollo**

### **Antes de Cada Sesión de Código**
1. Estado Cero de 5 min
2. Define UNA cosa a mejorar
3. Timebox: 60-90 min máximo
4. Commit y respira

### **Después de Cada Iteración**
1. Prueba el flujo completo
2. Anota qué mejoró / empeoró
3. Actualiza el CHANGELOG
4. Comparte con alguien

---

## 📚 **Recursos de Inspiración**

### **Diseño Minimalista**
- [linear.app](https://linear.app) - Animaciones sutiles
- [cal.com](https://cal.com) - Flujo simple
- [notion.so](https://notion.so) - Jerarquía visual

### **Interfaces Orgánicas**
- [Duolingo](https://duolingo.com) - Feedback inmediato
- [Headspace](https://headspace.com) - Paleta cálida
- [Things](https://culturedcode.com/things) - Animaciones respiratorias

---

## 🎯 **Próximos Pasos Concretos**

### **Esta Semana**
1. Usa el Estado Cero tú mismo 3 veces
2. Anota fricciones en Obsidian
3. Elige LA fricción más grande
4. Dedica 1 sesión a resolverla

### **Este Mes**
1. Invita a 2-3 personas a probarlo
2. Observa sin intervenir
3. Pregunta: "¿Qué sentiste?"
4. Itera basándote en cuerpo, no en mente

### **Este Trimestre**
1. 10+ usuarios activos
2. 3+ Estados Cero/semana promedio
3. Feedback cualitativo positivo
4. Documentación automática en Obsidian funcionando

---

## ✨ **Cierre**

El MVP no se trata de tener todas las features.
Se trata de tener UNA experiencia que funcione tan bien
que el usuario regrese mañana.

**Enfócate en el Estado Cero.**
Todo lo demás es secundario.

---

*Creado con 🕌 para respetar la autoridad sacral y operar al borde del caos.*

