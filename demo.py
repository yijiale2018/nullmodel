import networkx as nx
import csv
import matplotlib.pyplot as plt
import random

# 读取边 CSV 文件
edge_file = 'data9.csv'
with open(edge_file, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        edges = [tuple(row) for row in reader]

# 构建网络
G = nx.Graph()
G.add_edges_from(edges)

# 计算节点的度分布
degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
print(degree_sequence)
degree_count = nx.degree_histogram(G)

# # 绘制度分布直方图
plt.hist(degree_sequence, bins='auto')
plt.title("Degree Histogram")
plt.xlabel("Degree")
plt.ylabel("Count")
plt.show()



