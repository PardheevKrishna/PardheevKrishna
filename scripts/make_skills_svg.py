import os
import html

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "skills.svg")

W, H = 860, 360
PAD = 25
TITLEBAR_H = 30

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
MUTED = "#7d8590"
INK = "#c9d1d9"
SECTION = "#58a6ff"  # blue headers
PILL_BG = "#21262d"  # dark gray pills
PILL_BORDER = "#30363d"
PILL_TEXT = "#c9d1d9"

CATEGORIES = [
    {
        "title": "Languages",
        "skills": ["C", "C++", "Python", "Java", "JavaScript", "TypeScript", "PHP", "R", "Markdown"],
        "col": 0, "row": 0
    },
    {
        "title": "Web Dev",
        "skills": ["HTML5", "CSS3", "React", "Next.js", "Node.js", "Express", "Tailwind", "Three.js", "Vue.js"],
        "col": 1, "row": 0
    },
    {
        "title": "Databases",
        "skills": ["MySQL", "PostgreSQL", "MongoDB", "Redis"],
        "col": 2, "row": 0
    },
    {
        "title": "Basic AI & Data Sci",
        "skills": ["Python", "OpenCV", "NumPy", "Pandas", "scikit-learn", "SciPy"],
        "col": 0, "row": 1
    },
    {
        "title": "Advanced AI & ML",
        "skills": ["PyTorch", "TensorFlow", "Transformers", "Fine-Tuning", "RAG", "Agentic AI", "Vector DBs"],
        "col": 1, "row": 1
    },
    {
        "title": "Cloud & DevOps",
        "skills": ["AWS", "GCP", "Firebase", "Docker", "Git", "GitHub Actions", "NPM"],
        "col": 2, "row": 1
    }
]

def layout_pills(x_start, y_start, width, skills):
    elements = []
    curr_x = x_start
    curr_y = y_start
    pill_h = 22
    spacing_x = 6
    spacing_y = 8
    char_w = 7.0  # approximate width of monospace character at 11px
    for skill in skills:
        pill_w = len(skill) * char_w + 14
        if curr_x + pill_w > x_start + width:
            curr_x = x_start
            curr_y += pill_h + spacing_y
        elements.append((curr_x, curr_y, pill_w, skill))
        curr_x += pill_w + spacing_x
    return elements

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    '<defs>',
    f'<linearGradient id="sbg" x1="0" y1="0" x2="0" y2="1">',
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>',
    f'</linearGradient></defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#sbg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>'
]
for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{20 + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
parts.append(f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" '
             f'text-anchor="middle">PardheevKrishna@github: ~$ neofetch --skills</text>')

col_w = 250
col_gap = 30
row_h = 145

for cat in CATEGORIES:
    col = cat["col"]
    row = cat["row"]
    x = PAD + col * (col_w + col_gap)
    y = TITLEBAR_H + 25 + row * row_h
    delay = 0.1 + (row * 3 + col) * 0.08
    
    group_parts = []
    # Category Header
    group_parts.append(f'<text x="{x}" y="{y}" fill="{SECTION}" font-size="13" font-weight="700">'
                       f'&#8212; {html.escape(cat["title"])}</text>')
    
    pills = layout_pills(x, y + 10, col_w, cat["skills"])
    for px, py, pw, name in pills:
        group_parts.append(
            f'<rect x="{px:.1f}" y="{py:.1f}" width="{pw:.1f}" height="22" rx="4" '
            f'fill="{PILL_BG}" stroke="{PILL_BORDER}" stroke-width="1"/>'
            f'<text x="{px + pw/2:.1f}" y="{py + 15:.1f}" fill="{PILL_TEXT}" font-size="11" '
            f'text-anchor="middle">{html.escape(name)}</text>'
        )
        
    group_xml = "".join(group_parts)
    # Wrap in fade-in slide-up stagger animation
    parts.append(
        f'<g opacity="0" transform="translate(0,5)">{group_xml}'
        f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.4s" fill="freeze"/>'
        f'<animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" '
        f'begin="{delay:.2f}s" dur="0.4s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/></g>'
    )

parts.append("</svg>")
svg = "".join(parts)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)
print("wrote", OUT)
