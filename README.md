# Plantilla de repositorio base — Especialización en Desarrollo con IA Generativa (Accenture)

Esta es la estructura base que vas a usar como punto de partida para tu proyecto en este programa. Es la misma estructura que vas a ir ampliando bloque a bloque, hasta llegar a la aplicación completa que entregas en el Gate 3.

## Contenido

- [Qué hace la aplicación](#qué-hace-la-aplicación)
- [Requisitos previos](#requisitos-previos)
- [Cómo empezar](#cómo-empezar)
- [Estructura de carpetas](#estructura-de-carpetas)
- [Solución de problemas](#solución-de-problemas)
- [Reglas que se mantienen durante todo el programa](#reglas-que-se-mantienen-durante-todo-el-programa)
- [Registro del ensayo de instalación limpia](#registro-del-ensayo-de-instalación-limpia)

## Qué hace la aplicación

Es una miniaplicación de Python que consume la API de Gemini mediante peticiones HTTP (`requests`). En ella practicas, paso a paso:

- Armar la petición y enviarla al modelo, incluyendo `systemInstruction` y una respuesta estructurada en JSON.
- Medir la **latencia** y calcular el **costo** de cada llamada a partir de los tokens usados.
- Manejar errores de forma controlada (credencial inválida, límite de uso, caída del servicio, respuesta mal formada).
- Evaluar y comparar modelos, y comprobar la consistencia de las respuestas con un banco de prompts.

## Requisitos previos

- **Git**, para clonar el repositorio.
- **Python 3.10 o superior**. Verifica tu versión con `python --version`.
- Una **llave de API de Gemini** (se obtiene en [Google AI Studio](https://aistudio.google.com/apikey)).

## Cómo empezar

Estos pasos se completan de forma progresiva a lo largo de la Unidad U1.2, no todos el mismo día:

1. Clona este repositorio y entra a la carpeta del proyecto:

   ```bash
   git clone https://github.com/edlancelot/SkillNest
   cd SkillNest
   ```

2. Crea tu entorno virtual de Python usando el comando `python -m venv venv` en tu terminal y actívalo según tu sistema y terminal:

   - **macOS / Linux (Terminal, zsh o bash):**
     ```bash
     source venv/bin/activate
     ```

   - **Windows (PowerShell):**
     ```powershell
     venv\Scripts\Activate.ps1
     ```
     > Si PowerShell bloquea la ejecución de scripts, ejecuta primero:
     > `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`

   - **Windows (Git Bash):**
     ```bash
     source venv/Scripts/activate
     ```

   - **Windows (CMD):**
     ```cmd
     venv\Scripts\activate.bat
     ```

   Sabrás que quedó activo cuando veas `(venv)` al inicio de la línea de tu terminal.

3. Instala las dependencias del proyecto para poder usarlas en la aplicación:

   ```bash
   pip install -r requirements.txt
   ```

4. Copia `.env.example` a un archivo nuevo llamado `.env`. Usa el comando de tu terminal:

   - **PowerShell:**
     ```powershell
     Copy-Item .env.example .env
     ```

   - **macOS / Linux / Git Bash:**
     ```bash
     cp .env.example .env
     ```

   - **CMD:**
     ```cmd
     copy .env.example .env
     ```

   Luego abre `.env` y reemplaza `tu_llave_aqui` por tu llave real de Gemini:

   ```env
   GEMINI_API_KEY=tu_llave_aqui
   ```

   > ⚠️ El archivo `.env` contiene tu credencial: no lo compartas ni lo subas al repositorio. Ya está excluido en `.gitignore`; puedes comprobarlo con `git status`, donde `.env` no debe aparecer.

5. Ejecuta la aplicación desde la raíz del proyecto:

   ```bash
   python src/consumir_gemini.py
   ```

   Si todo está bien configurado, verás por cada petición la respuesta en JSON del modelo (con las claves `categoria` y `confianza`), junto con la latencia y el costo estimado:

   ```text
   Latencia Time: 1.20 segundos
   Costo de la petición: $0.000050 USD
   ```

   Los valores son solo un ejemplo y cambian en cada ejecución. Ten en cuenta que el script realiza varias llamadas seguidas a la API, por lo que consume parte de tu cuota.

## Estructura de carpetas

```text
.
├── src/                       código fuente del proyecto
│   ├── consumir_gemini.py     cliente de la API: petición, errores, costo y parseo de JSON
│   ├── evaluacion_modelos.py  compara modelos midiendo latencia y costo
│   ├── test_consistencia.py   prueba la consistencia de las respuestas con el banco de prompts
│   └── prompts/               banco de prompts y registro de resultados
├── docs/                      documentación técnica (diagramas, decisiones, notas)
├── tests/                     pruebas del código (se usan más adelante en el programa)
├── cliente.py                 envoltorio con reintentos sobre consumir_gemini (ejecutar desde la raíz)
├── requirements.txt           dependencias de Python
├── .env.example               plantilla de variables de entorno, sin valores reales
└── .gitignore                 archivos y carpetas que Git debe ignorar
```

- `requirements.txt`: permite que cualquier otra persona reconstruya tu entorno con un solo comando.
- `.env.example`: tu archivo `.env` real (con tus credenciales) nunca se commitea.
- `.gitignore`: entre otras cosas, ignora tu entorno virtual y tu archivo `.env`.

## Solución de problemas

| Síntoma | Causa probable | Qué hacer |
|---|---|---|
| `Credencial invalida o sin permiso` | `GEMINI_API_KEY` vacía, mal copiada o sin permisos | Revisa el valor en `.env` y que no tenga espacios ni comillas de más |
| `Límite excedido` | Demasiadas peticiones en poco tiempo | Espera unos segundos y vuelve a intentar |
| `El proveedor no pudo procesar la peticion` | Error temporal del servicio | Espera y reintenta |
| `No se puede conectar con el servicio` | Sin conexión a internet o red bloqueada | Revisa tu conexión |
| `ModuleNotFoundError` | El entorno virtual no está activo o faltan dependencias | Actívalo (paso 2) y ejecuta `pip install -r requirements.txt` |
| `python` no se reconoce como comando | Python no está instalado o no está en el `PATH` | Instálalo y vuelve a abrir la terminal |

## Reglas que se mantienen durante todo el programa

- Ningún secreto (contraseña, llave de API, token) va escrito directamente en el código ni en ningún archivo que se suba al repositorio.
- Cada proyecto nuevo tiene su propio entorno virtual: no se comparten dependencias entre proyectos distintos.
- Todo el trabajo que se entrega en este programa vive en un repositorio de GitHub, sin excepción.

## Registro del ensayo de instalación limpia

| Fecha | Encontrado | Corregido | Resultado tras la corrección |
|---|---|---|---|
| 22/10/2026 | En el README.md, no aparece el link del repositorio. | Se puso el link correcto del repositorio. | El repositorio se clonó de forma satisfactoria. |
