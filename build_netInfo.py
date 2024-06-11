class build_netInfo():

    def __init__(self, N, E, M):

        self.N = N
        self.E = E
        self.M = M

        self.net_orig = {}
        self.net_orig["n"] = self.N
        self.net_orig["nEdge"] = self.E
        self.net_orig["degree"] = [0 for i in range(self.N)]
        self.net_orig["Neighbor"] = [[] for i in range(self.N)]
        self.net_orig["AdjMatrix"] = [[0 for j in range(self.N)] for i in range(self.N)]


    def orig_network_size(self):

        return self.net_orig["n"]

    def orig_network_nEdge(self):

        return self.net_orig["nEdge"]

    def orig_network_degree(self, i):

        return self.net_orig["degree"][i]

    def orig_network_AdjMatrix(self, i, j):

        return self.net_orig["AdjMatrix"][i][j]

    def orig_network_Neighbor(self, i):

        return self.net_orig["Neighbor"][i]

    def orig_neighbor(self, i, j):

        if j not in self.net_orig["Neighbor"][i]:
            self.net_orig["Neighbor"][i].append(j)

    def build_netinfo(self):

        # 默认计算无向图结点的度，统计邻居，构建邻接矩阵
        for i in range(self.N):
            for j in range(self.N):
                if self.M[i][j] == 1:
                    self.net_orig["degree"][i] += 1

                    if j not in self.net_orig["Neighbor"][i]:
                        self.net_orig["Neighbor"][i].append(j)

        self.net_orig["AdjMatrix"] = self.M

        for tmp in self.net_orig["Neighbor"]:
            tmp.reverse()

