"""Regression tests for Flavor Bible visualization."""

import csv
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect, sync_playwright

# Paths
PROJECT_DIR = Path(__file__).parent
DEPLOY_FILE = PROJECT_DIR / "index.html"
CSV_FILE = PROJECT_DIR / "flavor_bible_full_w_levels.csv"


# --- Data helpers to compute expected values ---

def load_flavor_data():
    """Load and process CSV data the same way the JS does."""
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        raw_data = [
            {"main": row["MAIN"].lower(), "pairing": row["PAIRING"].lower()}
            for row in reader
        ]

    all_mains = set(row["main"] for row in raw_data)
    # smallerData: only keep rows where pairing is also a main ingredient
    smaller_data = [row for row in raw_data if row["pairing"] in all_mains]

    return raw_data, all_mains, smaller_data


def get_expected_graph(selected_flavors: list[str], smaller_data: list[dict]) -> tuple[set, set]:
    """
    Compute expected nodes and edges for a selection.
    Returns (nodes, edges) where edges are frozensets of (source, target).
    """
    selected = set(f.lower() for f in selected_flavors)

    nodes = set(selected)
    edges = set()

    for row in smaller_data:
        main, pairing = row["main"], row["pairing"]
        if main in selected:
            nodes.add(pairing)
            # Edge as frozenset so order doesn't matter
            edges.add(frozenset([main, pairing]))
        if pairing in selected:
            nodes.add(main)
            edges.add(frozenset([main, pairing]))

    return nodes, edges


def get_mutual_pairings(selected_flavors: list[str], smaller_data: list[dict]) -> set:
    """Get pairings that connect to ALL selected flavors."""
    selected = set(f.lower() for f in selected_flavors)
    if len(selected) <= 1:
        # With 0-1 selections, mutual is same as normal
        return get_expected_graph(selected_flavors, smaller_data)[0] - selected

    pairing_connections = {}  # pairing -> set of connected selected flavors
    for row in smaller_data:
        main, pairing = row["main"], row["pairing"]
        if main in selected and pairing not in selected:
            pairing_connections.setdefault(pairing, set()).add(main)
        if pairing in selected and main not in selected:
            pairing_connections.setdefault(main, set()).add(pairing)

    return {p for p, conns in pairing_connections.items() if conns == selected}


# --- Fixtures ---

@pytest.fixture(scope="module")
def flavor_data():
    """Load flavor data once for all tests."""
    return load_flavor_data()


