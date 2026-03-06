import streamlit as st

from visualizations.shared import render_p5_iframe

def render():
    st.title("Langton's Ant")
    st.markdown(r"""
    **Langton's Ant** is a two-dimensional universal Turing machine with incredibly simple rules:
    
    1. At a **dark square**, turn 90° right, flip the color, move forward.
    2. At a **bright square**, turn 90° left, flip the color, move forward.
    
    The Emergence: Despite completely deterministic and symmetrical rules, the ant behaves chaotically for the first ~10,000 steps, seemingly drawing pseudo-random garbage. Then, inexplicably, it "finds" a pattern and builds a permanent, diagonal "highway" out to infinity.
    
    Adjust **Simulation Speed** to instantly jump to the emergence of the highway!
    """, unsafe_allow_html=True)
    
    st.sidebar.header("Langton's Ant Parameters")
    
    speed = st.sidebar.slider("Simulation Speed (Steps/Frame)", min_value=10, max_value=2000, value=250, step=10)
    grid_res = st.sidebar.slider("Grid Resolution", min_value=100, max_value=400, value=200, step=10)

    script_body = f"""
    const stepsPerFrame = {speed};
    const gridWidth = {grid_res};
    const gridHeight = {grid_res};

    let grid;
    let x, y;
    let dir;

    const UP = 0;
    const RIGHT = 1;
    const DOWN = 2;
    const LEFT = 3;

    function setup() {{
      createCanvas(600, 600);
      pixelDensity(1);

      grid = new Array(gridWidth);
      for (let i = 0; i < gridWidth; i++) {{
        grid[i] = new Array(gridHeight).fill(0);
      }}

      x = Math.floor(gridWidth / 2);
      y = Math.floor(gridHeight / 2);
      dir = UP;

      background(11, 11, 11);
      noStroke();
    }}

    function draw() {{
      let hueVal = (frameCount * 0.2) % 360;
      colorMode(HSB, 360, 100, 100);
      let cellSize = width / gridWidth;

      for (let n = 0; n < stepsPerFrame; n++) {{
        let state = grid[x][y];

        if (state === 0) {{
          dir = (dir + 1) % 4;
          grid[x][y] = 1;
          fill(hueVal, 90, 100);
        }} else {{
          dir = (dir + 3) % 4;
          grid[x][y] = 0;
          fill(11, 11, 11);
        }}

        rect(x * cellSize, y * cellSize, cellSize, cellSize);

        if (dir === UP) y--;
        else if (dir === RIGHT) x++;
        else if (dir === DOWN) y++;
        else if (dir === LEFT) x--;

        if (x > gridWidth - 1) x = 0;
        else if (x < 0) x = gridWidth - 1;
        if (y > gridHeight - 1) y = 0;
        else if (y < 0) y = gridHeight - 1;
      }}

      fill(255);
      rect(x * cellSize, y * cellSize, cellSize, cellSize);
    }}
    """

    render_p5_iframe(
        script_body,
        height=650,
        canvas_css="""
        width: min(100%, 600px) !important;
        aspect-ratio: 1 / 1;
        border-radius: 8px;
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.05);
        image-rendering: pixelated;
        """,
    )
