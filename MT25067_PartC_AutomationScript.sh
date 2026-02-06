#!/bin/bash
# Roll Number: MT25067
# Part C: Automated Experiment Runner - FIXED VERSION
# Runs all combinations of implementations, message sizes, and thread counts
# Collects perf statistics and saves to CSV in main directory
#
# FIXES APPLIED:
# - Increased NUM_MESSAGES from 1000 to 5000 for stable profiling
# - Longer server wait time (5s instead of 2s) for complete data collection
# - Added perf output validation to catch errors early
# - Better synchronization between server and clients
# - Improved error handling and logging

set -e  # Exit on error

# Configuration
MESSAGE_SIZES=(256 1024 4096 16384)
THREAD_COUNTS=(1 2 4 8)
NUM_MESSAGES=5000  # FIXED: Increased for stable profiling (was 1000)
IMPLEMENTATIONS=("A1" "A2" "A3")
PORTS=(8080 8081 8082)  # Corresponding ports for A1, A2, A3

# Output directory for temporary files
TEMP_DIR="experiment_results"
# CSV file in main directory (no subfolders as per assignment requirement)
CSV_FILE="MT25067_ExperimentData.csv"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_debug() {
    echo -e "${BLUE}[DEBUG]${NC} $1"
}

# Function to check if a port is in use
check_port() {
    local port=$1
    # Try using ss (modern replacement for netstat)
    if ss -tuln 2>/dev/null | grep -q ":${port} "; then
        return 0
    fi
    # Fallback to lsof if ss fails
    if lsof -i :$port >/dev/null 2>&1; then
        return 0
    fi
    return 1
}

# Function to wait for port to be ready
wait_for_port() {
    local port=$1
    local max_wait=15  # FIXED: Increased from 10 to 15
    local count=0
    
    while [ $count -lt $max_wait ]; do
        if check_port $port; then
            return 0
        fi
        sleep 0.5
        count=$((count + 1))
    done
    return 1
}

# Function to kill process on port
kill_on_port() {
    local port=$1
    local pid=$(lsof -ti:$port 2>/dev/null || true)
    if [ ! -z "$pid" ]; then
        log_debug "Killing process $pid on port $port"
        kill -9 $pid 2>/dev/null || true
        sleep 1
    fi
}

# FIXED: Function to validate perf output
validate_perf_output() {
    local perf_file=$1
    local exp_name=$2
    
    # Check if file exists and is not empty
    if [ ! -s "$perf_file" ]; then
        log_error "Perf output is empty for $exp_name"
        return 1
    fi
    
    # Check if it has required metrics
    if ! grep -q "cycles" "$perf_file"; then
        log_error "Perf output missing 'cycles' metric for $exp_name"
        return 1
    fi
    
    if ! grep -q "cache-misses" "$perf_file"; then
        log_error "Perf output missing 'cache-misses' metric for $exp_name"
        return 1
    fi
    
    # Check for suspiciously low cache miss counts (< 5 is likely an error)
    local cache_misses=$(grep "cache-misses" "$perf_file" | awk '{print $1}' | tr -d ',' | head -1)
    if [ ! -z "$cache_misses" ] && [ "$cache_misses" -lt 5 ]; then
        log_warn "Suspiciously low cache misses ($cache_misses) for $exp_name - data may be incomplete"
    fi
    
    return 0
}

# Function to parse perf output and extract metrics
# Function to parse perf output and extract metrics
parse_perf_output() {
    local perf_file=$1
    local csv_line=$2
    
    # FIX: Pipe to 'tr -d ,' BEFORE 'awk' to handle large numbers correctly
    
    # Extract cycles
    local cycles=$(grep "cycles" $perf_file | tr -d ',' | awk '{sum += $1} END {print sum}')
    
    # Extract instructions
    local instructions=$(grep "instructions" $perf_file | tr -d ',' | awk '{sum += $1} END {print sum}')
    
    # Extract cache-misses
    local cache_misses=$(grep "cache-misses" $perf_file | tr -d ',' | awk '{sum += $1} END {print sum}')
    
    # Extract L1-dcache-load-misses
    local l1_misses=$(grep "L1-dcache-load-misses" $perf_file | tr -d ',' | awk '{sum += $1} END {print sum}')
    
    # Extract context-switches
    local ctx_switches=$(grep "context-switches" $perf_file | tr -d ',' | awk '{sum += $1} END {print sum}')
    
    # Extract time elapsed (usually has no commas, but order is fine)
    local time_elapsed=$(grep "seconds time elapsed" $perf_file | awk '{print $1}')
    
    # Handle empty values
    cycles=${cycles:-0}
    instructions=${instructions:-0}
    cache_misses=${cache_misses:-0}
    l1_misses=${l1_misses:-0}
    ctx_switches=${ctx_switches:-0}
    time_elapsed=${time_elapsed:-0}
    
    # Append to CSV line
    echo "${csv_line},${cycles},${instructions},${cache_misses},${l1_misses},${ctx_switches},${time_elapsed}"
}

