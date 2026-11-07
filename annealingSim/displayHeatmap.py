import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==========================
# SETTINGS
# ==========================

FILE_1 = "data_with_everything.csv"
FILE_2 = "data_without_regional_ties.csv"

# True: Dataset 1 - Dataset 2
# False: Dataset 2 - Dataset 1
SUBTRACT_ORDER = True

START_YEAR = 2026
END_YEAR = 2040

# ==========================
# LOAD DATA
# ==========================

df1 = pd.read_csv(FILE_1, index_col="Industry")
df2 = pd.read_csv(FILE_2, index_col="Industry")

# Ensure both datasets have matching rows and columns
df1, df2 = df1.align(df2, join="outer", axis=None)

# Convert to numerical matrices
matrix1 = df1.to_numpy(dtype=float)
matrix2 = df2.to_numpy(dtype=float)

industry_names = df1.index.tolist()
region_names = df1.columns.tolist()

# ==========================
# SUBTRACT DATASETS
# ==========================

if SUBTRACT_ORDER:
   matrix = matrix1 - matrix2
   title = "Difference in Regional Flip Years (Dataset 1 - Dataset 2)"
 
else:
    matrix = matrix2 - matrix1
    title = "Difference in Regional Flip Years (Dataset 2 - Dataset 1)"
   

# ==========================
# PLOT
# ==========================

fig, ax = plt.subplots(figsize=(15, 10))

cmap = plt.cm.coolwarm.copy()
cmap.set_bad("lightgray")

im = ax.imshow(
    np.ma.masked_invalid(matrix),
    aspect="auto",
    cmap=cmap,
    vmin=-2,
    vmax=2
    
)

ax.set_xticks(range(len(region_names)))
ax.set_xticklabels(
    region_names,
    rotation=45,
    ha="right"
)

ax.set_yticks(range(len(industry_names)))
ax.set_yticklabels(industry_names)

ax.set_title(title)

cbar = plt.colorbar(im, ax=ax)
cbar.set_label("Difference in Flip Year (years)")

# Mark industries that never flip in either dataset
for i in range(len(industry_names)):
    for j in range(len(region_names)):
        if np.isnan(matrix[i, j]):
            ax.text(
                j, i, "Never",
                ha="center",
                va="center",
                fontsize=7
            )

plt.tight_layout()
plt.show()