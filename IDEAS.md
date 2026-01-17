# Filtering Ideas for Flavor Bible Visualization

The graph can get overwhelming with many nodes. Here are approaches to help filter and navigate, from simple to sophisticated.

## Simple Additions

- [x] **Max Nodes Slider** - Slider to show top N pairings (sorted by recommendation level). Reduces visual clutter quickly.

- [x] **Search/Highlight Field** - Text input that highlights matching node names in orange without removing others. Helps find specific ingredients in a busy graph.

- [x] **Auto-Show Labels for Strong Connections** - Automatically display labels for nodes connected via level 3-4 links. No hovering required for the best pairings.

## Medium Complexity

- [ ] **Category Filtering** - Tag ingredients with categories (protein, vegetable, herb, spice, dairy, fruit, etc.). Add checkboxes to show/hide categories. Requires enriching the CSV data.

- [ ] **"Mutual Only" Toggle** - When multiple ingredients are selected, show only their shared pairings (ingredients that pair with ALL selected items). Great for building recipes.

- [ ] **Connection Count Filter** - "Hide nodes with < N connections" slider. Removes outliers and leaves the most versatile pairings visible.

- [ ] **Progressive Disclosure** - Start collapsed: show only selected ingredients. Click a node to expand its immediate neighbors. Click again to collapse. Explore one branch at a time.

## More Sophisticated

- [ ] **Radial Layout Mode** - Instead of force-directed layout, arrange nodes in concentric rings:
  - Center: selected ingredients
  - Ring 1: level 4 (classic) pairings
  - Ring 2: level 3 (strong)
  - Ring 3: level 2 (moderate)

  Much easier to scan visually.

- [ ] **Semantic Zoom** - As you zoom in, progressively reveal more:
  - Zoomed out: only selected + level 4
  - Mid zoom: + level 3 labels appear
  - Zoomed in: all labels, all levels

  Feels like Google Maps for flavors.

- [ ] **Focus Mode** - Double-click a node to "focus" on it—temporarily hides everything except that node and its direct connections. Click background to unfocus. Drill into one ingredient at a time without changing your selection.
