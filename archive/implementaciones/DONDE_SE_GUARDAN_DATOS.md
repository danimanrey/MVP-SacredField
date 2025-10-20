# 📦 Dónde se Guardan los Datos - Campo Sagrado MVP

**Actualizado:** 10 de octubre, 2025

---

## 🎯 **Arquitectura de Persistencia**

### **Configuración del Usuario**

**Guardado dual:**

1. **JSON (acceso rápido):**
   ```
   /Users/hp/Campo sagrado MVP/backend/storage/configuracion_usuario.json
   ```
   - Para lectura rápida del backend
   - Para sincronización con la app

2. **Obsidian (editable):**
   ```
   /Users/hp/Campo sagrado MVP/obsidian_vault/00-Pilares/Configuracion-Individual.md
   ```
   - Para edición manual
   - Para evolución en el tiempo
   - Para integración con knowledge graph

**Ejemplo del markdown en Obsidian:**
```markdown
---
tipo: configuracion-individual
user_id: default
fecha_creacion: 2025-10-10
---

# 🕌 Configuración Individual - Campo Sagrado

## No-Negociables

- Fajr (Estado Cero): ✓
- Dhuhr (Estado Cero): ✓
- Maghrib (Validación): ✓

## Dimensiones Prioritarias

- Finanzas
- Desarrollo

## Contexto

### Financiero
- **Runway:** 12 meses
- **Urgencia financiera:** Sí ⚡

### Biológico
- **Energía disponible:** 3/5
- **Patrón de sueño:** Regular
- **Ejercicio regular:** Sí

## Expresión Libre

Estoy en transición profesional...

---

**Puedes editar esta nota para actualizar tu configuración**
```

---

### **Estados Cero**

**Ubicación:**
```
/Users/hp/Campo sagrado MVP/obsidian_vault/50-Conversaciones-IA/Estados-Cero/
  └── 2025-10-10/
      ├── fajr.md
      ├── dhuhr.md
      └── maghrib.md
```

**También en SQLite:**
```
/Users/hp/Campo sagrado MVP/storage/organismo.db
  └── tabla: estados_cero
```

---

### **Espejo Diario**

**Google Calendar** (tiempo real):
- Eventos con categorías
- Sincronización bidireccional

**Obsidian** (documentación):
```
/Users/hp/Campo sagrado MVP/obsidian_vault/40-Journal/2025-10-10.md
```

---

## 🔄 **Flujo de Sincronización**

```
Usuario completa Onboarding
         ↓
Backend guarda en:
  1. storage/configuracion_usuario.json (rápido)
  2. obsidian_vault/00-Pilares/Configuracion-Individual.md (editable)
         ↓
Usuario puede:
  - Leer config desde la app (JSON)
  - Editar config en Obsidian (MD)
         ↓
(Futuro) Obsidian → Backend sync
```

---

## 📝 **Por qué Doble Guardado**

### **JSON:**
- ✅ Acceso rápido
- ✅ No requiere parsear
- ✅ Ideal para la app

### **Obsidian:**
- ✅ Editable manualmente
- ✅ Versionable (git)
- ✅ Integrado con knowledge graph
- ✅ Puede evolucionar en el tiempo
- ✅ El usuario tiene control total

---

## 🔮 **Futuro (Post-MVP)**

### **Anytype Integration:**
```
ConfiguracionIndividual (Object)
  ├── No-Negociables (Set)
  ├── Dimensiones (Relations)
  ├── Contexto Financiero (Object)
  └── Contexto Biológico (Object)
```

### **Sincronización Bidireccional:**
- Usuario edita en Obsidian → Backend detecta cambio → App actualiza
- Usuario edita en App → Backend guarda → Obsidian actualiza

---

**Arquitectura de persistencia dual: JSON (rápido) + Obsidian (editable)**

**إن شاء الله 🕌✨**

