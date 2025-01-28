#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>

#define GB ((size_t)1024 * 1024 * 1024) // Size in bytes for 1 GB
#define MAX_ALLOC_SIZE (8 * GB)         // Maximum memory to allocate in bytes
#define NUM_THREADS 4                    // Number of contention threads

// Function to simulate memory exhaustion
void *access_memory_exhaustion(void *arg) {
    size_t allocated = 0;
    char *memory_block;

    // Allocate memory until it fails
    while (allocated < MAX_ALLOC_SIZE) {
        memory_block = (char *)malloc(1 * GB); // Allocate 1 GB
        if (!memory_block) {
            fprintf(stderr, "Memory allocation failed at %zu GB\n", allocated / GB);
            break;  // Break if allocation fails
        }
        allocated += 1 * GB;
        printf("Allocated %zu GB\n", allocated / GB);
        free(memory_block);  // Free memory to avoid leaks
    }
    
    return NULL;
}

// Function to simulate memory contention
void *simulate_memory_contention(void *arg) {
    size_t allocated = 0;
    char *memory_block;

    // Each thread attempts to allocate memory
    while (allocated < MAX_ALLOC_SIZE) {
        memory_block = (char *)malloc(1 * GB); // Allocate 1 GB
        if (!memory_block) {
            fprintf(stderr, "Memory allocation failed by thread %ld at %zu GB\n", (long)arg, allocated / GB);
            break;  // Break if allocation fails
        }
        allocated += 1 * GB;
        printf("Thread %ld allocated %zu GB\n", (long)arg, allocated / GB);
        free(memory_block);  // Free memory after use
    }
    
    return NULL;
}

int main(int argc, char *argv[]) {
    pthread_t threads[NUM_THREADS];

    // Check command line arguments
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <exhaust|contend>\n", argv[0]);
        return EXIT_FAILURE;
    }

    if (strcmp(argv[1], "exhaust") == 0) {
        // Execute the memory exhaustion function
        access_memory_exhaustion(NULL);
    } else if (strcmp(argv[1], "contend") == 0) {
        // Create threads to simulate memory contention
        for (long i = 0; i < NUM_THREADS; i++) {
            pthread_create(&threads[i], NULL, simulate_memory_contention, (void *)i);
        }

        // Wait for all threads to finish
        for (int i = 0; i < NUM_THREADS; i++) {
            pthread_join(threads[i], NULL);
        }
    } else {
        fprintf(stderr, "Invalid argument. Use 'exhaust' or 'contend'.\n");
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}
