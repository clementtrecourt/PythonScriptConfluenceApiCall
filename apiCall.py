import requests, sys, os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# --- Load Environment Variables ---
load_dotenv() # This line reads the .env file

# --- Configuration ---
# Get credentials from environment variables; exit if not found
email = os.getenv("CONFLUENCE_EMAIL")
api_token = os.getenv("CONFLUENCE_API_TOKEN")
if not email or not api_token:
    sys.exit("Error: Ensure CONFLUENCE_EMAIL and CONFLUENCE_API_TOKEN are set in your .env file.")

page_id = "131284"
url = f"https://clementtpro.atlassian.net/wiki/rest/api/content/{page_id}"

# --- User Input & Confirmation ---
name = input("Enter name to update/add: ").strip()
score = input(f"Enter new score for '{name}': ").strip()
if 'y' not in input(f"This will update '{name}' with score '{score}'. Continue? (y/n): ").lower():
    sys.exit("Operation cancelled by user.")

try:
    # --- Step 1: GET Current Page Data ---
    auth = (email, api_token)
    response = requests.get(url, params={"expand": "body.storage,version"}, auth=auth)
    response.raise_for_status()
    data = response.json()
    soup = BeautifulSoup(data["body"]["storage"]["value"], "html.parser")

    # --- Step 2: Find and Update Table ---
    table = soup.find("table")
    if not table: raise ValueError("No table found on the page.")
    headers = [h.text.strip() for h in table.find("tr").find_all(["th", "td"])]
    name_idx, score_idx = headers.index("Name"), headers.index("Score")

    for row in table.find_all("tr")[1:]:
        cells = row.find_all("td")
        if len(cells) > name_idx and cells[name_idx].text.strip() == name:
            cells[score_idx].string = score
            break
    else:  # This block runs only if the name was not found in the loop
        new_row_cells = [''] * len(headers)
        new_row_cells[name_idx], new_row_cells[score_idx] = name, score
        new_row_html = f"<tr>{''.join(f'<td>{c}</td>' for c in new_row_cells)}</tr>"
        table.append(BeautifulSoup(new_row_html, "html.parser"))

    # --- Step 3: PUT Updated Page Back to Confluence ---
    payload = {
        "id": page_id, "type": "page", "title": data["title"],
        "body": {"storage": {"value": str(soup), "representation": "storage"}},
        "version": {"number": data["version"]["number"] + 1}
    }
    put_response = requests.put(url, json=payload, auth=auth)
    put_response.raise_for_status()
    print(f"Page updated successfully! '{name}' now has score '{score}'.")

except (requests.exceptions.RequestException, ValueError, IndexError) as e:
    sys.exit(f"An error occurred: {e}\nCheck page ID, API token, and table structure.")