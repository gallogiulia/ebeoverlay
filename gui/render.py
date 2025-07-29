from jinja2 import Environment, FileSystemLoader
import json

CONFIG_FILE = "config.json"


def render_template():
    # Load config
    with open(CONFIG_FILE) as f:
        config = json.load(f)

    mock_mode = config.get("mock_mode", False)

    if mock_mode:
        # Load mock data from scores.json
        try:
            with open("scores.json") as f:
                score_data = json.load(f)
        except FileNotFoundError:
            score_data = []  # fallback: empty list
        google_apps_script_url = ""
    else:
        score_data = []  # No mock data, so template uses fetch instead
        google_apps_script_url = config.get("google_apps_script_url", "")

    # Jinja setup
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("template.j2")

    # Collect division colors dynamically from config
    division_colors = {}
    for division in config.get("divisions", []):
        color_key = f"{division.lower()}_bg"
        division_colors[division] = config.get(color_key, "#ffffff")

    html = template.render(
        font_size=config["font_size"],
        font_family=config["font_family"],
        score1_color=config["score1_color"],
        score2_color=config["score2_color"],
        ends_bg=config["ends_bg"],
        col1_width=config["col1_width"],
        col2_width=config["col2_width"],
        col3_width=config["col3_width"],
        col4_width=config["col4_width"],
        google_apps_script_url=google_apps_script_url,
        divisions=config["divisions"],
        division_colors=division_colors,
        score_data=json.dumps(score_data),
        mock_mode=mock_mode
    )

    with open("preview.html", "w") as f:
        f.write(html)

if __name__ == "__main__":
    render_template()