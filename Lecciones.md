# Lecciones Aprendidas - Magnum

_Documentación de procesos resueltos para referencia futura._

---

## LECCIÓN 1: Configuración de Audio Independiente (2026-04-12)

### Problema
Jose quería que cada agente (Cornelio y Magnum) tuviera su propia voz independiente en Telegram. Antes compartían la misma configuración TTS, lo cual causaba confusión.

### Solución Implementada

1. **Magnum usa script manual:**
   ```bash
   python3 /root/.openclaw/workspace-magnum/scripts/audio/magnum_tts_directo.py "texto" salida.ogg
   curl -X POST ".../sendVoice" -F voice=@salida.ogg
   ```

2. **Cornelio debe usar su propio script** con su voice ID (`iwd8AcSi0Je5Quc56ezK`)

3. **TTS auto: OFF** en openclaw.json para ambos

4. **Regla bidireccional:**
   - AUDIO → SOLO AUDIO
   - TEXTO → SIEMPRE TEXTO

### Archivos Involucrados
- `scripts/audio/magnum_tts_directo.py`
- `SOUL.md` - Regla de oro
- `AGENTS.md` - Formato de respuesta

---

## LECCIÓN 2: NO_REPLY para Audio (2026-04-12)

### Problema
Cuando Jose mandaba audio, Magnum primero generaba el audio con curl, pero luego también mandaba texto de proceso interno. Esto aparecía en el grupo y confundía a Jose.

### Solución
Después de enviar el audio por curl, responder con `NO_REPLY` para que no llegue texto adicional al grupo.

### Importante
NO usar NO_REPLY cuando Jose manda texto - siempre responder con texto.

---

## LECCIÓN 3: Scrapping de Uber Eats con Playwright (2026-04-12)

### Problema
Jose queria capturar toda la información de un restaurante de Uber Eats, incluyendo imágenes de todos los platos del menú.

### Desafío Técnico
Uber Eats es una SPA (Single Page Application) - el contenido se carga con JavaScript después de que la página carga. Las imágenes se cargan lazily (solo cuando están visibles en viewport).

### Solución Implementada

1. **Playwright para ejecutar JavaScript:**
   ```bash
   npm install -g playwright
   npx playwright install chromium
   ```

2. **Mobile viewport para bypass anti-bot:**
   ```python
   context = await browser.new_context(
       viewport={"width": 412, "height": 915},
       user_agent="Mozilla/5.0 (Linux; Android 11; SM-G991B)..."
   )
   ```

3. **Deep scroll (bounce technique):**
   ```python
   for i in range(15):
       for y in range(0, total_height, 300):
           await page.evaluate(f"window.scrollTo(0, {y})")
           await page.wait_for_timeout(150)
       await page.evaluate("window.scrollTo(0, 0)")
   ```

4. **Filtrado de imágenes:**
   - >30KB = foto real de comida
   - <10KB = ícono o logo

### Resultado
- **71 fotos de comida** capturadas
- **86 items del menú** con precios
- **12 categorías** de productos
- Guardado en `woods-pizza-data/`

### Archivos Creados
- `skills/uber-eats-scraper/SKILL.md`
- `skills/uber-eats-scraper/scripts/scrape_uber_eats_complete.py`
- `skills/uber-eats-scraper/scripts/download_images.py`
- `skills/uber-eats-scraper/scripts/parse_menu.py`
- `woods-pizza-data/` (completo)

---

## LECCIÓN 4: Modo Trabajo (2026-04-12)

### Problema
Jose queria poder switchear entre modo audio normal y modo solo texto.

### Solución

**Activar modo trabajo:**
- Trigger: "activemos modo trabajo" / "pasemos a modo trabajo" / "cambien a modo trabajo"
- Comportamiento: TODO se responde con texto (incluyendo преобразование de audio a texto)

**Desactivar modo trabajo:**
- Trigger: "desactiven modo trabajo"
- Comportamiento: Volver al flujo normal (AUDIO→AUDIO, TEXTO→TEXTO)

---

