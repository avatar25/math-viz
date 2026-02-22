import streamlit as st
import streamlit.components.v1 as components

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

    p5_html = f"""
    <!DOCTYPE html>
    <html>
      <head>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.0/p5.min.js"></script>
        <style>
          body {{
            margin: 0;
            padding: 0;
            overflow: hidden;
            background-color: transparent;
            display: flex;
            justify-content: center;
            align-items: center;
          }}
          canvas {{
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0, 200, 255, 0.08); /* Ethereal blue glow */
            width: 800px !important;
            height: 600px !important;
            border: 1px solid rgba(255,255,255,0.05);
          }}
        </style>
      </head>
      <body>
        <script>
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
            
            // The ADD blend mode causes the extremely transparent points to stack together and "glow" organically, forming bright neon wisps like smoke.
            blendMode(ADD);
          }}

          function draw() {{
            translate(width / 2, height / 2);
            
            // Ultra-fine transparent brush stroke
            stroke(90, 180, 255, 10);
            strokeWeight(0.5);

            for (let i = 0; i < pointsPerFrame; i++) {{
              // The mathematics of the Clifford Attractor
              let nx = Math.sin(a * y) + c * Math.cos(a * x);
              let ny = Math.sin(b * x) + d * Math.cos(b * y);
              
              // Map output to canvas coordinates (a scale of 140 pushes it naturally towards the edges)
              let px = nx * 140;
              let py = ny * 140;
              
              point(px, py);
              
              // Step memory forward
              x = nx;
              y = ny;
            }}
          }}
        </script>
      </body>
    </html>
    """
    
    components.html(p5_html, height=650)
