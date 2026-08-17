import urllib.request
import json
import os
import sys

USERNAME = "Flexcrit"

def fetch_user_data():
    url = f"https://api.github.com/users/{USERNAME}"
    headers = {'User-Agent': 'Mozilla/5.0'}

    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        return None

def update_stats_svg(user_data):
    if not user_data:
        return

    public_repos = user_data.get('public_repos', 9)
    followers = user_data.get('followers', 4)
    following = user_data.get('following', 5)

    stats_svg = f'''<svg width="450" height="200" viewBox="0 0 450 200" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="450" height="200" rx="10" fill="#1a1a1a" stroke="#FFB000" stroke-width="1.5" stroke-opacity="0.4"/>
  <line x1="20" y1="45" x2="430" y2="45" stroke="#FFB000" stroke-opacity="0.15" stroke-dasharray="4 4"/>
  <line x1="20" y1="100" x2="430" y2="100" stroke="#FFB000" stroke-opacity="0.15" stroke-dasharray="4 4"/>
  <line x1="20" y1="155" x2="430" y2="155" stroke="#FFB000" stroke-opacity="0.15" stroke-dasharray="4 4"/>
  <line x1="225" y1="45" x2="225" y2="180" stroke="#FFB000" stroke-opacity="0.15" stroke-dasharray="4 4"/>

  <text x="20" y="30" fill="#FFB000" font-family="'Fira Code', monospace" font-size="14" font-weight="bold" letter-spacing="1">📡 TELEMETRY // GITHUB STATS</text>
  <circle cx="420" cy="25" r="4" fill="#FFB000">
    <animate attributeName="opacity" values="1;0.2;1" dur="2s" repeatCount="indefinite"/>
  </circle>

  <g font-family="'Fira Code', monospace" font-size="13">
    <text x="30" y="75" fill="#c9c9c9">Public Repositories:</text>
    <text x="190" y="75" fill="#FFB000" font-weight="bold">{public_repos}</text>

    <text x="30" y="110" fill="#c9c9c9">Total Commits:</text>
    <text x="190" y="110" fill="#FFB000" font-weight="bold">130+</text>

    <text x="30" y="145" fill="#c9c9c9">Stars Earned:</text>
    <text x="190" y="145" fill="#FFB000" font-weight="bold">1</text>

    <text x="250" y="75" fill="#c9c9c9">Followers:</text>
    <text x="380" y="75" fill="#FFB000" font-weight="bold">{followers}</text>

    <text x="250" y="110" fill="#c9c9c9">Following:</text>
    <text x="380" y="110" fill="#FFB000" font-weight="bold">{following}</text>

    <text x="250" y="145" fill="#c9c9c9">Signal Status:</text>
    <text x="380" y="145" fill="#00FF66" font-weight="bold">LOCKED</text>
  </g>
</svg>'''

    os.makedirs("assets", exist_ok=True)
    with open("assets/github-stats.svg", "w") as f:
        f.write(stats_svg)
    print("Updated assets/github-stats.svg cleanly.")

if __name__ == "__main__":
    user_data = fetch_user_data()
    if user_data:
        update_stats_svg(user_data)
    else:
        print("Failed to fetch user data.", file=sys.stderr)
        sys.exit(1)
