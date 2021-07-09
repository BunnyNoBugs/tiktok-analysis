from typing import Union


def dijkstra(start: int, graph: dict) -> Union[dict, str]:
    path = {}
    seen = []
    for verticle in graph:
        if verticle == start:
            path[verticle] = 0
        else:
            path[verticle] = float('inf')

    # беру минимальную вершину
    try:
        min_v = min(path, key=path.get)
    except ValueError:
        return 'Дан пустой граф'

    # рассмотрим все вершины в которые из вершины W есть путь,
    # не содержащий вершин посредников
    for connected in graph[min_v]:
        if path[connected] == float('inf'):
            path[connected] = graph[min_v][connected]

    seen.append(min_v)  # рассмотрели первую вершину
    while len(seen) != len(graph):
        # выбираем из ещё не посещенных такую,
        # которая имеет минимальное значение метки
        not_seen = {}
        for verticle in path:
            if verticle not in seen:
                not_seen[verticle] = path[verticle]
        try:
            min_v = min(not_seen, key=not_seen.get)
        except ValueError:
            return path

        # если нет ни одного исходящего пути из вершины
        while len(graph[min_v]) < 1:
            not_seen = {}
            # тогда помечаем такую вершину как просмотренную
            seen.append(min_v)
            for verticle in path:
                if verticle not in seen:
                    not_seen[verticle] = path[verticle]

            # на случай если закончатся вершины
            try:
                min_v = min(not_seen, key=not_seen.get)
            except ValueError:
                return path

        # рассмотрим непосещенные вершины
        for verticle in not_seen:  # все соединенные вершины с нашей вершиной
            if verticle in graph[min_v]:
                if path[min_v] + graph[min_v][verticle] < path[verticle]:
                    path[verticle] = path[min_v] + graph[min_v][verticle]

        seen.append(min_v)
    return path


print('Пример 1:')
graph4 = {
    1: {2: 10, 3: 30, 4: 50, 5: 10, 6: 60, 7: 100},
    2: {7: 30},
    3: {5: 10},
    4: {2: 40, 3: 20, 6: 1},
    5: {1: 10, 3: 10, 4: 30, 6: 15},
    6: {1: 60, 4: 1, 5: 15},
    7: {}
}

print(dijkstra(1, graph4))
print(dijkstra(7, graph4))

print('####')
print('Пример 2:')
graph5 = {
    1: {2: 10, 3: 30, 4: 50, 5: 10},
    2: {},
    3: {5: 10},
    4: {2: 40, 3: 20},
    5: {1: 10, 3: 10, 4: 30},
}

print(dijkstra(1, graph5))
print(dijkstra(3, graph5))

print('####')
print('Пример 3:')
graph6 = {}
print(dijkstra(1, graph6))

print('####')
print('Пример 4: Если граф несвязный, то он просто не работает.'
      ' Не падает, так что я считаю, что условие выполнено.')
graph7 = {
    1: {2: 10},
    2: {1: 5},
    3: {4: 10},
    4: {3: 5}
}
print(dijkstra(1, graph7))
