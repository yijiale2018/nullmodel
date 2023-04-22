import collections

import networkx as nx
from nullmodel import *
import numpy as np
import math
import matplotlib.pyplot as plt
import nullmodel as nm
import csv

#原始网络
edge_file='8.csv'
with open(edge_file, 'r') as f:
    reader = csv.reader(f)
    edges = [tuple(row) for row in reader]

# 构建网络
G = nx.Graph()
G.add_edges_from(edges)
list_G = list(G.subgraph(c) for c in nx.connected_components(G))
num = nx.number_connected_components(G)#连通组元数









#置乱网络
list_G1 = []
list_G2 = []
list_G3=[]
nswap = 2 * len(G.edges())
maxtry = 100 * nswap
#G1 = random_1k(G, nswap=nswap, max_tries=maxtry)
#G2 = random_1kc(G, nswap=nswap, max_tries=maxtry)
#print len(G1.edges()),len(G1.nodes())
#print len(G2.edges()),len(G2.nodes())
# for i in range(0,10):
G1 = random_0kc(G, nswap=nswap, max_tries=maxtry)
G2 = random_1kc(G, nswap=nswap, max_tries=maxtry)
G3 = random_2kc(G, nswap=nswap, max_tries=maxtry)
list_G1.append(G1)
list_G2.append(G2)
list_G3.append(G3)


dic = {'原始图':G,'0阶零模型':G1,'1阶零模型':G2,'2阶零模型':G3}
print(dict)


#---------------------节点数-----------------------#
print('节点数量:')
for idx,item in dic.items():
    print(idx+":"+str(item.number_of_nodes()))
print('---------------------------------------------------------')

#---------------------边数-----------------------#
print('边数量:')
for idx,item in dic.items():
    print(idx+":"+str(item.number_of_edges()))
print('---------------------------------------------------------')



#---------------------平均度-----------------------#
print('平均度:')
for idx,item in dic.items():
    degrees=dict(item.degree());
    avg_degree=sum(degrees.values())/len(degrees)
    print(idx+":"+str(avg_degree))
print('---------------------------------------------------------')

#---------------------度分布-----------------------#
# 计算每个节点的度数
print('度分布')
for idx,item in dic.items():

    degrees = dict(item.degree())

    # 统计每个度数出现的次数
    degree_counts =  {}
    for degree in degrees.values():
            if degree in degree_counts:
                 degree_counts[degree] += 1
            else:
                degree_counts[degree] = 1

    # 将次数归一化为概率
    n = len(G.nodes())
    degree_probs = {}
    for degree, count in degree_counts.items():
        degree_probs[degree] = count / n
    sorted_degree_probs = sorted(degree_probs.items())
    print(idx+":"+str(dict(sorted_degree_probs)))
print('---------------------------------------------------------')
# ---------------------计算余平均度1-----------------------#
# 绘制度分布直方图
#     plt.bar(degree_probs.keys(), degree_probs.values())
#     plt.xlabel('Degree')
#     plt.ylabel('Probability')
#     plt.show()


#---------------------计算余平均度1-----------------------#
# print('余平均度：')
# for idx,item in dic.items():
#     #计算每个节点的邻居节点之间的连边数量
#     node_triangles=nx.triangles(item)
#     #计算网络的余平均度
#     avg_clustering = sum(node_triangles.values()) / len(node_triangles)
#     print(idx+":"+str(avg_clustering))
# print('---------------------------------------------------------')

#---------------------计算余平均度-----------------------#
print('余平均度：')
for idx,item in dic.items():
    # 计算节点余平均度
    neighbor_degree_sum0 = {}  # 创建空字典，用于存储每个节点的邻接点的度之和
    for u in item.nodes():  # 遍历每个节点
        neighbor_degree_sum0[u] = 0
        for v in item.neighbors(u):  # 遍历节点
            neighbor_degree_sum0[u] += item.degree(v)
    for u in item.nodes():
        neighbor_degree_sum0[u] /= item.degree(u)  # 各节点的余平均度knn
    kn = sum(neighbor_degree_sum0.values()) / len(item)  # 计算网络的余平均度
    print(idx+":"+str(kn))

