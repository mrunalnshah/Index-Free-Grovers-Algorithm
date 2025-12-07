import matplotlib.pyplot as plt
import numpy as np

def ss_hist_visualize(probability):  
    probs = probability
    assert len(probs) == 4
    
    plt.rcParams.update({
        "figure.figsize": (9, 5.6),
        "font.size": 16,
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
        "axes.labelsize": 18,
        "axes.titlesize": 19,
        "xtick.labelsize": 17,
        "ytick.labelsize": 16,
        "axes.linewidth": 1.8,
    })
    
    fig, ax = plt.subplots()
    
    labels = [
        r"$|00\rangle$" + " (19)",
        r"$|01\rangle$" + " (100)",
        r"$|10\rangle$" + " (108)",
        r"$|11\rangle$" + " (33)"
    ]
    colors = ['#404040', '#404040', '#d32f2f', '#404040']
    
    ax.bar(range(4), probs, width=0.7, color=colors, edgecolor='black', linewidth=2.2, zorder=3)
    
    ax.set_ylim(0, 1.06)
    ax.set_ylabel("Probability")
    ax.set_xticks(range(4))
    ax.set_xticklabels(labels)
    ax.tick_params(axis='x', pad=15)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(1.8)
    ax.spines['bottom'].set_linewidth(1.8)
    ax.grid(axis='y', color='gray', linewidth=1.0, linestyle='-', alpha=0.35)
    ax.set_axisbelow(True)
    
    winner = np.argmax(probs)
    ax.text(winner, probs[winner] + 0.04,
            f"{probs[winner]:.16f}",
            ha='center', va='bottom', fontsize=17, fontweight='bold', color='#d32f2f')
    
    for i in range(4):
        if i != winner and probs[i] < 1e-10:
            ax.text(i, 0.04, r"$<10^{-15}$", 
                    ha='center', va='bottom', fontsize=15.5, color='#555555')
    
    plt.tight_layout(pad=1.2)
    
    plt.savefig("figures/small_scale_numerical_search.pdf", dpi=1200, bbox_inches='tight')
    
    plt.show()


def ls_hist_visualize(probability):
    probs = probability
    N = len(probs)
    winner_idx = np.argmax(probs)
    success_prob = probs[winner_idx]
    background_prob = 1.0 / N  # ≈ 0.0009765625
    
    print(f"Target at index: {winner_idx}")
    print(f"Success probability: {success_prob:.10f}")
    
    # === PLOT ===
    plt.rcParams.update({
        "figure.figsize": (13, 6.8),
        "font.size": 19,
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica", "Arial"],
        "axes.labelsize": 22,
        "axes.titlesize": 24,
        "xtick.labelsize": 18,
        "ytick.labelsize": 19,
        "axes.linewidth": 2.4,
    })
    
    fig, ax = plt.subplots()
    
    # Gray bars for all entries
    ax.bar(range(N), probs, width=1.0, color='#e0e0e0', edgecolor='none', alpha=0.9, zorder=1)
    
    # Red bar for target
    ax.bar(winner_idx, success_prob, color='#d32f2f', edgecolor='black', linewidth=3.5,
           label=f"Target (index {winner_idx})", zorder=3)
    
    # 1. TARGET PROBABILITY — printed clearly ABOVE the red bar
    ax.text(winner_idx + 5, success_prob + 0.0005,
            f"{success_prob:.10f}",
            ha='left', va='bottom', fontsize=20, fontweight='bold', color='#d32f2f')
    
    # 2. NON-TARGET LABEL — now clearly lifted up (was too low before)
    ax.text(N * 0.97, background_prob * 2.8,   # ← raised from *0.6 to *4.8
            f"Non-target entries\n≈ {background_prob:.6f}",
            ha='right', va='center', fontsize=20, color='#333333',
            bbox=dict(boxstyle="round,pad=0.7", facecolor="white", edgecolor="#888888", alpha=0.92))
    
    # Dashed line at exact 1/N level
    ax.axhline(background_prob, color='gray', linestyle='--', linewidth=2.5, alpha=0.9)
    
    # Axes
    ax.set_ylim(0, success_prob * 1.4)
    ax.set_xlim(0, N)
    ax.set_xlabel("Database index", labelpad=15)
    ax.set_ylabel("Measurement probability", labelpad=15)
    
    # Clean look
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(2.4)
    ax.spines['bottom'].set_linewidth(2.4)
    ax.grid(axis='y', alpha=0.35, linewidth=1.3)
    
    ax.legend(fontsize=19, loc="upper right", frameon=False)

    plt.tight_layout(pad=2.0)
    
    # Save perfection
    plt.savefig("figures/numeric_large_final.pdf", dpi=1200, bbox_inches='tight')
    plt.show()