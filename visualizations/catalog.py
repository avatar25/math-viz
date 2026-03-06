from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class VisualizationPage:
    key: str
    nav_label: str
    icon: str
    title: str
    description: str
    module_name: str | None = None


HOME_PAGE_KEY = "home"

PAGE_ORDER = (
    VisualizationPage(
        key=HOME_PAGE_KEY,
        nav_label="🏠 Home",
        icon="🏠",
        title="Math Visualizations",
        description="Explore interactive mathematical and physics-based chaotic systems.",
        module_name=None,
    ),
    VisualizationPage(
        key="lorenz",
        nav_label="🌀 Lorenz Attractor",
        icon="🌀",
        title="Lorenz Attractor",
        description="A 3D atmospheric convection model that helped define chaos theory and the butterfly effect.",
        module_name="visualizations.lorenz",
    ),
    VisualizationPage(
        key="aizawa",
        nav_label="🪐 Aizawa Attractor",
        icon="🪐",
        title="Aizawa Attractor",
        description="A spherical chaotic flow with a central void and beautifully tangled trajectories.",
        module_name="visualizations.aizawa",
    ),
    VisualizationPage(
        key="double-pendulum",
        nav_label="🪀 Double Pendulum",
        icon="🪀",
        title="Double Pendulum",
        description="Ten nearly identical pendulums diverge into dramatically different paths over time.",
        module_name="visualizations.double_pendulum",
    ),
    VisualizationPage(
        key="reaction-diffusion",
        nav_label="🦠 Reaction-Diffusion",
        icon="🦠",
        title="Reaction-Diffusion",
        description="Virtual chemicals diffuse and react to form striped, spotted, and coral-like patterns.",
        module_name="visualizations.reaction_diffusion",
    ),
    VisualizationPage(
        key="boids",
        nav_label="🕊️ Flocking Boids",
        icon="🕊️",
        title="Flocking Boids",
        description="Simple local rules for separation, alignment, and cohesion create lifelike swarms.",
        module_name="visualizations.boids",
    ),
    VisualizationPage(
        key="langtons-ant",
        nav_label="🐜 Langton's Ant",
        icon="🐜",
        title="Langton's Ant",
        description="A tiny deterministic agent turns simple flip rules into surprising large-scale structure.",
        module_name="visualizations.langtons_ant",
    ),
    VisualizationPage(
        key="fourier-epicycles",
        nav_label="🎼 Fourier Epicycles",
        icon="🎼",
        title="Fourier Epicycles",
        description="Complex curves are rebuilt from rotating circles and harmonics.",
        module_name="visualizations.fourier_epicycles",
    ),
    VisualizationPage(
        key="fractal-trees",
        nav_label="🌳 Fractal Trees",
        icon="🌳",
        title="Fractal Trees",
        description="Recursive branching rules grow a stylized tree that can sway in the wind.",
        module_name="visualizations.fractal_trees",
    ),
    VisualizationPage(
        key="clifford-attractor",
        nav_label="🌪️ Clifford Attractor",
        icon="🌪️",
        title="Clifford Attractor",
        description="A compact 2D system that paints smoky, silk-like chaotic textures.",
        module_name="visualizations.clifford_attractor",
    ),
)

PAGE_BY_KEY = {page.key: page for page in PAGE_ORDER}
VISUALIZATION_PAGES = tuple(page for page in PAGE_ORDER if page.module_name)
