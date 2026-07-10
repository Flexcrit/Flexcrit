import urllib.request
import json
import re

USERNAME = "Flexcrit"

def fetch_repos():
    url = f"https://api.github.com/users/{USERNAME}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return data.get("public_repos", 0)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def update_readme(repos):
    if repos is None:
        return
    
    with open("Readme.md", "r") as f:
        content = f.read()

    # Update Repos count using regex
    new_content = re.sub(r"Repos:\s*\.*\s*\d+", f"Repos: ........ {repos}", content)

    if new_content != content:
        with open("Readme.md", "w") as f:
            f.write(new_content)
        print(f"Updated README with {repos} repos.")
    else:
        print("No changes made to README.")

if __name__ == "__main__":
    repos = fetch_repos()
    update_readme(repos)
