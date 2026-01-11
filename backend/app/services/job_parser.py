import json
import re
from pathlib import Path
from typing import Dict, List

class JobParser:
    
    def __init__(self):
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
    
    def parse(self, job_text: str) -> Dict:
        # Normalizar texto
        normalized_text = job_text.lower()
        
        # Extraer requisitos
        required_skills = self._extract_required_skills(normalized_text)
        required_experience = self._extract_required_experience(normalized_text, job_text)
        nice_to_have = self._extract_nice_to_have(normalized_text)
        
        return {
            "required_skills": required_skills,
            "required_experience": required_experience,
            "nice_to_have_skills": nice_to_have,
            "total_requirements": self._count_total_requirements(required_skills)
        }
    
    def _extract_required_skills(self, text: str) -> Dict[str, List[str]]:
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
                if re.search(r'\b' + re.escape(skill.lower()) + r'\b', text):
                    found_skills[category].append(skill)
        
        found_skills = {k: v for k, v in found_skills.items() if v}
        
        return found_skills
    
    def _extract_required_experience(self, text: str, original_text: str) -> Dict:
        experience_data = {
            "years_required": [],
            "level_required": "unknown",
            "details": []
        }
        
        patterns = [
            r'(\d+)\s*(?:\+|o más)?\s*años?\s+de\s+experiencia',
            r'(\d+)\s*(?:\+|or more)?\s*years?\s+(?:of\s+)?experience',
            r'mínimo\s+(\d+)\s+años?',
            r'minimum\s+(\d+)\s+years?',
            r'al menos\s+(\d+)\s+años?',
            r'at least\s+(\d+)\s+years?'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                experience_data["years_required"].extend(matches)
        
        levels = self.skills_db.get('experience_keywords', {}).get('experience_levels', {})
        
        for level, keywords in levels.items():
            for keyword in keywords:
                if keyword.lower() in text:
                    experience_data["level_required"] = level
                    break
            if experience_data["level_required"] != "unknown":
                break
        
        return experience_data
    
    def _extract_nice_to_have(self, text: str) -> List[str]:
        nice_to_have_skills = []
        
        # Patrones que indican skills opcionales
        optional_patterns = [
            r'(?:nice to have|deseable|valorable|se valorará|plus|bonus).*?(?:\n|$)',
            r'(?:opcionales?|optional).*?(?:\n|$)'
        ]
        
        # Buscar secciones opcionales
        optional_sections = []
        for pattern in optional_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                optional_sections.append(match.group())
        
        # Si hay secciones opcionales, buscar skills en ellas
        if optional_sections:
            optional_text = ' '.join(optional_sections)
            technical_skills = self.skills_db.get('technical_skills', {})
            
            for category, skills_list in technical_skills.items():
                for skill in skills_list:
                    if re.search(r'\b' + re.escape(skill.lower()) + r'\b', optional_text):
                        nice_to_have_skills.append(skill)
        
        return nice_to_have_skills
    
    def _count_total_requirements(self, required_skills: Dict) -> int:
        return sum(len(skills) for skills in required_skills.values())