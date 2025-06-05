# Automated-DSE-5SIA0
Automation of a design space exploration assignment for the course embedded computer architecture.

## Step 0

This script automates the generation and execution of a wide range of microarchitectural simulations using the gem5 simulator. It systematically explores the design space of processor configurations by varying parameters such as:

CPU Core Type (e.g., ARM Cortex-A15, Cortex-A7)

Clock Frequency

L1 Instruction/Data Cache (size, associativity, performance type)

L2 Cache (enable/disable, prefetch, size, associativity, performance type)

🔧 What It Does:
Iterates over combinations of cache configurations and processor attributes.

Automatically updates a gem5 configuration file for each setup.

Runs the simulation (make simulate) for each configuration.

Saves the resulting performance statistics (from stats.txt) into the results/ directory using a descriptive filename.

Skips simulations for configurations that have already been completed.


## Step 1

This script processes the raw simulation output files generated in step_0_get_simulations.py. It extracts key performance and power metrics from the stats.txt files and compiles them into a structured CSV summary (summary_with_power.csv) for further analysis.

📊 What It Does:
Parses simulation result files from the results/ directory.

Infers configuration parameters (e.g., cache size/type, CPU core, frequency) from the filename.

Extracts performance metrics:

Simulation time

Energy usage

Cache miss/hit rates (L1I, L1D, L2)

Extracts detailed power metrics from memory controllers, CPU cores, and caches.

Writes a single CSV summary, with one row per simulation, capturing all relevant metrics and configuration parameters.

🧠 Why It's Useful:
This script consolidates a large number of simulations into a single, easy-to-analyze dataset—essential for:

Visualizing trends

Comparing cache designs or power strategies

Identifying performance bottlenecks

Informing architectural decisions

📥 Output:
A file named:

bash
Copy
Edit
results/summary_with_power.csv
containing columns such as:

freq, core, L1D_size, L2_type

sim_seconds, total_energy

Cache statistics (miss_rate, hits, misses)

Power breakdown for components (static/dynamic power)

## Step 2

This script executes a targeted second round of simulations with manually defined configurations to validate and further investigate results from the first design space exploration phase. It focuses on refined L1 and L2 cache configurations and collects detailed power and performance metrics.

🔁 What It Does:
Defines a list of custom Configuration objects with specific architectural parameters (L1D, L1I, L2).

For each configuration:

Replaces the gem5 simulation configuration.

Runs a new simulation.

Parses the output stats.txt to extract performance and power data.

Writes the results into a new summary CSV file for further evaluation.

💡 Why This Step?
While the first round explored broad variations, this step:

Zooms in on promising designs or specific parameter combinations.

Tests configurations with larger L1 cache sizes and varying associativity levels.

Compares low-power vs high-performance modes.

This allows for fine-grained optimization and comparison against previous results.

🧪 Output:
Runs simulations only for configurations not yet completed.

Stores results in:

bash
Copy
Edit
results/summary_with_power.csv
in the same format as previous scripts, enabling easy merging and comparison.

## Step 3

This script serves as the final execution and optimization test in the simulation workflow. It runs a selected or final configuration—presumably one identified as optimal from prior exploration—and collects detailed performance and power data from that simulation.

🚀 What It Does:
Runs a single simulation based on the current gem5 configuration.

Launches a secondary visualization tool (ristretto) to view the output (e.g., lincoln_out.bmp).

Uses the previously defined save_stats function to parse the simulation output.

Saves all extracted metrics to a simplified CSV file (summary_with_power.csv) focused on:

Performance (sim_seconds, total_energy, benchmark score)

Cache statistics (hits/misses/miss rates for L1 and L2)

Power breakdown across system components

🎯 Why It's Important:
This script acts as the final step in the optimization loop, confirming or validating configurations with promising tradeoffs between performance and power efficiency. It is especially useful for:

Re-running optimal configurations in isolation

Integrating with visualization tools

Summarizing power/performance tradeoffs post-optimization

🧪 Output:
The final simulation data is stored in:

bash
Copy
Edit
results/summary_with_power.csv
with one row of highly detailed metrics, suitable for reporting or presentation.

## Step 4

This script evaluates system performance and power consumption across eleven different image inputs. It uses a fixed set of hardware configurations and aggregates results across all image simulations to analyze cumulative workload behavior.

🧠 What It Does:
Defines a set of representative CPU/cache configurations.

For each configuration:

Loads and applies the setup.

Runs a simulation on the first image (im1/stats.txt).

Accumulates results by parsing and summing output from im2 to im14.

Aggregates total performance and power consumption across the entire image set.

Outputs the combined statistics in a single summarized CSV file.

📷 Why It’s Important:
Unlike earlier steps which evaluate configuration impact using one workload, this script:

Measures generalizability and stability of architectural choices across multiple real-world inputs.

Helps assess total cost (energy, latency, power) for processing a complete dataset (11 images), not just isolated scenarios.

Enables cross-input optimization rather than overfitting to a single simulation.

🧪 Output:
Results are saved in:

bash
Copy
Edit
results/summary_with_power.csv
with one row per configuration, reflecting accumulated metrics over 11 simulations:

Total energy consumption

Cache miss rates (L1D, L1I, L2)

Dynamic/static power use

Execution time and derived "benchmark" metric



## Step 5

General improvements: 
### Bitmask Optimization
I’ve defined bitmask constants (TL, TC, TR, etc.) and combined them to create spatial masks (TOP_ROW, LEFT_COLUMN, etc.). This improves readability and modularity. Instead of writing the same neighbor-checking logic 8 times per edge case, I pass the appropriate bitmask and reuse sub_mark_band.

### Efficient Border Handling
The sub_mark_band function uses bitmask checks to handle borders differently from center pixels, reducing the need for complex nested conditions. Edge pixels now get just enough checking without risking out-of-bounds access, with precise control over which neighbors are considered.

### Efficient Inner Pixel Checking
full_sub_mark_band uses arithmetic to flatten memory lookups into a single linear index, and it avoids unnecessary boundary checks by being called only on safe pixel regions (1 <= x < w-1, etc.).
