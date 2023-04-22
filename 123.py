import networkx as nx
import csv
import random
import copy
import pandas as pd
import numpy as np

data = pd.read_csv("data9.csv", sep=",", header=None)
data.to_csv("edge_data.txt", sep=" ", header=None, index=False)
# 边数据形成图（无向）
fh = open("edge_data.txt", 'rb')
G = nx.read_edgelist(fh)
fh.close()
G0 = G.to_undirected()
# 计算余平均度和余度分布并将结果保存于‘余度序列’
# 计算节点余平均度
neighbor_degree_sum0 = {}  # 创建空字典，用于存储每个节点的邻接点的度之和
for u in G0.nodes():  # 遍历每个节点
    neighbor_degree_sum0[u] = 0
    for v in G0.neighbors(u):  # 遍历节点
        neighbor_degree_sum0[u] += G0.degree(v)
for u in G0.nodes():
    neighbor_degree_sum0[u] /= G0.degree(u)  # 各节点的余平均度knn
Kn0 = sum(neighbor_degree_sum0.values())/len(G0)   # 计算网络的余平均度
print(Kn0)
# 计算余度分布-原始图
degrees = nx.degree_histogram(G0)
max_degree0 = max(degrees)
print(max_degree0)
ar0 = np.zeros(max+1)
#print(ar0)
for u in G0.nodes():  # 遍历每个节点
    for v in G0.neighbors(u):
        ar0[G0.degree(v)] += 1
x_ar0 = list(range(len(ar0)+1))
sum_ar0 = sum(ar0)
for u in range(len(ar0)):
    ar0[u] /= sum_ar0
Pnk0 = ar0
# 将 Pnk0 中值为0的元素去除


# 输出去除0后的结果
print(Pnk0)
# arr = [x for x in Pnk0 if x != 0]
# print(arr)