## LECCIÓN 5: No Intervenir en Conversaciones de Otros (2026-04-12)

### Problema
Cuando Jose le hablaba a Cornelio, Magnum también respondía y viceversa. Confusion.

### Solución
En el grupo "Los Menudos":
- Si Jose le habla a @CornelioAdelanteBot → Magnum NO_REPLY
- Si Jose le habla a @Magnum_XLBot → Solo Magnum responde
- Si Jose le habla a ambos → Ambos responden

Regla: "No meter la cosa si la cosa es con otro, y no conmigo"

---

## LECCIÓN 6: Reglas de Protección (2026-04-12)

### Reglas Importantes

1. **NO reiniciar gateway** sin autorización de Jose
2. **NO modificar workspace de otros agentes** sin autorización
3. **NO modificar archivos de raíz** sin autorización
4. **Documentar skills** cada vez que se crea una habilidad nueva

---

## Formato para Nueva Lección

```markdown
## LECCIÓN N: Título (Fecha)

### Problema
Descripción del problema encontrado.

### Solución Implementada
Pasos realizados para resolver.

### Archivos Involucrados
Lista de archivos creados o modificados.

### Resultado
Qué se logró.
```

---

_Ultima actualización: 2026-04-12_
---

## LECCIÓN 7: Gestión Segura de Tokens con 1Password (2026-04-12)

### Problema
Los tokens y claves de API se estaban guardando en archivos del workspace, lo cual presentaba riesgo de exposición en GitHub (el push del `.git-credentials` fue bloqueado).

### Solución Implementada

1. **Jose creó boveda "Cornelio" en 1Password**
2. **Token guardado en `/root/.openclaw/workspace-magnum/.secrets/`**
   - Directoro con permisos `700` (solo Magnum puede leer)
   - Archivos con permisos `600`
   - `.secrets/` agregado a `.gitignore`

3. **Ubicación de tokens seguros:**
   ```
   /root/.openclaw/workspace-magnum/.secrets/
   ├── 1password-config.json    # Metadata
   └── op_token.txt            # Token de 1Password Connect API
   ```

### Regla de Seguridad
⚠️ NUNCA guardar tokens en archivos que puedan ser pusheados a GitHub.
⚠️ Usar siempre la carpeta `.secrets/` con permisos restrictivos.

### Archivos Involucrados
- `.gitignore` - Actualizado para excluir `.secrets/`
- `.secrets/` - Carpeta segura para tokens

---

_Ultima actualización: 2026-04-12_

---

## LECCIÓN 8: Creación de Nuevo Agente "Prolix" (2026-04-12)

### Proceso Completado

1. **Workspace independiente** creado en `/root/.openclaw/workspace-prolix/`
2. **Archivos base:**
   - `IDENTITY.md` - Identidad del agente
   - `AGENTS.md` - Roles y responsabilidades
   - `scripts/audio/prolix_tts_directo.py` - Script TTS
   - `skills/uber-eats-scraper/` - Skill copiada de Magnum
3. **Registrado en `openclaw.json`** con id "prolix"
4. **Repo GitHub creado:** `josenavarrojimenez-sudo/prolix`

### Configuración en openclaw.json

```json
{
  "id": "prolix",
  "name": "Prolix - Agente de Investigación",
  "workspace": "/root/.openclaw/workspace-prolix",
  "agentDir": "/root/.openclaw/agents/prolix/agent",
  "sandbox": { "mode": "off" },
  "tools": { "allow": [...] }
}
```

### Archivos Creados

| Archivo | Descripción |
|---------|-------------|
| `IDENTITY.md` | Nombre, emoji, personalidad, background |
| `AGENTS.md` | Roles, cadena de mando, pattern de trabajo |
| `scripts/audio/prolix_tts_directo.py` | Script TTS propio |
| `skills/uber-eats-scraper/*` | Skill de scraping |

### Nota Importante

⚠️ Jose confirmó: cada agente debe tener workspace TOTALMENTE independiente.
⚠️ No compartir workspaces entre agentes.

---

_Ultima actualización: 2026-04-12_
