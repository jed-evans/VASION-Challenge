
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# 1. GLOBAL PARAMETERS
# ============================================================

START_YEAR = 2026
END_YEAR = 2040

A_START = 0.0
A_GROWTH = 0.07

TIE_SCALE = 0.15
REGIONAL_TIE = 0.05

NOISE_AMPLITUDE = 0.02
RANDOM_SEED = 42

rng = np.random.default_rng(RANDOM_SEED)


# ============================================================
# 2. INDUSTRY RESISTANCE
# ============================================================

base_resistance = {
    "Technology": 0.10,
    "Media": 0.20,
    "Telecom": 0.25,
    "Retail": 0.30,
    "Hospitality": 0.35,
    "Logistics": 0.40,
    "Banking": 0.45,
    "Accounting": 0.50,
    "Manufacturing": 0.50,
    "Insurance": 0.55,
    "Energy": 0.55,
    "Pharma": 0.60,
    "Education": 0.60,
    "Nonprofit": 0.65,
    "Real Estate": 0.65,
    "Construction": 0.70,
    "Agriculture": 0.70,
    "Healthcare": 0.75,
    "Government": 0.85,
    "Legal": 0.90,
}


# ============================================================
# 3. REGIONS AND REGIONAL RESISTANCE SHIFTS
# ============================================================

regions = {
    "Pacific Northwest": -0.049,
    "California": -0.060,
    "Mountain West": 0.076,
    "Southwest": -0.012,
    "Texas": 0.072,
    "Great Plains": 0.077,
    "Midwest": 0.027,
    "Great Lakes": 0.011,
    "Lower South": 0.083,
    "Upper South": 0.027,
    "Mid-Atlantic": -0.048,
    "Northeast": -0.046,
    "Alaska": 0
}

# regions = {
#     "Pacific Northwest": 0,
#     "California": 0,
#     "Mountain West": 0,
#     "Southwest": 0,
#     "Texas": 0,
#     "Great Plains": 0,
#     "Midwest": 0,
#     "Great Lakes": 0,
#     "Lower South": 0,
#     "Upper South": 0,
#     "Mid-Atlantic": 0,
#     "Northeast": 0,
#     "Alaska": 0
# }

# ============================================================
# 4. CREATE INDUSTRY-REGION NODES
# ============================================================

nodes = [
    (industry, region)
    for region in regions
    for industry in base_resistance
]


# Each node receives its own resistance value

resistance = {}

for industry, region in nodes:

    base = base_resistance[industry]
    regional_shift = regions[region]

    noise = rng.uniform(
        -NOISE_AMPLITUDE,
        NOISE_AMPLITUDE
    )

    resistance[(industry, region)] = np.clip(
        base + (2*regional_shift) + noise,
        0.0,
        1.0
    )


# ============================================================
# 5. INDUSTRY PARTNER TIES
# ============================================================

raw_ties = [
    ("Healthcare", "Insurance", 1.0),
    ("Manufacturing", "Logistics", 0.9),
    ("Banking", "Real Estate", 0.8),
    ("Retail", "Logistics", 0.8),
    ("Construction", "Real Estate", 0.8),
    ("Healthcare", "Pharma", 0.7),
    ("Legal", "Real Estate", 0.7),
    ("Healthcare", "Government", 0.6),
    ("Legal", "Government", 0.6),
    ("Accounting", "Banking", 0.6),
    ("Government", "Education", 0.6),
    ("Agriculture", "Logistics", 0.6),
    ("Telecom", "Technology", 0.6),
    ("Insurance", "Banking", 0.5),
    ("Legal", "Banking", 0.5),
    ("Energy", "Manufacturing", 0.5),
    ("Technology", "Media", 0.5),
    ("Insurance", "Legal", 0.4),
    ("Accounting", "Nonprofit", 0.4),
    ("Construction", "Government", 0.4),
    ("Hospitality", "Retail", 0.4),
    ("Pharma", "Logistics", 0.4),
    ("Nonprofit", "Education", 0.4),
    ("Media", "Retail", 0.3),
]


# Scale partner ties

partner_ties = [
    (i, j, strength * TIE_SCALE)
    for i, j, strength in raw_ties
]


# ============================================================
# 6. GEOGRAPHICALLY NEIGHBORING REGIONS
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
# 7. BUILD THE FULL NETWORK
# ============================================================

G = nx.DiGraph()

SOURCE = "__SOURCE__"
SINK = "__SINK__"

G.add_nodes_from(nodes)

# Within-region industry relationships

for region in regions:

    for industry1, industry2, J in partner_ties:

        node1 = (industry1, region)
        node2 = (industry2, region)

        G.add_edge(node1, node2, tie=J)
        G.add_edge(node2, node1, tie=J)


