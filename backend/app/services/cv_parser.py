import json
import re
from pathlib import Path
from typing import Dict, List, Set

class CVParser:
    
    def __init__(self):
        # Cargar las bases de datos
        self.skills_db = self._load_json('skills_database.json')
        self.keywords_db = self._load_json('keywords.json')
    
    def _load_json(self, filename: str) -> Dict:
        try:
            data_path = Path(__file__).parent.parent.parent / 'data' / filename
            with open(data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error cargando {filename}: {e}")
            return {}
    
    def parse(self, cv_text: str) -> Dict:
        # Normalizar texto para el análisis
        normalized_text = cv_text.lower()
        
        # Extraer información
        technical_skills = self._extract_technical_skills(normalized_text)
        soft_skills = self._extract_soft_skills(normalized_text)
        experience_info = self._extract_experience(normalized_text, cv_text)
        context_info = self._extract_context(normalized_text)
        roles = self._extract_roles(normalized_text)
        certifications = self._extract_certifications(normalized_text, cv_text)
        methodologies = self._extract_methodologies(normalized_text)
        
        return {
            "technical_skills": technical_skills,
            "soft_skills": soft_skills,
            "experience": experience_info,
            "context": context_info,
            "roles": roles,
            "certifications": certifications,
            "methodologies": methodologies,
            "summary": self._generate_summary(
                technical_skills, 
                experience_info, 
                context_info
            )
        }
    
    def _extract_technical_skills(self, text: str) -> Dict[str, List[str]]:
        found_skills = {
            "programming_languages": [],
            "frameworks_backend": [],
            "frameworks_frontend": [],
            "mobile_development": [],
            "databases": [],
            "cloud_platforms": [],
            "devops_tools": [],
            "version_control": [],
            "testing": [],
            "data_science_ml": [],
            "other_tools": []
        }
        
        technical_skills = self.skills_db.get('technical_skills', {})
        
        for category, skills_list in technical_skills.items():
            for skill in skills_list:
                # Buscar skill en el texto 
                if re.search(r'\b' + re.escape(skill.lower()) + r'\b', text):
                    found_skills[category].append(skill)
        
        # Eliminar categorías vacías
        found_skills = {k: v for k, v in found_skills.items() if v}
        
        return found_skills
    
    def _extract_soft_skills(self, text: str) -> List[str]:
        found_skills = []
        soft_skills = self.skills_db.get('soft_skills', [])
        
        for skill in soft_skills:
            if skill.lower() in text:
                found_skills.append(skill)
        
        return found_skills
    
    def _extract_experience(self, text: str, original_text: str) -> Dict:
        experience_data = {
            "years_detected": [],
            "level": "unknown",
            "details": []
        }
        
        # Buscar patrones de años de experiencia
        patterns = self.keywords_db.get('experience_patterns', {}).get('years_experience', [])
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                experience_data["years_detected"].extend(matches)
        
        # Detectar nivel 
        levels = self.skills_db.get('experience_keywords', {}).get('experience_levels', {})
        
        for level, keywords in levels.items():
            for keyword in keywords:
                if keyword.lower() in text:
                    experience_data["level"] = level
                    break
            if experience_data["level"] != "unknown":
                break
        
        # Buscar periodos de tiempo
        time_patterns = self.keywords_db.get('experience_patterns', {}).get('time_periods', [])
        for pattern in time_patterns:
            matches = re.findall(pattern, original_text)
            experience_data["details"].extend(matches)
        
        return experience_data
    
    def _extract_context(self, text: str) -> Dict[str, int]:
        context_counts = {
            "professional": 0,
            "academic": 0,
            "personal": 0
        }
        
        context_keywords = self.skills_db.get('context_keywords', {})
        
        for context_type, keywords in context_keywords.items():
            for keyword in keywords:
                # Contar cuántas veces aparece cada keyword
                count = len(re.findall(r'\b' + re.escape(keyword.lower()) + r'\b', text))
                context_counts[context_type] += count
        
        # Calcular porcentajes
        total = sum(context_counts.values())
        if total > 0:
            context_percentages = {
                k: round((v / total) * 100, 2) 
                for k, v in context_counts.items()
            }
        else:
            context_percentages = {k: 0 for k in context_counts.keys()}
        
        return {
            "counts": context_counts,
            "percentages": context_percentages,
            "dominant": max(context_percentages, key=context_percentages.get)
        }
    
    def _extract_roles(self, text: str) -> List[str]:
        found_roles = []
        roles = self.skills_db.get('job_roles', [])
        
        for role in roles:
            if re.search(r'\b' + re.escape(role.lower()) + r'\b', text):
                found_roles.append(role)
        
        return found_roles
    
    def _extract_certifications(self, text: str, original_text: str) -> List[str]:
        found_certs = []
        certifications = self.skills_db.get('certifications', [])
        
        for cert in certifications:
            if cert.lower() in text:
                found_certs.append(cert)
        
        return found_certs
    
    def _extract_methodologies(self, text: str) -> List[str]:
        found_methods = []
        methodologies = self.skills_db.get('methodologies', [])
        
        for method in methodologies:
            if re.search(r'\b' + re.escape(method.lower()) + r'\b', text):
                found_methods.append(method)
        
        return found_methods
    
    def _generate_summary(
        self, 
        technical_skills: Dict, 
        experience: Dict, 
        context: Dict
    ) -> Dict:
        total_technical_skills = sum(len(skills) for skills in technical_skills.values())
        
        return {
            "total_technical_skills": total_technical_skills,
            "skills_by_category": {k: len(v) for k, v in technical_skills.items()},
            "experience_level": experience.get("level", "unknown"),
            "dominant_context": context.get("dominant", "unknown"),
            "context_distribution": context.get("percentages", {})
        }