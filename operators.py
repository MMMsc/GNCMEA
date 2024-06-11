from __future__ import generator_stop
import random, gc
from parameter import *


class Operator():

    def __init__(self, cliqueNet, community, individual):

        self.individual = individual
        self.community = community
        self.cliqueNet = cliqueNet

        self.n = self.cliqueNet.network_size()

    def decode(self, gene):

        cn = 0
        c = [{} for i in range(self.n)]
        ind = {}

        c[cn] = self.community.new_community(gene[0])
        cn += 1

        for i in range(1, self.n):
            c[cn] = self.community.new_community(gene[i])
            # for j in range(cn+1):
            j = 0
            while (j != cn):
                bs = self.community.between(c[j], c[cn])

                # 构造有可能的community
                if self.community.tightness_inc(c[j], c[cn], bs) > 0:
                    c[j], c[cn] = self.community.merge(c[j], c[cn], bs)
                    del(c[cn])
                    break
                j += 1
            if j == cn:
                cn += 1

        ind["comm"] = c
        ind["comm_n"] = cn
        ind["refcount"] = 1
        # gene长度为clique数量
        ind["gene"] = [0 for i in range(self.n)]

        # 相当于将label作为初始的gene，label为由0-1构成的list，表示该community是否包含第i个clique
        ind["gene"] = self.community.community_to_label(c, ind["gene"], cn)
        # evalutate
        ind = self.individual.eval_individual(ind)

        return ind

    def crossover(self, p1, p2):

        if (random.random() > pc):
            p1["refcount"] += 1
            return p1
        else:
            gene = p1["gene"]

            node = random.randint(0, self.n-1)
            c = self.community.find_community(node, p2["comm"])

            # 交叉
            try:
                for l in c["member"]:
                    gene[l] = p2["gene"][l]
            except TypeError:
                pass

        return self.individual.new_individual(gene)

    # 轮盘赌算法
    def roulette_neighbor(self, i):

        l = self.cliqueNet.neighbor(i)
        prob = random.random()
        end = self.cliqueNet.link_sum(i) * prob

        for node in l:
            s = self.cliqueNet.weight(i, node)
            if (end <= s):
                return node
            else:
                end -= s

    def mutation(self, ind):

        label = [0 for i in range(self.n)]
        gene = []

        if (random.random() > pm): return ind

        label = self.community.community_to_label(
            ind["comm"], label, ind["comm_n"])

        for i in range(self.n):
            comm = ind["comm"][label[i]]

            if random.random() < self.community.tightness(comm):
                continue

            # 复制父类
            if gene == []:
                gene = ind["gene"]

        if gene != []:

            ind = self.individual.set_individual(ind)

        del label
        gc.collect()
        return ind

