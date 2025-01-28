#!/bin/bash
#SBATCH --comment="Memory Contention"  # Memory Contention or Memory Exhaustion
#SBATCH --job-name=mem_pressure        # Job name
#SBATCH --output=%x-%j.out             # Standard output and error log
#SBATCH --error=%x-%j.err              # Error log
#SBATCH --ntasks=1                     # Number of tasks (processes)
#SBATCH --cpus-per-task=1              # For contention use 8 CPU cores per task for exhaustion use 1
#SBATCH --mem=10G                      # For contention use 40G and for exhaustion use 1G
#SBATCH --time=00:30:00                # Time limit hrs:min:sec
#SBATCH --partition=debug              # Partition name
#SBATCH --account=rc-help              # Research Account

# Load the required modules
spack load --first gcc                 # Load GCC module
spack load llvm-openmp
spack load --first valgrind

# Define the source code file
SOURCE_FILE="mem_pressure.c"           # C source file name
OUTPUT_FILE="mem_pressure"             # Compiled output file name

# Compile the C program
gcc -Wall -Wextra -o $OUTPUT_FILE $SOURCE_FILE -pthread       # Compile with GCC

# Check if compilation succeeded
if [ $? -eq 0 ]; then
    echo "Compilation successful, running the program..."
    # Run the program with Valgrind to check for memory issues
    srun valgrind --tool=memcheck --leak-check=full --track-origins=yes ./$OUTPUT_FILE contend
else
    echo "Compilation failed!" >&2                            # Redirect error to stderr
fi
