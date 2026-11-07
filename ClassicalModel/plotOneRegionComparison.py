
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

# -----------------------------
# Load datasets
# -----------------------------

# Alaska adoption-year data
alaska_df = pd.read_csv("data_with_everything.csv").set_index("Industry")

# USA simulation data
usa_df = pd.read_csv("qaoa_node_states.csv")

# Extract years
years = usa_df["Year"].values

# -----------------------------
# Define four states
# -----------------------------

# 0 = Both Paper
# 1 = Both Digital
# 2 = Alaska Paper, USA Digital
# 3 = Alaska Digital, USA Paper

industries = alaska_df.index.tolist()

combined = np.zeros((len(industries), len(years)), dtype=int)

# -----------------------------
# Compare datasets
# -----------------------------

for i, industry in enumerate(industries):

    alaska_flip = alaska_df.loc[industry, "Alaska"]

    # Find matching USA column
    usa_column = f"('{industry}', 'USA')"

    for j, year in enumerate(years):

        # Alaska state
        alaska_state = 1 if year >= alaska_flip else 0

        # USA state: -1 = Paper, 1 = Digital
        usa_value = usa_df.loc[
            usa_df["Year"] == year, usa_column
        ].iloc[0]

        usa_state = 1 if usa_value == 1 else 0

        # Assign combined state
        if alaska_state == 0 and usa_state == 0:
            combined[i, j] = 0

        elif alaska_state == 1 and usa_state == 1:
            combined[i, j] = 1

        elif alaska_state == 0 and usa_state == 1:
            combined[i, j] = 2

        else:
            combined[i, j] = 3

# -----------------------------
# Plot heatmap
# -----------------------------

colors = [
    "saddlebrown",  # Both Paper
    "royalblue",    # Both Digital
    "gold",         # Alaska Paper, USA Digital
    "mediumseagreen" # Alaska Digital, USA Paper
]

cmap = ListedColormap(colors)

fig, ax = plt.subplots(figsize=(16, 10))

ax.imshow(
    combined,
    aspect="auto",
    cmap=cmap,
    vmin=-0.5,
    vmax=3.5
)

# Axis labels
ax.set_xticks(np.arange(len(years)))
ax.set_xticklabels(years)

ax.set_yticks(np.arange(len(industries)))
ax.set_yticklabels(industries)

ax.set_xlabel("Year")
ax.set_ylabel("Industry")
ax.set_title("Classical vs Quantum Hardware: Paper and Digital Adoption")

# Cell grid
ax.set_xticks(np.arange(-0.5, len(years), 1), minor=True)
ax.set_yticks(np.arange(-0.5, len(industries), 1), minor=True)

ax.grid(which="minor", color="white", linewidth=1)
ax.tick_params(which="minor", bottom=False, left=False)

# Legend
legend_elements = [
    Patch(facecolor=colors[0], label="Both Paper"),
    Patch(facecolor=colors[1], label="Both Digital"),
    Patch(facecolor=colors[2], label="Classical Paper, Quantum Digital"),
    Patch(facecolor=colors[3], label="Classical Digital, Quantum Paper")
]

ax.legend(
    handles=legend_elements,
    loc="upper left",
    bbox_to_anchor=(1.01, 1),
    title="Model Agreement"
)

plt.tight_layout()
plt.show()
