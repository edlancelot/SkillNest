<h1 align="center">🤖 Proyecto de Eduardo Rivas</h1>

<p align="center">
  <b>Especialización en Desarrollo con IA Generativa · Accenture</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Git-control%20de%20versiones-F05032?logo=git&logoColor=white" alt="Git">
  <img src="https://img.shields.io/badge/GitHub-repositorio-181717?logo=github&logoColor=white" alt="GitHub">
  <img src="https://img.shields.io/badge/Estado-en%20desarrollo-yellow" alt="Estado">
</p>

---

Esta es la estructura base que vas a usar como punto de partida para tu proyecto en este programa. Es la misma estructura que vas a ir ampliando bloque a bloque, hasta llegar a la aplicación completa que entregas en el Gate 3. 🎯

## 📑 Contenido

- [🚀 Cómo empezar](#-cómo-empezar)
- [📁 Estructura de carpetas](#-estructura-de-carpetas)
- [📏 Reglas del programa](#-reglas-que-se-mantienen-durante-todo-el-programa)

---

## 🚀 Cómo empezar

Estos pasos se completan de forma progresiva a lo largo de la Unidad U1.2, no todos el mismo día:

1. 📦 **Descarga y descomprime** el archivo comprimido (adjunto en la plataforma). Inicializa el control de versiones sobre esa carpeta y registra tu primer commit con esta estructura base, tal como llegó, antes de modificar nada.
2. 🐍 **Crea tu entorno virtual** de Python (por ejemplo, con `venv`) y actívalo.
3. 📚 **Instala las dependencias** que necesites y regístralas en `requirements.txt` (al inicio puede estar vacío o con muy pocas).
4. 🔑 **Configura tus credenciales**: copia `.env.example` a un archivo nuevo llamado `.env` y completa ahí tus llaves de API y tokens.

> [!IMPORTANT]
> El archivo `.env` **nunca** se sube al repositorio: ya está excluido en `.gitignore`.

## 📁 Estructura de carpetas

| Elemento | Descripción |
| --- | --- |
| 💻 `src/` | Todo el código fuente de tu proyecto va aquí. |
| 📝 `docs/` | Documentación técnica del proyecto (diagramas, decisiones de arquitectura, notas). |
| 🧪 `tests/` | Pruebas de tu código (las vas a usar más adelante, cuando el proyecto lo requiera). |
| 📋 `requirements.txt` | Dependencias de Python, para que cualquier persona reconstruya tu entorno con un solo comando. |
| 🔐 `.env.example` | Plantilla de las variables de entorno que necesita tu proyecto, sin valores reales. |
| 🙈 `.gitignore` | Le dice a Git qué ignorar (entre otros, tu entorno virtual y tu archivo `.env`). |

## 📏 Reglas que se mantienen durante todo el programa

> [!WARNING]
> Estas reglas aplican a todos los proyectos, sin excepción.

- 🔒 Ningún secreto (contraseña, llave de API, token) va escrito directamente en el código ni en ningún archivo que se suba al repositorio.
- 🧱 Cada proyecto nuevo tiene su propio entorno virtual: no se comparten dependencias entre proyectos distintos.
- 🐙 Todo el trabajo que se entrega en este programa vive en un repositorio de GitHub, sin excepción.
