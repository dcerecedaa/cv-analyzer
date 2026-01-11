const API_BASE_URL = 'http://localhost:8000/api';

async function analyzeCV(file, jobOfferText) {
    try {
        // Crear FormData para enviar archivo y texto
        const formData = new FormData();
        formData.append('cv_file', file);
        formData.append('job_offer', jobOfferText);

        // Realizar petición
        const response = await fetch(`${API_BASE_URL}/analyze`, {
            method: 'POST',
            body: formData
        });

        // Verificar si la respuesta es correcta
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Error en el análisis');
        }

        // Retornar datos
        const data = await response.json();
        return data;

    } catch (error) {
        console.error('Error al conectar con el backend:', error);
        throw error;
    }
}

async function checkBackendHealth() {
    try {
        const response = await fetch('http://localhost:8000/');
        return response.ok;
    } catch (error) {
        return false;
    }
}