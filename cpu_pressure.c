#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <time.h>
#include <math.h>

void *cpu_intensive_task(void *arg) {
    int thread_id = *(int*)arg;
    time_t start_time = time(NULL);
    double result = 0.0;

    printf("Thread %d started\n", thread_id);

    // Duration is passed through the argument structure
    int duration = ((int*)arg)[1]; 

    while (time(NULL) - start_time < duration) {
        // Perform intensive floating-point operations
        for (int i = 0; i < 10000000; i++) {
            result += sqrt((double)i) * sin((double)i);
        }
    }

    printf("Thread %d finished\n", thread_id);
    return NULL;
}

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <num_threads> <duration>\n", argv[0]);
        return 1;
    }

    int num_threads = atoi(argv[1]);
    int duration = atoi(argv[2]);

    if (num_threads <= 0 || duration <= 0) {
        fprintf(stderr, "num_threads and duration must be positive integers.\n");
        return 1;
    }

    pthread_t threads[num_threads];
    int thread_args[num_threads][2]; // Array to hold thread id and duration

    printf("Starting CPU pressure test with %d threads for %d seconds...\n", num_threads, duration);

    // Create threads
    for (int i = 0; i < num_threads; i++) {
        thread_args[i][0] = i;      // Thread ID
        thread_args[i][1] = duration; // Duration
        if (pthread_create(&threads[i], NULL, cpu_intensive_task, thread_args[i]) != 0) {
            perror("Failed to create thread");
            return 1;
        }
    }

    // Wait for all threads to complete
    for (int i = 0; i < num_threads; i++) {
        pthread_join(threads[i], NULL);
    }

    printf("CPU pressure test completed.\n");
    return 0;
}

