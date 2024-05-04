import sys

def all_visited(visited):
    return all(visited)

def tsp(visited, cost, current, path):
    global min_cost, ans
    if all_visited(visited):
        if cost + graph[current][0] < min_cost:
            min_cost = cost + graph[current][0]
            ans = path + [0]
        return

    for i in range(n):
        if not visited[i] and i != current:
            visited[i] = True
            tsp(visited, cost + graph[current][i], i, path + [i])
            visited[i] = False


print("Enter number of vertices:")
n = int(input())
graph = []
for i in range(n):
    row = []
    for j in range(n):
        if i != j:
            print("Enter cost of", i, "to", j)
            e = int(input())
            row.append(e)
        else:
            row.append(0)
        graph.append(row)

min_cost = sys.maxsize
ans = []
visited = [False] * n
visited[0] = True

tsp(visited, 0, 0, [0])

print("Shortest path:", ans)
print("Min Cost:", min_cost)

"""
Enter number of vertices:
3
Enter costs from vertex 0 to other vertices:
0 10 15
Enter costs from vertex 1 to other vertices:
10 0 20
Enter costs from vertex 2 to other vertices:
15 20 0
Shortest path: [0, 1, 2, 0]
Min Cost: 35
"""
