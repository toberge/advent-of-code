#include <stdio.h>
#include <string.h>

int main() {
    long counts[16] = { 0 };
    char line[100];
    int len = -1;
    long total = 0;
    while (fscanf(stdin, "%s\n", line) != -1) {
        if (len == -1) len = strlen(line);
        // Part 1 thing for most common stuff
        for (int i = 0; i < len; i++) {
            counts[i] += line[i] == '1';
        }
        total++;
    }
    // Gamma rate for part 1
    int gamma = 0;
    for (int i = 0; i < len; i++) {
        gamma = (gamma << 1) + (counts[i] > total / 2);
    }
    // Least common == complement of most common
    int epsilon = gamma ^ ((1 << len) - 1);
    int power_consumption = gamma * epsilon;
    printf("Part 1:\n");
    printf("%d*%d=%d\n", gamma, epsilon, power_consumption);

    return 0;
}
