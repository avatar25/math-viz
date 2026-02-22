import streamlit as st
import streamlit.components.v1 as components

def render():
    st.title("Double Pendulum Visualization")
    st.markdown("""
    The Double Pendulum is a classic example of a simple physical system that exhibits rich, chaotic, and unpredictable dynamics. 
    Here we simulate **ten** pendulums simultaneously. They start with an initial angle difference of just **0.001 radians** ($\approx 0.05^\circ$). 
    Watch how quickly their paths diverge—a phenomenon known as sensitive dependence on initial conditions (the butterfly effect).
    <br><br>
    Use the **Start** and **Stop** buttons in the visualization to pause the chaos and inspect the traces.
    """)
    
    st.sidebar.header("Pendulum Parameters")
    
    # Sliders for physical properties
    g = st.sidebar.slider("Gravity ($g$)", min_value=1.0, max_value=20.0, value=9.81, step=0.1)
    m1 = st.sidebar.slider("Mass 1 ($m_1$)", min_value=1.0, max_value=50.0, value=15.0, step=1.0)
    m2 = st.sidebar.slider("Mass 2 ($m_2$)", min_value=1.0, max_value=50.0, value=15.0, step=1.0)
    
    # Let lengths be fixed for visual consistency, or we could add sliders. We'll fix them to 150px in p5.
    
    st.markdown(f"**Current Parameters**: $g={g:.2f}$, $m_1={m1:.1f}$, $m_2={m2:.1f}$")

    # Construct the p5.js HTML string dynamically
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
            background-color: #0f0f0f; /* Matte black */
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
          }}
          canvas {{
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.5);
          }}
          .controls {{
            position: absolute;
            top: 20px;
            left: 20px;
            z-index: 10;
            display: flex;
            gap: 10px;
          }}
          button {{
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: #fff;
            padding: 8px 16px;
            border-radius: 4px;
            font-family: sans-serif;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.2s;
          }}
          button:hover {{
            background: rgba(255, 255, 255, 0.2);
            border-color: rgba(255, 255, 255, 0.5);
          }}
          button:active {{
            transform: scale(0.95);
          }}
        </style>
      </head>
      <body>
        <div class="controls">
          <button onclick="startSim()">Start</button>
          <button onclick="stopSim()">Stop</button>
        </div>
        <script>
          const g = {g} / 10; // scale gravity for the visual frame rate
          const m1 = {m1};
          const m2 = {m2};
          const r1 = 150; // Length of pendulum 1
          const r2 = 150; // Length of pendulum 2
          
          let cx, cy;

          class DoublePendulum {{
            constructor(a1, a2, colorStr) {{
              this.a1 = a1;
              this.a2 = a2;
              this.a1_v = 0;
              this.a2_v = 0;
              this.a1_a = 0;
              this.a2_a = 0;
              this.colorStr = colorStr;
              this.path = [];
            }}

            update() {{
              // Lagrangian Mechanics Equations for Double Pendulum
              let num1 = -g * (2 * m1 + m2) * Math.sin(this.a1);
              let num2 = -m2 * g * Math.sin(this.a1 - 2 * this.a2);
              let num3 = -2 * Math.sin(this.a1 - this.a2) * m2;
              let num4 = (this.a2_v * this.a2_v * r2 + this.a1_v * this.a1_v * r1 * Math.cos(this.a1 - this.a2));
              let den = r1 * (2 * m1 + m2 - m2 * Math.cos(2 * this.a1 - 2 * this.a2));
              this.a1_a = (num1 + num2 + num3 * num4) / den;

              num1 = 2 * Math.sin(this.a1 - this.a2);
              num2 = (this.a1_v * this.a1_v * r1 * (m1 + m2));
              num3 = g * (m1 + m2) * Math.cos(this.a1);
              num4 = this.a2_v * this.a2_v * r2 * m2 * Math.cos(this.a1 - this.a2);
              den = r2 * (2 * m1 + m2 - m2 * Math.cos(2 * this.a1 - 2 * this.a2));
              this.a2_a = (num1 * (num2 + num3 + num4)) / den;

              // Apply acceleration to velocity, velocity to angle
              this.a1_v += this.a1_a;
              this.a2_v += this.a2_a;
              this.a1 += this.a1_v;
              this.a2 += this.a2_v;
            }}

            getPositions() {{
              let x1 = r1 * Math.sin(this.a1);
              let y1 = r1 * Math.cos(this.a1);
              let x2 = x1 + r2 * Math.sin(this.a2);
              let y2 = y1 + r2 * Math.cos(this.a2);
              return {{x1, y1, x2, y2}};
            }}
          }}

          let pendulums = [];
          
          // Simulation toggle flag
          let isPlaying = true;

          function startSim() {{
            isPlaying = true;
          }}

          function stopSim() {{
            isPlaying = false;
          }}

          function setup() {{
            createCanvas(800, 600);
            cx = width / 2;
            cy = height / 3;
            
            // PI/2 is 90 degrees horizontal.
            let startAngle1 = PI / 2;
            let startAngle2 = PI / 2;
            let diff = 0.001;

            // 10 Vibrant Neon Colors for the palette
            let palette = [
              color(0, 255, 255),    // Neon Cyan
              color(0, 191, 255),    // Deep Sky Blue
              color(50, 205, 50),    // Lime Green
              color(173, 255, 47),   // Green-Yellow
              color(255, 255, 0),    // Yellow
              color(255, 140, 0),    // Dark Orange
              color(255, 69, 0),     // Red-Orange
              color(255, 20, 147),   // Deep Pink
              color(191, 0, 255),    // Electric Purple
              color(138, 43, 226)    // Blue Violet
            ];

            for (let i = 0; i < 10; i++) {{
              pendulums.push(new DoublePendulum(
                startAngle1 + (diff * i), 
                startAngle2 + (diff * i), 
                palette[i]
              ));
            }}
          }}

          function draw() {{
            background(15, 15, 15); // Clear every frame so we redraw lines to fade them smoothly
            
            // We want to fade the trails over 1000 frames using path histories.
            // Only update physics if playing
            for (let p of pendulums) {{
                if (isPlaying) {{
                    p.update();
                    let pos = p.getPositions();
                    p.path.push(createVector(pos.x2, pos.y2));
                    if (p.path.length > 1000) {{
                      p.path.shift();
                    }}
                }}
            }}

            push();
            translate(cx, cy);

            // 1. Draw Traces first so they are under the arms
            blendMode(ADD); // Additive blending for neon glowing build-up overlap
            for (let p of pendulums) {{
                noFill();
                beginShape();
                for (let i = 0; i < p.path.length; i++) {{
                   // Fade alpha from 0 at the tail to 30 at the head
                   let alpha = map(i, 0, p.path.length, 0, 30);
                   let strokeC = color(red(p.colorStr), green(p.colorStr), blue(p.colorStr), alpha);
                   stroke(strokeC);
                   strokeWeight(3);
                   vertex(p.path[i].x, p.path[i].y);
                }}
                endShape();
            }}
            blendMode(BLEND); // Reset to normal

            // 2. Draw Pendulum Arms (we just draw the heads/nodes for a cleaner look)
            for (let p of pendulums) {{
                let pos = p.getPositions();
                stroke(255, 100);
                strokeWeight(2);
                line(0, 0, pos.x1, pos.y1);
                line(pos.x1, pos.y1, pos.x2, pos.y2);
                
                fill(p.colorStr);
                noStroke();
                ellipse(pos.x1, pos.y1, m1 * 0.5, m1 * 0.5);
                ellipse(pos.x2, pos.y2, m2 * 0.5, m2 * 0.5);
            }}
            
            fill(255);
            ellipse(0, 0, 10, 10); // Pivot
            pop();

            // 3. Draw Phase Space Plot (bottom right)
            push();
            translate(width - 120, height - 120);
            fill(30);
            noStroke();
            rect(-100, -100, 200, 200, 10); // Background box for phase space
            
            // Grid lines
            stroke(60);
            strokeWeight(1);
            line(0, -100, 0, 100);
            line(-100, 0, 100, 0);

            // Phase space points (Angle 1 vs Angle 2 mapped to local coordinates)
            for (let p of pendulums) {{
               // Angles wrap, but drawing them continuously creates Lissajous
               // We'll normalize angles just for the plot bounds (-PI to PI)
               let theta1 = p.a1 % TWO_PI;
               let theta2 = p.a2 % TWO_PI;
               if (theta1 > PI) theta1 -= TWO_PI; else if (theta1 < -PI) theta1 += TWO_PI;
               if (theta2 > PI) theta2 -= TWO_PI; else if (theta2 < -PI) theta2 += TWO_PI;

               let px = map(theta1, -PI, PI, -90, 90);
               let py = map(theta2, -PI, PI, -90, 90);
               
               fill(p.colorStr);
               noStroke();
               ellipse(px, py, 4, 4);
            }}
            
            fill(255, 150);
            noStroke();
            textSize(10);
            text("θ1 vs θ2 (Phase Space)", -60, 90);
            pop();

          }}
        </script>
      </body>
    </html>
    """
    
    # Render the p5.js component
    components.html(p5_html, height=650)
