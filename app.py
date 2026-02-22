import streamlit as st
import importlib

# Set page config once
st.set_page_config(
    page_title="Math Visualizations",
    page_icon="🌌",
    layout="wide",
)

# --- Sidebar Navigation ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Lorenz Attractor", "Aizawa Attractor", "Double Pendulum"])

# --- Routing ---
if page == "Home":
    st.title("Math Visualizations Interactive App")
    st.markdown("""
    Welcome to the Math Visualizations web application! 
    
    This platform hosts interactive mathematical and physics-based visualizations.
    Currently featured:
    - **Lorenz Attractor**: A visual representation of a system of ordinary differential equations first studied by Edward Lorenz.
    - **Aizawa Attractor**: A spherical-like chaotic structure.
    - **Reaction-Diffusion (Turing)**: Patterns simulating chemical reactions and spreads.
    - **Double Pendulum**: A classic chaotic system exhibiting extreme sensitivity to initial conditions.
    
    Use the sidebar to navigate to the different visualizations.
    """)

elif page == "Lorenz Attractor":
    from visualizations import lorenz
    importlib.reload(lorenz)
    lorenz.render()

elif page == "Aizawa Attractor":
    from visualizations import aizawa
    importlib.reload(aizawa)
    aizawa.render()

# slow af. disabled for now.
#elif page == "Reaction-Diffusion (Turing)":
#   from visualizations import reaction_diffusion
#    importlib.reload(reaction_diffusion)
#    reaction_diffusion.render()

elif page == "Double Pendulum":
    from visualizations import double_pendulum
    importlib.reload(double_pendulum)
    double_pendulum.render()
