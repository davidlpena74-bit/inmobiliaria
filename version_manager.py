import json
import sys
import os

def incrementar_version(tipo):
    """
    Incrementa la versión en package.json siguiendo el esquema A.B.C
    A: Mayor (funcional mayor)
    B: Menor (funcional medio)
    C: Parche (funcional menor, estético, errores)
    """
    file_path = 'package.json'
    
    if not os.path.exists(file_path):
        print(f"Error: No se encontró {file_path}")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    version_actual = data.get('version', '0.0.0')
    parts = list(map(int, version_actual.split('.')))

    if tipo == 'A':
        parts[0] += 1
        parts[1] = 0
        parts[2] = 0
    elif tipo == 'B':
        parts[1] += 1
        parts[2] = 0
    elif tipo == 'C':
        parts[2] += 1
    else:
        print("Error: Tipo de versión no reconocido. Usa A, B o C.")
        return False

    nueva_version = '.'.join(map(str, parts))
    data['version'] = nueva_version

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"Version actualizada: {version_actual} -> {nueva_version}")
    return nueva_version

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python version_manager.py [A|B|C]")
    else:
        incrementar_version(sys.argv[1].upper())
