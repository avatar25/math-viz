import streamlit as st

from visualizations.shared import render_p5_iframe

def render():
    st.title("Aizawa Attractor Visualization")
    st.markdown("""
    The Aizawa Attractor creates a stunning spherical-like chaotic structure with a central tube. It's often associated with fluid dynamics and magnetic fields.
    """)
    
    st.sidebar.header("Aizawa Parameters")
    
    a = st.sidebar.slider("a", min_value=0.0, max_value=2.0, value=0.95, step=0.01)
    b = st.sidebar.slider("b", min_value=0.0, max_value=2.0, value=0.7, step=0.01)
    c = st.sidebar.slider("c", min_value=0.0, max_value=2.0, value=0.6, step=0.01)
    d = st.sidebar.slider("d", min_value=0.0, max_value=5.0, value=3.5, step=0.1)
    e = st.sidebar.slider("e", min_value=0.0, max_value=1.0, value=0.25, step=0.01)
    f = st.sidebar.slider("f", min_value=0.0, max_value=1.0, value=0.1, step=0.01)
    dt = st.sidebar.slider("Time Step ($dt$)", min_value=0.001, max_value=0.05, value=0.01, step=0.001)
    thickness = st.sidebar.slider("Line Thickness", min_value=0.5, max_value=10.0, value=1.5, step=0.1)

    st.markdown(f"**Current Parameters**: $a={a:.2f}$, $b={b:.2f}$, $c={c:.2f}$, $d={d:.2f}$, $e={e:.2f}$, $f={f:.2f}$, $dt={dt:.3f}$, `thickness={thickness}`")

    script_body = f"""
    const a = {a};
    const b = {b};
    const c = {c};
    const d = {d};
    const e = {e};
    const f = {f};
    const dt = {dt};
    const strokeThickness = {thickness};

    let x = 0.1;
    let y = 0;
    let z = 0;

    let points = [];

    function setup() {{
      createCanvas(800, 600, WEBGL);
      colorMode(HSB, 255);
    }}

    function draw() {{
      background(10, 10, 15);
      orbitControl();

      let dx = ((z - b) * x - d * y) * dt;
      let dy = (d * x + (z - b) * y) * dt;
      let dz = (c + a * z - z * z * z / 3 - (x * x + y * y) * (1 + e * z) + f * z * x * x * x) * dt;

      x += dx;
      y += dy;
      z += dz;

      points.push(createVector(x, y, z));

      if (points.length > 5000) {{
        points.shift();
      }}

      scale(150);
      translate(0, 0, -0.5);
      rotateX(Math.PI / 2);
      noFill();

      beginShape();
      for (let v of points) {{
        let mappedBright = map(v.z, -1, 2, 255, 50);
        stroke(140, 255, mappedBright);
        strokeWeight(strokeThickness);
        vertex(v.x, v.y, v.z);
      }}
      endShape();
    }}
    """

    render_p5_iframe(
        script_body,
        height=650,
        body_css="background-color: #0e1117;",
        canvas_css="""
        width: min(100%, 800px) !important;
        aspect-ratio: 4 / 3;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
        """,
    )
