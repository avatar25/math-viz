import streamlit as st
import streamlit.components.v1 as components

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

    p5_html = f"""
    <!DOCTYPE html>
    <html>
      <head>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.0/p5.js"></script>
        <style>
          body {{
            margin: 0;
            padding: 0;
            overflow: hidden;
            background-color: #0e1117;
            display: flex;
            justify-content: center;
            align-items: center;
          }}
          canvas {{
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.5);
          }}
        </style>
      </head>
      <body>
        <script>
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
            let dz = (c + a * z - z*z*z / 3 - (x*x + y*y) * (1 + e * z) + f * z * x*x*x) * dt;
            
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
              let mappedHue = map(v.z, -1, 2, 100, 255); 
              mappedHue = (mappedHue + frameCount * 0.5) % 255;
              
              stroke(mappedHue, 255, 255);
              strokeWeight(strokeThickness); 
              vertex(v.x, v.y, v.z);
            }}
            endShape();
          }}
        </script>
      </body>
    </html>
    """
    
    components.html(p5_html, height=650)
