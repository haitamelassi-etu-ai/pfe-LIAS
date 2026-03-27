# Cahier des charges
## Plateforme web institutionnelle et scientifique du laboratoire LIAS avec espace membre et intégration ORCID

## 1. Contexte
Le laboratoire LIAS a besoin d’une plateforme unique pour centraliser et valoriser ses activités scientifiques et institutionnelles.

Constat actuel :
- Informations dispersées (documents, fichiers, emails, profils externes)
- Mises à jour difficiles
- Suivi scientifique incomplet
- Faible capacité de reporting fiable

La solution attendue combine :
- Un site public institutionnel
- Un portail membre sécurisé
- Une intégration ORCID pour enrichir les profils et productions

## 2. Intitulé du projet
Conception et développement d’une plateforme web institutionnelle et scientifique pour le laboratoire LIAS, intégrant :
- Site public
- Portail membre
- Gestion des productions scientifiques
- Liaison ORCID

## 3. Problématique
Le laboratoire doit disposer d’un système centralisé permettant de :
- Présenter son identité, ses axes et ses activités
- Donner à chaque membre un espace personnel scientifique
- Gérer et valoriser publications, communications, événements et projets
- Produire des synthèses et exports fiables

## 4. Objectifs
### 4.1 Objectif général
Déployer une plateforme web durable qui améliore la visibilité du laboratoire et structure la gestion de l’information scientifique.

### 4.2 Objectifs spécifiques
- Mettre en ligne un site institutionnel moderne
- Créer un espace membre sécurisé
- Intégrer ORCID (liaison et import de base)
- Gérer publications, communications, événements, actualités, projets
- Offrir un back-office administrateur avec validation simple
- Fournir des tableaux de bord et exports simples

## 5. Périmètre
### 5.1 Inclus
- Site public du laboratoire
- Comptes utilisateurs et authentification
- Gestion des profils membres
- Liaison ORCID
- Gestion des publications
- Gestion des communications
- Gestion des événements
- Gestion des actualités
- Gestion des projets et axes de recherche
- Back-office d’administration
- Recherche multicritère
- Tableaux de bord basiques
- Exports CSV/PDF simples

### 5.2 Exclus (version initiale)
- Réseau social interne complet
- Rédaction collaborative temps réel
- Intégration ERP universitaire complète
- Gestion financière avancée
- Bibliométrie avancée
- Recommandation intelligente complète
- Application mobile native
- Workflow complexe multi-niveaux

## 6. Parties prenantes et utilisateurs
### 6.1 Public externe
- Visiteurs
- Étudiants
- Partenaires institutionnels
- Chercheurs externes
- Invités événements
- Futurs doctorants

### 6.2 Public interne
- Membres permanents
- Enseignants-chercheurs
- Doctorants
- Responsables scientifiques
- Administrateurs plateforme

### 6.3 Acteurs et rôles
- Visiteur : consultation du site public
- Membre : gestion profil, ORCID, productions
- Doctorant : gestion activités académiques
- Administrateur/Responsable : modération, validation, pilotage

## 7. Exigences fonctionnelles
### 7.1 Site public
Pages minimales :
- Accueil
- Présentation (historique, mission)
- Axes de recherche
- Membres
- Projets
- Publications
- Événements
- Actualités
- Partenaires
- Contact (formulaire)

Fonctions :
- Galerie médias
- Mise en avant des contenus validés
- Visibilité des appels à communication (optionnel V1)

### 7.2 Comptes et profils
- Inscription/création de comptes par rôle autorisé
- Connexion/déconnexion
- Réinitialisation mot de passe
- Gestion des rôles
- Édition du profil

Champs profil :
- Nom, prénom
- Photo
- Email professionnel
- Grade/fonction
- Spécialité
- Équipe/axe
- Biographie courte
- Domaines d’intérêt
- Liens académiques
- Identifiant ORCID

