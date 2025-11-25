import os
import yaml
import json

# Configuration
CAPABILITIES_DIR = "controller/capabilities/extracted"

# Liste noire des paramètres internes de Blender à supprimer (au cas où ils seraient encore là)
BLACKLIST_PARAMS = {
    "name", "properties", "has_reports", "bl_idname", "bl_label", 
    "bl_translation_context", "bl_description", "bl_undo_group", 
    "bl_options", "bl_cursor_pending", "layout", "options", "macros",
    "rna_type"
}

def process_json_to_yaml(json_filepath):
    yaml_filepath = json_filepath.replace(".json", ".yaml")
    print(f"Conversion de {json_filepath} -> {yaml_filepath}...")
    
    with open(json_filepath, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Erreur de lecture JSON: {e}")
            return

    if not data:
        return

    # Nettoyage des données
    for category_name, category_data in data.items():
        tools = category_data.get('tools', [])
        cleaned_tools_count = 0
        
        for tool in tools:
            if 'params' in tool:
                original_params = tool['params']
                cleaned_params = {
                    k: v for k, v in original_params.items() 
                    if k not in BLACKLIST_PARAMS
                }
                
                if len(cleaned_params) < len(original_params):
                    tool['params'] = cleaned_params
                    cleaned_tools_count += 1
        
        print(f"  - {cleaned_tools_count} outils nettoyés supplémentaires dans '{category_name}'")

    # Sauvegarde en YAML
    with open(yaml_filepath, 'w', encoding='utf-8') as f:
        # allow_unicode=True pour garder les accents si présents
        # sort_keys=False pour garder l'ordre naturel
        yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
    
    print(f"  -> Fichier YAML sauvegardé.")
    
    # Suppression du JSON source
    try:
        os.remove(json_filepath)
        print("  -> Fichier JSON source supprimé.")
    except OSError as e:
        print(f"  -> Erreur lors de la suppression du JSON: {e}")

def main():
    if not os.path.exists(CAPABILITIES_DIR):
        print(f"Dossier non trouvé: {CAPABILITIES_DIR}")
        return

    json_files = [f for f in os.listdir(CAPABILITIES_DIR) if f.endswith(".json")]
    
    if not json_files:
        print("Aucun fichier .json trouvé à traiter.")
        return

    for filename in json_files:
        filepath = os.path.join(CAPABILITIES_DIR, filename)
        process_json_to_yaml(filepath)

if __name__ == "__main__":
    main()