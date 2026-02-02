#!/bin/bash
# MT25067
# Part C: Automated Experiment Runner
# Runs all combinations of implementations, message sizes, and thread counts
# Collects perf statistics and saves to CSV

set -e  # Exit on error

# Configuration
MESSAGE_SIZES=(256 1024 4096 16384)
THREAD_COUNTS=(1 2 4 8)
NUM_MESSAGES=1000  # Reduced for faster testing, increase for production
IMPLEMENTATIONS=("A1" "A2" "A3")
PORTS=(8080 8081 8082)  # Corresponding ports for A1, A2, A3

# Output directory
OUTPUT_DIR="experiment_results"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
CSV_FILE="${OUTPUT_DIR}/MT25067_AllResults_${TIMESTAMP}.csv"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
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

# Function to check if a port is in use
check_port() {
    local port=$1
    if netstat -tuln 2>/dev/null | grep -q ":${port} "; then
        return 0  # Port in use
    else
        return 1  # Port free
    fi
}

# Function to wait for port to be ready
wait_for_port() {
    local port=$1
    local max_wait=10
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
        log_info "Killing process $pid on port $port"
        kill -9 $pid 2>/dev/null || true
        sleep 1
    fi
}

# Function to parse perf output and extract metrics
parse_perf_output() {
    local perf_file=$1
    local csv_line=$2
    
    # Extract cycles (sum of atom and core)
    local cycles=$(grep "cycles" $perf_file | awk '{sum += $1} END {print sum}' | tr -d ',')
    
    # Extract instructions
    local instructions=$(grep "instructions" $perf_file | awk '{sum += $1} END {print sum}' | tr -d ',')
    
    # Extract cache-misses
    local cache_misses=$(grep "cache-misses" $perf_file | awk '{sum += $1} END {print sum}' | tr -d ',')
    
    # Extract L1-dcache-load-misses
    local l1_misses=$(grep "L1-dcache-load-misses" $perf_file | awk '{sum += $1} END {print sum}' | tr -d ',')
    
    # Extract context-switches
    local ctx_switches=$(grep "context-switches" $perf_file | awk '{sum += $1} END {print sum}' | tr -d ',')
    
    # Extract time elapsed
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
parse_client_output() {
    local client_file=$1
    
    # Extract throughput (Mbps)
    local throughput=$(grep "Throughput:" $client_file | awk '{print $2}')
    
    # Extract latency (µs)
    local latency=$(grep "Average latency:" $client_file | awk '{print $3}')
    
    # Extract total bytes
    local total_bytes=$(grep "Total bytes:" $client_file | awk '{print $3}')
    
    # Handle empty values
    throughput=${throughput:-0}
    latency=${latency:-0}
    total_bytes=${total_bytes:-0}
    
    echo "${throughput},${latency},${total_bytes}"
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
    
    # File names
    local perf_output="${OUTPUT_DIR}/perf_${exp_name}.txt"
    local server_output="${OUTPUT_DIR}/server_${exp_name}.txt"
    local client_output="${OUTPUT_DIR}/client_${exp_name}.txt"
    
    # Clean up any existing processes on this port
    kill_on_port $port
    
    # Start server with perf
    log_info "Starting server for $exp_name on port $port"
    sudo perf stat -e cycles,instructions,cache-misses,L1-dcache-load-misses,context-switches \
        -o "$perf_output" \
        ./MT25067_Part${impl}_Server $msg_size $NUM_MESSAGES $num_threads \
        > "$server_output" 2>&1 &
    
    local server_pid=$!
    
    # Wait for server to be ready
    if ! wait_for_port $port; then
        log_error "Server failed to start on port $port"
        kill $server_pid 2>/dev/null || true
        return 1
    fi
    
    log_info "Server ready, starting $num_threads client(s)"
    
    # Start clients
    local client_pids=()
    for ((i=1; i<=$num_threads; i++)); do
        ./MT25067_Part${impl}_Client $msg_size $NUM_MESSAGES \
            > "${OUTPUT_DIR}/client_${exp_name}_${i}.txt" 2>&1 &
        client_pids+=($!)
    done
    
    # Wait for all clients to complete
    for pid in "${client_pids[@]}"; do
        wait $pid
    done
    
    log_info "Clients completed, waiting for server to finish"
    
    # Give server time to complete
    sleep 2
    
    # Kill server if still running
    kill $server_pid 2>/dev/null || true
    wait $server_pid 2>/dev/null || true
    
    # Additional cleanup
    kill_on_port $port
    
    # Parse results from first client (they should all be similar)
    local client_metrics=$(parse_client_output "${OUTPUT_DIR}/client_${exp_name}_1.txt")
    
    # Build CSV line
    local csv_line="${impl},${msg_size},${num_threads},${client_metrics}"
    
    # Parse perf output and complete CSV line
    local complete_line=$(parse_perf_output "$perf_output" "$csv_line")
    
    # Append to CSV
    echo "$complete_line" >> "$CSV_FILE"
    
    log_info "Experiment $exp_name completed successfully"
    
    # Clean up individual client files to save space
    rm -f ${OUTPUT_DIR}/client_${exp_name}_*.txt
    
    return 0
}

# Main execution
main() {
    log_info "=== MT25067 Automated Experiment Runner ==="
    log_info "Timestamp: $TIMESTAMP"
    
    # Create output directory
    mkdir -p "$OUTPUT_DIR"
    
    # Check if binaries exist
    for impl in "${IMPLEMENTATIONS[@]}"; do
        if [ ! -f "./MT25067_Part${impl}_Server" ] || [ ! -f "./MT25067_Part${impl}_Client" ]; then
            log_error "Binaries for Part ${impl} not found. Please run 'make all' first."
            exit 1
        fi
    done
    
    # Create CSV header
    echo "Implementation,MessageSize,NumThreads,Throughput_Mbps,Latency_us,TotalBytes,CPU_Cycles,Instructions,CacheMisses,L1_Misses,ContextSwitches,TimeElapsed_sec" > "$CSV_FILE"
    
    log_info "CSV file: $CSV_FILE"
    log_info "Output directory: $OUTPUT_DIR"
    
    # Count total experiments
    local total_experiments=$((${#IMPLEMENTATIONS[@]} * ${#MESSAGE_SIZES[@]} * ${#THREAD_COUNTS[@]}))
    local current_experiment=0
    
    log_info "Total experiments to run: $total_experiments"
    log_info "Configuration:"
    log_info "  Message sizes: ${MESSAGE_SIZES[*]}"
    log_info "  Thread counts: ${THREAD_COUNTS[*]}"
    log_info "  Messages per client: $NUM_MESSAGES"
    echo ""
    
    # Run all experiments
    for impl_idx in "${!IMPLEMENTATIONS[@]}"; do
        local impl="${IMPLEMENTATIONS[$impl_idx]}"
        
        for msg_size in "${MESSAGE_SIZES[@]}"; do
            for num_threads in "${THREAD_COUNTS[@]}"; do
                current_experiment=$((current_experiment + 1))
                
                log_info "Progress: $current_experiment / $total_experiments"
                
                if ! run_experiment "$impl" "$impl_idx" "$msg_size" "$num_threads"; then
                    log_warn "Experiment failed, continuing..."
                fi
                
                # Brief pause between experiments
                sleep 2
                
                echo ""
            done
        done
    done
    
    log_info "=== All experiments completed! ==="
    log_info "Results saved to: $CSV_FILE"
    log_info ""
    log_info "Summary:"
    wc -l "$CSV_FILE"
    echo ""
    log_info "First few lines of results:"
    head -5 "$CSV_FILE"
    echo ""
    log_info "You can now use this CSV for Part D (plotting)"
}

# Run main function
main
