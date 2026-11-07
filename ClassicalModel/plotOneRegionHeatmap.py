
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

# Load data
df = pd.read_csv("data_with_everything.csv")

# Keep Alaska adoption years
df = df.set_index("Industry")
flip_years = df["Alaska"]

# Define timeline
years = np.arange(2026, 2041)

# Build matrix: 0 = Paper, 1 = Digital
heatmap_data = pd.DataFrame(
    index=df.index,
    columns=years,
    dtype=int
)

for industry in df.index:
    flip_year = flip_years[industry]

    for year in years:
        heatmap_data.loc[industry, year] = (
            1 if year >= flip_year else 0
        )

# Plot heatmap
cmap = ListedColormap(["saddlebrown", "royalblue"])

fig, ax = plt.subplots(figsize=(16, 10))

ax.imshow(
    heatmap_data.values,
    aspect="auto",
    cmap=cmap,
    vmin=0,
    vmax=1
)

# Axis labels
ax.set_xticks(np.arange(len(years)))
ax.set_xticklabels(years)

ax.set_yticks(np.arange(len(df.index)))
ax.set_yticklabels(df.index)

ax.set_xlabel("Year")
ax.set_ylabel("Industry")
ax.set_title("Alaska: Paper vs Digital Industry Adoption")

# Grid lines
ax.set_xticks(np.arange(-0.5, len(years), 1), minor=True)
ax.set_yticks(np.arange(-0.5, len(df.index), 1), minor=True)
ax.grid(which="minor", color="white", linewidth=1)
ax.tick_params(which="minor", bottom=False, left=False)

# Legend
legend_elements = [
    Patch(facecolor="saddlebrown", label="Paper"),
    Patch(facecolor="royalblue", label="Digital")
]

ax.legend(handles=legend_elements, loc="upper left",
          bbox_to_anchor=(1.01, 1))

plt.tight_layout()
plt.show()
