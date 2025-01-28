#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

#define ARRAY_SIZE 10000000
#define BLOCK_SIZE 1024
#define PREFETCH_DISTANCE 64

// Structure with poor locality
typedef struct {
    int value;
    char padding[60]; // Simulates poor locality
} PoorLocality;

// Structure with good locality
typedef struct {
    int value;
} GoodLocality;

// Function to measure execution time
double measure_time(void (*func)(void*, size_t), void* data, size_t size) {
    clock_t start = clock();
    func(data, size);
    clock_t end = clock();
    return ((double)(end - start)) / CLOCKS_PER_SEC;
}

// Poor locality access
void poor_locality_access(void* data, size_t size) {
    PoorLocality* array = (PoorLocality*)data;
    for (size_t i = 0; i < size; i++) {
        array[i].value *= 2;
    }
}

// Good locality access
void good_locality_access(void* data, size_t size) {
    GoodLocality* array = (GoodLocality*)data;
    for (size_t i = 0; i < size; i++) {
        array[i].value *= 2;
    }
}

// Cache-friendly blocked access
void blocked_access(void* data, size_t size) {
    int* array = (int*)data;
    for (size_t i = 0; i < size; i += BLOCK_SIZE) {
        for (size_t j = i; j < i + BLOCK_SIZE && j < size; j++) {
            array[j] *= 2;
        }
    }
}

// Prefetching access
void prefetch_access(void* data, size_t size) {
    int* array = (int*)data;
    for (size_t i = 0; i < size; i++) {
        __builtin_prefetch(&array[i + PREFETCH_DISTANCE], 0, 1);
        array[i] *= 2;
    }
}

int main() {
    // Allocate memory for different data structures
    PoorLocality* poor_array = malloc(ARRAY_SIZE * sizeof(PoorLocality));
    GoodLocality* good_array = malloc(ARRAY_SIZE * sizeof(GoodLocality));
    int* normal_array = malloc(ARRAY_SIZE * sizeof(int));
    int* blocked_array = malloc(ARRAY_SIZE * sizeof(int));
    int* prefetch_array = malloc(ARRAY_SIZE * sizeof(int));

    // Initialize arrays
    for (size_t i = 0; i < ARRAY_SIZE; i++) {
        poor_array[i].value = i;
        good_array[i].value = i;
        normal_array[i] = i;
        blocked_array[i] = i;
        prefetch_array[i] = i;
    }

    // Measure and print execution times
    printf("Poor locality access time: %f seconds\n", 
           measure_time(poor_locality_access, poor_array, ARRAY_SIZE));
    printf("Good locality access time: %f seconds\n", 
           measure_time(good_locality_access, good_array, ARRAY_SIZE));
    printf("Normal access time: %f seconds\n", 
           measure_time(good_locality_access, normal_array, ARRAY_SIZE));
    printf("Blocked access time: %f seconds\n", 
           measure_time(blocked_access, blocked_array, ARRAY_SIZE));
    printf("Prefetch access time: %f seconds\n", 
           measure_time(prefetch_access, prefetch_array, ARRAY_SIZE));

    // Free allocated memory
    free(poor_array);
    free(good_array);
    free(normal_array);
    free(blocked_array);
    free(prefetch_array);

    return 0;
}
