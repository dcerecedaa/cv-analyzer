class ResultsRenderer {
    constructor() {
        // Elementos del DOM
        this.resultsSection = document.getElementById('resultsSection');
        this.scoreValue = document.getElementById('scoreValue');
        this.scoreCircle = document.getElementById('scoreCircle');
        this.scoreDescription = document.getElementById('scoreDescription');
        
        // Breakdown
        this.skillsScore = document.getElementById('skillsScore');
        this.skillsBar = document.getElementById('skillsBar');
        this.skillsDetail = document.getElementById('skillsDetail');
        
        this.experienceScore = document.getElementById('experienceScore');
        this.experienceBar = document.getElementById('experienceBar');
        this.experienceDetail = document.getElementById('experienceDetail');
        
        this.contextScore = document.getElementById('contextScore');
        this.contextBar = document.getElementById('contextBar');
        this.contextDetail = document.getElementById('contextDetail');
        
        // Skills
        this.foundCount = document.getElementById('foundCount');
        this.missingCount = document.getElementById('missingCount');
        this.skillsFound = document.getElementById('skillsFound');
        this.skillsMissing = document.getElementById('skillsMissing');
        
        // Recomendaciones
        this.criticalList = document.getElementById('criticalList');
        this.improvementsList = document.getElementById('improvementsList');
        this.strengthsList = document.getElementById('strengthsList');
        this.criticalGroup = document.getElementById('criticalGroup');
        this.improvementsGroup = document.getElementById('improvementsGroup');
        this.strengthsGroup = document.getElementById('strengthsGroup');
    }
    
    render(data) {
        const { match_result, recommendations } = data;
        
        // Mostrar sección de resultados
        this.resultsSection.classList.add('active');
        
        setTimeout(() => {
            this.resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 300);
        
        // Renderizar cada sección
        this.renderScore(match_result);
        this.renderBreakdown(match_result.breakdown);
        this.renderSkills(match_result);
        this.renderRecommendations(recommendations);
    }
    
    renderScore(matchResult) {
        const score = matchResult.total_score;
        this.scoreValue.textContent = `${score}%`;
        
        const circumference = 565.48; 
        const offset = circumference - (score / 100) * circumference;
        
        setTimeout(() => {
            this.scoreCircle.style.strokeDashoffset = offset;
        }, 100);
        
        // Cambiar color según el score
        let strokeColor;
        if (score >= 70) {
            strokeColor = '#4caf50'; 
        } else if (score >= 40) {
            strokeColor = '#ff9800'; 
        } else {
            strokeColor = '#f44336'; 
        }
        this.scoreCircle.style.stroke = strokeColor;
        
        // Descripción
        this.scoreDescription.textContent = this.getScoreDescription(score);
    }
    
    renderBreakdown(breakdown) {
        // Skills
        this.skillsScore.textContent = `${breakdown.skills.score}%`;
        this.skillsBar.style.width = `${breakdown.skills.score}%`;
        this.skillsDetail.textContent = `Encontradas: ${breakdown.skills.details.found}/${breakdown.skills.details.required} | Peso: 60%`;
        
        // Experiencia
        this.experienceScore.textContent = `${breakdown.experience.score}%`;
        this.experienceBar.style.width = `${breakdown.experience.score}%`;
        this.experienceDetail.textContent = `${breakdown.experience.details.match || 'Evaluado'} | Peso: 30%`;
        
        // Contexto
        this.contextScore.textContent = `${breakdown.context.score}%`;
        this.contextBar.style.width = `${breakdown.context.score}%`;
        this.contextDetail.textContent = `Dominante: ${breakdown.context.details.dominant} | Peso: 10%`;
    }
    
    renderSkills(matchResult) {
        const { skills_found, skills_missing, total_found, total_required } = matchResult;
        
        // Actualizar contadores
        this.foundCount.textContent = total_found;
        this.missingCount.textContent = total_required - total_found;
        
        // Renderizar skills encontradas
        if (Object.keys(skills_found).length > 0) {
            this.skillsFound.innerHTML = '';
            for (const [category, skills] of Object.entries(skills_found)) {
                const categoryDiv = this.createSkillCategory(category, skills, 'found');
                this.skillsFound.appendChild(categoryDiv);
            }
        } else {
            this.skillsFound.innerHTML = '<p class="empty-state">No se encontraron coincidencias de skills técnicas</p>';
        }
        
        // Renderizar skills faltantes
        if (Object.keys(skills_missing).length > 0) {
            this.skillsMissing.innerHTML = '';
            for (const [category, skills] of Object.entries(skills_missing)) {
                const categoryDiv = this.createSkillCategory(category, skills, 'missing');
                this.skillsMissing.appendChild(categoryDiv);
            }
        } else {
            this.skillsMissing.innerHTML = '<p class="empty-state">¡Tienes todas las skills requeridas!</p>';
        }
    }
    
    createSkillCategory(category, skills, type) {
        const categoryDiv = document.createElement('div');
        categoryDiv.className = 'skill-category';
        
        const categoryName = document.createElement('div');
        categoryName.className = 'skill-category-name';
        categoryName.textContent = this.formatCategoryName(category);
        
        const skillsContainer = document.createElement('div');
        skillsContainer.style.display = 'flex';
        skillsContainer.style.flexWrap = 'wrap';
        skillsContainer.style.gap = '8px';
        
        skills.forEach(skill => {
            const tag = document.createElement('span');
            tag.className = `skill-tag ${type}`;
            tag.textContent = skill;
            skillsContainer.appendChild(tag);
        });
        
        categoryDiv.appendChild(categoryName);
        categoryDiv.appendChild(skillsContainer);
        
        return categoryDiv;
    }
    
    renderRecommendations(recommendations) {
        // Críticas
        if (recommendations.critical && recommendations.critical.length > 0) {
            this.criticalList.innerHTML = '';
            recommendations.critical.forEach(rec => {
                const li = document.createElement('li');
                li.textContent = rec;
                this.criticalList.appendChild(li);
            });
            this.criticalGroup.style.display = 'block';
        } else {
            this.criticalGroup.style.display = 'none';
        }
        
        // Mejoras
        if (recommendations.improvements && recommendations.improvements.length > 0) {
            this.improvementsList.innerHTML = '';
            recommendations.improvements.forEach(rec => {
                const li = document.createElement('li');
                li.textContent = rec;
                this.improvementsList.appendChild(li);
            });
            this.improvementsGroup.style.display = 'block';
        } else {
            this.improvementsGroup.style.display = 'none';
        }
        
        // Fortalezas
        if (recommendations.strengths && recommendations.strengths.length > 0) {
            this.strengthsList.innerHTML = '';
            recommendations.strengths.forEach(rec => {
                const li = document.createElement('li');
                li.textContent = rec;
                this.strengthsList.appendChild(li);
            });
            this.strengthsGroup.style.display = 'block';
        } else {
            this.strengthsGroup.style.display = 'none';
        }
    }
    
    getScoreDescription(score) {
        if (score >= 80) {
            return '¡Excelente match! El perfil se ajusta muy bien a esta oferta.';
        } else if (score >= 60) {
            return 'Buen match. Cumple con la mayoría de requisitos importantes.';
        } else if (score >= 40) {
            return 'Match moderado. Considera reforzar algunas áreas clave.';
        } else {
            return 'Match bajo. Esta oferta requiere habilidades que aún no tienes desarrolladas.';
        }
    }
    
    formatCategoryName(category) {
        const translations = {
            "programming_languages": "Lenguajes de Programación",
            "frameworks_backend": "Frameworks Backend",
            "frameworks_frontend": "Frameworks Frontend",
            "mobile_development": "Desarrollo Móvil",
            "databases": "Bases de Datos",
            "cloud_platforms": "Plataformas Cloud",
            "devops_tools": "Herramientas DevOps",
            "version_control": "Control de Versiones",
            "testing": "Testing",
            "data_science_ml": "Data Science/ML",
            "other_tools": "Otras Herramientas"
        };
        return translations[category] || category.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    }
}