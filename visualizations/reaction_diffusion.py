import streamlit as st
import streamlit.components.v1 as components

def render():
    st.title("Reaction-Diffusion (Turing Pattern)")
    st.markdown(r"""
    The Gray-Scott Reaction-Diffusion model simulates how two virtual chemicals—"A" and "B"—diffuse and react.
    It is the biological gold standard for emergent patterns, naturally springing into shapes akin to leopard skin or tropical fish.
    
    The formulas are simple:
    $$\frac{\partial A}{\partial t} = D_A \nabla^2 A - AB^2 + f(1 - A)$$
    $$\frac{\partial B}{\partial t} = D_B \nabla^2 B + AB^2 - (k + f)B$$
    
    Use the **real-time sliders below the simulation** to dynamically adjust the **Feed Rate** ($f$) and **Kill Rate** ($k$) and watch a "striped" labyrinthine matrix actively melt into a "spotted" world!
    """, unsafe_allow_html=True)
    
    # We use purely HTML/JS sliders embedded directly with the p5 canvas!
    # This prevents Streamlit from reloading the Python script and resetting the p5.js array state,
    # achieving TRUE real-time "melting" and biological emergence.

    p5_html = """
    <!DOCTYPE html>
    <html>
      <head>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.0/p5.min.js"></script>
        <style>
          body {
            margin: 0;
            padding: 0;
            overflow: hidden;
            background-color: transparent;
            display: flex;
            flex-direction: column;
            align-items: center;
          }
          canvas {
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,255,255,0.15);
            width: 500px !important;
            height: 500px !important;
            image-rendering: auto; 
            border: 1px solid rgba(255,255,255,0.05);
            margin-bottom: 20px;
          }
          .controls-container {
            display: flex;
            flex-direction: row;
            gap: 40px;
            font-family: 'Fira Code', monospace;
            color: #ffffff;
            background: rgba(11, 11, 11, 0.4);
            padding: 15px 30px;
            border-radius: 8px;
            border: 1px solid rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
          }
          .slider-group {
            display: flex;
            flex-direction: column;
            gap: 5px;
            font-size: 14px;
          }
          input[type=range] {
            accent-color: #00ffff;
            width: 200px;
          }
          .presets {
             display: flex;
             gap: 10px;
             margin-top: 10px;
          }
          button {
             background: rgba(0, 255, 255, 0.1);
             border: 1px solid #00ffff;
             color: #00ffff;
             padding: 5px 10px;
             border-radius: 4px;
             cursor: pointer;
             font-family: 'Fira Code', monospace;
          }
          button:hover { background: rgba(0, 255, 255, 0.3); }
        </style>
      </head>
      <body>
        <!-- The p5 canvas drops here automatically -->
        
        <div class="controls-container" id="controls">
            <div class="slider-group">
                <label>Feed Rate (f): <span id="f-val">0.055</span></label>
                <input type="range" id="f-slider" min="0.010" max="0.100" step="0.001" value="0.055">
            </div>
            <div class="slider-group">
                <label>Kill Rate (k): <span id="k-val">0.062</span></label>
                <input type="range" id="k-slider" min="0.040" max="0.100" step="0.001" value="0.062">
            </div>
            <div class="slider-group">
                <button onclick="setPreset(0.055, 0.062)">Coral Focus</button>
                <button onclick="setPreset(0.035, 0.065)">Spotted</button>
                <button onclick="setPreset(0.045, 0.065)">Striped</button>
            </div>
        </div>

        <script>
          const dA = 1.0;
          const dB = 0.5;
          let feed = 0.055;
          let k = 0.062;
          const dt = 1.0;

          // Wire up HTML sliders
          document.getElementById('f-slider').addEventListener('input', (e) => {
              feed = parseFloat(e.target.value);
              document.getElementById('f-val').innerText = feed.toFixed(3);
          });
          document.getElementById('k-slider').addEventListener('input', (e) => {
              k = parseFloat(e.target.value);
              document.getElementById('k-val').innerText = k.toFixed(3);
          });

          function setPreset(newF, newK) {
              feed = newF; k = newK;
              document.getElementById('f-slider').value = newF;
              document.getElementById('k-slider').value = newK;
              document.getElementById('f-val').innerText = newF.toFixed(3);
              document.getElementById('k-val').innerText = newK.toFixed(3);
          }

          // Optimized 1D array representations for hyper-fast CPU simulation
          const w = 200; 
          const h = 200;
          let gridA = new Float32Array(w * h);
          let gridB = new Float32Array(w * h);
          let nextA = new Float32Array(w * h);
          let nextB = new Float32Array(w * h);

          function setup() {
            let cnv = createCanvas(w, h);
            cnv.parent(document.body);
            // Move canvas before controls visually
            document.body.insertBefore(cnv.elt, document.getElementById('controls'));
            
            pixelDensity(1);
            
            // Initialization
            gridA.fill(1.0);
            gridB.fill(0.0);
            
            // Seed the grid with B to start the reaction
            for (let i = 0; i < 20; i++) {
              let startX = floor(random(10, w - 10));
              let startY = floor(random(10, h - 10));
              for (let x = startX; x < startX + 15; x++) {
                for (let y = startY; y < startY + 15; y++) {
                  gridB[y * w + x] = 1.0;
                }
              }
            }
          }

          function draw() {
            // Multi-pass iterations per frame for speed
            for (let iter = 0; iter < 10; iter++) {
              for (let x = 1; x < w - 1; x++) {
                for (let y = 1; y < h - 1; y++) {
                  let i = y * w + x;
                  let a = gridA[i];
                  let b = gridB[i];
                  
                  // Compute laplacian
                  let lapA = a * -1 
                           + gridA[(y-1)*w + x]*0.2 + gridA[(y+1)*w + x]*0.2 
                           + gridA[y*w + (x-1)]*0.2 + gridA[y*w + (x+1)]*0.2
                           + gridA[(y-1)*w + (x-1)]*0.05 + gridA[(y-1)*w + (x+1)]*0.05 
                           + gridA[(y+1)*w + (x-1)]*0.05 + gridA[(y+1)*w + (x+1)]*0.05;
                           
                  let lapB = b * -1 
                           + gridB[(y-1)*w + x]*0.2 + gridB[(y+1)*w + x]*0.2 
                           + gridB[y*w + (x-1)]*0.2 + gridB[y*w + (x+1)]*0.2
                           + gridB[(y-1)*w + (x-1)]*0.05 + gridB[(y-1)*w + (x+1)]*0.05 
                           + gridB[(y+1)*w + (x-1)]*0.05 + gridB[(y+1)*w + (x+1)]*0.05;

                  let valA = a + (dA * lapA - a * b * b + feed * (1 - a)) * dt;
                  let valB = b + (dB * lapB + a * b * b - (k + feed) * b) * dt;

                  nextA[i] = constrain(valA, 0, 1);
                  nextB[i] = constrain(valB, 0, 1);
                }
              }
              // Swap buffers
              let tempA = gridA; gridA = nextA; nextA = tempA;
              let tempB = gridB; gridB = nextB; nextB = tempB;
            }

            // Draw to canvas
            loadPixels();
            for (let i = 0; i < gridA.length; i++) {
              let b = gridB[i];
              let pIndex = i * 4;
              
              // Bioluminescent Cyan mapping onto Obsidian (#0b0b0b)
              let bVal = constrain(b, 0, 1); 
              
              // Base dark color is r=11, g=11, b=11
              let r = 11 + (bVal * 30);
              let g = 11 + (bVal > 0.2 ? bVal * 255 : bVal * 120);
              let bCol = 11 + (bVal > 0.1 ? bVal * 255 * 1.5 : bVal * 150);
              
              pixels[pIndex + 0] = constrain(r, 0, 255);
              pixels[pIndex + 1] = constrain(g, 0, 255);
              pixels[pIndex + 2] = constrain(bCol, 0, 255);
              pixels[pIndex + 3] = 255; // Alpha
            }
            updatePixels();
          }
        </script>
      </body>
    </html>
    """
    
    # Iframe container for p5.js (made slightly taller to fit UI)
    components.html(p5_html, height=700)
