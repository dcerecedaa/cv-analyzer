# 🎯 CV Analyzer

Sistema de análisis inteligente de currículums que evalúa la compatibilidad entre un CV y una oferta de trabajo mediante un modelo de scoring ponderado.

## 📖 Descripción

CV Analyzer es una aplicación web que permite evaluar automáticamente qué tan bien encaja un perfil profesional con los requisitos de una oferta laboral. A diferencia de los sistemas básicos de detección de palabras clave, este proyecto implementa un modelo de puntuación que considera múltiples factores:

- **Skills técnicas** (60%): Coincidencia de tecnologías, lenguajes y herramientas
- **Experiencia** (30%): Nivel profesional y años de experiencia
- **Contexto** (10%): Origen de la experiencia (profesional, académico, personal)

El objetivo es simular el primer filtro que realizan los ATS y recruiters, ofreciendo un análisis claro, visual y accionable.

## ✨ Características principales

- 📄 Extracción automática de texto desde archivos PDF
- 🔍 Detección de habilidades técnicas organizadas por categorías
- 📊 Análisis del nivel de experiencia (junior, mid, senior)
- 🎯 Identificación del contexto de uso de las tecnologías
- ⚖️ Sistema de scoring ponderado y explicable
- 💡 Recomendaciones personalizadas para mejorar el perfil
- 📱 Interfaz limpia y responsive

## 🛠️ Stack tecnológico

### Backend
- Python 3.10+
- FastAPI - Framework web moderno y rápido
- PyPDF2 - Extracción de texto de PDFs
- Pydantic - Validación de datos
- Uvicorn - Servidor ASGI

### Frontend
- HTML5 / CSS3
- JavaScript vanilla (sin frameworks)
- Diseño responsive

## 📁 Estructura del proyecto
```
cv-analyzer/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   │       └── analyzer.py       # Endpoints de la API
│   │   ├── services/
│   │   │   ├── pdf_extractor.py      # Extracción de texto PDF
│   │   │   ├── cv_parser.py          # Análisis del CV
│   │   │   ├── job_parser.py         # Análisis de ofertas
│   │   │   ├── scoring_engine.py     # Motor de puntuación
│   │   │   └── recommendations.py    # Generador de recomendaciones
│   │   └── main.py                   # Configuración FastAPI
│   ├── data/
│   │   ├── skills_database.json      # Base de datos de tecnologías
│   │   └── keywords.json             # Patrones de detección
│   └── requirements.txt
│
└── frontend/
    ├── css/
    │   ├── main.css                  # Estilos base
    │   ├── components.css            # Componentes reutilizables
    │   └── dashboard.css             # Visualización de resultados
    ├── js/
    │   ├── main.js                   # Lógica principal
    │   ├── api.js                    # Comunicación con backend
    │   └── results-renderer.js       # Renderizado de resultados
    └── index.html
```

## 🚀 Instalación y ejecución

### Requisitos previos
- Python 3.10 o superior
- pip

### 1. Configurar el backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

El servidor API estará corriendo en `http://localhost:8000`

### 2. Abrir el frontend

Abre el archivo `frontend/index.html` con tu navegador o usando Live Server en VS Code.

**Nota:** El backend (puerto 8000) solo expone la API REST. La interfaz visual está en el archivo HTML del frontend.

## 💻 Uso

1. Asegúrate de que el backend esté corriendo en el puerto 8000
2. Abre `frontend/index.html` en tu navegador
3. Sube tu CV en formato PDF (máx. 5MB)
4. Pega el texto completo de la oferta de trabajo
5. Haz clic en "Analizar Compatibilidad"
6. Revisa los resultados:
   - Score de compatibilidad global
   - Desglose por categorías
   - Skills encontradas vs faltantes
   - Recomendaciones personalizadas

## ⚙️ Modelo de scoring

El sistema utiliza un modelo de ponderación configurable:
```python
weights = {
    "skills": 0.60,        # 60% - Coincidencia de tecnologías
    "experience": 0.30,    # 30% - Nivel y años de experiencia
    "context": 0.10        # 10% - Contexto de uso (profesional > personal > académico)
}
```

Este modelo puede ajustarse según las necesidades específicas de cada empresa o sector.

## 🔌 API Endpoints

### POST `/api/analyze`

Analiza un CV contra una oferta de trabajo.

**Request:**
- `cv_file` (file): PDF del currículum
- `job_offer` (string): Texto de la oferta

**Response:**
```json
{
  "status": "success",
  "data": {
    "cv_analysis": { ... },
    "job_analysis": { ... },
    "match_result": {
      "total_score": 66.33,
      "breakdown": { ... },
      "skills_found": { ... },
      "skills_missing": { ... }
    },
    "recommendations": {
      "critical": [ ... ],
      "improvements": [ ... ],
      "strengths": [ ... ]
    }
  }
}
```

## ⚠️ Limitaciones conocidas

- Solo soporta archivos PDF (no DOCX)
- La detección de años de experiencia es básica y puede mejorarse con regex más complejos
- El análisis está optimizado para perfiles técnicos (desarrollo de software)
- No hay persistencia de datos (sin base de datos)

## 🔮 Posibles mejoras futuras

- Soporte para más formatos de CV (DOCX, TXT)
- Integración con LinkedIn API
- Comparación de múltiples CVs para una misma oferta
- Exportación de resultados a PDF
- Sistema de usuarios e historial de análisis
- Scraping automático de ofertas de empleo
- Fine-tuning del modelo con datos reales

## 🤝 Contribuciones

Este proyecto está abierto a sugerencias y feedback. Si tienes ideas de mejora o encuentras algún bug, no dudes en abrir un issue.

## 📜 Derechos de uso

Este código es de visualización pública con fines demostrativos. Puedes explorar y aprender del código, pero **no está permitido su uso en proyectos comerciales o personales**. El propósito es mostrar habilidades técnicas y lógica de programación.

## 👨‍💻 Autor

David Cereceda Pérez  
[GitHub](https://github.com/dcerecedaa) | [LinkedIn](https://linkedin.com/in/david-cereceda-perez-3ba0962b6)

---

**Nota:** Este proyecto fue desarrollado como demostración de habilidades técnicas en desarrollo full-stack y procesamiento de lenguaje natural aplicado.
