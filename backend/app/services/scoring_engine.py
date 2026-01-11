from typing import Dict, List, Set

class ScoringEngine:
    """
    Motor de scoring que calcula la compatibilidad entre CV y oferta
    Modelo de ponderación:
    - 60% Coincidencia de skills
    - 30% Nivel de experiencia
    - 10% Contexto profesional
    """
    
    def __init__(self):
        self.weights = {
            "skills": 0.60,
            "experience": 0.30,
            "context": 0.10
        }
    
    def calculate_match(
        self, 
        cv_analysis: Dict, 
        job_analysis: Dict
    ) -> Dict:

        skills_score = self._calculate_skills_match(
            cv_analysis.get("technical_skills", {}),
            job_analysis.get("required_skills", {})
        )
        
        experience_score = self._calculate_experience_match(
            cv_analysis.get("experience", {}),
            job_analysis.get("required_experience", {})
        )
        
        context_score = self._calculate_context_match(
            cv_analysis.get("context", {})
        )
        
        total_score = (
            skills_score["score"] * self.weights["skills"] +
            experience_score["score"] * self.weights["experience"] +
            context_score["score"] * self.weights["context"]
        )
        
        skills_comparison = self._compare_skills(
            cv_analysis.get("technical_skills", {}),
            job_analysis.get("required_skills", {})
        )
        
        return {
            "total_score": round(total_score, 2),
            "breakdown": {
                "skills": {
                    "score": round(skills_score["score"], 2),
                    "weight": self.weights["skills"] * 100,
                    "contribution": round(skills_score["score"] * self.weights["skills"], 2),
                    "details": skills_score["details"]
                },
                "experience": {
                    "score": round(experience_score["score"], 2),
                    "weight": self.weights["experience"] * 100,
                    "contribution": round(experience_score["score"] * self.weights["experience"], 2),
                    "details": experience_score["details"]
                },
                "context": {
                    "score": round(context_score["score"], 2),
                    "weight": self.weights["context"] * 100,
                    "contribution": round(context_score["score"] * self.weights["context"], 2),
                    "details": context_score["details"]
                }
            },
            "skills_found": skills_comparison["found"],
            "skills_missing": skills_comparison["missing"],
            "total_required": skills_comparison["total_required"],
            "total_found": skills_comparison["total_found"]
        }
    
    def _calculate_skills_match(
        self, 
        cv_skills: Dict[str, List[str]], 
        job_skills: Dict[str, List[str]]
    ) -> Dict:
        if not job_skills:
            return {
                "score": 100.0,
                "details": "No hay requisitos técnicos específicos en la oferta"
            }
        
        cv_skills_flat = set()
        for skills_list in cv_skills.values():
            cv_skills_flat.update([s.lower() for s in skills_list])
        
        job_skills_flat = set()
        for skills_list in job_skills.values():
            job_skills_flat.update([s.lower() for s in skills_list])
        
        matching_skills = cv_skills_flat.intersection(job_skills_flat)
        
        if len(job_skills_flat) == 0:
            match_percentage = 100.0
        else:
            match_percentage = (len(matching_skills) / len(job_skills_flat)) * 100
        
        return {
            "score": match_percentage,
            "details": {
                "required": len(job_skills_flat),
                "found": len(matching_skills),
                "missing": len(job_skills_flat) - len(matching_skills),
                "match_rate": f"{len(matching_skills)}/{len(job_skills_flat)}"
            }
        }
    
    def _calculate_experience_match(
        self, 
        cv_experience: Dict, 
        job_experience: Dict
    ) -> Dict:
        score = 0
        details = {}
        
        level_scores = {
            "junior": 1,
            "mid": 2,
            "senior": 3,
            "unknown": 0
        }
        
        cv_level = cv_experience.get("level", "unknown")
        required_level = job_experience.get("level_required", "unknown")
        
        if required_level == "unknown":
            score = 85.0
            details["note"] = "No hay requisito de nivel específico"
        else:
            cv_level_score = level_scores.get(cv_level, 0)
            required_level_score = level_scores.get(required_level, 0)
            
            if cv_level_score >= required_level_score:
                score = 100.0
                details["match"] = f"Nivel {cv_level} cumple con requisito de {required_level}"
            elif cv_level_score == required_level_score - 1:
                score = 70.0
                details["match"] = f"Nivel {cv_level} está un escalón por debajo de {required_level}"
            else:
                score = 40.0
                details["match"] = f"Nivel {cv_level} está por debajo de {required_level}"
        
        required_years = job_experience.get("years_required", [])
        if required_years:
            try:
                min_years_required = int(required_years[0])
                details["years_required"] = min_years_required
                
                if cv_level_score >= required_level_score:
                    details["years_note"] = "Nivel adecuado sugiere experiencia suficiente"
                else:
                    details["years_note"] = "Puede requerir más experiencia"
            except:
                pass
        
        return {
            "score": score,
            "details": details
        }
    
    def _calculate_context_match(self, cv_context: Dict) -> Dict:
        percentages = cv_context.get("percentages", {})
        professional_percentage = percentages.get("professional", 0)
        academic_percentage = percentages.get("academic", 0)
        personal_percentage = percentages.get("personal", 0)
        
        score = (
            professional_percentage * 1.0 +
            personal_percentage * 0.6 +
            academic_percentage * 0.3
        )
        
        score = min(score, 100)
        
        details = {
            "professional": f"{professional_percentage}%",
            "academic": f"{academic_percentage}%",
            "personal": f"{personal_percentage}%",
            "dominant": cv_context.get("dominant", "unknown")
        }
        
        return {
            "score": score,
            "details": details
        }
    
    def _compare_skills(
        self, 
        cv_skills: Dict[str, List[str]], 
        job_skills: Dict[str, List[str]]
    ) -> Dict:
        found = {}
        missing = {}
        
        for category, required_skills in job_skills.items():
            cv_skills_in_category = cv_skills.get(category, [])
            
            cv_skills_lower = [s.lower() for s in cv_skills_in_category]
            required_skills_lower = [s.lower() for s in required_skills]
            
            found_in_category = []
            missing_in_category = []
            
            for skill in required_skills:
                if skill.lower() in cv_skills_lower:
                    found_in_category.append(skill)
                else:
                    missing_in_category.append(skill)
            
            if found_in_category:
                found[category] = found_in_category
            
            if missing_in_category:
                missing[category] = missing_in_category
        
        total_required = sum(len(skills) for skills in job_skills.values())
        total_found = sum(len(skills) for skills in found.values())
        
        return {
            "found": found,
            "missing": missing,
            "total_required": total_required,
            "total_found": total_found
        }