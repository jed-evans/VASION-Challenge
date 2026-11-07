import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==========================
# SETTINGS
# ==========================

FILENAME = "data_without_regional_ties.csv"
#FILENAME = "data_with_everything.csv"

START_YEAR = 2026
END_YEAR = 2040

# ==========================
# LOAD DATA
# ==========================

df = pd.read_csv(FILENAME, index_col="Industry")

# Convert dataframe to a numerical matrix (blank cells become NaNs automatically)
matrix = df.to_numpy(dtype=float)

industry_names = df.index.tolist()
region_names = df.columns.tolist()

# ==========================
# PLOT
# ==========================

fig, ax = plt.subplots(figsize=(15, 10))

# Restored the original coolwarm colormap and lightgray for missing/Never values
cmap = plt.cm.coolwarm.copy()
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

ax.set_title("AI Adoption Year by Industry and Region (2026–2040)")

cbar = plt.colorbar(im, ax=ax)
cbar.set_label("Adoption Year")

# ==========================
# ADD TEXT VALUES TO BOXES
# ==========================
for i in range(len(industry_names)):
    for j in range(len(region_names)):
        val = matrix[i, j]
        if np.isnan(val):
            text_label = "Never"
            text_color = "black"
        else:
            # Format as a clean integer year (e.g., 2029)
            text_label = f"{int(val)}"
            
            # Dynamic text coloring based on the coolwarm colormap spectrum
            # (coolwarm is darker at the extreme ends, lighter in the middle)
            text_color = "white" if (val < 2028 or val > 2038) else "black"

        ax.text(
            j, i, text_label,
            ha="center",
            va="center",
            fontsize=7,
            color=text_color
        )

plt.tight_layout()
plt.show()