from typing import Dict, List

class RecommendationsEngine:
    
    def generate(
        self, 
        cv_analysis: Dict, 
        job_analysis: Dict, 
        match_result: Dict
    ) -> Dict[str, List[str]]:
        recommendations = {
            "critical": [],      
            "improvements": [],  
            "strengths": []      
        }
        
        self._analyze_missing_skills(
            match_result.get("skills_missing", {}),
            match_result.get("skills_found", {}),
            recommendations
        )
        
        self._analyze_experience(
            cv_analysis.get("experience", {}),
            job_analysis.get("required_experience", {}),
            match_result.get("breakdown", {}).get("experience", {}),
            recommendations
        )
        
        self._analyze_context(
            cv_analysis.get("context", {}),
            match_result.get("breakdown", {}).get("context", {}),
            recommendations
        )
        
        self._identify_strengths(
            match_result.get("skills_found", {}),
            cv_analysis,
            recommendations
        )
        
        return recommendations
    
    def _analyze_missing_skills(
        self, 
        missing_skills: Dict, 
        found_skills: Dict,
        recommendations: Dict
    ):
        
        critical_categories = [
            "programming_languages",
            "frameworks_backend",
            "frameworks_frontend"
        ]
        
        common_skills = ["git", "github", "html", "css"]
        
        for category, skills in missing_skills.items():
            category_name = self._format_category_name(category)
            
            for skill in skills:
                skill_lower = skill.lower()
                
                if skill_lower in common_skills:
                    recommendations["improvements"].append(
                        f"Si has usado {skill}, añádelo a tu CV - es una tecnología fundamental"
                    )
                
                elif category in critical_categories:
                    recommendations["critical"].append(
                        f"Tecnología requerida: {skill} ({category_name}) - considera aprenderla o destacarla si ya la conoces"
                    )
                else:
                    recommendations["improvements"].append(
                        f"Considera aprender {skill} ({category_name}) para mejorar tu perfil"
                    )
        
        total_missing = sum(len(skills) for skills in missing_skills.values())
        if total_missing >= 5:
            recommendations["improvements"].append(
                f"Faltan {total_missing} tecnologías requeridas. Prioriza aprender las más críticas para este rol"
            )
    
    def _analyze_experience(
        self,
        cv_experience: Dict,
        job_experience: Dict,
        experience_match: Dict,
        recommendations: Dict
    ):
        
        score = experience_match.get("score", 0)
        cv_level = cv_experience.get("level", "unknown")
        required_level = job_experience.get("level_required", "unknown")
        
        if score < 70:
            if cv_level == "junior" and required_level in ["mid", "senior"]:
                recommendations["improvements"].append(
                    f"La oferta busca nivel {required_level} y tu perfil es {cv_level}. Destaca proyectos relevantes que demuestren más experiencia"
                )
        
        elif score >= 90:
            recommendations["strengths"].append(
                f"Tu nivel de experiencia ({cv_level}) coincide con lo requerido"
            )
        
        required_years = job_experience.get("years_required", [])
        if required_years:
            try:
                min_years = int(required_years[0])
                recommendations["improvements"].append(
                    f"La oferta requiere al menos {min_years} años de experiencia. Si los tienes, asegúrate de mencionarlo claramente en tu CV"
                )
            except:
                pass
    
    def _analyze_context(
        self,
        cv_context: Dict,
        context_match: Dict,
        recommendations: Dict
    ):
        
        percentages = cv_context.get("percentages", {})
        professional = percentages.get("professional", 0)
        academic = percentages.get("academic", 0)
        personal = percentages.get("personal", 0)
        
        # Si el contexto es mayormente académico
        if academic > 60:
            recommendations["improvements"].append(
                "Tu experiencia es principalmente académica. Destaca prácticas, proyectos universitarios aplicados o contribuciones open source"
            )
            
            if personal > 0:
                recommendations["improvements"].append(
                    "Tienes proyectos personales - descríbelos con más detalle para demostrar aplicación práctica"
                )
        
        # Si tiene experiencia profesional
        if professional > 0:
            recommendations["strengths"].append(
                f"Tienes {professional}% de contexto profesional - esto es muy valorado"
            )
        
        # Si es 100% académico sin proyectos personales
        if academic == 100:
            recommendations["critical"].append(
                "Desarrolla proyectos personales o contribuye a open source para complementar tu formación académica"
            )
    
    def _identify_strengths(
        self,
        found_skills: Dict,
        cv_analysis: Dict,
        recommendations: Dict
    ):
        
        total_found = sum(len(skills) for skills in found_skills.values())
        if total_found > 0:
            for category, skills in found_skills.items():
                category_name = self._format_category_name(category)
                recommendations["strengths"].append(
                    f"Coincidencia en {category_name}: {', '.join(skills)} - destácalos en tu CV"
                )
        
        soft_skills = cv_analysis.get("soft_skills", [])
        if soft_skills:
            recommendations["strengths"].append(
                f"Skills blandas identificadas: {', '.join(soft_skills)}"
            )
        
        methodologies = cv_analysis.get("methodologies", [])
        if methodologies:
            recommendations["strengths"].append(
                f"Conoces metodologías: {', '.join(methodologies)} - menciónalas si son relevantes"
            )
    
    def _format_category_name(self, category: str) -> str:
        translations = {
            "programming_languages": "Lenguajes de programación",
            "frameworks_backend": "Frameworks backend",
            "frameworks_frontend": "Frameworks frontend",
            "mobile_development": "Desarrollo móvil",
            "databases": "Bases de datos",
            "cloud_platforms": "Plataformas cloud",
            "devops_tools": "Herramientas DevOps",
            "version_control": "Control de versiones",
            "testing": "Testing",
            "data_science_ml": "Data Science/ML",
            "other_tools": "Otras herramientas"
        }
        return translations.get(category, category.replace("_", " ").title())