# Between-region relationships
# Same industry in neighboring regions

for region1, region2 in regional_connections:

    for industry in base_resistance:

        node1 = (industry, region1)
        node2 = (industry, region2)

        G.add_edge(
            node1, node2,
            tie=REGIONAL_TIE
        )

        G.add_edge(
            node2, node1,
            tie=REGIONAL_TIE
        )


# ============================================================
# 8. MINIMUM CUT SOLVER
# ============================================================

def solve_year(A):

    H = nx.DiGraph()

    H.add_nodes_from(G.nodes)

    # Add unary resistance / AI pressure costs

    for node in nodes:

        h = A - resistance[node]

        cost_paper = max(h, 0)
        cost_digital = max(-h, 0)

        H.add_edge(
            SOURCE,
            node,
            capacity=cost_paper
        )

        H.add_edge(
            node,
            SINK,
            capacity=cost_digital
        )

    # Add all network coupling strengths

    for node1, node2 in G.edges:

        H.add_edge(
            node1,
            node2,
            capacity=G[node1][node2]["tie"]
        )

    # Find global minimum energy

    cut_value, partition = nx.minimum_cut(
        H,
        SOURCE,
        SINK
    )

    source_side, sink_side = partition

    states = {}

    for node in nodes:

        if node in source_side:
            states[node] = 1

        else:
            states[node] = -1

    return states, cut_value


# ============================================================
# 9. SIMULATE 2026-2040
# ============================================================

results = {}
cut_values = {}

for year in range(START_YEAR, END_YEAR + 1):

    A = A_START + A_GROWTH * (year - START_YEAR)

    states, cut = solve_year(A)

    results[year] = states
    cut_values[year] = cut


# ============================================================
# 10. EXTRACT FLIP YEARS
# ============================================================

flip_years = {}

for node in nodes:

    flip_years[node] = None

    for year in range(START_YEAR, END_YEAR + 1):

        if results[year][node] == 1:

            flip_years[node] = year
            break


# ============================================================
# 11. PRINT RESULTS BY REGION
# ============================================================

for region in regions:

    print("\n" + "=" * 55)
    print(region.upper())
    print("=" * 55)

    for industry in base_resistance:

        node = (industry, region)

        year = flip_years[node]

        year_text = str(year) if year else "Never"

        print(
            f"{industry:20s} "
            f"R={resistance[node]:.3f} "
            f"Flip={year_text}"
        )


# ============================================================
# 12. NETWORK SUMMARY
# ============================================================

print("\nNETWORK SUMMARY")
print("-" * 40)

print("Regions:", len(regions))
print("Industries per region:", len(base_resistance))
print("Total nodes:", len(nodes))
print("Within-region partner ties:",
      len(partner_ties) * len(regions))

print("Regional connections:",
      len(regional_connections))

print("Between-region industry ties:",
      len(regional_connections) * len(base_resistance))

print("Total unique relationships:",
      G.number_of_edges() // 2)


# Create flip-year matrix

industry_names = list(base_resistance.keys())
region_names = list(regions.keys())

matrix = np.full(
    (len(industry_names), len(region_names)),
    np.nan
)

for i, industry in enumerate(industry_names):

    for j, region in enumerate(region_names):

        year = flip_years[(industry, region)]

        if year is not None:
            matrix[i, j] = year


# Plot

fig, ax = plt.subplots(figsize=(15, 10))

cmap = plt.cm.viridis.copy()
cmap.set_bad("lightgray")

im = ax.imshow(
    np.ma.masked_invalid(matrix),
    aspect="auto",
    cmap=cmap,
    vmin=START_YEAR,
    vmax=END_YEAR
)

ax.set_xticks(range(len(region_names)))
ax.set_xticklabels(
    region_names,
    rotation=45,
    ha="right"
)

ax.set_yticks(range(len(industry_names)))
ax.set_yticklabels(industry_names)

ax.set_title("Industry Digital Adoption: Regional Flip Years")

cbar = plt.colorbar(im, ax=ax)
cbar.set_label("Flip Year")

# Mark industries that never flip
for i in range(len(industry_names)):
    for j in range(len(region_names)):
        if np.isnan(matrix[i, j]):
            ax.text(
                j, i, "Never",
                ha="center",
                va="center",
                fontsize=7
            )

# Save optimization results to a CSV file
import pandas as pd

df = pd.DataFrame(
    matrix,
    index=industry_names,
    columns=region_names
)

df.index.name = "Industry"

df.to_csv("regional_flip_years.csv")

print("Results saved to regional_flip_years.csv")

plt.tight_layout()
plt.show()