### 7.3 Intégration ORCID
- Liaison compte membre ↔ ORCID
- Récupération des données publiques du profil
- Préremplissage profil
- Import de publications (niveau de base)
- Possibilité de corriger localement les données importées

### 7.4 Publications
Types : article, communication conférence, chapitre, ouvrage, poster, rapport, brevet, thèse/mémoire.

Données :
- Titre
- Auteurs
- Type
- Année
- Revue/conférence/éditeur
- Résumé
- Mots-clés
- DOI
- Lien externe
- PDF ou lien
- Statut validation
- Axe/projet associé

Fonctions :
- Ajout manuel
- Import ORCID
- Modification/suppression
- Recherche/filtre
- Affichage profil membre
- Publication publique après validation

### 7.5 Communications scientifiques
Types : nationale, internationale, orale, poster, séminaire, colloque/congrès.

Données :
- Titre
- Auteurs
- Événement
- Type
- Lieu/pays
- Date
- Résumé
- Statut (soumise, acceptée, présentée)
- Support/document

Fonctions :
- CRUD complet
- Classement par année
- Affichage profil membre
- Publication publique selon autorisation/validation

### 7.6 Événements
- Création et édition
- Description, date, lieu
- Programme, intervenants
- Affiche/visuel
- Statut (à venir, passé)
- Archivage automatique des événements passés
- Formulaire d’inscription simple (optionnel V1)

### 7.7 Actualités
- Création, publication, modification
- Archivage
- Mise en avant sur la page d’accueil

### 7.8 Projets de recherche
Données : titre, résumé, responsable, membres, partenaires, dates, financement, statut, axe, publications liées.

Fonctions :
- CRUD
- Visibilité publique ou privée
- Lien avec profils membres

### 7.9 Axes de recherche
- Titre et description
- Responsables
- Membres associés
- Projets/publications/événements associés

### 7.10 Tableau de bord membre
- Résumé profil
- Publications récentes
- Communications récentes
- Données ORCID importées
- Actions rapides d’ajout

### 7.11 Tableau de bord administrateur
Indicateurs de base :
- Nombre membres
- Nombre publications
- Communications par année
- Événements organisés
- Répartition par axe
- Contenus en attente de validation

### 7.12 Recherche multicritère
Recherche par :
- Nom membre
- Titre publication
- Année
- Type production
- Axe
- Événement
- Projet

### 7.13 Workflow de validation
Workflow simple :
1. Soumission par membre
2. Vérification administrateur
3. Décision : validé, rejeté, à corriger

### 7.14 Exports et rapports
- Export CSV des productions
- PDF fiche membre
- Bilan annuel membre
- Bilan scientifique global (version simple)

## 8. Exigences non fonctionnelles
### 8.1 Ergonomie
- Interface moderne, claire, responsive
- Navigation simple et cohérente
- Accessibilité de base (contrastes, formulaires lisibles, navigation clavier essentielle)

### 8.2 Sécurité
- Authentification sécurisée
- Mots de passe hashés
- Gestion stricte des droits par rôle
- Protection des données personnelles
- Journalisation minimale des actions sensibles

### 8.3 Performance
- Chargement rapide des pages principales
- Pagination sur grandes listes
- Requêtes de recherche optimisées

### 8.4 Maintenabilité
- Architecture modulaire
- Documentation technique
- Versionning Git
- Standards de code

### 8.5 Disponibilité
- Déploiement possible sur serveur institutionnel ou hébergement web standard

### 8.6 Référencement
- Structure SEO : titres, méta, URLs lisibles, sitemap

## 9. Architecture technique recommandée
### 9.1 Vue d’ensemble
Architecture 3 couches :
- Frontend
- Backend API
- Base de données

### 9.2 Stack proposée (recommandée pour PFE)
- Frontend : Next.js
- Backend API : FastAPI
- Base : PostgreSQL
- Auth : JWT + rafraîchissement sécurisé
- Stockage fichiers : local V1, S3-compatible en évolution

