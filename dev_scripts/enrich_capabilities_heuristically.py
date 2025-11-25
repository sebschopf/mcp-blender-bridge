import os
import yaml
import re

# --- Configuration ---
CAPABILITIES_DIR = "controller/capabilities"

# Dictionnaire de synonymes pour enrichir les tags
SYNONYMS = {
    "add": ["create", "make", "generate", "new", "insert"],
    "remove": ["delete", "erase", "clear", "dissolve"],
    "select": ["pick", "choose", "grab"],
    "transform": ["move", "rotate", "scale", "resize"],
    "translate": ["move", "grab", "position"],
    "rotate": ["spin", "turn", "orient"],
    "resize": ["scale", "size", "bigger", "smaller"],
    "primitive": ["shape", "geometry", "mesh", "object"],
    "cube": ["box", "square", "block"],
    "sphere": ["ball", "round", "globe"],
    "cylinder": ["tube", "pipe"],
    "cone": ["pyramid", "pointy"],
    "plane": ["floor", "ground", "flat"],
    "circle": ["ring", "disc", "loop"],
    "camera": ["view", "shot", "lens"],
    "light": ["lamp", "illumination", "sun", "spot"],
    "material": ["texture", "color", "shader", "surface"],
    "render": ["image", "picture", "export"],
    "anim": ["animation", "motion", "keyframe"],
    "pose": ["posture", "rigging", "armature"],
    "node": ["graph", "connection", "logic"],
    "subdivide": ["smooth", "refine", "detail"],
    "extrude": ["extend", "push", "pull"],
    "bevel": ["chamfer", "round edge", "smooth corner"],
    "join": ["merge", "combine", "unite"],
    "separate": ["split", "detach", "disconnect"]
}

def enrich_tool(tool):
    name = tool.get("name", "")
    current_tags = set(tool.get("tags", []))
    
    # 1. Extraire des mots du nom de l'outil
    # Ex: bpy.ops.mesh.primitive_cube_add -> ['bpy', 'ops', 'mesh', 'primitive', 'cube', 'add']
    name_parts = re.split(r'[._]', name)
    
    # Filtrer les mots trop génériques ou courts
    ignored_words = {"bpy", "ops", "ot"}
    meaningful_words = [w.lower() for w in name_parts if len(w) > 2 and w.lower() not in ignored_words]
    
    # Ajouter les mots du nom aux tags
    current_tags.update(meaningful_words)
    
    # 2. Ajouter des synonymes
    synonyms_to_add = set()
    for tag in current_tags:
        if tag in SYNONYMS:
            synonyms_to_add.update(SYNONYMS[tag])
            
    current_tags.update(synonyms_to_add)
    
    # 3. Améliorer la description si elle est trop générique
    description = tool.get("description", "")
    # Si la description est juste "Operator mesh.cube_add", on essaie de faire mieux
    if description.lower().strip() == f"operator {name.replace('bpy.ops.', '')}".lower().strip() or not description:
        # Essayer de construire une phrase simple : "Primitive Cube Add" -> "Primitive Cube Add operation"
        readable_name = " ".join([w.title() for w in meaningful_words])
        tool["description"] = f"{readable_name} operation."
    
    # Mise à jour finale
    tool["tags"] = list(current_tags)
    return tool

def process_file(filepath):
    print(f"Traitement de {filepath}...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            
        if not data:
            return

        modified = False
        for category_name, category_data in data.items():
            tools = category_data.get("tools", [])
            for tool in tools:
                enrich_tool(tool)
                modified = True
                
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
            print(f"  -> Enrichi et sauvegardé.")
            
    except Exception as e:
        print(f"  -> Erreur : {e}")

def main():
    if not os.path.exists(CAPABILITIES_DIR):
        print(f"Dossier non trouvé : {CAPABILITIES_DIR}")
        return

    for root, dirs, files in os.walk(CAPABILITIES_DIR):
        for file in files:
            if file.endswith(".yaml"):
                process_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
