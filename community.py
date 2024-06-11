from parameter import *


class Community():

    def __init__(self, cliqueNet):

        self.cliqueNet = cliqueNet
        self.n = self.cliqueNet.network_size()

    def new_community(self, i):

        c = {}
        c["member"] = [i]

        c["Pin"] = 0.0
        c["Pout"] = self.cliqueNet.link_sum(i)
        c["size"] = 1

        return c

    def between(self, c1, c2):

        b = 0

        for i in c1["member"]:
            for j in c2["member"]:
                # print("c1->head: %d c2->head: %d" %(i, j), end='  ')
                b += self.cliqueNet.weight(i, j)

        return b

    def merge(self, c1, c2, bs):

        for i in c2["member"]:
            c1["member"].append(i)

        c1["Pin"] += c2["Pin"] + 2*bs
        c1["Pout"] += c2["Pout"] - 2*bs
        c1["size"] += c2["size"]

        return c1, c2

    def tightness(self, c):

        if not c["Pin"] and not c["Pout"]:
            return 0

        tightness = c["Pin"] / pow(c["Pin"]+c["Pout"], alpha)
        # print(f"\nthe tightness is {tightness}")
        return tightness

    # 判断c1、c2是否需要合并
    def tightness_inc(self, c1, c2, bs):

        t1 = self.tightness(c1)

        Sin = c1["Pin"] + c2["Pin"] + 2*bs
        Sout = c1["Pout"] + c2["Pout"] - 2*bs
        if not Sin and not Sout:
            return -t1
        tightness_inc = Sin / pow(Sin+Sout, alpha) - t1
        # print(f"\nthe Sin is {Sin}, the Sout is {Sout}\nthe tightness_inc is {tightness_inc}")
        return tightness_inc

    def community_size(self, c):

        return c["size"]

    def community_to_label(self, c, l, n):

        for i in range(n):
            for p in c[i]["member"]:
                l[p] = i

        return l

    def find_community(self, node, c):

        for comm in c:
            if node in comm["member"]:
                return comm

        return None

    def label_to_community(self, p, c):

        cn = 0
        l = [0 for i in range(self.n)]
        label = 0

        for i in range(self.n):
            label = p[i] # gene

            c[cn] = self.new_community(i)

            if l[label] == 0:
                l[label] = cn+1
                cn += 1
            else:
                comm = c[l[label]-1]
                bs = self.between(c[cn], comm)
                comm, c[cn] = self.merge(comm, c[cn], bs)

        # 删去空的{}
        while {} in c:
            c.remove({})

        return p, c, cn

