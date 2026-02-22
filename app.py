import streamlit as st
import importlib

# Set page config once
st.set_page_config(
    page_title="Math Visualizations",
    page_icon="⚛️",
    layout="wide",
)

# Load CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- Sidebar Navigation ---
st.sidebar.title("")
page = st.sidebar.radio("Go to", [
    "🏠 Home", 
    "🌀 Lorenz Attractor", 
    "🪐 Aizawa Attractor", 
    "🪀 Double Pendulum",
    "🦠 Reaction-Diffusion",
    "🕊️ Flocking Boids"
])

# --- Routing ---
if page == "🏠 Home":
    st.title("Math Vizualizations")
    st.markdown("""
    Explore interactive mathematical and physics-based chaotic visualizations.
    """)
    
    st.markdown("""
    <div class="cards-container">
        <div class="viz-card" onclick="window.parent.document.querySelectorAll('div[role=\\'radiogroup\\'] label')[1].click();">
            <div class="icon">🌀</div>
            <h3>Lorenz Attractor</h3>
            <p>An intricate 3D representation of atmospheric convection equations that birthed Chaos Theory and the Butterfly Effect.</p>
        </div>
        <div class="viz-card" onclick="window.parent.document.querySelectorAll('div[role=\\'radiogroup\\'] label')[2].click();">
            <div class="icon">🪐</div>
            <h3>Aizawa Attractor</h3>
            <p>A mesmerizing spherical-like chaotic structure with a central tubal void, commonly associated with complex fluid dynamics.</p>
        </div>
        <div class="viz-card" onclick="window.parent.document.querySelectorAll('div[role=\\'radiogroup\\'] label')[3].click();">
            <div class="icon">🪀</div>
            <h3>Double Pendulum</h3>
            <p>Ten simultaneous non-linear pendulums demonstrating sensitive dependence on initial conditions through exploding neon traces.</p>
        </div>
        <div class="viz-card" onclick="window.parent.document.querySelectorAll('div[role=\\'radiogroup\\'] label')[4].click();">
            <div class="icon">🦠</div>
            <h3>Reaction-Diffusion</h3>
            <p>Simulates how virtual chemicals diffuse and react, naturally sprouting complex biological patterns like leopard spots and zebra stripes.</p>
        </div>
        <div class="viz-card" onclick="window.parent.document.querySelectorAll('div[role=\\'radiogroup\\'] label')[5].click();">
            <div class="icon">🕊️</div>
            <h3>Flocking Boids</h3>
            <p>Simulates the mesmerzing, fluid-like murmuration of birds using three simple localized vector rules: Separation, Alignment, and Cohesion.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Living Background: Sumi-e ink-wash double pendulum painted directly into the DOM
    st.markdown("""
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.0/p5.min.js"></script>
    <script>
    (function() {
      // Prevent duplicate injection on Streamlit reruns
      if (document.getElementById('sumie-canvas')) return;

      const sketch = (p) => {
        let pendulums = [];
        let cx, cy;

        class Pendulum {
          constructor(a) {
            this.a1 = a; this.a2 = a;
            this.a1_v = 0; this.a2_v = 0;
            this.path = [];
            this.r1 = 0; this.r2 = 0;
            this.m1 = 10; this.m2 = 10;
            this.g = 1;
          }
          update(h) {
            this.r1 = h * 0.22; this.r2 = h * 0.22;
            let num1 = -this.g * (2*this.m1+this.m2) * Math.sin(this.a1);
            let num2 = -this.m2 * this.g * Math.sin(this.a1 - 2*this.a2);
            let num3 = -2 * Math.sin(this.a1 - this.a2) * this.m2;
            let num4 = this.a2_v*this.a2_v*this.r2 + this.a1_v*this.a1_v*this.r1*Math.cos(this.a1-this.a2);
            let den = this.r1*(2*this.m1+this.m2-this.m2*Math.cos(2*this.a1-2*this.a2));
            let a1_a = (num1+num2+num3*num4)/den;

            num1 = 2*Math.sin(this.a1-this.a2);
            num2 = this.a1_v*this.a1_v*this.r1*(this.m1+this.m2);
            num3 = this.g*(this.m1+this.m2)*Math.cos(this.a1);
            num4 = this.a2_v*this.a2_v*this.r2*this.m2*Math.cos(this.a1-this.a2);
            den = this.r2*(2*this.m1+this.m2-this.m2*Math.cos(2*this.a1-2*this.a2));
            let a2_a = (num1*(num2+num3+num4))/den;

            this.a1_v += a1_a; this.a2_v += a2_a;
            this.a1 += this.a1_v; this.a2 += this.a2_v;

            let x2 = this.r1*Math.sin(this.a1) + this.r2*Math.sin(this.a2);
            let y2 = this.r1*Math.cos(this.a1) + this.r2*Math.cos(this.a2);
            this.path.push(p.createVector(x2, y2));
            if (this.path.length > 150) this.path.shift();
          }
          show() {
            p.noFill();
            p.beginShape();
            for (let i = 0; i < this.path.length; i++) {
              p.strokeWeight(p.map(i, 0, this.path.length, 0.5, 6));
              p.stroke(200, 200, 210, p.map(i, 0, this.path.length, 0, 60));
              p.vertex(this.path[i].x, this.path[i].y);
            }
            p.endShape();
          }
        }

        p.setup = function() {
          let cnv = p.createCanvas(p.windowWidth, p.windowHeight);
          cnv.id('sumie-canvas');
          cnv.style('position', 'fixed');
          cnv.style('top', '0');
          cnv.style('left', '0');
          cnv.style('z-index', '-1');
          cnv.style('pointer-events', 'none');
          cnv.style('opacity', '0.35');
          cx = p.width / 2;
          cy = p.height / 3;
          pendulums.push(new Pendulum(p.PI / 2));
          pendulums.push(new Pendulum(p.PI / 2 + 0.08));
          pendulums.push(new Pendulum(p.PI / 2 - 0.08));
        };

        p.draw = function() {
          p.noStroke();
          p.fill(11, 11, 11, 12);
          p.rect(0, 0, p.width, p.height);
          p.translate(cx, cy);
          for (let pend of pendulums) {
            pend.update(p.height);
            pend.show();
          }
        };

        p.windowResized = function() {
          p.resizeCanvas(p.windowWidth, p.windowHeight);
          cx = p.width / 2;
          cy = p.height / 3;
        };
      };

      new p5(sketch);
    })();
    </script>
    """, unsafe_allow_html=True)

elif page == "🌀 Lorenz Attractor":
    from visualizations import lorenz
    importlib.reload(lorenz)
    lorenz.render()

elif page == "🪐 Aizawa Attractor":
    from visualizations import aizawa
    importlib.reload(aizawa)
    aizawa.render()

elif page == "🦠 Reaction-Diffusion":
    from visualizations import reaction_diffusion
    importlib.reload(reaction_diffusion)
    reaction_diffusion.render()

elif page == "🪀 Double Pendulum":
    from visualizations import double_pendulum
    importlib.reload(double_pendulum)
    double_pendulum.render()

elif page == "🕊️ Flocking Boids":
    from visualizations import boids
    importlib.reload(boids)
    boids.render()