### 9.3 Intégration ORCID (V1)
- OAuth ORCID pour liaison de compte
- Lecture des données publiques
- Import manuel déclenché par l’utilisateur

## 10. Modules du système
- Module A : Site public institutionnel
- Module B : Comptes, profils, rôles
- Module C : ORCID (liaison + import de base)
- Module D : Gestion scientifique (publications, communications, projets)
- Module E : Administration (validation, modération, contenus)
- Module F : Reporting (statistiques et exports simples)

## 11. Modèle de données simplifié
Entités :
- Utilisateur
- ProfilMembre
- Publication
- Communication
- Evenement
- Actualite
- Projet
- AxeRecherche
- Document
- Validation

Relations clés :
- Un Utilisateur possède un ProfilMembre
- Un ProfilMembre a plusieurs Publications et Communications
- Un ProfilMembre appartient à un ou plusieurs AxeRecherche
- Un Projet implique plusieurs ProfilMembre
- Une Publication peut être liée à un Projet et/ou un AxeRecherche
- Un contenu publiable porte un statut Validation

## 12. Règles métier minimales
- Un contenu non validé ne doit pas être visible publiquement
- Un membre ne peut modifier que ses propres contenus (hors admin)
- Un administrateur peut valider/rejeter/renvoyer pour correction
- ORCID ne remplace pas la donnée locale : il l’enrichit
- Toute suppression critique doit être confirmée

## 13. MVP (version soutenable en PFE)
Fonctionnalités obligatoires V1 :
- Site public complet (pages institutionnelles)
- Authentification et rôles
- Profil membre complet
- CRUD publications
- CRUD communications
- CRUD actualités/événements/projets (admin)
- Validation simple
- Liaison ORCID + import de base
- Recherche multicritère basique
- Tableau de bord membre/admin basique
- Exports CSV de base

Fonctionnalités reportables V2 :
- PDF avancé
- Inscriptions événements
- Bibliométrie simple
- Multilingue
- Intégrations externes supplémentaires

## 14. Livrables
- Cahier des charges
- Étude de l’existant
- Maquettes UI
- Diagrammes UML
- Modèle relationnel
- Application web fonctionnelle
- Documentation technique
- Guide utilisateur
- Rapport final et support de soutenance

## 15. Planning indicatif (6 phases)
1. Analyse et cadrage
2. Conception (UML, BDD, maquettes)
3. Développement site public
4. Développement espace membre + ORCID
5. Développement administration + reporting
6. Tests, documentation, démonstration

## 16. Critères d’acceptation
- Site public opérationnel et responsive
- Gestion comptes/profils fonctionnelle
- Ajout et consultation publications/communications
- Liaison ORCID active avec import de base
- Gestion actualités/événements/projets opérationnelle
- Validation admin effective
- Données stables et exploitables pour usage réel

## 17. Risques et mesures
- Risque de surcharge fonctionnelle : limiter au MVP
- Risque ORCID (temps/intégration) : cadrer à l’import de base
- Risque qualité données : imposer validation et champs obligatoires
- Risque délai : livraisons incrémentales toutes les 2 semaines

## 18. Répartition possible en équipe (si plusieurs étudiants)
- Frontend/UX : interfaces publiques et membres
- Backend/API : auth, logique métier, ORCID
- Data/Admin : modèle, reporting, tests, qualité

## 19. Évolutions possibles
- CV scientifique automatique
- Connecteurs Scholar et autres sources
- Module doctorants/thèses enrichi
- Module appels à projets
- Statistiques et bibliométrie avancées
- Newsletter
- Multilingue
- Dépôt d’archives internes

## 20. Conclusion
La plateforme proposée répond au besoin stratégique du laboratoire LIAS :
- visibilité institutionnelle
- centralisation scientifique
- pilotage administratif

La démarche MVP garantit une réalisation réaliste en contexte PFE tout en préparant des évolutions futures.