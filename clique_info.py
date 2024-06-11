import time


class CliqueInfo():

    def __init__(self, NetOrig, buildClique):

        # self.buildClique = BuildClique('data/social_network', 'r')
        # self.buildClique = BuildClique('data/network', 'g')
        # self.NetOrig = self.buildClique.NetOrig

        self.netOrig = NetOrig
        self.buildClique = buildClique
        self.net_clique = {}
        self.orig_n = self.netOrig.orig_network_size()

        self.para_node = 0.33333
        self.para_edge_overlapping = 0.33333
        self.para_edge_joint = 0.33333
        self.clique_ave_weight = 0.0
        self.label = []
        self.intersection = []

    def num_of_clique_node(self, i):

        return self.net_clique["clique"][i]["k"]

    def node_of_clique(self, i):

        return self.net_clique["clique"][i]["node"]

    def orig_network_size(self):

        return self.orig_n

    def clique_weight(self):

        temp = 0
        for i in range(self.orig_n):
            for j in range(i+1, self.orig_n):
                temp += self.netOrig.orig_network_AdjMatrix(i, j)

        return temp

    # 计算不同m-clique间的重叠结点
    # def clique_Node(self, a, size_a, b, size_b):

    #     num = 0
    #     for i in range(size_a):
    #         for j in range(size_b):
    #             if a[i] == b[j]:
    #                 self.intersection[num] = a[i]
    #                 self.label[a[i]] = 1
    #                 num += 1
    #                 break
    #     return num


    # 计算不同m-clique间的重叠边和临近边
    def clique_Edge(self, a, b, inter_num):

        edge1 = 0
        edge2 = 0

        for i in a:
            for j in b:
                edge1 += self.netOrig.orig_network_AdjMatrix(i, j)

        for i in range(inter_num):
            for j in range(i+1, inter_num):
                edge2 += self.netOrig.orig_network_AdjMatrix(
                    self.intersection[i], self.intersection[j])

        return self.para_edge_joint * edge1 + self.para_edge_overlapping * edge2


    # 构建maximal-clique图
    def construct_clique_network(self):

        n = 0
        en_original = 0

        self.net_clique["size_n"] = 0

        CliqueCount = self.buildClique.CliqueCount
        for i in range(CliqueCount):
            self.net_clique["size_n"] += self.buildClique.MaxClique_size(i)

        num = self.net_clique["size_n"]

        weight_sum_orig = self.netOrig.net_orig["nEdge"]

        self.net_clique["Adj"] = [0.0 for i in range(num*num)]

        self.net_clique["clique"] = [{} for i in range(num)]

        for i in range(CliqueCount):
            if self.buildClique.MaxClique_size(i) == 0:
                continue
            for j in range(self.buildClique.MaxClique_size(i)):
                self.net_clique["clique"][n]["k"] = i+1
                self.net_clique["clique"][n]["node"] = self.buildClique.MaxClique_Clique(i, j)
                n += 1

        # 下面应该是最耗时间的

        # 计算link strength
        for i in range(num):
            intersection_node = 0
            edge_rate = 0.0

            if self.net_clique["clique"][i]["k"] == 1:
                continue
            for j in range(i+1, num):
                self.intersection = []
                self.label = [0 for i in range(self.orig_n)]

                # self.intersection为重叠结点集
                self.intersection = list(set(self.net_clique["clique"][i]["node"]) & set(self.net_clique["clique"][j]["node"]))
                for tmp in self.intersection:
                    self.label[tmp] = 1
                intersection_node = len(self.intersection)

                # lon
                node_rate = self.para_node * intersection_node / \
                    (self.net_clique["clique"][i]["k"] +
                     self.net_clique["clique"][j]["k"] - intersection_node)

                # loe && lje
                nodes_m = list(set(self.net_clique["clique"][i]["node"]) ^ set(self.intersection))
                nodes_n = list(set(self.net_clique["clique"][j]["node"]) ^ set(self.intersection))

                edge_rate = self.clique_Edge(
                    nodes_m, nodes_n, intersection_node) / weight_sum_orig

                self.net_clique["Adj"][i*num+j] = float(node_rate + edge_rate)

                if self.net_clique["Adj"][i*num+j] > 0:
                    en_original += 1
                    self.clique_ave_weight += self.net_clique["Adj"][i*num+j]

        # # 重新计算均值
        # self.clique_ave_weight = 0.0
        # for i in range(self.net_clique["size_n"]):
        #     for j in range(i+1, self.net_clique["size_n"]):
        #         w = self.net_clique["Adj"][i * self.net_clique["size_n"] + j]
        #         if w > 0:
        #             en_original += 1
        #             self.clique_ave_weight += w

        self.clique_ave_weight = self.clique_ave_weight / en_original


    def output_clique_network(self, name):

        n = self.net_clique["size_n"]

        f = open(name+"_clique_network_orig.dat", 'w+', encoding='utf-8')
        t = open(name+"_clique_network_cut.dat", 'w+', encoding='utf-8')

        print("\n--------------saving network---------------\n")

        for i in range(self.net_clique["size_n"]):
            for j in range(self.net_clique["size_n"]):
                if self.net_clique["Adj"][i*n+j] > 0:
                    f.write("%d  %d  %lf\n" %
                            (i+1, j+1, self.net_clique["Adj"][i * n + j]))

                if self.net_clique["Adj"][i*n+j] > self.clique_ave_weight:
                    t.write("%d  %d  %lf\n" %
                            (i+1, j+1, self.net_clique["Adj"][i * n + j]))

        f.close()
        t.close()
