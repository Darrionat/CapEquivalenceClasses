#include <stdio.h>
#include <stdlib.h>

int max(int arr[], int size)
{
    int max = arr[0]; // Assume the first element is the maximum
    for (int i = 1; i < size; i++)
    {
        if (arr[i] > max)
        {
            max = arr[i];
        }
    }
    return max;
}

int main()
{
    // INPUT
    int dim;
    printf("Enter the dimension of the set: ");
    scanf("%d", &dim);
    int spaceSize = 1 << dim; // 2^d

    int sizeOfSet;
    printf("Enter the size of the set: ");
    scanf("%d", &sizeOfSet);

    int *sidonSet = (int *)malloc(sizeOfSet * sizeof(int));
    printf("Enter %d values for set:\n", sizeOfSet);
    for (int i = 0; i < sizeOfSet; ++i)
    {
        scanf("%d", &sidonSet[i]);
    }

    printf("Sidon set:\n");
    for (int i = 0; i < sizeOfSet; i++)
    {
        printf("%d ", sidonSet[i]);
    }
    printf("\n");

    printf("Values stored\n");

    // Table:
    // Key = Point in \F_2^{2n}, Value = Exclude Multiplicity
    int *excludeMultiplicties = (int *)malloc(spaceSize * sizeof(int));

    for (int i = 0; i < sizeOfSet; i++)
    {
        for (int j = i + 1; j < sizeOfSet; j++)
        {
            for (int k = j + 1; k < sizeOfSet; k++)
            {
                excludeMultiplicties[sidonSet[i] ^ sidonSet[j] ^ sidonSet[k]]++;
            }
        }
    }

    free(sidonSet);

    int maxExcludeMult = max(excludeMultiplicties, spaceSize);
    printf("\nExclude Distribution:\n");
    printf("Mult\t\tFreq\n");
    for (int mult = 0; mult <= maxExcludeMult; mult++)
    {
        int count = (mult == 0) ? -sizeOfSet : 0;
        for (int point = 0; point < spaceSize; point++)
        {
            if (excludeMultiplicties[point] == mult)
            {
                count++;
            }
        }
        if (count > 0)
        {
            printf("%d\t\t%d\n", mult, count);
        }
    }
    free(excludeMultiplicties);
    return 0;
}
