
import networkx as nx
import matplotlib.pyplot as plt


# ============================================================
# 1. REGIONAL CONNECTIONS
# ============================================================

regional_connections = [
    ("Pacific Northwest", "California"),
    ("Pacific Northwest", "Mountain West"),
    ("California", "Mountain West"),
    ("California", "Southwest"),
    ("Mountain West", "Southwest"),
    ("Mountain West", "Great Plains"),
    ("Southwest", "Texas"),
    ("Southwest", "Great Plains"),
    ("Texas", "Great Plains"),
    ("Texas", "Lower South"),
    ("Great Plains", "Midwest"),
    ("Midwest", "Great Lakes"),
    ("Midwest", "Lower South"),
    ("Great Lakes", "Upper South"),
    ("Great Lakes", "Mid-Atlantic"),
    ("Lower South", "Upper South"),
    ("Upper South", "Mid-Atlantic"),
    ("Mid-Atlantic", "Northeast"),
]


# ============================================================
# 2. BUILD NETWORK
# ============================================================

G = nx.Graph()

G.add_node("Alaska")
G.add_edges_from(regional_connections)


# ============================================================
# 3. MANUALLY ASSIGN POSITIONS
# ============================================================

# Approximate geographic arrangement.
# These are visualization coordinates, not actual coordinates.

pos = {
    "Pacific Northwest": (-3, 4),
    "California": (-4, 1.5),
    "Mountain West": (-1.5, 2.5),
    "Southwest": (-1.5, 0),
    "Great Plains": (1, 2),
    "Texas": (1, -0.5),
    "Midwest": (3, 3),
    "Great Lakes": (4.5, 3),
    "Lower South": (3, -1.5),
    "Upper South": (5, 0),
    "Mid-Atlantic": (6.5, 2),
    "Northeast": (8, 3.5),

    "Alaska": (-3.5, -1.5),
}


# ============================================================
# 4. DRAW NETWORK
# ============================================================

plt.figure(figsize=(8, 7))

# Draw connections
nx.draw_networkx_edges(
    G,
    pos,
    width=2,
    edge_color="gray",
    alpha=0.7
)

# Draw regional nodes
nx.draw_networkx_nodes(
    G,
    pos,
    node_size=2500,
    node_color="skyblue",
    edgecolors="black",
    linewidths=1.5
)

# Draw region labels
nx.draw_networkx_labels(
    G,
    pos,
    font_size=9,
    font_weight="bold"
)

plt.title(
    "Regional Economic Connection Network",
    fontsize=16
)

plt.axis("off")
plt.tight_layout()
plt.show()


# ============================================================
# 5. PRINT CONNECTION SUMMARY
# ============================================================

print("\nREGIONAL CONNECTIONS")
print("-" * 40)

for region in sorted(G.nodes()):

    neighbors = sorted(G.neighbors(region))

    print(f"\n{region}:")

    for neighbor in neighbors:
        print(f"    -> {neighbor}")

print("\nTotal regions:", G.number_of_nodes())
print("Total connections:", G.number_of_edges())