print('---------------------------------------------------------')
#---------------------计算余度分布-----------------------#
print('计算余度分布:')
for idx, item in dic.items():
    Gt = nx.to_numpy_array(item)
    N_num = np.shape(Gt)[0]  # 节点数
    M_num = np.sum(Gt) / 2  # 边数
    K_avg = 2 * M_num / N_num  # 平均度
    # 计算度分布P_K，各个度的频率除以网络中节点数
    node_M_num = np.sum(Gt, axis=1)  # 节点度
    P_K = collections.Counter(np.sort(node_M_num))
    for value in P_K:
        P_K[value] = P_K[value] / N_num
    # 计算余度分布Pn_K
    Pn_K = {}  # 使用hash表保存Pn_K
    for value1 in P_K:
        # 计算Pn(value1)
        sum1 = 0
        for value2 in P_K:
            sum2 = 0
            # 计算P(value2, k) 1、找到度为j的节点  2、计数度为j节点中度为k的节点数量
            if value2 == value1:
                u = 2
            else:
                u = 1
            for i in range(N_num):
                if node_M_num[i] == value2:
                    tmp = collections.Counter(Gt[i] * node_M_num)
                    sum2 += tmp[value1]
            sum1 += sum2 * u / (2 * M_num)
        Pn_K[value1] = sum1
    print(idx+":"+str(Pn_K))

print('---------------------------------------------------------')
#---------------------平均路径长度-----------------------#
print('平均路径长度')
for idx,item in dic.items():
    # 计算平均路径长度
    avg_path_length = nx.average_shortest_path_length(item)
    print(idx+":"+str(avg_path_length))
print('---------------------------------------------------------')
#---------------------聚类系数-----------------------#
print('聚类系数')
for idx,item in dic.items():
    # 计算聚类系数
    avg_clustering = nx.average_clustering(item)
    print(idx+":"+str(avg_clustering))

#---------------------度分布-----------------------#
l0 = dict(G.degree()).values()#度序列
l1 = dict(G1.degree()).values()
l2 = dict(G2.degree()).values()
l3 = dict(G3.degree()).values()
colors = ['r','b','g','#1f77b4']
labels = ['原始图','0阶零模型','1阶零模型','2阶零模型']
markers = ['o','s','x','*']
alphas = [1,0.5,1,0.5]
size = [30,60,80,100]
j=0
for t in [l0,l1,l2,l3]:
    dt = {e:list(t).count(e)/float(len(t)) for e in set(t)}
    #print(dt)
    x = dt.keys()
    y = dt.values()
    plt.scatter(x,y,s=size[j],c=colors[j],label=labels[j],marker=markers[j],alpha=alphas[j])
    plt.plot(x,y,c=colors[j])
    j += 1
plt.legend(loc='upper right')
plt.xlabel('degree')
plt.ylabel('P')
plt.show()
print('---------------------------------------------------------')
#---------------------计算余度分布2-----------------------#
# for idx,item in dic.items():
#     # 计算余度分布Pn_K
#     Pn_K = {}  # 使用hash表保存Pn_K
#     for value1 in dict(degree_probs):
#         # 计算Pn(value1)
#         sum1 = 0
#         for value2 in degree_probs:
#             sum2 = 0
#             # 计算P(value2, k) 1、找到度为j的节点  2、计数度为j节点中度为k的节点数量
#             if value2 == value1:
#                 u = 2
#             else:
#                 u = 1
#             #print(item.number_of_nodes())
#             for i in range(item.number_of_nodes()):
#                 print(item.number_of_nodes())
#                 if  item.degree(i) == value2:
#                     #tmp = collections.Counter(nx.to_numpy_array(item)[i] * item.number_of_edges())
#                     tmp = collections.Counter(item[i] * item.number_of_edges())
#                     sum2 += tmp[value1]
#             sum1 += sum2 * u / (2 * item.number_of_edges())
#         Pn_K[value1] = sum1
#     #print(P_K)
# for idx, item in dic.items():
#     G = nx.to_numpy_array(item)
#     N_num = np.shape(G)[0]  # 节点数
#     M_num = np.sum(G) / 2  # 边数
#     K_avg = 2 * M_num / N_num  # 平均度
#     # 计算度分布P_K，各个度的频率除以网络中节点数
#     node_M_num = np.sum(G, axis=1)  # 节点度
#     P_K = collections.Counter(np.sort(node_M_num))
#     for value in P_K:
#         P_K[value] = P_K[value] / N_num
#     # 计算余度分布Pn_K
#     Pn_K = {}  # 使用hash表保存Pn_K
#     for value1 in P_K:
#         # 计算Pn(value1)
#         sum1 = 0
#         for value2 in P_K:
#             sum2 = 0
#             # 计算P(value2, k) 1、找到度为j的节点  2、计数度为j节点中度为k的节点数量
#             if value2 == value1:
#                 u = 2
#             else:
#                 u = 1
#             for i in range(N_num):
#                 if node_M_num[i] == value2:
#                     tmp = collections.Counter(G[i] * node_M_num)
#                     sum2 += tmp[value1]
#             sum1 += sum2 * u / (2 * M_num)
#         Pn_K[value1] = sum1
#     print(Pn_K)