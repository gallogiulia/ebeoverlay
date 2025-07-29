import json
from jinja2 import Environment, FileSystemLoader

def render_template():
    with open("config.json", "r") as f:
        config = json.load(f)

    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("template.j2")  # instead of template.html

    output = template.render(**config)

    with open("preview.html", "w", encoding="utf-8") as f:
        f.write(output)

    print("✅ preview.html generated successfully.")

if __name__ == "__main__":
    render_template()
