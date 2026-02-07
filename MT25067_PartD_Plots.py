#!/usr/bin/env python3
"""
MT25067
Part D: Plotting and Visualization
Uses HARDCODED experimental data (as per assignment constraints)
Generates PNG plots only.

System Configuration:
- OS: Ubuntu 22.04.5 LTS
- CPU: Intel Core i7-12700 (12th Gen)
- Date: February 6, 2026
"""

import matplotlib.pyplot as plt

# Set publication-quality plot style
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.figsize'] = (12, 9)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['legend.fontsize'] = 10

# System configuration string for plot annotations
SYSTEM_CONFIG = """System: Ubuntu 22.04.5 LTS
CPU: Intel Core i7-12700 (12th Gen)
Kernel: 6.8.0-90-generic
Network: Localhost
Data: Feb 6, 2026"""

# =============================================================================
# HARDCODED EXPERIMENTAL DATA
# Data Source: MT25067_ExperimentData.csv
# =============================================================================
# Structure: data[implementation][message_size][num_threads] = {metrics}
# Note: 'cycles' are stored in Millions (1e6) to match plotting logic

# --- DATA START ---
data = {
    'A1': {
        256: {
            1: {'throughput': 1.35, 'latency': 1.51, 'total_bytes': 1280000, 'cycles': 57.611533, 'cache_misses': 340306, 'l1_misses': 180721},
            2: {'throughput': 1.67, 'latency': 1.23, 'total_bytes': 1280000, 'cycles': 86.368053, 'cache_misses': 69890, 'l1_misses': 192025},
            4: {'throughput': 2.13, 'latency': 0.96, 'total_bytes': 1280000, 'cycles': 147.068045, 'cache_misses': 210172, 'l1_misses': 319146},
            8: {'throughput': 2.43, 'latency': 0.84, 'total_bytes': 1280000, 'cycles': 285.403107, 'cache_misses': 168499, 'l1_misses': 658348},
        },
        1024: {
            1: {'throughput': 2.98, 'latency': 2.75, 'total_bytes': 5120000, 'cycles': 116.827023, 'cache_misses': 85493, 'l1_misses': 307551},
            2: {'throughput': 4.26, 'latency': 1.92, 'total_bytes': 5120000, 'cycles': 153.748252, 'cache_misses': 136064, 'l1_misses': 426639},
            4: {'throughput': 4.37, 'latency': 1.87, 'total_bytes': 5120000, 'cycles': 353.304692, 'cache_misses': 98099, 'l1_misses': 985857},
            8: {'throughput': 3.58, 'latency': 2.29, 'total_bytes': 5120000, 'cycles': 712.122390, 'cache_misses': 188990, 'l1_misses': 2365953},
        },
        4096: {
            1: {'throughput': 10.45, 'latency': 3.13, 'total_bytes': 20480000, 'cycles': 128.215704, 'cache_misses': 80490, 'l1_misses': 523278},
            2: {'throughput': 9.52, 'latency': 3.44, 'total_bytes': 20480000, 'cycles': 273.870669, 'cache_misses': 159785, 'l1_misses': 1100013},
            4: {'throughput': 9.91, 'latency': 3.31, 'total_bytes': 20480000, 'cycles': 525.781881, 'cache_misses': 147943, 'l1_misses': 2110699},
            8: {'throughput': 8.45, 'latency': 3.88, 'total_bytes': 20480000, 'cycles': 1158.825163, 'cache_misses': 318518, 'l1_misses': 6094991},
        },
        16384: {
            1: {'throughput': 30.23, 'latency': 4.34, 'total_bytes': 81920000, 'cycles': 175.746499, 'cache_misses': 199269, 'l1_misses': 2513201},
            2: {'throughput': 33.44, 'latency': 3.92, 'total_bytes': 81920000, 'cycles': 309.458403, 'cache_misses': 781304, 'l1_misses': 4648122},
            4: {'throughput': 33.34, 'latency': 3.93, 'total_bytes': 81920000, 'cycles': 655.119355, 'cache_misses': 286684, 'l1_misses': 9497289},
            8: {'throughput': 31.94, 'latency': 4.10, 'total_bytes': 81920000, 'cycles': 1315.622332, 'cache_misses': 871905, 'l1_misses': 20386406},
        },
    },
    'A2': {
        256: {
            1: {'throughput': 1.31, 'latency': 1.56, 'total_bytes': 1280000, 'cycles': 67.137710, 'cache_misses': 60051, 'l1_misses': 119992},
            2: {'throughput': 1.88, 'latency': 1.09, 'total_bytes': 1280000, 'cycles': 113.789584, 'cache_misses': 62466, 'l1_misses': 237242},
            4: {'throughput': 1.84, 'latency': 1.11, 'total_bytes': 1280000, 'cycles': 178.447407, 'cache_misses': 413252, 'l1_misses': 391251},
            8: {'throughput': 1.81, 'latency': 1.13, 'total_bytes': 1280000, 'cycles': 364.125717, 'cache_misses': 162576, 'l1_misses': 773582},
        },
        1024: {
            1: {'throughput': 3.99, 'latency': 2.05, 'total_bytes': 5120000, 'cycles': 82.736829, 'cache_misses': 367536, 'l1_misses': 237910},
            2: {'throughput': 3.22, 'latency': 2.55, 'total_bytes': 5120000, 'cycles': 183.701345, 'cache_misses': 65821, 'l1_misses': 520070},
            4: {'throughput': 3.96, 'latency': 2.07, 'total_bytes': 5120000, 'cycles': 366.350476, 'cache_misses': 145928, 'l1_misses': 1025830},
            8: {'throughput': 3.08, 'latency': 2.66, 'total_bytes': 5120000, 'cycles': 794.646097, 'cache_misses': 218243, 'l1_misses': 2569589},
        },
        4096: {
            1: {'throughput': 9.65, 'latency': 3.39, 'total_bytes': 20480000, 'cycles': 135.747322, 'cache_misses': 259867, 'l1_misses': 536715},
            2: {'throughput': 8.14, 'latency': 4.03, 'total_bytes': 20480000, 'cycles': 297.524319, 'cache_misses': 154883, 'l1_misses': 1152800},
            4: {'throughput': 8.95, 'latency': 3.66, 'total_bytes': 20480000, 'cycles': 577.519490, 'cache_misses': 161508, 'l1_misses': 2471170},
            8: {'throughput': 7.04, 'latency': 4.65, 'total_bytes': 20480000, 'cycles': 1305.706294, 'cache_misses': 469137, 'l1_misses': 6760988},
        },
        16384: {
            1: {'throughput': 31.85, 'latency': 4.12, 'total_bytes': 81920000, 'cycles': 159.875443, 'cache_misses': 829295, 'l1_misses': 2369198},
            2: {'throughput': 27.83, 'latency': 4.71, 'total_bytes': 81920000, 'cycles': 365.550165, 'cache_misses': 174552, 'l1_misses': 5020981},
            4: {'throughput': 23.26, 'latency': 5.64, 'total_bytes': 81920000, 'cycles': 764.280684, 'cache_misses': 147239, 'l1_misses': 10725239},
            8: {'throughput': 25.35, 'latency': 5.17, 'total_bytes': 81920000, 'cycles': 1682.051140, 'cache_misses': 520076, 'l1_misses': 23141904},
        },
    },
    'A3': {
        256: {
            1: {'throughput': 0.61, 'latency': 3.35, 'total_bytes': 1280000, 'cycles': 275.906484, 'cache_misses': 92969, 'l1_misses': 233140},
            2: {'throughput': 0.72, 'latency': 2.84, 'total_bytes': 1280000, 'cycles': 403.716202, 'cache_misses': 237522, 'l1_misses': 686090},
            4: {'throughput': 0.86, 'latency': 2.38, 'total_bytes': 1280000, 'cycles': 496.320886, 'cache_misses': 127017, 'l1_misses': 1773010},
            8: {'throughput': 0.54, 'latency': 3.77, 'total_bytes': 1280000, 'cycles': 1631.574085, 'cache_misses': 394502, 'l1_misses': 6002859},
        },
        1024: {
            1: {'throughput': 2.38, 'latency': 3.44, 'total_bytes': 5120000, 'cycles': 311.283216, 'cache_misses': 228203, 'l1_misses': 428987},
            2: {'throughput': 2.55, 'latency': 3.21, 'total_bytes': 5120000, 'cycles': 363.551702, 'cache_misses': 163698, 'l1_misses': 1478164},
            4: {'throughput': 2.98, 'latency': 2.75, 'total_bytes': 5120000, 'cycles': 849.382398, 'cache_misses': 168416, 'l1_misses': 2083929},
            8: {'throughput': 2.29, 'latency': 3.58, 'total_bytes': 5120000, 'cycles': 2148.750000, 'cache_misses': 527819, 'l1_misses': 6487124},
        },
        4096: {
            1: {'throughput': 6.00, 'latency': 5.46, 'total_bytes': 20480000, 'cycles': 390.806322, 'cache_misses': 252125, 'l1_misses': 714221},
            2: {'throughput': 6.83, 'latency': 4.80, 'total_bytes': 20480000, 'cycles': 762.318916, 'cache_misses': 1238875, 'l1_misses': 1740911},
            4: {'throughput': 6.75, 'latency': 4.86, 'total_bytes': 20480000, 'cycles': 991.037715, 'cache_misses': 481666, 'l1_misses': 3786128},
            8: {'throughput': 5.25, 'latency': 6.25, 'total_bytes': 20480000, 'cycles': 3078.580000, 'cache_misses': 367014, 'l1_misses': 9439266},
        },
        16384: {
            1: {'throughput': 21.88, 'latency': 5.99, 'total_bytes': 81920000, 'cycles': 281.083876, 'cache_misses': 189835, 'l1_misses': 3223257},
            2: {'throughput': 19.37, 'latency': 6.77, 'total_bytes': 81920000, 'cycles': 719.137500, 'cache_misses': 205013, 'l1_misses': 5605023},
            4: {'throughput': 22.12, 'latency': 5.93, 'total_bytes': 81920000, 'cycles': 1037.526424, 'cache_misses': 648181, 'l1_misses': 12981869},
            8: {'throughput': 16.46, 'latency': 7.96, 'total_bytes': 81920000, 'cycles': 2805.570000, 'cache_misses': 635733, 'l1_misses': 27453971},
        },
    },
}
# --- DATA END ---

