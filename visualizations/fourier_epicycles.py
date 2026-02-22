import streamlit as st
import streamlit.components.v1 as components

def render():
    st.title("Fourier Series (Drawing with Epicycles)")
    st.markdown(r"""
    The **Fourier Transform** is one of the most profound discoveries in mathematics. It states that *any* complex continuous shape or signal can be perfectly decomposed into a series of elegantly spinning circles (sine waves) rotating at different speeds.
    
    In this visualization, we compute the Discrete Fourier Transform (DFT) of a mathematical silhouette. By connecting the centers of these spinning gears (epicycles) mathematically, we can trace beautiful, complex shapes.
    
    Adjust the **Number of Epicycles** below. Notice how a small number gives a crude, fuzzy approximation, while adding higher-frequency harmonics instantly pulls the chaotic line into a razor-sharp, crisp form.
    """, unsafe_allow_html=True)
    
    st.sidebar.header("Fourier Parameters")
    
    shapes_list = [
        "Heart", 
        "Trefoil Knot", 
        "Infinity (Lemniscate)", 
        "Butterfly Curve", 
        "Spirograph (Hypotrochoid)", 
        "Lissajous Knot", 
        "Star Epicycloid"
    ]
    shape = st.sidebar.selectbox("Silhouette Shape", shapes_list)
    
    # Send shape as integer to JS
    shape_map = {k: v for v, k in enumerate(shapes_list)}
    shape_id = shape_map[shape]
    
    # The max number of harmonics is bounded by the number of points we sample
    harmonics = st.sidebar.slider("Number of Epicycles (Harmonics)", min_value=1, max_value=300, value=50, step=1)
    
    speed = st.sidebar.slider("Drawing Speed", min_value=0.1, max_value=5.0, value=1.0, step=0.1)

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
            box-shadow: 0 10px 40px rgba(0,255,255,0.05);
            width: 800px !important;
            height: 600px !important;
            border: 1px solid rgba(255,255,255,0.1);
          }}
        </style>
      </head>
      <body>
        <script>
          const shapeId = {shape_id};
          let maxHarmonics = {harmonics};
          const speedMulti = {speed};
          
          let time = 0;
          let path = [];
          let fourierTarget = [];

          function dft(x) {{
            let X = [];
            const N = x.length;
            for (let k = 0; k < N; k++) {{
              let re = 0;
              let im = 0;
              for (let n = 0; n < N; n++) {{
                let phi = (TWO_PI * k * n) / N;
                // Complex multiplication: (x_re + i * x_im) * (cos(phi) - i * sin(phi))
                re += x[n].x * cos(phi) + x[n].y * sin(phi);
                im += x[n].y * cos(phi) - x[n].x * sin(phi);
              }}
              re = re / N;
              im = im / N;
              
              let freq = k;
              let amp = sqrt(re * re + im * im);
              let phase = atan2(im, re);
              
              X[k] = {{ re, im, freq, amp, phase }};
            }}
            return X;
          }}

          function setup() {{
            createCanvas(800, 600);
            
            // 1. Sample the mathematical shape
            const N = 600; // Higher fidelity for complex shapes
            let rawPoints = [];
            for (let i = 0; i < N; i++) {{
              let t = map(i, 0, N, 0, TWO_PI);
              let bx = 0, by = 0;
              
              if (shapeId === 0) {{
                // Heart Curve
                bx = 16 * pow(sin(t), 3);
                by = -(13 * cos(t) - 5 * cos(2*t) - 2 * cos(3*t) - cos(4*t));
                bx *= 12; by *= 12; // Scale up
              }} else if (shapeId === 1) {{
                // Trefoil Knot
                bx = sin(t) + 2 * sin(2 * t);
                by = cos(t) - 2 * cos(2 * t);
                bx *= 60; by *= 60;
              }} else if (shapeId === 2) {{
                // Lemniscate of Bernoulli (Infinity)
                let scale = 200;
                bx = (scale * cos(t)) / (1 + pow(sin(t), 2));
                by = (scale * sin(t) * cos(t)) / (1 + pow(sin(t), 2));
              }} else if (shapeId === 3) {{
                // Temple's Butterfly Curve (needs 12pi domain to fully lock structural fractal)
                let bt = map(i, 0, N, 0, TWO_PI * 12);
                bx = sin(bt) * (exp(cos(bt)) - 2 * cos(4*bt) - pow(sin(bt/12), 5));
                by = -cos(bt) * (exp(cos(bt)) - 2 * cos(4*bt) - pow(sin(bt/12), 5));
                bx *= 50; by *= 50;
              }} else if (shapeId === 4) {{
                // Spirograph / Hypotrochoid
                let ht = map(i, 0, N, 0, TWO_PI * 3);
                let R = 5, r = 3, d = 5;
                bx = (R - r) * cos(ht) + d * cos(((R - r) / r) * ht);
                by = (R - r) * sin(ht) - d * sin(((R - r) / r) * ht);
                bx *= 25; by *= 25;
              }} else if (shapeId === 5) {{
                // Dense Lissajous Knot Phase
                bx = sin(3 * t + PI / 2);
                by = sin(2 * t);
                bx *= 200; by *= 200;
              }} else if (shapeId === 6) {{
                // Epicycloid Star
                let et = map(i, 0, N, 0, TWO_PI * 2);
                let R = 5, r = 2; // k = 2.5
                bx = (R + r) * cos(et) - r * cos(((R + r) / r) * et);
                by = (R + r) * sin(et) - r * sin(((R + r) / r) * et);
                bx *= 25; by *= 25;
              }}
              
              rawPoints.push({{ x: bx, y: by }});
            }}
            
            // 2. Compute the Discrete Fourier Transform
            fourierTarget = dft(rawPoints);
            
            // 3. Sort by amplitude so the largest gears are drawn first
            fourierTarget.sort((a, b) => b.amp - a.amp);
          }}

          function epicycles(x, y, rotation, fourier, maxCircs) {{
            for (let i = 0; i < maxCircs; i++) {{
              if (i >= fourier.length) break;
              
              let prevx = x;
              let prevy = y;
              
              let freq = fourier[i].freq;
              let radius = fourier[i].amp;
              let phase = fourier[i].phase;
              
              x += radius * cos(freq * time + phase + rotation);
              y += radius * sin(freq * time + phase + rotation);
              
              // Draw the subtle spinning gears
              stroke(255, 255, 255, 70);
              noFill();
              strokeWeight(1.5);
              ellipse(prevx, prevy, radius * 2);
              
              // Draw the spoke connecting center to edge
              stroke(150, 255, 255, 180);
              strokeWeight(2.5);
              line(prevx, prevy, x, y);
            }}
            return createVector(x, y);
          }}

          function draw() {{
            background(11, 11, 11);
            
            // Move origin to center
            let vx = epicycles(width / 2, height / 2, 0, fourierTarget, maxHarmonics);
            
            path.unshift(vx);
            
            // Trace the beautiful line
            beginShape();
            noFill();
            
            // Add native glowing shadow effect for HTML canvas
            drawingContext.shadowBlur = 20;
            drawingContext.shadowColor = '#00FFFF';
            
            for (let i = 0; i < path.length; i++) {{
               // Rich, neon cyan glowing stroke
               strokeWeight(4.5);
               // Fade slightly so you can see the head of the drawing clearly against the tail
               stroke(0, 255, 255, map(i, 0, path.length, 255, 60));
               vertex(path[i].x, path[i].y);
            }}
            endShape();
            
            // Turn off shadow for next geometric paints
            drawingContext.shadowBlur = 0;
            
            let dt = TWO_PI / fourierTarget.length;
            time += dt * speedMulti;
            
            // Don't blank out the trail! Just pop the oldest points so it creates a continuous, unbroken, glowing loop
            let maxPoints = Math.floor(TWO_PI / (dt * speedMulti)) + 2;
            if (path.length > maxPoints) {{
              path.pop();
            }}
            
            if (time > TWO_PI) {{
              time = 0;
            }}
          }}
        </script>
      </body>
    </html>
    """
    
    components.html(p5_html, height=650)
