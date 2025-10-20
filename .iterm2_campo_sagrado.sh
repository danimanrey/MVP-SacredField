# ~/.iterm2_campo_sagrado.sh
#!/bin/bash

clear
echo "🕌 ═══════════════════════════════════════════"
echo "   CAMPO SAGRADO DEL ENTRELAZADOR"
echo "   Operando al borde del caos"
echo "═══════════════════════════════════════════"
echo ""
echo "📍 Ubicación: $(pwd)"
echo "⏰ Momento: $(date '+%H:%M:%S - %A, %d %B %Y')"
echo ""
echo "🔥 Sistema inicializando..."
echo ""

# Verificar servicios
if pgrep -f "fastapi" > /dev/null; then
    echo "✅ Backend: Operativo"
else
    echo "⚠️  Backend: Inactivo"
fi

if pgrep -f "next-server" > /dev/null; then
    echo "✅ Frontend: Operativo"
else
    echo "⚠️  Frontend: Inactivo"
fi

echo ""
echo "═══════════════════════════════════════════"
echo ""
echo "Comandos disponibles:"
echo "  inicio    - Iniciar organismo completo"
echo "  estado    - Capturar Estado Cero"
echo "  espejo    - Ver Espejo Diario"
echo "  audit     - Ver Audit Trail de hoy"
echo "  salud     - Verificar salud del sistema"
echo ""
```

**4. Configurar en Profiles → General → Command:**
```
Login shell
Send text at start: source ~/.iterm2_campo_sagrado.sh
```

**5. Status Bar (Bottom)**
```
iTerm2 → Preferences → Profiles → Session → Configure Status Bar

Añadir componentes:
- CPU Utilization
- Memory Utilization  
- Clock (formato personalizado: %H:%M:%S)
- Git branch (si estás en repo)