import matplotlib.pyplot as plt
from networkx import nx


G = nx.Graph()

for i in range(1, 21):
    G.add_node(i, data=str(i))

edges = [[1, 2], [1, 5], [1, 8], [2, 3], [2, 10], [3, 4], [3, 12], [4, 5], [4, 14], [5, 6], [6, 7], [6, 15],
         [7, 8], [7, 17], [8, 9], [9, 10], [9, 18], [10, 11], [11, 12], [11, 19], [12, 13], [13, 14], [13, 20],
         [14, 15], [15, 16], [16, 17], [16, 20], [17, 18], [18, 19], [19, 20]]

for [a, b] in edges:
    G.add_edge(a, b)

nx.draw(G, with_labels=True)

# display
plt.show()