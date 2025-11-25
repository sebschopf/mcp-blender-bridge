import bpy
import json
import os
import re

# --- CONFIGURATION ---
OUTPUT_DIR = "C:/Users/sebas/Documents/MCP_Outils/MCP_Blender_02/controller/capabilities/extracted" 

CATEGORIES_TO_EXTRACT = {
    "mesh": "Outils de modélisation polygonale",
    "object": "Gestion et transformation d'objets",
    "node": "Outils pour les nœuds",
    "curve": "Outils pour les courbes",
    "sculpt": "Outils de sculpture",
    "armature": "Rigging",
    "pose": "Posing",
    "anim": "Animation",
    "transform": "Transformation",
    "material": "Matériaux",
    "camera": "Caméras",
    "view3d": "Vue 3D",
}

IGNORE_PROPS = {
    'rna_type', 'name', 'properties', 'has_reports', 'layout', 'options', 'macros',
    'bl_idname', 'bl_label', 'bl_description', 'bl_translation_context', 'bl_undo_group',
    'bl_options', 'bl_cursor_pending'
}

def get_op_rna(module, op_name, category_id):
    """Tente de récupérer le RNA de l'opérateur de plusieurs façons."""
    # Méthode 1 : Via la fonction (C-defined operators)
    try:
        op_func = getattr(module, op_name)
        if hasattr(op_func, "get_rna_type"):
            return op_func.get_rna_type()
    except Exception:
        pass

    # Méthode 2 : Via la classe (Python operators)
    try:
        type_name = f"{category_id.upper()}_OT_{op_name}"
        rna = getattr(bpy.types, type_name, None)
        if rna:
            return rna.bl_rna
    except Exception:
        pass

    return None

def python_type_to_yaml_type(prop_type):
    if prop_type == 'FLOAT': return 'float'
    if prop_type == 'INT': return 'integer'
    if prop_type == 'BOOLEAN': return 'boolean'
    if prop_type == 'STRING': return 'string'
    if prop_type in ('FLOAT_VECTOR', 'INT_VECTOR'): return 'list'
    if prop_type == 'ENUM': return 'string'
    return 'string'

def generate_data_for_category(category_id, description):
    print(f"Extraction de la catégorie : {category_id}...")
    
    category_data = {
        "description": description,
        "tools": []
    }
    
    count = 0
    
    if hasattr(bpy.ops, category_id):
        module = getattr(bpy.ops, category_id)
        for op_name in dir(module):
            if op_name.startswith("_"): continue
            
            rna = get_op_rna(module, op_name, category_id)
            if rna is None: continue
            
            op_idname = f"{category_id}.{op_name}"
            desc = rna.description if rna.description else f"Operator {op_idname}"
            label = rna.name if rna.name else op_name.replace('_', ' ').title()
            
            tool_entry = {
                "name": f"bpy.ops.{op_idname}",
                "label": label,
                "description": desc,
                "tags": [category_id, op_name.replace('_', ' ')],
                "params": {}
            }
            
            props = rna.properties
            valid_props = [p for p in props if p.identifier not in IGNORE_PROPS and not p.is_hidden]
            
            if valid_props:
                params_dict = {}
                for prop in valid_props:
                    p_name = prop.identifier
                    p_type = python_type_to_yaml_type(prop.type)
                    p_desc = prop.description if prop.description else p_name
                    params_dict[p_name] = { "type": p_type, "description": p_desc }
                tool_entry["params"] = params_dict
            
            category_data["tools"].append(tool_entry)
            count += 1
            
    return {category_id: category_data}, count

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR, exist_ok=True)

    total_tools = 0
    
    for cat_id, cat_desc in CATEGORIES_TO_EXTRACT.items():
        dict_data, count = generate_data_for_category(cat_id, cat_desc)
        if count > 0:
            filename = os.path.join(OUTPUT_DIR, f"{cat_id}.json")
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(dict_data, f, indent=2, ensure_ascii=False)
            print(f"  -> Sauvegardé {filename} ({count} outils)")
            total_tools += count
        else:
            print(f"  -> Aucun outil trouvé pour {cat_id} (ou module inaccessible)")

    print(f"\nTerminé ! {total_tools} outils extraits au total (format JSON).")

if __name__ == "__main__":
    main()