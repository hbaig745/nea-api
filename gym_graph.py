import math, sys


class WeightedMatrixGraph:
    def __init__(self):
        self.matrix = [[]]

    def is_empty(self):
        return len(self.matrix[0] == 0)

    def contains(self, node):
        return node in self.matrix[0]

    def __contains__(self, node):
        return self.contains(node)

    def add_node(self, node):
        if not node in self.matrix[0]:
            self.matrix[0].append(node)
            for n in range(1, len(self.matrix)):
                self.matrix[n].append(None)
            self.matrix.append([None for n in range(len(self.matrix[0]))])

    def delete_node(self, node):
        if node in self.matrix[0]:
            index = self.matrix[0].index(node)
            del self.matrix[0][index]
            del self.matrix[index]
            for n in range(1, len(self.matrix)):
                del self.matrix[n][index]

    def add_edge(self, from_node, to_node, weight=1):
        if from_node in self.matrix[0] and to_node in self.matrix[0]:
            from_index = self.matrix[0].index(from_node)
            to_index = self.matrix[0].index(to_node)
            self.matrix[from_index + 1][to_index] = weight

    def neighbours(self, current_node):
        n = []

        for node in self.matrix[0]:
            if (
                self.is_connected(current_node, node) != None
                or self.is_connected(node, current_node) != None
            ):
                n.append(node)

        return n

    def is_connected(self, from_node, to_node):
        if from_node in self.matrix[0] and to_node in self.matrix[0]:
            from_index = self.matrix[0].index(from_node)
            to_index = self.matrix[0].index(to_node)
            return self.matrix[from_index + 1][to_index]
        elif to_node in self.matrix[0] and from_node in self.matrix[0]:
            to_index = self.matrix[0].index(to_node)
            from_index = self.matrix[0].index(from_node)
            return self.matrix[to_index + 1][from_index]
        return None

    def dfs(self, start_node, end_node=None):
        visited = []
        stack = Stack()

        visited.append(start_node)
        stack.Push(start_node)

        while not stack.isEmpty():
            current_node = stack.Peek()
            stack.Pop()
            for node in self.neighbours(current_node):
                if node not in visited:
                    visited.append(node)
                    stack.Push(node)

        return visited

    def bfs(self, start_node, end_node=None):
        discovered = []
        queue = Queue()

        discovered.append(start_node)
        queue.Enqueue(start_node)

        while not queue.isEmpty():
            current_node = queue.Peek()
            queue.Dequeue()
            for n in self.neighbours(current_node):
                if n not in discovered:
                    discovered.append(n)
                    queue.Enqueue(n)

        return discovered

    def dijkstra(self, start_node, end_node=None):
        unvisited = {}
        visited = {}

        for node in self.matrix[0]:
            unvisited[node] = [sys.maxsize, None]

        unvisited[start_node][0] = 0

        finished = False
        while finished == False:
            if len(unvisited) == 0:
                finished = True
            else:
                lowest = sys.maxsize
                for li in unvisited:
                    if unvisited[li][0] < lowest:
                        lowest = unvisited[li][0]
                        current_node = li

                neighbours = self.neighbours(current_node)
                for node in neighbours:
                    if node not in visited:
                        try:
                            cost = unvisited[current_node][0] + self.is_connected(
                                current_node, node
                            )
                        except:
                            cost = unvisited[current_node][0] + self.is_connected(
                                node, current_node
                            )

                        if cost < unvisited[node][0]:
                            unvisited[node][0] = cost
                            unvisited[node][1] = current_node

                visited[current_node] = unvisited[current_node]
                del unvisited[current_node]

        return visited


class Stack:
    def __init__(self):
        self.Contents = []

    def Push(self, Item):
        self.Contents.append(Item)

    def Pop(self):

        if not self.isEmpty():
            del self.Contents[-1]

    def Peek(self):
        return self.Contents[-1]

    def isEmpty(self):
        if len(self.Contents) == 0:
            return True
        else:
            return False


class Queue:
    def __init__(self):
        self.contents = []

    def Peek(self):
        return self.contents[0]

    def Enqueue(self, item):
        self.contents.append(item)

    def Dequeue(self):
        self.contents.pop(0)

    def isEmpty(self):
        if len(self.contents) == 0:
            return True
        else:
            return False

def initialise_graph():
    g = WeightedMatrixGraph()
    g.add_node("A")
    g.add_node("B")
    g.add_node("C")
    g.add_node("D")
    g.add_node("E")
    g.add_node("F")
    g.add_node("G")

    g.add_edge('A', 'B', 38)
    g.add_edge('A', 'G', 23)
    g.add_edge('B', 'C', 40)
    g.add_edge('B', 'D', 26)
    g.add_edge('C', 'D', 41)
    g.add_edge('C', 'E', 69)
    g.add_edge('D', 'G', 29)
    g.add_edge('D', 'F', 48)
    g.add_edge('D', 'E', 62)
    g.add_edge('G', 'F', 52)

    return g


if __name__ == "__main__":

    def test_weighted_graph():
        g = WeightedMatrixGraph()
        g.add_node("A")
        g.add_node("B")
        g.add_node("C")
        g.add_node("D")
        g.add_node("E")
        g.add_node("F")
        g.add_node("G")

        g.add_edge('A', 'B', 38)
        g.add_edge('A', 'G', 23)
        g.add_edge('B', 'C', 40)
        g.add_edge('B', 'D', 26)
        g.add_edge('C', 'D', 41)
        g.add_edge('C', 'E', 69)
        g.add_edge('D', 'G', 29)
        g.add_edge('D', 'F', 48)
        g.add_edge('D', 'E', 62)
        g.add_edge('G', 'F', 52)

        table = g.dijkstra("A", "E")

        print(table)

    test_weighted_graph()
