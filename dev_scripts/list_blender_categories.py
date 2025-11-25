import bpy

def list_all_categories():
    print("-" * 40)
    print("LISTE DES CATÉGORIES D'OUTILS BLENDER (bpy.ops)")
    print("-" * 40)
    
    categories = []
    
    # bpy.ops contient tous les modules d'opérateurs
    # dir(bpy.ops) nous donne la liste des noms
    for module_name in dir(bpy.ops):
        # On ignore les méthodes internes comme __init__, etc.
        if module_name.startswith("_"): continue
        
        try:
            module = getattr(bpy.ops, module_name)
            # On compte le nombre de fonctions dans le module
            # dir(module) renvoie les noms des opérateurs
            tool_count = len([f for f in dir(module) if not f.startswith("_")])
            
            if tool_count > 0:
                categories.append((module_name, tool_count))
        except Exception:
            pass

    # Trier par nombre d'outils (décroissant)
    categories.sort(key=lambda x: x[1], reverse=True)
    
    for cat, count in categories:
        print(f"{cat:<15} : {count} outils")
        
    print("-" * 40)
    print(f"Total: {len(categories)} catégories trouvées.")

if __name__ == "__main__":
    list_all_categories()
