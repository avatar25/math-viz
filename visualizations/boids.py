import streamlit as st

from visualizations.shared import render_p5_iframe

def render():
    st.title("Boids (Flocking Algorithm)")
    st.markdown(r"""
    Created by Craig Reynolds in 1986, **Boids** simulates the flocking behavior of birds and fish. 
    It demonstrates how complex, fluid-like murmuration emerges not from a central "flock master", but from three simple localized vector rules applied to every individual:
    
    1. **Separation**: Steer to avoid crowding local flockmates.
    2. **Alignment**: Steer towards the average heading of local flockmates.
    3. **Cohesion**: Steer to move towards the average position of local flockmates.
    
    $$\vec{v}_{total} = w_1\vec{v}_{sep} + w_2\vec{v}_{ali} + w_3\vec{v}_{coh}$$
    
    Adjust the sliders below to see how these individual rules dictate the collective emergence.
    """, unsafe_allow_html=True)
    
    st.sidebar.header("Boid Parameters")
    
    separation = st.sidebar.slider("Separation ($w_1$)", min_value=0.0, max_value=3.0, value=1.5, step=0.1)
    alignment = st.sidebar.slider("Alignment ($w_2$)", min_value=0.0, max_value=3.0, value=1.0, step=0.1)
    cohesion = st.sidebar.slider("Cohesion ($w_3$)", min_value=0.0, max_value=3.0, value=1.0, step=0.1)
    max_speed = st.sidebar.slider("Max Speed", min_value=1.0, max_value=10.0, value=4.0, step=0.5)

    script_body = f"""
    const w1 = {separation};
    const w2 = {alignment};
    const w3 = {cohesion};
    const maxSpd = {max_speed};
    const viewDist = 50;

    let flock = [];

    function setup() {{
      createCanvas(800, 600);
      for (let i = 0; i < 150; i++) {{
        flock.push(new Boid());
      }}
    }}

    function draw() {{
      background(11, 11, 11, 60);

      for (let boid of flock) {{
        boid.edges();
        boid.flock(flock);
        boid.update();
        boid.show();
      }}
    }}

    class Boid {{
      constructor() {{
        this.position = createVector(random(width), random(height));
        this.velocity = p5.Vector.random2D();
        this.velocity.setMag(random(2, 4));
        this.acceleration = createVector();
        this.maxForce = 0.2;
        this.maxSpeed = maxSpd;
        this.history = [];
      }}

      edges() {{
        let wrapped = false;
        if (this.position.x > width) {{ this.position.x = 0; wrapped = true; }}
        else if (this.position.x < 0) {{ this.position.x = width; wrapped = true; }}

        if (this.position.y > height) {{ this.position.y = 0; wrapped = true; }}
        else if (this.position.y < 0) {{ this.position.y = height; wrapped = true; }}

        if (wrapped) {{
          this.history = [];
        }}
      }}

      align(boids) {{
        let steering = createVector();
        let total = 0;
        for (let other of boids) {{
          let d = dist(this.position.x, this.position.y, other.position.x, other.position.y);
          if (other !== this && d < viewDist) {{
            steering.add(other.velocity);
            total++;
          }}
        }}
        if (total > 0) {{
          steering.div(total);
          steering.setMag(this.maxSpeed);
          steering.sub(this.velocity);
          steering.limit(this.maxForce);
        }}
        return steering;
      }}

      cohesion(boids) {{
        let steering = createVector();
        let total = 0;
        for (let other of boids) {{
          let d = dist(this.position.x, this.position.y, other.position.x, other.position.y);
          if (other !== this && d < viewDist) {{
            steering.add(other.position);
            total++;
          }}
        }}
        if (total > 0) {{
          steering.div(total);
          steering.sub(this.position);
          steering.setMag(this.maxSpeed);
          steering.sub(this.velocity);
          steering.limit(this.maxForce);
        }}
        return steering;
      }}

      separation(boids) {{
        let steering = createVector();
        let total = 0;
        for (let other of boids) {{
          let d = dist(this.position.x, this.position.y, other.position.x, other.position.y);
          if (other !== this && d < viewDist / 2) {{
            let diff = p5.Vector.sub(this.position, other.position);
            diff.div(d * d);
            steering.add(diff);
            total++;
          }}
        }}
        if (total > 0) {{
          steering.div(total);
          steering.setMag(this.maxSpeed);
          steering.sub(this.velocity);
          steering.limit(this.maxForce * 1.5);
        }}
        return steering;
      }}

      flock(boids) {{
        let alignment = this.align(boids);
        let cohesion = this.cohesion(boids);
        let separation = this.separation(boids);

        alignment.mult(w2);
        cohesion.mult(w3);
        separation.mult(w1);

        this.acceleration.add(alignment);
        this.acceleration.add(cohesion);
        this.acceleration.add(separation);
      }}

      update() {{
        this.position.add(this.velocity);
        this.velocity.add(this.acceleration);
        this.velocity.limit(this.maxSpeed);
        this.acceleration.mult(0);

        this.history.push(createVector(this.position.x, this.position.y));
        if (this.history.length > 8) {{
          this.history.shift();
        }}
      }}

      show() {{
        noFill();
        beginShape();
        for (let i = 0; i < this.history.length; i++) {{
          strokeWeight(map(i, 0, this.history.length, 1, 3));
          stroke(255, 255, 255, map(i, 0, this.history.length, 0, 150));
          vertex(this.history[i].x, this.history[i].y);
        }}
        endShape();

        let theta = this.velocity.heading() + radians(90);
        fill(255, 255, 255);
        noStroke();
        push();
        translate(this.position.x, this.position.y);
        rotate(theta);
        beginShape();
        vertex(0, -5);
        vertex(-3, 3);
        vertex(3, 3);
        endShape(CLOSE);
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
        box-shadow: 0 10px 40px rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        """,
    )
