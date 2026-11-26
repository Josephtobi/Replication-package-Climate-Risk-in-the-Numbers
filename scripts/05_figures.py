"""Publication figures for Paper C (svg + 300 dpi png)."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
FIG = ROOT / "outputs" / "figures"
FIG.mkdir(parents=True, exist_ok=True)

# greyscale-safe with one muted accent
ACCENT = "#4C6A7A"
GREYS = ["#f7f7f7", "#d9d9d9", "#969696", "#525252"]


def save(fig, name: str) -> None:
    fig.tight_layout()
    fig.savefig(FIG / f"{name}.svg")
    fig.savefig(FIG / f"{name}.png", dpi=300)
    plt.close(fig)


def main() -> None:
    m = pd.read_csv(TABLES / "table_master_firm_scores.csv", keep_default_na=False)
    p = pd.read_csv(ROOT / "data" / "coded" / "firm_profiles.csv", keep_default_na=False)
    df = m.merge(p[["firm_id", "sr_risks_named_count", "adoption_group"]], on="firm_id", suffixes=("", "_y"))
    if "adoption_group_y" in df.columns:
        df["adoption_group"] = df["adoption_group"].fillna(df["adoption_group_y"])
    df["ci"] = df["connectivity_index"].astype(float)
    df["sr_risks_named_count"] = pd.to_numeric(df["sr_risks_named_count"], errors="coerce").fillna(0)

    inds = ["C1", "C2", "C3", "C4", "C5a", "C5b", "C6", "C7", "A1"]
    # fig1 heatmap
    heat = df.sort_values("ci", ascending=False).set_index("company")[inds]
    mat = heat.apply(pd.to_numeric, errors="coerce").to_numpy()
    fig, ax = plt.subplots(figsize=(10, 7))
    cmap = plt.cm.Greys
    im = ax.imshow(np.nan_to_num(mat, nan=-1), aspect="auto", cmap=cmap, vmin=-1, vmax=3)
    ax.set_xticks(range(len(inds)))
    ax.set_xticklabels(inds, rotation=45, ha="right")
    ax.set_yticks(range(len(heat)))
    ax.set_yticklabels(heat.index)
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            val = mat[i, j]
            label = "–" if np.isnan(val) else str(int(val))
            ax.text(j, i, label, ha="center", va="center", color="black", fontsize=8)
    ax.set_title("Figure 1. Climate connectivity scores by firm and indicator")
    fig.colorbar(im, ax=ax, fraction=0.03, label="Score (– = NA)")
    save(fig, "fig1_indicator_heatmap")

    # fig2 indicator averages
    means = []
    for ind in ["C1", "C2", "C3", "C4", "C5a", "C5b", "C6", "C7"]:
        vals = pd.to_numeric(df[ind], errors="coerce").dropna()
        if len(vals):
            means.append((ind, float(vals.mean()), float(vals.median())))
    means = sorted(means, key=lambda x: x[1])
    fig, ax = plt.subplots(figsize=(8, 5))
    y = np.arange(len(means))
    ax.barh(y, [m[1] for m in means], color=ACCENT, label="Mean")
    ax.scatter([m[2] for m in means], y, color="black", zorder=3, label="Median")
    ax.set_yticks(y)
    ax.set_yticklabels([m[0] for m in means])
    ax.set_xlabel("Score (0–3)")
    ax.set_xlim(0, 3)
    ax.set_title("Figure 2. Average connectivity score by indicator")
    ax.legend(loc="lower right")
    save(fig, "fig2_indicator_averages")

    # fig3 sector dotplot
    sectors = ["Oil and gas", "Banking", "Cement", "Telecoms"]
    fig, ax = plt.subplots(figsize=(8, 5))
    for i, sec in enumerate(sectors):
        sub = df[df["sector"] == sec]
        ax.scatter(sub["ci"], [i] * len(sub), color=ACCENT, s=60, zorder=3)
        if len(sub):
            med = sub["ci"].median()
            ax.plot([med, med], [i - 0.25, i + 0.25], color="black", lw=2)
            for _, r in sub.iterrows():
                ax.text(r["ci"] + 0.8, i + 0.08, r["company"].split()[0], fontsize=7)
    ax.set_yticks(range(len(sectors)))
    ax.set_yticklabels(sectors)
    ax.set_xlabel("Connectivity Index (%)")
    ax.set_xlim(-2, 105)
    ax.set_title("Figure 3. Connectivity Index by sector (line = sector median)")
    save(fig, "fig3_sector_dotplot")

    # fig4 overall ranking
    rank = df.sort_values("ci", ascending=True)
    fig, ax = plt.subplots(figsize=(8, 7))
    colors = {"Oil and gas": "#252525", "Banking": ACCENT, "Cement": "#737373", "Telecoms": "#bdbdbd"}
    ax.scatter(rank["ci"], range(len(rank)), c=[colors[s] for s in rank["sector"]], s=70)
    ax.set_yticks(range(len(rank)))
    ax.set_yticklabels(rank["company"])
    ax.axvline(33, color="grey", ls="--", lw=1)
    ax.axvline(66, color="grey", ls="--", lw=1)
    ax.set_xlabel("Connectivity Index (%)")
    ax.set_title("Figure 4. Overall firm ranking by Connectivity Index")
    save(fig, "fig4_overall_ranking_dotplot")

    # fig5 SR vs FS scatter
    fig, ax = plt.subplots(figsize=(7, 6))
    markers = {"Phase 1": "o", "Voluntary": "s", "Non-adopter": "^"}
    for grp, g in df.groupby("adoption_group"):
        ax.scatter(
            g["sr_risks_named_count"],
            g["ci"],
            marker=markers.get(grp, "o"),
            s=70,
            label=grp,
            color=ACCENT if grp == "Phase 1" else ("#525252" if grp == "Voluntary" else "#bdbdbd"),
        )
        for _, r in g.iterrows():
            ax.text(r["sr_risks_named_count"] + 0.05, r["ci"] + 0.8, r["company"].split()[0], fontsize=7)
    ax.set_xlabel("Climate risks named in the annual report (count)")
    ax.set_ylabel("Connectivity Index (%)")
    ax.set_title("Figure 5. Sustainability-report richness vs financial-statement CI")
    ax.legend()
    save(fig, "fig5_sr_vs_fs_scatter")
    print(f"Wrote figures to {FIG}")


if __name__ == "__main__":
    main()
