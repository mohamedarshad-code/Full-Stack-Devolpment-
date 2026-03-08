import os
import json

base_dir = r"d:\FULL STACK WEB DEVOLPMENT\tailwind-css"
folders = ["1-glassmorphism-card", "2-modern-pricing", "3-animated-login", "4-dashboard-widget", "5-gradient-landing"]

def fix_configs():
    for folder in folders:
        folder_path = os.path.join(base_dir, folder)
        input_css_path = os.path.join(folder_path, "src", "input.css")
        
        if not os.path.exists(input_css_path):
            continue
            
        with open(input_css_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Update to v4 style
        content = content.replace('@tailwind base;', '@import "tailwindcss";')
        content = content.replace('@tailwind components;', '')
        content = content.replace('@tailwind utilities;', '')
        
        # Add @source to ensure detection relative to the folder if needed, 
        # but the CLI should handle it if we fix the paths.
        # Actually, let's just use @import "tailwindcss"; and fix the CLI commands.
        
        with open(input_css_path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
            
    # Update package.json scripts to run from the ROOT but with corrected paths
    package_json_path = os.path.join(base_dir, "package.json")
    with open(package_json_path, "r", encoding="utf-8") as f:
        pkg = json.load(f)
        
    scripts = pkg.get("scripts", {})
    for folder in folders:
        short_name = folder.split("-")[1]
        # Use --content to specify the index.html path relative to where the command is run (the root)
        # In v4, --content is not strictly a thing in the same way, but the CLI should scan.
        # Best: Specify the content in the command if v4 CLI supports it or just use the config correctly.
        # Actually, in v4, you can just pass the path to the CLI.
        # Let's just fix the Config.
        
        config_path = os.path.join(folder_path, "tailwind.config.js")
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(f"""/** @type {{import('tailwindcss').Config}} */
module.exports = {{
  content: ["./{folder}/index.html"],
  theme: {{
    extend: {{}},
  }},
  plugins: [],
}}
""")
            
    with open(package_json_path, "w", encoding="utf-8") as f:
        json.dump(pkg, f, indent=2)

if __name__ == "__main__":
    fix_configs()
    print("Configs updated.")
