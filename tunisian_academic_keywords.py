class TunisianAcademicKeywords:
    def __init__(self):
        # University domains
        self.domains = [
            "rnu.tn",  # National Network of Universities
            "utm.tn",  # University of Tunis El Manar
            "utunis.rnu.tn",  # University of Tunis
            "uma.tn",  # University of Manouba
            "universitecentrale.tn",  # Central University
            "umk.rnu.tn",  # University of Monastir
            "uc.rnu.tn",  # University of Carthage
            "uss.rnu.tn",  # University of Sfax
            "univ-gafsa.tn",  # University of Gafsa
            "ugb.rnu.tn",  # University of Gabes
            "uz.rnu.tn",  # University of Ez-Zitouna
            "uj.rnu.tn",  # University of Jendouba
            "uk.rnu.tn",  # University of Kairouan
            "univsoukra.rnu.tn"  # University of Sousse
        ]

        # Universities and major institutions
        self.universities = [
            "Université de Tunis",
            "University of Tunis",
            "Université de Carthage",
            "University of Carthage",
            "Université de Monastir",
            "University of Monastir",
            "Université de Sfax",
            "University of Sfax",
            "Université de Sousse",
            "University of Sousse",
            "Université de Gabès",
            "University of Gabes",
            "Université de Gafsa",
            "University of Gafsa",
            "Université de Jendouba",
            "University of Jendouba",
            "Université de Kairouan",
            "University of Kairouan",
            "Université Zitouna",
            "Ez-Zitouna University",
            "Université de la Manouba",
            "University of Manouba",
            "Université Tunis El Manar",
            "Tunis El Manar University",
            "Université Centrale de Tunis",
            "Central University of Tunisia"
        ]

        # Engineering Schools
        self.engineering_schools = [
            "ENIT",  # École Nationale d'Ingénieurs de Tunis
            "ENSI",  # École Nationale des Sciences de l'Informatique
            "ENSIT",  # École Nationale Supérieure d'Ingénieurs de Tunis
            "ESPRIT",  # École Supérieure Privée d'Ingénierie et de Technologies
            "INSAT",  # Institut National des Sciences Appliquées et de Technologie
            "SUP'COM",  # École Supérieure des Communications de Tunis
            "ENIS",  # École Nationale d'Ingénieurs de Sfax
            "ENISO",  # École Nationale d'Ingénieurs de Sousse
            "ENIM",  # École Nationale d'Ingénieurs de Monastir
            "ENIG",  # École Nationale d'Ingénieurs de Gabès
            "Institut Préparatoire aux Études d'Ingénieurs"
        ]

        # Research Centers and Institutes
        self.research_centers = [
            "CNSTN",  # Centre National des Sciences et Technologies Nucléaires
            "CBBC",  # Centre de Biotechnologie de Borj Cedria
            "CERTE",  # Centre de Recherches et des Technologies des Eaux
            "CERT",  # Centre d'Études et de Recherches des Télécommunications
            "INSTM",  # Institut National des Sciences et Technologies de la Mer
            "Institut Pasteur de Tunis",
            "Pasteur Institute of Tunis",
            "Centre de Biotechnologie de Sfax",
            "CBS",  # Centre de Biotechnologie de Sfax
            "INAT",  # Institut National Agronomique de Tunisie
            "INRAT",  # Institut National de la Recherche Agronomique de Tunisie
            "IRMC",  # Institut de Recherche sur le Maghreb Contemporain
            "INNTA",  # Institut National de Nutrition et de Technologie Alimentaire
            "IPT",  # Institut Pasteur Tunis
            "CNUDST"  # Centre National Universitaire de Documentation Scientifique et Technique
        ]

        # Major Hospitals and Medical Centers
        self.medical_centers = [
            "Hôpital Charles Nicolle",
            "Charles Nicolle Hospital",
            "Hôpital La Rabta",
            "La Rabta Hospital",
            "Hôpital Habib Bourguiba",
            "Habib Bourguiba Hospital",
            "Hôpital Fattouma Bourguiba",
            "Fattouma Bourguiba Hospital",
            "Hôpital Sahloul",
            "Sahloul Hospital",
            "Hôpital Hédi Chaker",
            "Hedi Chaker Hospital",
            "Hôpital Farhat Hached",
            "Farhat Hached Hospital",
            "Institut Mohamed Kassab",
            "Mohamed Kassab Institute",
            "Institut National de Neurologie",
            "National Institute of Neurology",
            "Institut Salah Azaiz",
            "Salah Azaiz Institute"
        ]

        # Cities with major academic institutions
        self.academic_cities = [
            "Tunis",
            "Sfax",
            "Sousse",
            "Monastir",
            "Gabès",
            "Gabes",
            "Gafsa",
            "Bizerte",
            "Nabeul",
            "Kairouan",
            "Jendouba",
            "Carthage",
            "Ariana",
            "Manouba",
            "Sidi Bouzid",
            "Ben Arous",
            "Borj Cedria",
            "Hammam-Lif",
            "Marsa"
        ]

        # Technology Parks
        self.tech_parks = [
            "Technopole de Borj Cedria",
            "Borj Cedria Technopark",
            "Pôle El-Ghazala",
            "El-Ghazala Technopark",
            "Technopole de Sfax",
            "Sfax Technopark",
            "Technopole de Sousse",
            "Sousse Technopark",
            "Technopole de Monastir",
            "Monastir Technopark",
            "Technopole de Sidi Thabet",
            "Sidi Thabet Technopark"
        ]

    def get_search_query(self):
        """
        Combines all keywords into a search query with proper formatting and weighting
        Returns a query string optimized for Google Scholar search
        """
        all_terms = []
        
        # Add domains with high specificity
        all_terms.extend([f'"{domain}"' for domain in self.domains])
        
        # Add universities and institutions (both French and English names)
        all_terms.extend([f'"{univ}"' for univ in self.universities])
        
        # Add engineering schools (very specific to Tunisia)
        all_terms.extend([f'"{school}"' for school in self.engineering_schools])
        
        # Add research centers
        all_terms.extend([f'"{center}"' for center in self.research_centers])
        
        # Add medical centers
        all_terms.extend([f'"{center}"' for center in self.medical_centers])
        
        # Add tech parks
        all_terms.extend([f'"{park}"' for park in self.tech_parks])
        
        # Add cities only when combined with academic terms
        city_terms = []
        for city in self.academic_cities:
            city_terms.extend([
                f'"{city}" "university"',
                f'"{city}" "research"',
                f'"{city}" "faculty"',
                f'"{city}" "institut"',
                f'"{city}" "école"'
            ])
        
        all_terms.extend(city_terms)
        
        # Combine all terms with OR operator
        return " OR ".join(all_terms)