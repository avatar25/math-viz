# math-viz

Interactive mathematical and chaos-theory visualizations built with Streamlit and p5.js.

## Included sketches

- Lorenz attractor
- Aizawa attractor
- Double pendulum
- Reaction-diffusion
- Flocking boids
- Langton's ant
- Fourier epicycles
- Fractal trees
- Clifford attractor

## Running locally

1. Create and activate a virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Start the app with `streamlit run app.py`.

The app stores the active page in the URL as `?page=...`, so individual sketches can be bookmarked.

## Project structure

- `app.py`: Streamlit shell, navigation, and home page
- `visualizations/`: one module per sketch
- `visualizations/catalog.py`: page metadata used by the app shell
- `visualizations/shared.py`: shared iframe and asset-loading helpers
- `assets/style.css`: global app styling
- `assets/vendor/p5.min.js`: local p5.js bundle used by all sketches

## Tests

Run the lightweight smoke tests with:

```bash
python3 -m unittest discover -s tests
```
