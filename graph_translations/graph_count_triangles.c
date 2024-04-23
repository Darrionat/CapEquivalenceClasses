#include <stdio.h>
#include <stdlib.h>

int *translateSet(int *to_translate, int size, int t);
int **getAllGraphTranslations(int *graph, int n);
long long countTriangles(int **adjacencyMatrix, int numVertices);
int areDisjoint(int *array1, int size1, int *array2, int size2);

int *translateSet(int *to_translate, int size, int t)
{
    int *result = (int *)malloc(size * sizeof(int));
    if (result == NULL)
    {
        fprintf(stderr, "Memory allocation failed in translateSet\n");
        exit(EXIT_FAILURE);
    }

    for (int i = 0; i < size; i++)
    {
        result[i] = t ^ to_translate[i];
    }
    return result;
}

/**
 * Get all translations of a function graph.
 * Returns all arrays of the form (a,b) + G_F where a,b \in \Z_2^n and G_F is the graph of a function F from \Z_2^n to itself.
 */
int **getAllGraphTranslations(int *graph, int n)
{
    int sizeOfGraph = 1 << n;           // 2^n
    int numTranslations = 1 << (2 * n); // 2^(2n)

    int **result = (int **)malloc(numTranslations * sizeof(int *));

    for (int t = 0; t < numTranslations; t++)
    {
        result[t] = translateSet(graph, sizeOfGraph, t);
    }

    return result;
}

long long countTriangles(int **adjacencyMatrix, int numVertices)
{
    long long count = 0;
    for (int i = 0; i < numVertices; i++)
    {
        for (int j = i + 1; j < numVertices; j++)
        {
            for (int k = j + 1; k < numVertices; k++)
            {
                // Check if the triplet forms a triangle
                /*
                    i
                   / \
                  j---k

                */
                if (adjacencyMatrix[i][j] && adjacencyMatrix[j][k] && adjacencyMatrix[i][k])
                {
                    count++;
                }
            }
        }
    }
    // Each triangle is counted three times (once for each permutation of vertices)
    return count;
}

int areDisjoint(int *array1, int size1, int *array2, int size2)
{
    for (int i = 0; i < size1; ++i)
    {
        for (int j = 0; j < size2; ++j)
        {
            if (array1[i] == array2[j])
            {
                // Found a common element, arrays are not disjoint
                return 0;
            }
        }
    }
    // No common elements found, arrays are disjoint
    return 1;
}
int main()
{
    // INPUT
    int n;
    printf("Enter the value of n: ");
    scanf("%d", &n);
    int sizeOfGraph = 1 << n; // 2^n

    int *functionGraph = (int *)malloc(sizeOfGraph * sizeof(int));
    printf("Enter %d values for the function graph:\n", sizeOfGraph);
    for (int i = 0; i < sizeOfGraph; ++i)
    {
        scanf("%d", &functionGraph[i]);
    }

    printf("Function Graph:\n");
    for (int i = 0; i < sizeOfGraph; i++)
    {
        printf("%d ", functionGraph[i]);
    }
    printf("\n");

    printf("Values stored\n");

    int vertices = 1 << (2 * n); // 2^(2n)
    int **adjacencyMatrix = (int **)malloc(vertices * sizeof(int *));
    for (int i = 0; i < vertices; i++)
    {
        adjacencyMatrix[i] = (int *)malloc(vertices * sizeof(int));
    }

    int **graphTranslations = getAllGraphTranslations(functionGraph, n);
    free(functionGraph);

    printf("Graph translations built\n");
    printf("Computing Kneser graph adjacency matrix\n");

    for (int i = 0; i < vertices; i++)
    {
        for (int j = i + 1; j < vertices; j++)
        {
            int *translation1 = graphTranslations[i];
            int *translation2 = graphTranslations[j];
            if (areDisjoint(translation1, sizeOfGraph, translation2, sizeOfGraph))
            {
                adjacencyMatrix[i][j] = 1;
            }
        }
    }
    printf("Adjacency matrix built\n");

    // printf("Adjacency Matrix:\n");
    // for (int i = 0; i < vertices; i++)
    // {
    //     for (int j = 0; j < vertices; j++)
    //     {
    //         printf("%d ", adjacencyMatrix[i][j]);
    //     }
    //     printf("\n");
    // }

    long long triangleCount = countTriangles(adjacencyMatrix, vertices);

    printf("Number of triangles in the graph: %lld\n", triangleCount);

    for (int i = 0; i < vertices; i++)
    {
        free(graphTranslations[i]);
    }
    free(graphTranslations);

    for (int i = 0; i < vertices; i++)
    {
        free(adjacencyMatrix[i]);
    }
    free(adjacencyMatrix);

    return 0;
}
