import requests
import re 
import os

repo = "Novik/ruTorrent"

releases_url = f"https://api.github.com/repos/{repo}/releases"

release_response = requests.get(releases_url)
latest_release = release_response.json()[0]

tag_name = latest_release["tag_name"] 
version = re.search(r'v(\d+\.\d+(\.\d+)?)', tag_name).group(1)
release_sha = latest_release["target_commitish"]

print(f"Latest version: {version}")
print(f"Release SHA: {release_sha}")

base_dir = os.environ.get("BASE_DIR")
dockerfile_path = os.path.join(base_dir, "rtorrent-rutorrent-cross-seed", "Dockerfile")

with open(dockerfile_path, "r") as f:
    lines = f.readlines()
    
comment_line_index = None  
arg_line_index = None

for i, line in enumerate(lines):
    if line.startswith("# Novik/ruTorrent"): 
        comment_line_index = i
        
    if line.startswith("ARG RUTORRENT_VERSION="):
        arg_line_index = i

if comment_line_index is not None:
    lines[comment_line_index] = f'# Novik/ruTorrent {version}\n' 

if arg_line_index is not None:
    lines[arg_line_index] = f'ARG RUTORRENT_VERSION={release_sha}\n'

print("Content of Dockerfile before updating:")
print("".join(lines))

with open(dockerfile_path, "w") as f:
    f.writelines(lines)
    
print("Content of Dockerfile after updating:")
with open(dockerfile_path, "r") as f:
    print(f.read())

print("Dockerfile updated")

