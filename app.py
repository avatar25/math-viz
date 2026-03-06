from __future__ import annotations

import importlib

import streamlit as st

from visualizations.catalog import HOME_PAGE_KEY, PAGE_BY_KEY, PAGE_ORDER, VISUALIZATION_PAGES
from visualizations.shared import load_project_text


st.set_page_config(
    page_title="Math Visualizations",
    page_icon="⚛️",
    layout="wide",
)


def apply_styles() -> None:
    styles = load_project_text("assets", "style.css")
    st.markdown(f"<style>{styles}</style>", unsafe_allow_html=True)


def normalize_query_page(value: object) -> str:
    if isinstance(value, list):
        value = value[0] if value else None
    if isinstance(value, str) and value in PAGE_BY_KEY:
        return value
    return HOME_PAGE_KEY


def set_current_page(page_key: str) -> None:
    st.session_state["current_page"] = page_key
    st.query_params["page"] = page_key


def get_current_page() -> str:
    query_page = normalize_query_page(st.query_params.get("page"))
    current_page = st.session_state.get("current_page", query_page)

    if query_page != current_page:
        current_page = query_page

    if current_page not in PAGE_BY_KEY:
        current_page = HOME_PAGE_KEY

    set_current_page(current_page)
    return current_page


def render_home() -> None:
    st.title("Math Visualizations")
    st.markdown(
        """
        Explore interactive mathematical and physics-based chaotic visualizations.
        Each sketch runs in the browser, so you can tweak parameters and see the system respond immediately.
        """
    )
    st.caption("Tip: the current page is mirrored in the URL as `?page=...`, so individual sketches are easy to bookmark.")

    columns = st.columns(3, gap="large")
    for index, page in enumerate(VISUALIZATION_PAGES):
        with columns[index % 3]:
            with st.container(border=True):
                st.markdown(
                    f"""
                    <div class="home-card">
                        <div class="home-card-icon">{page.icon}</div>
                        <h3>{page.title}</h3>
                        <p>{page.description}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button(f"Open {page.title}", key=f"open_{page.key}", use_container_width=True):
                    set_current_page(page.key)
                    st.rerun()


def render_visualization(page_key: str) -> None:
    page = PAGE_BY_KEY[page_key]
    if page.module_name is None:
        render_home()
        return

    module = importlib.import_module(page.module_name)
    render = getattr(module, "render", None)
    if render is None:
        st.error(f"The page module `{page.module_name}` does not expose a `render()` function yet.")
        return
    render()


apply_styles()

current_page = get_current_page()
selected_page = st.sidebar.radio(
    "Go to",
    options=[page.key for page in PAGE_ORDER],
    index=[page.key for page in PAGE_ORDER].index(current_page),
    format_func=lambda page_key: PAGE_BY_KEY[page_key].nav_label,
)
st.sidebar.caption("Client-side p5.js sketches with Streamlit controls.")

if selected_page != current_page:
    set_current_page(selected_page)
    current_page = selected_page

render_visualization(current_page)
