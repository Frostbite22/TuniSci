class TunisianAcademicKeywords:
    def __init__(self):
        # Inherit previous variant handling mechanisms
        self.name_variants = {
            # Previous variants remain the same
            "El-Manar": ["El Manar", "Elmanar", "El-Manar", "Manar"],
            "El-Ghazala": ["El Ghazala", "Elghazala", "El-Ghazala", "Ghazala"],
            "Ez-Zitouna": ["Ez Zitouna", "Ezzitouna", "El-Zitouna", "Zitouna", "Zeitouna"],
            "Faculté": ["Faculte", "Facultés", "Facultes"],
            "Institut": ["Institute", "Institue"],
            "École": ["Ecole", "School"],
            "Université": ["Universite", "University"],
            "Supérieur": ["Superieur", "Superior"],
            "Ingénieur": ["Ingenieur", "Engineer"],
            "Médecine": ["Medecine", "Medicine"],
            "Économique": ["Economique", "Economic"],
            "Études": ["Etudes", "Studies"],
            "Préparatoire": ["Preparatoire", "Preparatory"],
            "Génie": ["Genie", "Engineering"],
            "Supérieure": ["Superieure", "Superior"],
            "Appliquées": ["Appliquees", "Applied"]
        }

        # Complete list of public universities
        self.public_universities = [
            # Tunis
            "Université de Tunis",
            "Université de Tunis El Manar",
            "Université de Carthage",
            "Université de la Manouba",
            "Université Virtuelle de Tunis",
            "Université Ez-Zitouna",
            
            # Northern Tunisia
            "Université de Jendouba",
            "Université de Bizerte",
            
            # Coastal Tunisia
            "Université de Sousse",
            "Université de Monastir",
            "Université de Sfax",
            
            # Central Tunisia
            "Université de Kairouan",
            "Université de Gafsa",
            
            # Southern Tunisia
            "Université de Gabès",
            "Université de Tozeur"
        ]

        # Complete list of private universities
        self.private_universities = [
            "Université Centrale Privée de Tunis",
            "Université Libre de Tunis",
            "Université Internationale de Tunis",
            "Université Méditerranéenne de Tunis",
            "Université Privée de Sousse",
            "Université Privée de Sfax"
        ]

        # Complete list of engineering schools
        self.engineering_schools = [
            # Tunis Region
            "École Nationale d'Ingénieurs de Tunis (ENIT)",
            "École Nationale des Sciences de l'Informatique (ENSI)",
            "École Nationale Supérieure d'Ingénieurs de Tunis (ENSIT)",
            "École Supérieure Privée d'Ingénierie et de Technologies (ESPRIT)",
            "École Supérieure des Communications de Tunis (Sup'Com)",
            "Institut National des Sciences Appliquées et de Technologie (INSAT)",
            "École Polytechnique de Tunisie (EPT)",
            "École Supérieure de la Statistique et de l'Analyse de l'Information (ESSAI)",
            
            # Sfax
            "École Nationale d'Ingénieurs de Sfax (ENIS)",
            "École Supérieure d'Informatique et de Multimédia de Sfax",
            
            # Sousse
            "École Nationale d'Ingénieurs de Sousse (ENISo)",
            "Institut Supérieur des Sciences Appliquées et de Technologie de Sousse",
            
            # Monastir
            "École Nationale d'Ingénieurs de Monastir (ENIM)",
            
            # Gabès
            "École Nationale d'Ingénieurs de Gabès (ENIG)",
            
            # Gafsa
            "École Nationale d'Ingénieurs de Gafsa (ENIG-Gafsa)"
        ]

        # Complete list of specialized institutes
        self.specialized_institutes = {
            "Computer Science": [
                "Institut Supérieur d'Informatique (ISI)",
                "Institut Supérieur d'Informatique et de Mathématiques de Monastir",
                "Institut Supérieur d'Informatique et de Multimédia de Sfax",
                "Institut Supérieur d'Informatique et des Techniques de Communication Hammam Sousse",
                "Institut Supérieur d'Informatique de Mahdia",
                "Institut Supérieur d'Informatique du Kef",
                "Institut Supérieur d'Informatique de Medenine"
            ],
            
            "Business": [
                "Institut Supérieur de Gestion de Tunis",
                "Institut des Hautes Études Commerciales de Carthage",
                "Institut Supérieur de Comptabilité et d'Administration des Entreprises",
                "École Supérieure des Sciences Économiques et Commerciales de Tunis",
                "Institut Supérieur de Gestion de Sousse",
                "Institut Supérieur d'Administration des Affaires de Sfax"
            ],
            
            "Technology": [
                "Institut Supérieur des Études Technologiques de Radès",
                "Institut Supérieur des Études Technologiques de Nabeul",
                "Institut Supérieur des Études Technologiques de Sfax",
                "Institut Supérieur des Études Technologiques de Sousse",
                "Institut Supérieur des Études Technologiques de Kairouan",
                "Institut Supérieur des Études Technologiques de Gafsa",
                "Institut Supérieur des Études Technologiques de Gabès",
                "Institut Supérieur des Études Technologiques de Bizerte",
                "Institut Supérieur des Études Technologiques de Jendouba",
                "Institut Supérieur des Études Technologiques de Kélibia",
                "Institut Supérieur des Études Technologiques de Mahdia",
                "Institut Supérieur des Études Technologiques de Médenine",
                "Institut Supérieur des Études Technologiques de Sidi Bouzid",
                "Institut Supérieur des Études Technologiques de Siliana",
                "Institut Supérieur des Études Technologiques de Tataouine",
                "Institut Supérieur des Études Technologiques de Zaghouan",
                "Institut Supérieur des Études Technologiques de Béja",
                "Institut Supérieur des Études Technologiques du Kef",
                "Institut Supérieur des Études Technologiques de Kasserine",
                "Institut Supérieur des Études Technologiques de Tozeur"
            ],
            
            "Applied Sciences": [
                "Institut Supérieur des Sciences Appliquées et de Technologie de Mateur",
                "Institut Supérieur des Sciences Appliquées et de Technologie de Gabès",
                "Institut Supérieur des Sciences Appliquées et de Technologie de Gafsa",
                "Institut Supérieur des Sciences Appliquées et de Technologie de Kairouan",
                "Institut Supérieur des Sciences Appliquées et de Technologie de Mahdia"
            ],
            
            "Preparatory Institutes": [
                "Institut Préparatoire aux Études d'Ingénieurs de Tunis",
                "Institut Préparatoire aux Études d'Ingénieurs de Nabeul",
                "Institut Préparatoire aux Études d'Ingénieurs de Sfax",
                "Institut Préparatoire aux Études d'Ingénieurs de Monastir",
                "Institut Préparatoire aux Études d'Ingénieurs de Gafsa"
            ]
        }

        # Complete list of research institutes
        self.research_institutes = [
            "Institut Pasteur de Tunis",
            "Centre de Biotechnologie de Sfax",
            "Institut National de Recherche et d'Analyse Physico-chimique",
            "Institut National des Sciences et Technologies de la Mer",
            "Centre National des Sciences et Technologies Nucléaires",
            "Institut National de la Recherche Agronomique de Tunisie",
            "Centre de Recherche en Numérique de Sfax",
            "Institut de l'Olivier",
            "Centre International des Technologies de l'Environnement de Tunis",
            "Institut National de la Météorologie",
            "Centre de Recherches et des Technologies de l'Energie",
            "Institut National de Recherche en Génie Rural, Eaux et Forêts"
        ]

        # Complete list of medical faculties and institutes
        self.medical_institutions = [
            "Faculté de Médecine de Tunis",
            "Faculté de Médecine de Sfax",
            "Faculté de Médecine de Sousse",
            "Faculté de Médecine de Monastir",
            "Faculté de Pharmacie de Monastir",
            "Faculté de Médecine Dentaire de Monastir",
            "Institut Supérieur des Sciences Infirmières de Tunis",
            "Institut Supérieur des Sciences Infirmières de Sfax",
            "Institut Supérieur des Sciences Infirmières de Sousse",
            "École Supérieure des Sciences et Techniques de la Santé de Tunis",
            "École Supérieure des Sciences et Techniques de la Santé de Sfax",
            "École Supérieure des Sciences et Techniques de la Santé de Monastir",
            "École Supérieure des Sciences et Techniques de la Santé de Sousse"
        ]

    def generate_all_variants(self, institution_name):
        """
        Generates all possible variants for an institution name
        """
        variants = [institution_name]
        for key, values in self.name_variants.items():
            if key in institution_name:
                for variant in values:
                    new_variants = [name.replace(key, variant) for name in variants]
                    variants.extend(new_variants)
        
        # Add variants with and without parentheses for abbreviations
        if "(" in institution_name:
            base_name = institution_name[:institution_name.find("(")].strip()
            abbrev = institution_name[institution_name.find("(")+1:institution_name.find(")")].strip()
            variants.append(base_name)
            variants.append(abbrev)
        
        return list(set(variants))

    def get_all_institutions(self):
        """
        Returns all institutions with their variants
        """
        all_institutions = []
        
        # Process all categories
        for category in [self.public_universities, self.private_universities, 
                        self.engineering_schools, self.research_institutes, 
                        self.medical_institutions]:
            for institution in category:
                all_institutions.extend(self.generate_all_variants(institution))
        
        # Process specialized institutes
        for category in self.specialized_institutes.values():
            for institution in category:
                all_institutions.extend(self.generate_all_variants(institution))
        
        return list(set(all_institutions))

    def export_to_json(self):
        """
        Exports all institutions and their variants to JSON
        """
        import json
        return json.dumps({
            'public_universities': self.public_universities,
            'private_universities': self.private_universities,
            'engineering_schools': self.engineering_schools,
            'specialized_institutes': self.specialized_institutes,
            'research_institutes': self.research_institutes,
            'medical_institutions': self.medical_institutions,
            'all_variants': self.get_all_institutions()
        }, indent=2, ensure_ascii=False)