# Guide Utilisateur - Mobile-Morpher

## Introduction

Mobile-Morpher est un outil professionnel permettant de transformer n'importe quelle application Android (APK) en une version personnalisée unique.

## Installation

### Prérequis
- Docker Desktop (Windows/Mac) ou Docker Engine (Linux)
- 4 GB de RAM minimum
- 10 GB d'espace disque libre

### Étapes d'installation

1. **Télécharger le projet**
   ```bash
   git clone https://github.com/votre-username/Mobile-Morpher.git
   cd Mobile-Morpher
   ```

2. **Lancer l'environnement**
   ```bash
   docker-compose up -d
   ```

3. **Accéder à l'interface**
   Ouvrez votre navigateur et allez sur `http://localhost:3000`

## Utilisation

### Mode Express (Rapide)

Idéal pour une transformation simple et rapide (< 120 secondes).

1. Sélectionnez "Express" dans l'interface
2. Glissez votre fichier APK dans la zone de dépôt
3. Saisissez le nouveau nom de l'application
4. Entrez le nouvel identifiant (ex: com.monentreprise.monapp)
5. Cliquez sur "Transformer l'APK"
6. Téléchargez votre APK personnalisé

### Mode Design

Pour personnaliser l'apparence.

1. Sélectionnez "Design"
2. Chargez votre APK
3. Configurez le nom et l'ID
4. Choisissez un thème (Material Design 3 automatique)
5. Personnalisez les couleurs et polices
6. Générez l'APK

### Mode Développeur

Accès complet au code.

1. Sélectionnez "Developer"
2. Chargez l'APK
3. Accédez à l'éditeur de code Smali
4. Modifiez les classes et méthodes
5. Appliquez les suggestions de l'IA
6. Reconstruisez l'APK

## FAQ

**Q: L'APK modifié ne s'installe pas ?**
R: Vérifiez que vous avez activé "Sources inconnues" dans les paramètres Android.

**Q: Combien de temps prend une transformation ?**
R: En mode Express, moins de 120 secondes. Les modes avancés peuvent prendre plus de temps.

**Q: Mes fichiers sont-ils conservés ?**
R: Non, ils sont supprimés automatiquement après la fin de votre session.

**Q: Puis-je modifier plusieurs APK à la fois ?**
R: Chaque session traite un APK à la fois pour garantir la sécurité.
