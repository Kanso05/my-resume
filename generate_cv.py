#!/usr/bin/env python3
"""
Générateur de CV local avec Claude API
Utilisation : 
  python generate_cv_local.py              # Génère tous les CV
  python generate_cv_local.py --force      # Force la régénération
  python generate_cv_local.py CV/fichier.md # Génère un CV spécifique
"""

import anthropic
import os
import hashlib
import glob
import sys
import argparse
from pathlib import Path
from datetime import datetime

def read_file(filepath):
    """Lit un fichier avec gestion d'erreur."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ Fichier introuvable: {filepath}")
        return None
    except Exception as e:
        print(f"❌ Erreur lecture {filepath}: {e}")
        return None

def write_file(filepath, content):
    """Écrit un fichier avec encodage UTF-8."""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"❌ Erreur écriture {filepath}: {e}")
        return False

def file_hash(filepath):
    """Calcule le hash MD5 d'un fichier."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return hashlib.md5(f.read().encode()).hexdigest()
    except:
        return None

def generate_cv_with_claude(cv_content, template_content, cv_filename, api_key):
    """Génère le CV avec Claude."""
    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        prompt = f"""
        Tu es un expert en génération de CV professionnel français. Tu DOIS inclure TOUT le contenu du CV sans exception.
        
        **CV Markdown COMPLET ({cv_filename}) :**
        ```markdown
        {cv_content}
        ```
        
        **Template HTML :**
        ```html
        {template_content}
        ```
        
        **OBLIGATION CRITIQUE - INCLURE TOUT LE CONTENU :**
        - TOUTES les sections doivent être présentes dans le HTML final
        - TOUS les tableaux doivent être convertis en HTML
        - TOUTES les descriptions détaillées d'expériences doivent être incluses
        - AUCUNE troncature n'est acceptable
        
        **Instructions techniques :**
        1. **Encodage** : UTF-8 avec caractères français (é, è, à, ç, etc.)
        2. **Tableaux** : Convertis en <table> HTML responsive
        3. **Pagebreaks** : Traite `<!-- pagebreak -->` comme séparateurs CSS
        4. **Sections longues** : Toutes les descriptions détaillées doivent apparaître
        5. **Hiérarchie** : H1>H2>H3 respectée
        6. **Listes** : <ul><li> avec styles du template
        
        Réponds UNIQUEMENT avec le HTML final COMPLET incluant TOUT le contenu.
        """
        
        print(f"  🤖 Appel à Claude API (streaming)...")
        
        # Appel Claude avec streaming pour CV longs
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=16000,
            stream=True,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        # Collecte du contenu streamé
        generated_html = ""
        for chunk in response:
            if chunk.type == "content_block_delta":
                generated_html += chunk.delta.text
        
        generated_html = generated_html.strip()
        
        # Nettoyage du contenu
        if generated_html.startswith('```html'):
            generated_html = generated_html.split('```html')[1].split('```')[0].strip()
        elif generated_html.startswith('```'):
            generated_html = generated_html.split('```')[1].split('```')[0].strip()
        
        return generated_html
        
    except Exception as e:
        print(f"  ❌ Erreur Claude API: {e}")
        return None

def parse_arguments():
    """Parse les arguments de ligne de commande."""
    parser = argparse.ArgumentParser(description='Générateur de CV avec Claude API')
    parser.add_argument('--force', action='store_true', 
                       help='Force la régénération même si inchangés')
    parser.add_argument('--all', action='store_true',
                       help='Génère tous les CV (défaut)')
    parser.add_argument('files', nargs='*', 
                       help='Fichiers CV spécifiques à générer')
    return parser.parse_args()

def main():
    """Fonction principale."""
    args = parse_arguments()
    
    print("🚀 Génération locale des CV")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Vérifier la clé API
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("❌ Variable d'environnement ANTHROPIC_API_KEY non définie")
        print("💡 Exporter votre clé: export ANTHROPIC_API_KEY='votre_cle'")
        return
    
    # Vérifier la structure
    if not os.path.exists('CV'):
        print("❌ Répertoire CV/ introuvable")
        return
    
    if not os.path.exists('Template/Cv_modern.html'):
        print("❌ Template Template/Cv_modern.html introuvable")
        return
    
    # Créer Output/ si nécessaire
    os.makedirs('Output', exist_ok=True)
    
    # Lire le template
    print("📖 Lecture du template...")
    template_content = read_file('Template/Cv_modern.html')
    if not template_content:
        return
    
    # Déterminer les fichiers à traiter
    if args.files:
        cv_files = [f for f in args.files if f.endswith('.md') and os.path.exists(f)]
        if not cv_files:
            print("❌ Aucun fichier CV valide spécifié")
            return
        print(f"🎯 Mode spécifique: {len(cv_files)} fichier(s)")
    else:
        cv_files = glob.glob('CV/*.md')
        if not cv_files:
            print("❌ Aucun fichier .md trouvé dans CV/")
            return
        print(f"📝 Mode complet: {len(cv_files)} fichier(s) trouvé(s)")
    
    if args.force:
        print("🔄 Mode forcé activé")
    
    print("\nFichiers à traiter:")
    for cv_file in cv_files:
        print(f"  - {cv_file}")
    print()
    
    # Traiter chaque fichier
    files_generated = []
    files_updated = []
    files_unchanged = []
    
    for cv_file in cv_files:
        print(f"🔄 Traitement de {cv_file}...")
        
        cv_content = read_file(cv_file)
        if not cv_content:
            continue
        
        cv_filename = Path(cv_file).stem
        output_file = f"Output/{cv_filename}.html"
        
        print(f"  📄 {cv_file} → {output_file}")
        
        # Générer avec Claude
        generated_html = generate_cv_with_claude(cv_content, template_content, cv_filename, api_key)
        if not generated_html:
            continue
        
        # Vérifier si mise à jour nécessaire
        file_exists = os.path.exists(output_file)
        needs_update = args.force
        
        if file_exists and not args.force:
            old_hash = file_hash(output_file)
            new_hash = hashlib.md5(generated_html.encode()).hexdigest()
            
            if old_hash == new_hash:
                print(f"  ✅ Déjà à jour")
                files_unchanged.append(output_file)
                needs_update = False
            else:
                print(f"  🔄 Contenu différent")
                files_updated.append(output_file)
                needs_update = True
        elif not file_exists:
            print(f"  ✨ Nouveau fichier")
            files_generated.append(output_file)
            needs_update = True
        elif args.force:
            print(f"  🔄 Régénération forcée")
            if file_exists:
                files_updated.append(output_file)
            else:
                files_generated.append(output_file)
        
        if needs_update:
            if write_file(output_file, generated_html):
                print(f"  ✅ Succès !")
            else:
                print(f"  ❌ Échec")
        
        print()
    
    # Résumé
    print("📊 Résumé:")
    print(f"  ✨ Créés: {len(files_generated)}")
    print(f"  🔄 Mis à jour: {len(files_updated)}")
    print(f"  ✅ Inchangés: {len(files_unchanged)}")
    
    if files_generated:
        print("\n📁 Nouveaux:")
        for f in files_generated:
            print(f"  - {f}")
    
    if files_updated:
        print("\n🔄 Mis à jour:")
        for f in files_updated:
            print(f"  - {f}")
    
    print(f"\n🎉 Terminé !")

if __name__ == "__main__":
    main()
