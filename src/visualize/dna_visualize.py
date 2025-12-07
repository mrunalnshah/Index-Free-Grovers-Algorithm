import matplotlib.pyplot as plt
import numpy as np

def ss_hist_visualize(results):
    # DNA labels for x-axis
    dna_list = list("AGGTCCT") + ['pad']  # padded to 8
    labels = [f"{i}\n{dna_list[i]}" for i in range(8)]
    
    # Colors: red for T, gray for others
    colors = ['#404040' if dna_list[i] != 'T' else '#d32f2f' for i in range(8)]
    
    # Professional style
    plt.rcParams.update({
        "figure.figsize": (9, 5.8),
        "font.size": 15,
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica", "Arial"],
        "axes.labelsize": 18,
        "axes.titlesize": 19,
        "xtick.labelsize": 17,
        "ytick.labelsize": 16,
        "axes.linewidth": 1.5,
    })
    
    fig, ax = plt.subplots()
    
    ax.bar(range(8), list(results.values()), width=0.7, color=colors, edgecolor='black', linewidth=1.8, zorder=3)
    
    ax.set_ylim(0, 0.6)
    ax.set_ylabel("Probability", labelpad=10)
    
    ax.set_xticks(range(8))
    ax.set_xticklabels(labels)
    ax.tick_params(axis='x', pad=12)
    
    # Clean spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(1.5)
    ax.spines['bottom'].set_linewidth(1.5)
    
    # Grid
    ax.grid(axis='y', color='gray', linewidth=0.8, linestyle='-', alpha=0.25)
    ax.set_axisbelow(True)
    
    # Annotate T bars with exact values
    for i in [3, 6]:
        p = results[i]
        ax.text(i, p + 0.02, f"{p}", ha='center', va='bottom', fontsize=17, fontweight='bold', color='#d32f2f')
    
    # Annotate non-T as <10^{-8}
    for i in [0,1,2,4,5,7]:
        ax.text(i, 0.04, r"$<10^{-8}$", ha='center', va='bottom', fontsize=15, color='#555555')
    
    plt.tight_layout(pad=1.0)
    
    # Save to your file name
    plt.savefig("figures/dna_small_probabilities.pdf", dpi=800, bbox_inches='tight', format='pdf')
    plt.savefig("figures/dna_small_probabilities.png", dpi=600, bbox_inches='tight')
    plt.show()

def ls_hist_visualize(results, dna):
    if isinstance(results, dict):
        probs = [results[i] for i in range(len(results))]
    else:
        probs = results
    
    N = len(probs)
    target_nucleotide = 'C'
    dna_sequence = dna 
    
    # Find ALL C positions
    c_positions = [i for i, base in enumerate(dna_sequence) if base == 'C']
    print(f"Found {len(c_positions)} positions with '{target_nucleotide}'")
    
    # === PLOT ===
    plt.rcParams.update({
        "figure.figsize": (14.5, 7.5),
        "font.size": 20,
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica", "Arial"],
        "axes.labelsize": 25,
        "axes.titlesize": 28,
        "xtick.labelsize": 18,
        "ytick.labelsize": 19,
        "axes.linewidth": 3.0,
    })
    
    fig, ax = plt.subplots()
    
    # 1. ALL positions in solid, visible light gray — NO alpha!
    ax.bar(range(N), probs, width=1.0, color='#e0e0e0', edgecolor='#bbbbbb', linewidth=0.3, zorder=1)
    
    # 2. ALL C positions in bold #d32f2f with thick black border
    ax.bar(c_positions, [probs[i] for i in c_positions],
           width=1.0, color='#d32f2f', edgecolor='#d32f2f', zorder=3)
    
    
    # Auto-fit y-axis with perfect headroom
    max_prob = max(probs)
    ax.set_ylim(0, max_prob * 1.42)
    ax.set_xlim(-20, N + 20)
    
    # Labels
    ax.set_xlabel("Position in DNA sequence", labelpad=20, fontsize=26)
    ax.set_ylabel("Measurement probability", labelpad=20, fontsize=26)
    
    # Clean spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(3.0)
    ax.spines['bottom'].set_linewidth(3.0)
    
    # Strong grid
    ax.grid(axis='y', color='gray', linewidth=1.6, alpha=0.6, zorder=0)
    
    plt.tight_layout()
    
    # Save in high quality
    plt.savefig("figures/dna_large_scale.pdf", dpi=1500, bbox_inches='tight')
    plt.show()