@pytest.fixture(scope="module")
def browser():
    """Launch browser once for all tests."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    """Fresh page for each test."""
    page = browser.new_page()
    page.goto(f"file://{DEPLOY_FILE}")
    page.wait_for_selector("#graph")
    yield page
    page.close()


# --- Helper functions ---

def select_flavors(page: Page, flavors: list[str]):
    """Select flavors using the Select2 dropdown."""
    # Clear existing selections
    page.evaluate("$('#flavorInput').val(null).trigger('change')")
    page.wait_for_timeout(100)

    # Select new flavors
    flavor_list = [f.lower() for f in flavors]
    page.evaluate(f"$('#flavorInput').val({flavor_list}).trigger('change')")
    # Wait for graph to update
    page.wait_for_timeout(500)


def count_nodes(page: Page) -> int:
    """Count visible nodes in the graph."""
    return page.locator("#graph .node").count()


def count_edges(page: Page) -> int:
    """Count visible edges in the graph."""
    return page.locator("#graph .link").count()


def get_node_ids(page: Page) -> set[str]:
    """Get IDs of all nodes in the graph."""
    nodes = page.evaluate("""
        () => Array.from(document.querySelectorAll('#graph .node'))
            .map(n => n.__data__?.id || '')
            .filter(id => id)
    """)
    return set(nodes)


# --- Tests ---

class TestPageLoad:
    """Basic page load tests."""

    def test_page_loads(self, page):
        """Page should load without errors."""
        expect(page.locator("#graph-container")).to_be_visible()

    def test_default_selection_renders(self, page):
        """Default selection should render nodes."""
        # The app has default selections, so nodes should exist
        assert count_nodes(page) > 0
        assert count_edges(page) > 0


class TestEdgeCounts:
    """Verify correct number of edges for various selections."""

    def test_single_ingredient_edges(self, page, flavor_data):
        """Single ingredient should show correct edge count."""
        _, all_mains, smaller_data = flavor_data

        test_ingredient = "chicken"
        select_flavors(page, [test_ingredient])

        expected_nodes, expected_edges = get_expected_graph([test_ingredient], smaller_data)

        actual_nodes = count_nodes(page)
        actual_edges = count_edges(page)

        assert actual_nodes == len(expected_nodes), \
            f"Expected {len(expected_nodes)} nodes, got {actual_nodes}"
        assert actual_edges == len(expected_edges), \
            f"Expected {len(expected_edges)} edges, got {actual_edges}"

    def test_two_ingredients_edges(self, page, flavor_data):
        """Two ingredients should show combined edges."""
        _, all_mains, smaller_data = flavor_data

        test_ingredients = ["chicken", "lemons"]
        select_flavors(page, test_ingredients)

        expected_nodes, expected_edges = get_expected_graph(test_ingredients, smaller_data)

        actual_nodes = count_nodes(page)
        actual_edges = count_edges(page)

        assert actual_nodes == len(expected_nodes), \
            f"Expected {len(expected_nodes)} nodes, got {actual_nodes}"
        assert actual_edges == len(expected_edges), \
            f"Expected {len(expected_edges)} edges, got {actual_edges}"

    def test_garlic_edges(self, page, flavor_data):
        """Garlic (common ingredient) should have many edges."""
        _, all_mains, smaller_data = flavor_data

        select_flavors(page, ["garlic"])

        expected_nodes, expected_edges = get_expected_graph(["garlic"], smaller_data)

        actual_edges = count_edges(page)

        # Garlic should have many pairings
        assert actual_edges > 50, f"Garlic should have many edges, got {actual_edges}"
        assert actual_edges == len(expected_edges)


class TestNodeCorrectness:
    """Verify correct nodes appear for selections."""

    def test_selected_nodes_present(self, page, flavor_data):
        """Selected ingredients should appear as nodes."""
        _, _, smaller_data = flavor_data

        test_ingredients = ["chicken", "garlic", "lemons"]
        select_flavors(page, test_ingredients)

        node_ids = get_node_ids(page)

        for ingredient in test_ingredients:
            assert ingredient in node_ids, \
                f"Selected ingredient '{ingredient}' should be a node"

    def test_connected_nodes_present(self, page, flavor_data):
        """Nodes connected to selection should appear."""
        _, _, smaller_data = flavor_data

        select_flavors(page, ["chicken"])

        expected_nodes, _ = get_expected_graph(["chicken"], smaller_data)
        actual_nodes = get_node_ids(page)

        assert expected_nodes == actual_nodes, \
            f"Node mismatch. Missing: {expected_nodes - actual_nodes}, Extra: {actual_nodes - expected_nodes}"


class TestMutualOnly:
    """Tests for Mutual Only toggle."""

    def test_mutual_only_filters_pairings(self, page, flavor_data):
        """Mutual Only should show only shared pairings."""
        _, _, smaller_data = flavor_data

        select_flavors(page, ["chicken", "lemons"])
        normal_nodes = count_nodes(page)

        # Enable Mutual Only
        page.click("#mutual-only")
        page.wait_for_timeout(300)

        mutual_nodes = count_nodes(page)
        expected_mutual = get_mutual_pairings(["chicken", "lemons"], smaller_data)

        # Mutual should have fewer nodes (intersection < union)
        assert mutual_nodes < normal_nodes
        # Plus 2 for the selected ingredients themselves
        assert mutual_nodes == len(expected_mutual) + 2

    def test_mutual_only_toggle_off_restores(self, page, flavor_data):
        """Disabling Mutual Only should restore full pairings."""
        _, _, smaller_data = flavor_data

        select_flavors(page, ["chicken", "lemons"])
        normal_nodes = count_nodes(page)

        # Enable then disable Mutual Only
        page.click("#mutual-only")
        page.wait_for_timeout(300)
        page.click("#mutual-only")
        page.wait_for_timeout(300)

        restored_nodes = count_nodes(page)
        assert restored_nodes == normal_nodes

    def test_mutual_only_single_selection(self, page, flavor_data):
        """Mutual Only with single selection should behave same as normal."""
        _, _, smaller_data = flavor_data

        select_flavors(page, ["chicken"])
        normal_nodes = count_nodes(page)

        # Enable Mutual Only
        page.click("#mutual-only")
        page.wait_for_timeout(300)

        mutual_nodes = count_nodes(page)
        # With single selection, mutual = normal (all pairings connect to the one selected)
        assert mutual_nodes == normal_nodes


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
