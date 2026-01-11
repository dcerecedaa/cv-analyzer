// Elementos del DOM
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const analyzeBtn = document.getElementById('analyzeBtn');
const jobOffer = document.getElementById('jobOffer');

// Variable para almacenar el archivo
let uploadedFile = null;

// Inicializar renderer de resultados
const resultsRenderer = new ResultsRenderer();

// ===== DRAG & DROP =====

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, preventDefaults, false);
    document.body.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, highlight, false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, unhighlight, false);
});

function highlight() {
    dropZone.classList.add('drag-over');
}

function unhighlight() {
    dropZone.classList.remove('drag-over');
}

dropZone.addEventListener('drop', handleDrop, false);

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;

    if (files.length > 0) {
        handleFile(files[0]);
    }
}

// ===== CLICK PARA SELECCIONAR =====

dropZone.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFile(e.target.files[0]);
    }
});

// ===== VALIDACIÓN Y PROCESAMIENTO DEL ARCHIVO =====

function handleFile(file) {
    // Validar tipo de archivo
    if (file.type !== 'application/pdf') {
        alert('Por favor, sube solo archivos PDF');
        return;
    }

    // Validar tamaño (5MB máximo)
    const maxSize = 5 * 1024 * 1024; // 5MB en bytes
    if (file.size > maxSize) {
        alert('El archivo es demasiado grande. Máximo 5MB');
        return;
    }

    // Archivo válido
    uploadedFile = file;
    
    // Mostrar información del archivo
    fileName.textContent = `${file.name} (${formatFileSize(file.size)})`;
    fileInfo.classList.add('active');

    checkFormReady();
}

// ===== VALIDACIÓN DEL FORMULARIO =====

jobOffer.addEventListener('input', checkFormReady);

function checkFormReady() {
    if (uploadedFile && jobOffer.value.trim().length > 50) {
        analyzeBtn.disabled = false;
    } else {
        analyzeBtn.disabled = true;
    }
}

// ===== FUNCIONES AUXILIARES =====

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// ===== BOTÓN DE ANÁLISIS =====

analyzeBtn.addEventListener('click', async () => {
    try {
        // Cambiar estado del botón
        analyzeBtn.textContent = '  Analizando...';
        analyzeBtn.disabled = true;

        // Llamar al backend
        const result = await analyzeCV(uploadedFile, jobOffer.value);

        // Log en consola para debugging
        console.log('========================================');
        console.log(' RESULTADO DEL ANÁLISIS COMPLETO');
        console.log('========================================');
        console.log('Respuesta completa:', result);
        console.log('========================================');
        
        // Renderizar resultados en el dashboard
        resultsRenderer.render(result.data);

    } catch (error) {
        console.error('Error:', error);
        alert(`Error: ${error.message}`);
    } finally {
        analyzeBtn.textContent = 'Analizar Compatibilidad';
        checkFormReady(); 
    }
});