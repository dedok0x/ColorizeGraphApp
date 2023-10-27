# Функция для получения списка соседних вершин
def get_neighbors(vertex, graph):
    return graph[vertex]

# Функция для определения цвета, который еще не использовался для соседних вершин
def get_color(vertex, color_map, graph):
    used_colors = set()
    for neighbor in get_neighbors(vertex, graph):
        if neighbor in color_map:
            used_colors.add(color_map[neighbor])
    for color in range(len(graph)):
        if color not in used_colors:
            return color
    return 0

# Функция для жадной раскраски графа
def greedy_coloring(graph):
    color_map = {}
    for vertex in graph:
        color_map[vertex] = get_color(vertex, color_map, graph)
    return color_map

def input_graph():
    graph = {}

    print("Задайте граф, который необходимо раскрасить. (для завершения введите: \"exit\")")
    while True:
        try:
            vertex = input("Введите вершину: ")
            if vertex == "exit":
                break
            neighbors = input("Через пробел введите связные вершины: ").split()
            if vertex:
                graph[vertex] = neighbors
        except ValueError:
            print("invalid")
            continue
    return graph
color_map = greedy_coloring(input_graph())
print(color_map) # {'A': 0, 'B': 1, 'C': 2, 'D': 0, 'E': 1, 'F': 2}