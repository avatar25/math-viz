import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Math Visualizations",
    page_icon="🌌",
    layout="wide",
)

# --- Sidebar Navigation ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Lorenz Attractor", "Aizawa Attractor", "Reaction-Diffusion (Turing)"])

# --- Home Page ---
if page == "Home":
    st.title("Math Visualizations Interactive App")
    st.markdown("""
    Welcome to the Math Visualizations web application! 
    
    This platform hosts interactive mathematical and physics-based visualizations.
    Currently featured:
    - **Lorenz Attractor**: A visual representation of a system of ordinary differential equations first studied by Edward Lorenz.
    
    Use the sidebar to navigate to the different visualizations.
    """)

# --- Lorenz Attractor ---
elif page == "Lorenz Attractor":
    st.title("Lorenz Attractor Visualization")
    st.markdown("""
    The Lorenz system is a system of ordinary differential equations first studied by Edward Lorenz. It is notable for having chaotic solutions for certain parameter values and initial conditions. In particular, the Lorenz attractor is a set of chaotic solutions of the Lorenz system.
    """)
    
    st.sidebar.header("Lorenz Parameters")
    
    # Sliders for system constants and visual properties
    sigma = st.sidebar.slider(r"$\sigma$ (Sigma)", min_value=0.0, max_value=50.0, value=10.0, step=0.1)
    rho = st.sidebar.slider(r"$\rho$ (Rho)", min_value=0.0, max_value=100.0, value=28.0, step=0.1)
    beta = st.sidebar.slider(r"$\beta$ (Beta)", min_value=0.0, max_value=10.0, value=2.667, step=0.01) # 8/3 approx
    dt = st.sidebar.slider("Time Step ($dt$)", min_value=0.001, max_value=0.05, value=0.01, step=0.001)
    thickness = st.sidebar.slider("Line Thickness", min_value=0.5, max_value=5.0, value=1.5, step=0.1)
    
    st.markdown(f"**Current Parameters**: $\sigma={sigma:.2f}$, $\rho={rho:.2f}$, $\beta={beta:.3f}$, $dt={dt:.3f}$, `thickness={thickness}`")

    # Construct the p5.js HTML string dynamically, injecting our python variables.
    # We use string formatting to inject the Python slider values into the JS variables
    
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
            background-color: #0e1117; /* Streamlit dark mode match */
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
          // Parameters injected from Streamlit
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
            
            // Allow user to rotate and zoom with mouse
            orbitControl();
            
            // Calculate next point
            let dx = (sigma * (y - x)) * dt;
            let dy = (x * (rho - z) - y) * dt;
            let dz = (x * y - beta * z) * dt;
            
            x += dx;
            y += dy;
            z += dz;
            
            points.push(createVector(x, y, z));
            
            // Prevent array from growing infinitely and slowing down
            if (points.length > 5000) {{ // Limit max points
                points.shift();
            }}

            // Scale and draw
            scale(5); // Adjust scale to fit on screen
            
            // We need to shift everything down a bit because the attractor typically grows entirely positive in Z
            translate(0, 0, -30);

            noFill();
            
            let hu = 0;

            beginShape();
            for (let v of points) {{
              // Map z to hue for a rainbow effect
              let mappedHue = map(v.z, 0, 50, 0, 255);
              mappedHue = (mappedHue + frameCount * 0.5) % 255; // Dynamic pulsing color
              
              stroke(mappedHue, 255, 255);
              strokeWeight(strokeThickness); // Stroke weight needs scaling down since we scaled up by 5
              vertex(v.x, v.y, v.z);
            }}
            endShape();
          }}
        </script>
      </body>
    </html>
    """
    
    # Render the p5.js component
    # Use components.html, adjusting height to accommodate the canvas
    components.html(p5_html, height=650)

# --- Aizawa Attractor ---
elif page == "Aizawa Attractor":
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

            scale(150); // Aizawa attractor is contained roughly in [-2, 2] ranges
            
            // Adjust to center
            translate(0, 0, -0.5); 
            rotateX(Math.PI / 2); // Rotate to make it vertical usually looks better
            
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

# --- Reaction-Diffusion (Turing Patterns) ---
elif page == "Reaction-Diffusion (Turing)":
    st.title("Reaction-Diffusion Visualization")
    st.markdown("""
    Reaction-Diffusion systems simulate how chemicals interact (react) and spread (diffuse) to create patterns in nature, like leopard spots or zebra stripes. It's essentially "math that grows." In this model, we simulate two virtual chemicals, A and B.
    """)
    
    st.sidebar.header("Reaction-Diffusion Parameters")
    
    Da = st.sidebar.slider("Diffusion Rate A ($D_A$)", min_value=0.1, max_value=2.0, value=1.0, step=0.01)
    Db = st.sidebar.slider("Diffusion Rate B ($D_B$)", min_value=0.1, max_value=1.0, value=0.5, step=0.01)
    feed = st.sidebar.slider("Feed Rate ($f$)", min_value=0.01, max_value=0.1, value=0.055, step=0.001)
    k = st.sidebar.slider("Kill Rate ($k$)", min_value=0.01, max_value=0.1, value=0.062, step=0.001)
    dt = st.sidebar.slider("Time Step ($dt$)", min_value=0.1, max_value=2.0, value=1.0, step=0.1)
    
    st.markdown(f"**Current Parameters**: $D_A={Da:.2f}$, $D_B={Db:.2f}$, $f={feed:.3f}$, $k={k:.3f}$, $dt={dt:.1f}$")

    # The Reaction-Diffusion simulation requires a pixel grid. We use p5.js with a small canvas (scaled up via CSS for performance).
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
            /* Scale the small canvas up so it runs fast but looks large */
            width: 600px !important;
            height: 600px !important;
            image-rendering: pixelated; /* Keeps it sharp when scaled */
          }}
        </style>
      </head>
      <body>
        <script>
          const dA = {Da};
          const dB = {Db};
          const feed = {feed};
          const k = {k};
          const dt = {dt};

          let grid;
          let next;
          // Canvas size for simulation. Keep it relatively small (e.g. 200x200) for performance since JS is single-threaded.
          const width = 200; 
          const height = 200;

          function setup() {{
            createCanvas(width, height);
            pixelDensity(1);
            
            grid = new Array(width)
            next = new Array(width)
            for (let x = 0; x < width; x++) {{
              grid[x] = new Array(height)
              next[x] = new Array(height)
              for (let y = 0; y < height; y++) {{
                grid[x][y] = {{ a: 1, b: 0 }}
                next[x][y] = {{ a: 1, b: 0 }}
              }}
            }}
            
            // Seed a few areas with chemical B
            for (let i = 0; i < 10; i++) {{
              let startX = floor(random(10, width - 10));
              let startY = floor(random(10, height - 10));
              for (let x = startX; x < startX + 10; x++) {{
                for (let y = startY; y < startY + 10; y++) {{
                  grid[x][y].b = 1;
                }}
              }}
            }}
          }}

          function draw() {{
            background(51);

            // Run physics a few times per frame to speed it up visually
            for (let iter = 0; iter < 10; iter++) {{
              for (let x = 1; x < width - 1; x++) {{
                for (let y = 1; y < height - 1; y++) {{
                  let a = grid[x][y].a;
                  let b = grid[x][y].b;
                  
                  next[x][y].a = a + (dA * laplaceA(x, y) - a * b * b + feed * (1 - a)) * dt;
                  next[x][y].b = b + (dB * laplaceB(x, y) + a * b * b - (k + feed) * b) * dt;
                  
                  // Clamp values to prevent explosions
                  next[x][y].a = constrain(next[x][y].a, 0, 1);
                  next[x][y].b = constrain(next[x][y].b, 0, 1);
                }}
              }}
              // Swap grids
              let temp = grid;
              grid = next;
              next = temp;
            }}

            loadPixels();
            for (let x = 0; x < width; x++) {{
              for (let y = 0; y < height; y++) {{
                let pix = (x + y * width) * 4;
                let a = grid[x][y].a;
                let b = grid[x][y].b;
                let c = floor((a - b) * 255);
                c = constrain(c, 0, 255);
                
                // We'll give it a nice colorful aesthetic instead of standard grayscale.
                // Map the difference (a-b) to colors
                if (c > 200) {{
                   pixels[pix + 0] = Math.max(10, c * 0.1); // R
                   pixels[pix + 1] = Math.max(10, c * 0.2); // G
                   pixels[pix + 2] = Math.max(15, c * 0.5); // B
                }} else {{
                   // Chemical B dominant areas get bright vibrant color
                   let bVal = b * 255;
                   pixels[pix + 0] = constrain(bVal * 1.5, 0, 255); // R
                   pixels[pix + 1] = constrain(bVal * 0.5, 0, 255); // G
                   pixels[pix + 2] = constrain(bVal * 2.0, 0, 255); // B (Purple-ish)
                }}
                pixels[pix + 3] = 255;
              }}
            }}
            updatePixels();
          }}

          function laplaceA(x, y) {{
            let sumA = 0;
            sumA += grid[x][y].a * -1;
            sumA += grid[x - 1][y].a * 0.2;
            sumA += grid[x + 1][y].a * 0.2;
            sumA += grid[x][y + 1].a * 0.2;
            sumA += grid[x][y - 1].a * 0.2;
            sumA += grid[x - 1][y - 1].a * 0.05;
            sumA += grid[x + 1][y - 1].a * 0.05;
            sumA += grid[x + 1][y + 1].a * 0.05;
            sumA += grid[x - 1][y + 1].a * 0.05;
            return sumA;
          }}

          function laplaceB(x, y) {{
            let sumB = 0;
            sumB += grid[x][y].b * -1;
            sumB += grid[x - 1][y].b * 0.2;
            sumB += grid[x + 1][y].b * 0.2;
            sumB += grid[x][y + 1].b * 0.2;
            sumB += grid[x][y - 1].b * 0.2;
            sumB += grid[x - 1][y - 1].b * 0.05;
            sumB += grid[x + 1][y - 1].b * 0.05;
            sumB += grid[x + 1][y + 1].b * 0.05;
            sumB += grid[x - 1][y + 1].b * 0.05;
            return sumB;
          }}
        </script>
      </body>
    </html>
    """
    
    components.html(p5_html, height=650)
