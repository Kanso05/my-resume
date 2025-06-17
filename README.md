# 🤖 Générateur de CV Automatique

Système de génération automatique de CV utilisant GitHub Actions et l'API Claude d'Anthropic. Convertit automatiquement vos CV en markdown vers HTML en utilisant un template moderne.

## ✨ Fonctionnalités

- **Génération automatique** : Conversion MD → HTML déclenchée par les commits
- **Template unique** : Un seul template HTML pour tous les CV
- **Régénération globale** : Modification du template = tous les CV mis à jour
- **Détection intelligente** : Génère uniquement si le contenu a changé
- **Commits automatiques** : Nouvelles versions commitées automatiquement
- **Test local** : Script Python pour tester avant commit

## 📁 Structure du projet

```
├── CV/                          # CV en format Markdown
│   ├── Architecte_de_Donnée.md
│   └── Data_Architect.md
├── Template/                    # Template HTML
│   └── Cv_modern.html
├── Output/                      # CV générés (créé automatiquement)
│   ├── Architecte_de_Donnée.html
│   └── Data_Architect.html
├── .github/workflows/
│   └── generate-cv.yml         # Workflow GitHub Actions
└── generate_cv_local.py        # Script pour tests locaux
```

## ⚡ Déclenchement automatique

### Modification d'un CV
```
Modification → CV/Data_Architect.md
Génération → Output/Data_Architect.html
Commit → "🤖 Mise à jour automatique des CV"
```

### Modification du template
```
Modification → Template/Cv_modern.html
Génération → Tous les CV dans Output/
Commit → "🎨 Régénération automatique des CV suite à modification du template"
```

## 🚀 Configuration

### 1. Clé API Claude
1. Obtenez votre clé API sur [console.anthropic.com](https://console.anthropic.com)
2. Dans GitHub : **Settings** → **Secrets and variables** → **Actions**
3. Ajoutez `ANTHROPIC_API_KEY` avec votre clé

### 2. Activation du workflow
Le workflow `.github/workflows/generate-cv.yml` se déclenche automatiquement sur :
- Modifications dans `CV/*.md`
- Modifications dans `Template/Cv_modern.html`

## 📝 Format des CV (Markdown)

Exemple de structure recommandée :

```markdown
# Jean Dupont
## Développeur Full-Stack Senior

### 📧 Contact
- **Email** : jean.dupont@email.com
- **LinkedIn** : [linkedin.com/in/jean-dupont](https://linkedin.com/in/jean-dupont)
- **Téléphone** : +33 6 12 34 56 78

### 💼 Expérience professionnelle

**Développeur Senior** - TechCorp (2022-2024)
- Développement d'applications React/Node.js
- Management d'équipe de 3 développeurs
- Architecture microservices sur AWS

### 🛠️ Compétences techniques
- **Frontend** : React, Vue.js, TypeScript
- **Backend** : Node.js, Python, Java
- **Bases de données** : PostgreSQL, MongoDB
```

## 🧪 Test local

### Installation
```bash
pip install anthropic
export ANTHROPIC_API_KEY="votre_cle_api"
```

### Utilisation
```bash
# Génère tous les CV
python generate_cv_local.py

# Force la régénération (même si inchangés)
python generate_cv_local.py --force

# Génère un CV spécifique
python generate_cv_local.py CV/Data_Architect.md
```

## 🎨 Personnalisation du template

Le template `Template/Cv_modern.html` peut contenir :
- CSS personnalisé
- Structure HTML moderne
- Classes Bootstrap ou Tailwind
- Animations et effets visuels

Lors de la modification du template, tous les CV sont automatiquement régénérés.

## 📊 Workflow détaillé

1. **Détection** : GitHub Actions détecte les modifications
2. **Lecture** : Lecture du CV markdown et du template HTML
3. **Génération** : Claude fusionne le contenu dans le template
4. **Comparaison** : Vérification si le fichier de sortie a changé
5. **Commit** : Nouveau commit si modifications détectées

## 🔧 Messages de commit automatiques

### Changement de CV
```
🤖 Mise à jour automatique des CV

Fichiers générés:
- Output/Data_Architect.html

Généré le 2025-06-17 à 14:30:25
```

### Changement de template
```
🎨 Régénération automatique des CV suite à modification du template

Template mis à jour: Template/Cv_modern.html
Fichiers régénérés:
- Output/Architecte_de_Donnée.html
- Output/Data_Architect.html

Généré le 2025-06-17 à 14:30:25
```

## 🚨 Prérequis

- Repository GitHub
- Clé API Claude (Anthropic)
- Python 3.x (pour tests locaux)

## 📖 Utilisation quotidienne

1. **Modifier un CV** : Éditez `CV/votre_cv.md`
2. **Commit** : `git commit -m "Ajout compétence Python"`
3. **Automatique** : GitHub génère le HTML et commit
4. **Résultat** : Nouveau `Output/votre_cv.html` disponible

## 🤝 Contribution

Pour ajouter un nouveau CV :
1. Créez `CV/nouveau_cv.md`
2. Commitez le fichier
3. Le HTML sera automatiquement généré dans `Output/nouveau_cv.html`

Pour modifier le design :
1. Éditez `Template/Cv_modern.html`
2. Commitez les modifications
3. Tous les CV seront régénérés automatiquement