# Function to parse client output for throughput and latency
# Function to parse client output for throughput and latency
parse_client_output() {
    local client_file=$1
    
    # Extract throughput (Mbps) from client output
    local throughput_mbps=$(grep "Throughput:" "$client_file" | awk '{print $2}')
    
    # NEW: Convert Mbps to Gbps (divide by 1000)
    # Using awk for floating point division
    local throughput_gbps=$(echo "$throughput_mbps" | awk '{printf "%.5f", $1/1000}')
    
    # Extract latency (µs)
    local latency=$(grep "Average latency:" "$client_file" | awk '{print $3}')
    
    # Extract total bytes
    local total_bytes=$(grep "Total bytes:" "$client_file" | awk '{print $3}')
    
    # Handle empty values
    throughput_gbps=${throughput_gbps:-0}
    latency=${latency:-0}
    total_bytes=${total_bytes:-0}
    
    echo "${throughput_gbps},${latency},${total_bytes}"
}

# Function to run a single experiment
run_experiment() {
    local impl=$1
    local impl_idx=$2
    local msg_size=$3
    local num_threads=$4
    local port=${PORTS[$impl_idx]}
    
    local exp_name="${impl}_${msg_size}B_${num_threads}T"
    log_info "Running experiment: $exp_name"
    
    # File names (all in temp directory)
    local perf_output="${TEMP_DIR}/perf_${exp_name}.txt"
    local server_output="${TEMP_DIR}/server_${exp_name}.txt"
    local client_output="${TEMP_DIR}/client_${exp_name}.txt"
    
    # Clean up any existing processes on this port
    kill_on_port $port
    
    # FIXED: Additional wait after cleanup
    sleep 1
    
    # Start server with perf
    log_info "Starting server for $exp_name on port $port"
    sudo perf stat -e cycles,instructions,cache-misses,L1-dcache-load-misses,context-switches \
        -o "$perf_output" \
        ./MT25067_Part${impl}_Server $msg_size $NUM_MESSAGES $num_threads \
        > "$server_output" 2>&1 &
    
    local server_pid=$!
    log_debug "Server PID: $server_pid"
    
    # Wait for server to be ready
    if ! wait_for_port $port; then
        log_error "Server failed to start on port $port"
        kill $server_pid 2>/dev/null || true
        return 1
    fi
    
    log_info "Server ready, starting $num_threads client(s)"
    
    # FIXED: Small delay before starting clients
    sleep 0.5
    
    # Start clients
    local client_pids=()
    for ((i=1; i<=$num_threads; i++)); do
        ./MT25067_Part${impl}_Client $msg_size $NUM_MESSAGES \
            > "${TEMP_DIR}/client_${exp_name}_${i}.txt" 2>&1 &
        client_pids+=($!)
    done
    
    log_debug "Started ${#client_pids[@]} clients"
    
    # Wait for all clients to complete
    for pid in "${client_pids[@]}"; do
        wait $pid
    done
    
    log_info "Clients completed, waiting for server to finish..."
    
    # FIXED: Longer wait for server to complete and flush perf data
    sleep 5  # Increased from 2 to 5 seconds
    
    # Wait for server process to finish naturally (if it hasn't already)
    wait $server_pid 2>/dev/null || true
    
    # FIXED: Additional wait for perf to write all data
    sleep 1
    
    # Kill server if somehow still running
    if ps -p $server_pid > /dev/null 2>&1; then
        log_debug "Server still running, killing it"
        kill -9 $server_pid 2>/dev/null || true
    fi
    
    # Additional cleanup
    kill_on_port $port
    
    # FIXED: Validate perf output before parsing
    if ! validate_perf_output "$perf_output" "$exp_name"; then
        log_error "Perf data validation failed for $exp_name - skipping this experiment"
        return 1
    fi
    
    # Parse results from first client (they should all be similar)
    if [ ! -f "${TEMP_DIR}/client_${exp_name}_1.txt" ]; then
        log_error "Client output file not found for $exp_name"
        return 1
    fi
    
    local client_metrics=$(parse_client_output "${TEMP_DIR}/client_${exp_name}_1.txt")
    
    # Build CSV line
    local csv_line="${impl},${msg_size},${num_threads},${client_metrics}"
    
    # Parse perf output and complete CSV line
    local complete_line=$(parse_perf_output "$perf_output" "$csv_line")
    
    # Append to CSV in main directory
    echo "$complete_line" >> "$CSV_FILE"
    
    log_info "✓ Experiment $exp_name completed successfully"
    
    return 0
}

