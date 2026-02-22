import streamlit as st
import streamlit.components.v1 as components

def render():
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

            for (let iter = 0; iter < 10; iter++) {{
              for (let x = 1; x < width - 1; x++) {{
                for (let y = 1; y < height - 1; y++) {{
                  let a = grid[x][y].a;
                  let b = grid[x][y].b;
                  
                  next[x][y].a = a + (dA * laplaceA(x, y) - a * b * b + feed * (1 - a)) * dt;
                  next[x][y].b = b + (dB * laplaceB(x, y) + a * b * b - (k + feed) * b) * dt;
                  
                  next[x][y].a = constrain(next[x][y].a, 0, 1);
                  next[x][y].b = constrain(next[x][y].b, 0, 1);
                }}
              }}
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
                
                if (c > 200) {{
                   pixels[pix + 0] = Math.max(10, c * 0.1); 
                   pixels[pix + 1] = Math.max(10, c * 0.2); 
                   pixels[pix + 2] = Math.max(15, c * 0.5); 
                }} else {{
                   let bVal = b * 255;
                   pixels[pix + 0] = constrain(bVal * 1.5, 0, 255); 
                   pixels[pix + 1] = constrain(bVal * 0.5, 0, 255); 
                   pixels[pix + 2] = constrain(bVal * 2.0, 0, 255);
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
