import streamlit as st
import streamlit.components.v1 as components

def render():
    st.title("Lorenz Attractor Visualization")
    st.markdown("""
    The Lorenz system is a system of ordinary differential equations first studied by Edward Lorenz. It is notable for having chaotic solutions for certain parameter values and initial conditions. In particular, the Lorenz attractor is a set of chaotic solutions of the Lorenz system.
    """)
    
    st.sidebar.header("Lorenz Parameters")
    
    sigma = st.sidebar.slider(r"$\sigma$ (Sigma)", min_value=0.0, max_value=50.0, value=10.0, step=0.1)
    rho = st.sidebar.slider(r"$\rho$ (Rho)", min_value=0.0, max_value=100.0, value=28.0, step=0.1)
    beta = st.sidebar.slider(r"$\beta$ (Beta)", min_value=0.0, max_value=10.0, value=2.667, step=0.01) # 8/3 approx
    dt = st.sidebar.slider("Time Step ($dt$)", min_value=0.001, max_value=0.05, value=0.01, step=0.001)
    thickness = st.sidebar.slider("Line Thickness", min_value=0.5, max_value=5.0, value=1.5, step=0.1)
    
    st.markdown(f"**Current Parameters**: $\sigma={sigma:.2f}$, $\rho={rho:.2f}$, $\beta={beta:.3f}$, $dt={dt:.3f}$, `thickness={thickness}`")

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
          const sigma = {sigma};
          const rho = {rho};
          const beta = {beta};
          const dt = {dt};
          const strokeThickness = {thickness};

          let x = 0.01;
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
            
            let dx = (sigma * (y - x)) * dt;
            let dy = (x * (rho - z) - y) * dt;
            let dz = (x * y - beta * z) * dt;
            
            x += dx;
            y += dy;
            z += dz;
            
            points.push(createVector(x, y, z));
            
            if (points.length > 5000) {{
                points.shift();
            }}

            scale(5);
            translate(0, 0, -30);
            noFill();
            
            beginShape();
            for (let v of points) {{
              let mappedHue = map(v.z, 0, 50, 0, 255);
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