# Experimental parameters
MESSAGE_SIZES = [256, 1024, 4096, 16384]
THREAD_COUNTS = [1, 2, 4, 8]
IMPLEMENTATIONS = ['A1', 'A2', 'A3']

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def add_footer(fig):
    """Adds a standard footer with system configuration to the figure."""
    # Reserve space at the bottom (left, bottom, right, top)
    fig.subplots_adjust(bottom=0.15)
    
    # Add text in the reserved space
    fig.text(0.5, 0.04, SYSTEM_CONFIG, 
             ha='center', va='center', fontsize=10, 
             bbox=dict(facecolor='#f0f0f0', edgecolor='gray', boxstyle='round,pad=0.5', alpha=0.8))
    
# =============================================================================
# PLOTTING FUNCTIONS
# =============================================================================

def plot_throughput_vs_message_size():
    """Plot 1: Throughput vs Message Size for different thread counts"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Throughput vs Message Size\n(Different Thread Counts)', 
                 fontsize=16, fontweight='bold')
    
    colors = {'A1': 'blue', 'A2': 'orange', 'A3': 'green'}
    markers = {'A1': 'o', 'A2': 's', 'A3': '^'}
    labels = {'A1': 'A1 (Two-Copy)', 'A2': 'A2 (One-Copy)', 'A3': 'A3 (Zero-Copy)'}
    
    for idx, threads in enumerate(THREAD_COUNTS):
        ax = axes[idx // 2, idx % 2]
        
        for impl in IMPLEMENTATIONS:
            throughputs = [data[impl][size][threads]['throughput'] 
                          for size in MESSAGE_SIZES]
            
            ax.plot(MESSAGE_SIZES, throughputs, 
                   marker=markers[impl], 
                   color=colors[impl],
                   linewidth=2, markersize=8, 
                   label=labels[impl])
            
            # Add value annotations
            for size, thr in zip(MESSAGE_SIZES, throughputs):
                ax.annotate(f'{thr:.1f}', (size, thr),  # Changed to 1 decimal for Gbps
                           textcoords="offset points", xytext=(0,5), 
                           ha='center', fontsize=8)
        
        ax.set_xlabel('Message Size (bytes)', fontweight='bold')
        ax.set_ylabel('Throughput (Gbps)', fontweight='bold') # <--- FIXED HERE
        ax.set_title(f'{threads} Thread(s)', fontweight='bold')
        ax.set_xscale('log', base=2)
        ax.grid(True, alpha=0.3)
        ax.legend()
    
    add_footer(fig)

    plt.tight_layout(rect=[0, 0.08, 1, 0.96])
    plt.savefig('MT25067_Plot1_Throughput_vs_MessageSize.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: MT25067_Plot1_Throughput_vs_MessageSize.png")
    plt.close()

def plot_latency_vs_thread_count():
    """Plot 2: Latency vs Thread Count for different message sizes"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Latency vs Thread Count\n(Different Message Sizes)', 
                 fontsize=16, fontweight='bold')
    
    colors = {'A1': 'blue', 'A2': 'orange', 'A3': 'green'}
    markers = {'A1': 'o', 'A2': 's', 'A3': '^'}
    labels = {'A1': 'A1 (Two-Copy)', 'A2': 'A2 (One-Copy)', 'A3': 'A3 (Zero-Copy)'}
    
    for idx, msg_size in enumerate(MESSAGE_SIZES):
        ax = axes[idx // 2, idx % 2]
        
        for impl in IMPLEMENTATIONS:
            latencies = [data[impl][msg_size][t]['latency'] 
                        for t in THREAD_COUNTS]
            
            ax.plot(THREAD_COUNTS, latencies, 
                   marker=markers[impl],
                   color=colors[impl],
                   linewidth=2, markersize=8, 
                   label=labels[impl])
        
        ax.set_xlabel('Number of Threads', fontweight='bold')
        ax.set_ylabel('Average Latency (µs)', fontweight='bold')
        ax.set_title(f'Message Size: {msg_size} bytes', fontweight='bold')
        ax.set_xticks(THREAD_COUNTS)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
    add_footer(fig)
    plt.tight_layout(rect=[0, 0.08, 1, 0.96])
    plt.savefig('MT25067_Plot2_Latency_vs_ThreadCount.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: MT25067_Plot2_Latency_vs_ThreadCount.png")
    plt.close()

def plot_cache_misses_vs_message_size():
    """Plot 3: Cache Misses (LLC and L1) vs Message Size for 1 thread"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('Cache Misses vs Message Size (1 Thread)', 
                 fontsize=16, fontweight='bold')
    
    colors = {'A1': 'blue', 'A2': 'orange', 'A3': 'green'}
    markers = {'A1': 'o', 'A2': 's', 'A3': '^'}
    labels = {'A1': 'A1 (Two-Copy)', 'A2': 'A2 (One-Copy)', 'A3': 'A3 (Zero-Copy)'}
    threads = 1
    
    # LLC Cache Misses
    for impl in IMPLEMENTATIONS:
        cache_misses = [data[impl][size][threads]['cache_misses'] 
                       for size in MESSAGE_SIZES]
        ax1.plot(MESSAGE_SIZES, cache_misses, 
                marker=markers[impl],
                color=colors[impl],
                linewidth=2, markersize=8, 
                label=labels[impl])
    
    ax1.set_xlabel('Message Size (bytes)', fontweight='bold')
    ax1.set_ylabel('LLC Cache Misses', fontweight='bold')
    ax1.set_title('Last Level Cache Misses', fontweight='bold')
    ax1.set_xscale('log', base=2)
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # L1 Cache Misses
    for impl in IMPLEMENTATIONS:
        l1_misses = [data[impl][size][threads]['l1_misses'] 
                    for size in MESSAGE_SIZES]
        ax2.plot(MESSAGE_SIZES, l1_misses, 
                marker=markers[impl],
                color=colors[impl],
                linewidth=2, markersize=8, 
                label=labels[impl])
    
    ax2.set_xlabel('Message Size (bytes)', fontweight='bold')
    ax2.set_ylabel('L1 D-Cache Misses', fontweight='bold')
    ax2.set_title('L1 Data Cache Misses', fontweight='bold')
    ax2.set_xscale('log', base=2)
    ax2.grid(True, alpha=0.3)
    ax2.legend()

    add_footer(fig)
    plt.tight_layout(rect=[0, 0.08, 1, 0.96])
    plt.savefig('MT25067_Plot3_CacheMisses_vs_MessageSize.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: MT25067_Plot3_CacheMisses_vs_MessageSize.png")
    plt.close()

def plot_cpu_cycles_per_byte():
    """Plot 4: CPU Cycles per Byte Transferred for different thread counts"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('CPU Cycles per Byte Transferred\n(Different Thread Counts)', 
                 fontsize=16, fontweight='bold')
    
    colors = {'A1': 'blue', 'A2': 'orange', 'A3': 'green'}
    markers = {'A1': 'o', 'A2': 's', 'A3': '^'}
    labels = {'A1': 'A1 (Two-Copy)', 'A2': 'A2 (One-Copy)', 'A3': 'A3 (Zero-Copy)'}
    
    for idx, threads in enumerate(THREAD_COUNTS):
        ax = axes[idx // 2, idx % 2]
        
        for impl in IMPLEMENTATIONS:
            cpb = []
            for size in MESSAGE_SIZES:
                d = data[impl][size][threads]
                cycles = d['cycles'] * 1e6  # Convert back to actual cycles
                total_bytes = d['total_bytes']
                cpb.append(cycles / total_bytes if total_bytes > 0 else 0)
            
            ax.plot(MESSAGE_SIZES, cpb, 
                   marker=markers[impl], 
                   color=colors[impl],
                   linewidth=2, markersize=8, 
                   label=labels[impl])
        
        ax.set_xlabel('Message Size (bytes)', fontweight='bold')
        ax.set_ylabel('CPU Cycles per Byte', fontweight='bold')
        ax.set_title(f'{threads} Thread(s)', fontweight='bold')
        ax.set_xscale('log', base=2)
        ax.grid(True, alpha=0.3)
        ax.legend()
    
    add_footer(fig)
    plt.tight_layout(rect=[0, 0.08, 1, 0.96])
    plt.savefig('MT25067_Plot4_CPUCycles_per_Byte.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: MT25067_Plot4_CPUCycles_per_Byte.png")
    plt.close()

def plot_overall_comparison():
    """Plot 5: Overall Comparison for largest message size (16KB)"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    msg_size = 16384
    
    fig.suptitle(f'Comprehensive Comparison - {msg_size}B Messages\nAll Metrics vs Thread Count', 
                 fontsize=16, fontweight='bold')
    
    colors = {'A1': 'blue', 'A2': 'orange', 'A3': 'green'}
    markers = {'A1': 'o', 'A2': 's', 'A3': '^'}
    
    # Throughput
    for impl in IMPLEMENTATIONS:
        vals = [data[impl][msg_size][t]['throughput'] for t in THREAD_COUNTS]
        ax1.plot(THREAD_COUNTS, vals, marker=markers[impl], color=colors[impl],
                linewidth=2, markersize=8, label=impl)
    ax1.set_xlabel('Threads', fontweight='bold')
    ax1.set_ylabel('Throughput (Gbps)', fontweight='bold') # <--- FIXED HERE
    ax1.set_title('Throughput', fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_xticks(THREAD_COUNTS)
    
    # Latency
    for impl in IMPLEMENTATIONS:
        vals = [data[impl][msg_size][t]['latency'] for t in THREAD_COUNTS]
        ax2.plot(THREAD_COUNTS, vals, marker=markers[impl], color=colors[impl],
                linewidth=2, markersize=8, label=impl)
    ax2.set_xlabel('Threads', fontweight='bold')
    ax2.set_ylabel('Latency (µs)', fontweight='bold')
    ax2.set_title('Latency', fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_xticks(THREAD_COUNTS)
    
    # CPU Cycles
    for impl in IMPLEMENTATIONS:
        vals = [data[impl][msg_size][t]['cycles'] for t in THREAD_COUNTS]
        ax3.plot(THREAD_COUNTS, vals, marker=markers[impl], color=colors[impl],
                linewidth=2, markersize=8, label=impl)
    ax3.set_xlabel('Threads', fontweight='bold')
    ax3.set_ylabel('CPU Cycles (Millions)', fontweight='bold')
    ax3.set_title('CPU Cycles', fontweight='bold')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    ax3.set_xticks(THREAD_COUNTS)
    
    # Cache Misses
    for impl in IMPLEMENTATIONS:
        vals = [data[impl][msg_size][t]['cache_misses'] for t in THREAD_COUNTS]
        ax4.plot(THREAD_COUNTS, vals, marker=markers[impl], color=colors[impl],
                linewidth=2, markersize=8, label=impl)
    ax4.set_xlabel('Threads', fontweight='bold')
    ax4.set_ylabel('Cache Misses', fontweight='bold')
    ax4.set_title('LLC Cache Misses', fontweight='bold')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    ax4.set_xticks(THREAD_COUNTS)
    
    add_footer(fig)
    plt.tight_layout(rect=[0, 0.08, 1, 0.96])
    plt.savefig('MT25067_Plot5_Overall_Comparison.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: MT25067_Plot5_Overall_Comparison.png")
    plt.close()

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    print("=" * 70)
    print("MT25067 - Part D: Plotting and Visualization")
    print("=" * 70)
    print(SYSTEM_CONFIG)
    print("\n" + "=" * 70)
    print("Using HARDCODED experimental data (no CSV reading)")
    print("Data extracted from valid experimental run (Millions of cycles)")
    print("=" * 70)
    
    print(f"\nData summary:")
    print(f"  Implementations: {IMPLEMENTATIONS}")
    print(f"  Message sizes: {MESSAGE_SIZES} bytes")
    print(f"  Thread counts: {THREAD_COUNTS}")
    
    print("\nGenerating plots...")
    print()
    
    # Generate all plots
    plot_throughput_vs_message_size()
    plot_latency_vs_thread_count()
    plot_cache_misses_vs_message_size()
    plot_cpu_cycles_per_byte()
    plot_overall_comparison()
    
    print()
    print("=" * 70)
    print("All plots generated successfully!")
    print("=" * 70)

if __name__ == "__main__":
    main()