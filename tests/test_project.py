from __future__ import annotations

import importlib
import unittest

from visualizations.catalog import HOME_PAGE_KEY, PAGE_ORDER, PAGE_BY_KEY, VISUALIZATION_PAGES
from visualizations.shared import P5_BUNDLE_PATH, load_project_text


class ProjectStructureTests(unittest.TestCase):
    def test_home_page_is_registered(self) -> None:
        self.assertIn(HOME_PAGE_KEY, PAGE_BY_KEY)
        self.assertIsNone(PAGE_BY_KEY[HOME_PAGE_KEY].module_name)

    def test_visualization_pages_have_render_functions(self) -> None:
        for page in VISUALIZATION_PAGES:
            module = importlib.import_module(page.module_name)
            self.assertTrue(callable(getattr(module, "render", None)), page.module_name)

    def test_every_page_key_is_unique(self) -> None:
        self.assertEqual(len(PAGE_ORDER), len(PAGE_BY_KEY))

    def test_stylesheet_is_loadable(self) -> None:
        stylesheet = load_project_text("assets", "style.css")
        self.assertIn(":root", stylesheet)

    def test_local_p5_bundle_exists(self) -> None:
        self.assertTrue(P5_BUNDLE_PATH.exists())


if __name__ == "__main__":
    unittest.main()
