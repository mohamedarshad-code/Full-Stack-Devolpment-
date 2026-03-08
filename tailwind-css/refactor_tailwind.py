import os
import re

base_dir = r"d:\FULL STACK WEB DEVOLPMENT\tailwind-css"
folders = ["1-glassmorphism-card", "2-modern-pricing", "3-animated-login", "4-dashboard-widget", "5-gradient-landing"]

config_template = """/** @type {{import('tailwindcss').Config}} */
module.exports = {{
  content: ["./index.html", "./src/**/*.{{js,css}}"],
  theme: {{
    extend: {{}},
  }},
  plugins: [],
}}
"""

package_json_path = os.path.join(base_dir, "package.json")

def refactor():
    scripts = {}
    for folder in folders:
        folder_path = os.path.join(base_dir, folder)
        index_path = os.path.join(folder_path, "index.html")
        
        if not os.path.exists(index_path):
            continue
            
        with open(index_path, "r", encoding="utf-8") as f:
            html = f.read()
            
        # Extract style
        style_match = re.search(r'<style>(.*?)</style>', html, re.DOTALL)
        custom_css = style_match.group(1).strip() if style_match else ""
        
        # Create src folder and input.css
        src_path = os.path.join(folder_path, "src")
        if not os.path.exists(src_path):
            os.makedirs(src_path)
            
        input_css_content = f"""@tailwind base;
@tailwind components;
@tailwind utilities;

@layer components {{
{custom_css}
}}
"""
        with open(os.path.join(src_path, "input.css"), "w", encoding="utf-8") as f:
            f.write(input_css_content)
            
        # Create tailwind.config.js
        with open(os.path.join(folder_path, "tailwind.config.js"), "w", encoding="utf-8") as f:
            f.write(config_template)
            
        # Update index.html
        # Remove CDN
        html = re.sub(r'<script src="https://cdn.tailwindcss.com"></script>', '', html)
        # Remove Style tag
        html = re.sub(r'<style>.*?</style>', '', html, flags=re.DOTALL)
        # Add link to output.css (we'll put it in dist/output.css)
        link_tag = '  <link href="./dist/output.css" rel="stylesheet">'
        if '<head>' in html:
            html = html.replace('</head>', f'{link_tag}\n</head>')
            
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(html)
            
        # Create build script name
        short_name = folder.split("-")[1]
        scripts[f"build:{short_name}"] = f"npx tailwindcss -i ./{folder}/src/input.css -o ./{folder}/dist/output.css --config ./{folder}/tailwind.config.js"

    # Update package.json scripts
    import json
    with open(package_json_path, "r", encoding="utf-8") as f:
        pkg = json.load(f)
        
    if "scripts" not in pkg:
        pkg["scripts"] = {}
        
    pkg["scripts"].update(scripts)
    pkg["scripts"]["build:all"] = " && ".join(scripts.keys()) # this won't work directly, need "npm run ..."
    pkg["scripts"]["build:all"] = " && ".join([f"npm run {k}" for k in scripts.keys()])
    
    with open(package_json_path, "w", encoding="utf-8") as f:
        json.dump(pkg, f, indent=2)

    print("Refactoring complete.")

if __name__ == "__main__":
    refactor()
