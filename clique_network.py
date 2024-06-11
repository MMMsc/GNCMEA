from torch import var
from parameter import *
import time


class CliqueNet():

    def __init__(self, cliqueInfo):

        self.net = {}

        self.net_clique = cliqueInfo.net_clique
        self.clique_ave_weight = cliqueInfo.clique_ave_weight

    def network_size(self):

        return self.net["n"]

    def neighbor(self, i):

        return self.net["e"][i]

    def weight(self, i, j):

        return self.net["w"][i * (self.net["n"]) + j]

    def link_sum(self, i):

        return self.net["ls"][i]

    def degree(self, i):

        return self.net["degree"][i]

    # 添加i到j的边和对应权重
    def add_link(self, i, j, w):

        if j not in self.net["e"][i]:
            self.net["e"][i].append(j)

        self.net["w"][i * (self.net["n"]) + j] = w

    def sum_link(self):

        n = self.net_clique["size_n"]
        s = [0.0 for i in range(n)]
        l = self.net["e"]

        for i in range(n):
            for j in l[i]:
                x = self.weight(i, j)
                s[i] += x
        return s

    def parameter_of_clique_network(self, varDim):

        en_threshold = 0
        n = self.net_clique["size_n"]

        self.net["n"] = n
        self.net["w"] = [0.0 for i in range(n*n)]
        self.net["degree"] = [0 for i in range(n)]
        self.net["e"] = [[] for i in range(n)]
        print("original nodes: %d" % varDim)
        print("clique num: %d" % n)

        self.clique_ave_weight = (n / varDim) * self.clique_ave_weight

        for i in range(n):
            for j in range(i+1, n):
                w = self.net_clique["Adj"][i * self.net_clique["size_n"] + j]

                if w < self.clique_ave_weight:
                    self.net_clique["Adj"][i * self.net_clique["size_n"] + j] = 0

                else:
                    self.add_link(i, j, w)
                    self.add_link(j, i, w)
                    self.net["degree"][i] += 1
                    self.net["degree"][j] += 1
                    en_threshold += 1

        print("clique edges: %d" % en_threshold)
        print("ave_weight: %lf" % self.clique_ave_weight)

        self.net["ls"] = self.sum_link()

        for tmp in range(len(self.net["e"])-1, -1, -1):
            self.net["e"][tmp].reverse()
            if self.net["e"][tmp] == []:
                del self.net["e"][tmp]

        # f = open("result/experiment/paras_"+str(para)+".dat", 'a+', encoding='utf-8')
        # f.write("edges: "+str(en_threshold))
        # f.write("\n")
        # f.write("threshold: "+str(self.clique_ave_weight))
        # f.write("\n")
        # f.write("\n")
        # f.close()

