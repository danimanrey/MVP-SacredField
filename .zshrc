# ~/.zshrc o ~/.bashrc

# Campo Sagrado Aliases
alias cs='cd ~/Campo\ sagrado\ MVP'
alias csback='cd ~/Campo\ sagrado\ MVP/backend'
alias csfront='cd ~/Campo\ sagrado\ MVP/campo-sagrado-nextjs'
alias csvault='cd ~/Documents/CampoSagrado'

# Comandos del Organismo
alias inicio='cs && ./backend/scripts/inicio_diario.sh'
alias estado='open http://localhost:3000/estado-cero-inmersivo'
alias espejo='open http://localhost:3000/espejo-diario'
alias dashboard='open http://localhost:3000/dashboard'
alias audit='cat ~/Documents/CampoSagrado/00_System/Audit_Trail/$(date +%Y-%m-%d).md'
alias salud='curl -s http://localhost:8000/api/health | jq'

# Claude Code con contexto
alias cc='claude-code'
alias cccs='cs && claude-code'

# Git simplificado
alias gs='git status'
alias ga='git add'
alias gc='git commit -m'
alias gp='git push'

# Utilidades
alias ll='ls -lah'
alias ..='cd ..'
alias ...='cd ../..'