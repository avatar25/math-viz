from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import streamlit.components.v1 as components


PROJECT_ROOT = Path(__file__).resolve().parent.parent
P5_BUNDLE_PATH = PROJECT_ROOT / "assets" / "vendor" / "p5.min.js"
P5_CDN_URL = "https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.0/p5.min.js"

DEFAULT_BODY_CSS = """
margin: 0;
padding: 0;
overflow: hidden;
background-color: transparent;
display: flex;
justify-content: center;
align-items: center;
"""

DEFAULT_CANVAS_CSS = """
display: block;
max-width: 100%;
height: auto !important;
"""


@lru_cache(maxsize=None)
def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_project_text(*parts: str) -> str:
    return read_text(PROJECT_ROOT.joinpath(*parts))


def p5_script_tag() -> str:
    if P5_BUNDLE_PATH.exists():
        return f"<script>{read_text(P5_BUNDLE_PATH)}</script>"
    return f'<script src="{P5_CDN_URL}"></script>'


def render_p5_iframe(
    script_body: str,
    *,
    height: int = 650,
    body_html: str = "",
    body_css: str = "",
    canvas_css: str = "",
    extra_css: str = "",
    head_html: str = "",
) -> None:
    html = f"""
    <!DOCTYPE html>
    <html>
      <head>
        {p5_script_tag()}
        {head_html}
        <style>
          body {{
            {DEFAULT_BODY_CSS}
            {body_css}
          }}

          canvas {{
            {DEFAULT_CANVAS_CSS}
            {canvas_css}
          }}

          {extra_css}
        </style>
      </head>
      <body>
        {body_html}
        <script>
          {script_body}
        </script>
      </body>
    </html>
    """
    components.html(html, height=height)
