import requests, sys, os, argparse
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# --- Charger les variables d'environnement ---
load_dotenv()
email = os.getenv("CONFLUENCE_EMAIL")
api_token = os.getenv("CONFLUENCE_API_TOKEN")
base_api_url = "https://clementtpro.atlassian.net/wiki/rest/api"

# --- Définir et lire les arguments ---
parser = argparse.ArgumentParser(description="Mise à jour d'une table dans Confluence via son ID.")
parser.add_argument("--page-id", required=True, help="ID de la page Confluence à modifier.")
parser.add_argument("--ref", required=True, help="La référence unique du client à chercher.")
parser.add_argument("--login", required=True, help="Le nouveau login à insérer/mettre à jour.")
parser.add_argument("--password", required=True, help="Le nouveau mot de passe à insérer/mettre à jour.")
args = parser.parse_args()

# --- Vérification des identifiants ---
if not email or not api_token:
    sys.exit("ERREUR: CONFLUENCE_EMAIL et CONFLUENCE_API_TOKEN doivent être définis dans le fichier .env")

try:
    auth = (email, api_token)
    page_id = args.page_id
    page_content_url = f"{base_api_url}/content/{page_id}"

    # --- 1. Récupérer le contenu de la page ---
    response = requests.get(page_content_url, params={"expand": "body.storage,version"}, auth=auth)
    response.raise_for_status()
    data = response.json()
    
    # --- 2. Modifier la table (logique inchangée) ---
    soup = BeautifulSoup(data["body"]["storage"]["value"], "html.parser")
    table = soup.find("table")
    if not table: raise ValueError("Aucune table trouvée sur la page.")
    
    headers = [h.text.strip() for h in table.find("tr").find_all(["th", "td"])]
    ref_idx, login_idx, password_idx = headers.index("Ref"), headers.index("Login"), headers.index("Password")

    row_found = False
    for row in table.find_all("tr")[1:]:
        cells = row.find_all("td")
        if len(cells) > ref_idx and cells[ref_idx].text.strip() == args.ref:
            cells[login_idx].string = args.login
            cells[password_idx].string = args.password
            row_found = True
            break
    
    if not row_found:
        new_row_cells = [''] * len(headers)
        new_row_cells[ref_idx], new_row_cells[login_idx], new_row_cells[password_idx] = args.ref, args.login, args.password
        new_row_html = f"<tr>{''.join(f'<td>{c}</td>' for c in new_row_cells)}</tr>"
        table.append(BeautifulSoup(new_row_html, "html.parser"))

    # --- 3. Envoyer le HTML mis à jour ---
    payload = {
        "id": page_id, "type": "page", "title": data["title"],
        "body": {"storage": {"value": str(soup), "representation": "storage"}},
        "version": {"number": data["version"]["number"] + 1}
    }
    put_response = requests.put(page_content_url, json=payload, auth=auth)
    put_response.raise_for_status()
    
    print(f"SUCCES: La page ID '{page_id}' a été mise à jour pour la Ref '{args.ref}'.")

except (ValueError, IndexError) as e:
    sys.exit(f"ERREUR de structure: {e}. Vérifiez que la table contient les colonnes 'Ref', 'Login', et 'Password'.")
except requests.exceptions.RequestException as e:
    sys.exit(f"ERREUR de requête: {e.response.status_code} - {e.response.text}")
except Exception as e:
    sys.exit(f"ERREUR inattendue: {e}")