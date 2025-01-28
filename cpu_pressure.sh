#!/bin/bash
#SBATCH --job-name=cpu_pressure        # Job name
#SBATCH --output=%x-%j.out             # Standard output and error log
#SBATCH --error=%x-%j.err              # Error log
#SBATCH --ntasks=1                     # Number of tasks (processes)
#SBATCH --cpus-per-task=36             # Number of CPU cores per task
#SBATCH --mem=1G                       # Job memory request
#SBATCH --time=00:15:00                # Time limit hrs:min:sec
#SBATCH --partition=debug              # Partition name
#SBATCH --account=rc-help              # Research Account

# Load the required modules
spack load --first gcc                 # Load GCC module
spack load llvm-openmp

# Define the number of threads and program duration
NUM_THREADS=72
DURATION=300
# Define the source code file
SOURCE_FILE="cpu_pressure.c"           # C source file name
OUTPUT_FILE="cpu_pressure"             # Compiled output file name

# Compile the C program
gcc -o $OUTPUT_FILE $SOURCE_FILE -lpthread -lm  # Compile with GCC

# Check if compilation succeeded
if [ $? -eq 0 ]; then
    echo "Compilation successful, running the program..."
    # Run the compiled program
    ./$OUTPUT_FILE $NUM_THREADS $DURATION 
else
    echo "Compilation failed!" >&2          # Redirect error message to stderr
fi