# Main execution
main() {
    echo ""
    log_info "=========================================="
    log_info "MT25067 Automated Experiment Runner"
    log_info "=========================================="
    echo ""
    
    # Create temp directory for intermediate files
    mkdir -p "$TEMP_DIR"
    
    # Check if binaries exist
    log_info "Compiling all implementations..."
    
    # Optional: clean first to ensure a fresh build
    if make clean >/dev/null 2>&1; then
        log_debug "Cleaned previous builds."
    fi

    # Run make all (suppress output unless there's an error)
    if ! make all; then
        log_error "Compilation failed! Check your Makefile."
        exit 1
    fi
    
    log_info "Compilation successful ✓"
        
    # Create CSV header in main directory
    echo "Implementation,MessageSize,NumThreads,Throughput_Gbps,Latency_us,TotalBytes,CPU_Cycles,Instructions,LLC_Misses,L1_Misses,ContextSwitches,TimeElapsed_sec" > "$CSV_FILE"    
    log_info "CSV file: $CSV_FILE (main directory)"
    log_info "Temp directory: $TEMP_DIR"
    echo ""
    
    # Count total experiments
    local total_experiments=$((${#IMPLEMENTATIONS[@]} * ${#MESSAGE_SIZES[@]} * ${#THREAD_COUNTS[@]}))
    local current_experiment=0
    local failed_experiments=0
    
    log_info "Configuration:"
    log_info "  Message sizes: ${MESSAGE_SIZES[*]} bytes"
    log_info "  Thread counts: ${THREAD_COUNTS[*]}"
    log_info "  Messages per client: $NUM_MESSAGES (FIXED: increased for stability)"
    log_info "  Total experiments: $total_experiments"
    echo ""
    
    log_warn "NOTE: This will take approximately $(( (total_experiments * 30) / 60 )) minutes"
    log_warn "Press Ctrl+C within 5 seconds to cancel..."
    sleep 5
    echo ""
    
    # Run all experiments
    for impl_idx in "${!IMPLEMENTATIONS[@]}"; do
        local impl="${IMPLEMENTATIONS[$impl_idx]}"
        
        for msg_size in "${MESSAGE_SIZES[@]}"; do
            for num_threads in "${THREAD_COUNTS[@]}"; do
                current_experiment=$((current_experiment + 1))
                
                echo ""
                log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                log_info "Progress: $current_experiment / $total_experiments"
                log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                
                if ! run_experiment "$impl" "$impl_idx" "$msg_size" "$num_threads"; then
                    log_warn "Experiment failed, continuing..."
                    failed_experiments=$((failed_experiments + 1))
                fi
                
                # Brief pause between experiments
                sleep 2
            done
        done
    done
    
    echo ""
    log_info "=========================================="
    log_info "All experiments completed!"
    log_info "=========================================="
    log_info "Results saved to: $CSV_FILE (main directory)"
    log_info "Successful: $((total_experiments - failed_experiments)) / $total_experiments"
    if [ $failed_experiments -gt 0 ]; then
        log_warn "Failed: $failed_experiments / $total_experiments"
    fi
    echo ""
    
    # Cleanup temp directory and all intermediate files
    log_info "Cleaning up temporary files..."
    rm -rf "$TEMP_DIR"
    log_info "✓ Cleanup complete (removed $TEMP_DIR directory)"
    echo ""
    
    log_info "Summary:"
    wc -l "$CSV_FILE"
    echo ""
    log_info "First few lines of results:"
    head -5 "$CSV_FILE"
    echo ""
    log_info "Last few lines of results:"
    tail -5 "$CSV_FILE"
    echo ""
    
    # FIXED: Data quality check
    log_info "Running data quality checks..."
    echo ""
    
    # Check for suspiciously low cache misses
    local suspicious=$(awk -F, 'NR>1 && $9 < 10 {print}' "$CSV_FILE" | wc -l)
    if [ $suspicious -gt 0 ]; then
        log_warn "Found $suspicious rows with very low cache misses (< 10)"
        log_warn "This may indicate data collection issues"
    else
        log_info "✓ Cache miss values look reasonable"
    fi
    
    # Check for zero values
    local zeros=$(awk -F, 'NR>1 && ($4 == 0 || $7 == 0) {print}' "$CSV_FILE" | wc -l)
    if [ $zeros -gt 0 ]; then
        log_warn "Found $zeros rows with zero values - data may be incomplete"
    else
        log_info "✓ No zero values detected"
    fi
    
    echo ""
    log_info "You can now use this CSV for Part D (plotting)"
    log_info "Run: python3 MT25067_PartD_Plots.py"
    echo ""
}

# Run main function
main