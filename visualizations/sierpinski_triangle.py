import streamlit as st

from visualizations.shared import render_p5_iframe


def render():
    st.title("Sierpinski Triangle (Chaos Game)")
    st.markdown(
        r"""
        The **Sierpinski Triangle** is a classic self-similar fractal. One of the simplest ways to generate it is the
        **chaos game**:

        1. Start from any point inside a triangle.
        2. Randomly pick one of the triangle's vertices.
        3. Move a fixed fraction of the way toward that vertex.
        4. Repeat.

        With a jump ratio of **0.5**, the forbidden gaps emerge naturally and the fractal appears point by point.

        $$P_{n+1} = (1-r)P_n + rV_k$$
        """
    )

    st.sidebar.header("Triangle Parameters")

    points_per_frame = st.sidebar.slider("Points Per Frame", min_value=100, max_value=8000, value=1500, step=100)
    jump_ratio = st.sidebar.slider("Jump Ratio", min_value=0.35, max_value=0.75, value=0.50, step=0.01)
    point_size = st.sidebar.slider("Point Size", min_value=1.0, max_value=4.0, value=1.4, step=0.1)
    glow = st.sidebar.slider("Glow Strength", min_value=0.02, max_value=0.3, value=0.08, step=0.01)

    st.markdown(
        f"**Current Parameters**: `points/frame={points_per_frame}`, `jump_ratio={jump_ratio:.2f}`, `point_size={point_size:.1f}`, `glow={glow:.2f}`"
    )

    script_body = f"""
    const pointsPerFrame = {points_per_frame};
    const jumpRatio = {jump_ratio};
    const pointSize = {point_size};
    const glowStrength = {glow};

    let vertices = [];
    let currentPoint;
    let iterations = 0;

    function buildVertices() {{
      const margin = 60;
      const usableWidth = width - margin * 2;
      const triangleHeight = usableWidth * sqrt(3) / 2;
      const topY = max(margin, (height - triangleHeight) / 2);
      const bottomY = topY + triangleHeight;

      vertices = [
        createVector(width / 2, topY),
        createVector(margin, bottomY),
        createVector(width - margin, bottomY)
      ];
    }}

    function setup() {{
      createCanvas(700, 700);
      pixelDensity(1);
      colorMode(HSB, 360, 100, 100, 1);
      background(0, 0, 6);
      blendMode(ADD);
      buildVertices();
      currentPoint = createVector(random(width), random(height));
    }}

    function drawFrameGuide() {{
      push();
      blendMode(BLEND);
      stroke(185, 30, 100, 0.25);
      strokeWeight(1.5);
      noFill();
      triangle(
        vertices[0].x, vertices[0].y,
        vertices[1].x, vertices[1].y,
        vertices[2].x, vertices[2].y
      );

      noStroke();
      fill(185, 25, 100, 0.6);
      for (const vertex of vertices) {{
        circle(vertex.x, vertex.y, 10);
      }}

      fill(0, 0, 100, 0.7);
      textSize(12);
      text(`iterations: ${{iterations.toLocaleString()}}`, 16, 24);
      pop();
    }}

    function draw() {{
      blendMode(ADD);
      noStroke();

      for (let i = 0; i < pointsPerFrame; i++) {{
        const targetIndex = floor(random(vertices.length));
        const target = vertices[targetIndex];

        currentPoint.x = lerp(currentPoint.x, target.x, jumpRatio);
        currentPoint.y = lerp(currentPoint.y, target.y, jumpRatio);

        const hueVal = (targetIndex * 110 + frameCount * 0.6 + i * 0.02) % 360;
        fill(hueVal, 85, 100, glowStrength);
        circle(currentPoint.x, currentPoint.y, pointSize);
        iterations += 1;
      }}

      drawFrameGuide();
    }}
    """

    render_p5_iframe(
        script_body,
        height=750,
        canvas_css="""
        width: min(100%, 700px) !important;
        aspect-ratio: 1 / 1;
        border-radius: 12px;
        box-shadow: 0 10px 40px rgba(0, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.08);
        """,
    )
