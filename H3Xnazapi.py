import requests
import os
from datetime import datetime

banner = r"""
 /$$   /$$  /$$$$$$  /$$   /$$
| $$  | $$ /$$__  $$| $$  / $$
| $$  | $$|__/  \ $$|  $$/ $$/
| $$$$$$$$   /$$$$$/ \  $$$$/ 
| $$__  $$  |___  $$  >$$  $$ 
| $$  | $$ /$$  \ $$ /$$/\  $$
| $$  | $$|  $$$$$$/| $$  \ $$
|__/  |__/ \______/ |__/  |__/ NAZAPI
"""

class Nazapi:
    def __init__(self, token):
        self.token = token
        self.url = "https://leakosintapi.com/"
    
    def search(self, request):
        data = {
            "token": self.token,
            "request": request
        }

        response = requests.post(self.url, json=data)
        try:
            return response.json()
        except:
            return {"error": "Réponse invalide"}


def show_help():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(banner)
    print("\n" + "="*60)
    
    print("\n📋 COMMANDES DISPONIBLES:")
    print("  /clear    - effacer les recherches")
    print("  /log      - Active/désactive la sauvegarde des résultats")
    print("  /exit     - Quitte le programme")
    
    print("\n🔍 RECHERCHES POSSIBLES:")
    print("  • Adresses email")
    print("  • Noms d'utilisateur")
    print("  • Noms de personnes")
    print("  • Numéros de téléphone")
    print("  • Adresses IP")
    print("  • Domaines")
    
    print("\n" + "="*60)
    print("/back pour retourner au menu principal")
    print("="*60)


def save_log(search_query, output_lines):
    safe_filename = "".join(c for c in search_query if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_filename = safe_filename.replace(' ', '_')
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"save/{safe_filename}_{timestamp}.txt"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(banner)
            f.write(f"\n\nRecherche effectuée le: {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}")
            f.write(f"\nRequête: {search_query}")
            f.write("\n" + "="*50 + "\n\n")
            
            for line in output_lines:
                f.write(line + "\n")
        
        print(f"\n✅ Résultats sauvegardés dans: {filename}")
    except Exception as e:
        print(f"\n❌ Erreur lors de la sauvegarde: {e}")


def load_saved_key():
    key_file = 'key/api_key.txt'
    if os.path.exists(key_file):
        try:
            with open(key_file, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except:
            return None
    return None

def save_key(api_token):
    try:
        with open('key/api_key.txt', 'w', encoding='utf-8') as f:
            f.write(api_token)
        print("✅ Clé API sauvegardée")
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde de la clé: {e}")

if __name__ == "__main__":
    print(banner)
    
    api_token = load_saved_key()
    
    if not api_token:
        api_token = input(" clé Nazapi: ").strip()
        while not api_token:
            print("Vous devez entrer une clé API pour continuer.")
            api_token = input("Veuillez entrer votre clé API Nazapi: ").strip()
        save_key(api_token)
    naz = Nazapi(token=api_token)
    log_mode = False
    help_mode = False
    print("\n/exit pour quitter.")
    print("/help pour voir les commandes")
    while True:
        q = input("Recherche: ").strip()
        if q.lower() == "/exit":
            print("Goated by sosaf.")
            break
        if q.lower() == "/clear":
            os.system('cls' if os.name == 'nt' else 'clear')
            print(banner)
            continue
        if q.lower() == "/log":
            log_mode = not log_mode
            status = "activé" if log_mode else "désactivé"
            print(f"Mode sauvegarde {status}")
            continue
        if q.lower() == "/help":
            show_help()
            help_mode = True
            continue
        if q.lower() == "/back":
            if help_mode:
                help_mode = False
                print("\nRetour au menu principal")
                print("/exit pour quitter.")
                print("/help voir les commandes disponibles")
            else:
                print("déjà dans le menu principal")
            continue
        if not q:
            continue
        
        if help_mode:
            print("/back pour retourner au menu principal.")
            continue
            
        print("Recherche en cours...")
        result = naz.search(q)
        
        output_lines = []
        if "error" in result:
            error_msg = f"Erreur: {result['error']}"
            print(error_msg)
            output_lines.append(error_msg)
        elif "List" in result:
            for base, infos in result["List"].items():
                section = f"\n=== {base} ==="
                print(section)
                output_lines.append(section)
                
                info_leak = infos.get("InfoLeak", "")
                if info_leak:
                    print(info_leak)
                    output_lines.append(info_leak)
                
                data = infos.get("Data", [])
                if data:
                    for entry in data:
                        for k, v in entry.items():
                            line = f" {k}: {v}"
                            print(line)
                            output_lines.append(line)
                        separator = "-" * 30
                        print(separator)
                        output_lines.append(separator)
                else:
                    no_data = "[Pas de données]"
                    print(no_data)
                    output_lines.append(no_data)
        elif "Error code" in result:
            error_msg = "no result"
            print(error_msg)
            output_lines.append(error_msg)
        else:
            result_str = str(result)
            print(result_str)
            output_lines.append(result_str)
        
        if log_mode:
            save_log(q, output_lines)
