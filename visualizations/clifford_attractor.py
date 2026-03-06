import streamlit as st

from visualizations.shared import render_p5_iframe

def render():
    st.title("Clifford Attractor (Digital Silk)")
    st.markdown(r"""
    The **Clifford Attractor** is a striking 2D chaotic system that generates images resembling sheer silk, blowing smoke, or quantum foam. 
    
    Despite producing millions of infinitesimally structured points, the entire structure is defined by only a few trigonometric operations, iterated recursively on a 2D coordinate $(x, y)$.
    
    The formulas are beautifully compact:
    $$x_{n+1} = \sin(a \cdot y_n) + c \cdot \cos(a \cdot x_n)$$
    $$y_{n+1} = \sin(b \cdot x_n) + d \cdot \cos(b \cdot y_n)$$
    """, unsafe_allow_html=True)
    
    st.sidebar.header("Attractor Parameters")
    
    preset = st.sidebar.selectbox("Aesthetic Preset", ["Default Silk", "Ghostly Velvet", "Nebula Core", "Quantum Foam", "Custom Tuning"])
    
    if preset == "Default Silk":
        a, b, c, d = -1.4, 1.6, 1.0, 0.7
    elif preset == "Ghostly Velvet":
        a, b, c, d = 1.7, 1.7, 0.6, 1.2
    elif preset == "Nebula Core":
        a, b, c, d = -1.7, 1.3, -0.1, -1.2
    elif preset == "Quantum Foam":
        a, b, c, d = -1.7, 1.8, -1.9, -0.4
    else:
        a = st.sidebar.slider("Parameter a", min_value=-3.0, max_value=3.0, value=-1.4, step=0.01)
        b = st.sidebar.slider("Parameter b", min_value=-3.0, max_value=3.0, value=1.6, step=0.01)
        c = st.sidebar.slider("Parameter c", min_value=-3.0, max_value=3.0, value=1.0, step=0.01)
        d = st.sidebar.slider("Parameter d", min_value=-3.0, max_value=3.0, value=0.7, step=0.01)

    points_per_frame = st.sidebar.slider("Rendering Speed (Points/Frame)", min_value=5000, max_value=150000, value=30000, step=5000)

    script_body = f"""
    const a = {a};
    const b = {b};
    const c = {c};
    const d = {d};
    const pointsPerFrame = {points_per_frame};

    let x = 0;
    let y = 0;

    function setup() {{
      createCanvas(800, 600);
      background(11, 11, 11);
      blendMode(ADD);
    }}

    function draw() {{
      translate(width / 2, height / 2);
      stroke(90, 180, 255, 10);
      strokeWeight(0.5);

      for (let i = 0; i < pointsPerFrame; i++) {{
        let nx = Math.sin(a * y) + c * Math.cos(a * x);
        let ny = Math.sin(b * x) + d * Math.cos(b * y);
        let px = nx * 140;
        let py = ny * 140;

        point(px, py);
        x = nx;
        y = ny;
      }}
    }}
    """

    render_p5_iframe(
        script_body,
        height=650,
        canvas_css="""
        width: min(100%, 800px) !important;
        aspect-ratio: 4 / 3;
        border-radius: 12px;
        box-shadow: 0 10px 40px rgba(0, 200, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.05);
        """,
    )
