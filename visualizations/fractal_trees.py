import streamlit as st

from visualizations.shared import render_p5_iframe

def render():
    st.title("Fractal Trees (L-Systems)")
    st.markdown(r"""
    **Lindenmayer Systems (L-Systems)** use strict recursive rules to simulate the organic growth of plants, fractals, and biological structures.
    
    The Emergence: You start with a single "stem" and a simple rule: *At every end, grow two smaller branches at an angle.* By repeating this simple instruction recursively, a beautifully complex Japanese Bonsai structure organically emerges.
    
    Adjust the sliders below to watch the stick physically bloom into a tree, and turn up the **Wind** to watch it gracefully sway!
    """, unsafe_allow_html=True)
    
    st.sidebar.header("Tree Parameters")
    
    depth = st.sidebar.slider("Recursion Depth (Growth)", min_value=1, max_value=13, value=10, step=1)
    angle_deg = st.sidebar.slider("Branch Angle", min_value=10, max_value=90, value=25, step=1)
    wind = st.sidebar.slider("Wind Intensity", min_value=0.0, max_value=3.0, value=1.0, step=0.1)

    script_body = f"""
    const maxDepth = {depth};
    const baseAngle = {angle_deg} * (Math.PI / 180);
    const windIntensity = {wind};

    let time = 0;

    function setup() {{
      createCanvas(800, 600);
    }}

    function draw() {{
      background(11, 11, 11);
      time += 0.02;
      let currentWind = sin(time * windIntensity * 2) * (0.08 * windIntensity);
      translate(width / 2, height);
      branch(160, 0, currentWind);
    }}

    function branch(len, depth, windOffset) {{
      strokeWeight(map(len, 5, 160, 0.5, 6));

      if (depth >= maxDepth - 2 && maxDepth > 4) {{
        stroke(150, 255, 180, 220);
      }} else {{
        stroke(220, 220, 230, map(depth, 0, 10, 255, 150));
      }}

      line(0, 0, 0, -len);
      translate(0, -len);

      if (depth < maxDepth - 1) {{
        let windPhysics = windOffset * (depth * 0.3);

        push();
        rotate(baseAngle + windPhysics);
        branch(len * 0.67, depth + 1, windOffset);
        pop();

        push();
        rotate(-baseAngle + windPhysics);
        branch(len * 0.67, depth + 1, windOffset);
        pop();
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
        box-shadow: 0 10px 40px rgba(0, 255, 100, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.05);
        """,
    )
