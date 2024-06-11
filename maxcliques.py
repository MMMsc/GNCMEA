import time


class BuildClique(object):

    def __init__(self, netOrig):
        self.NetOrig = netOrig

        self.flag_node = [0 for i in range(self.NetOrig.orig_network_size())]
        self.setA = [0 for i in range(
            self.NetOrig.orig_network_size())]  # 存储目标派系
        self.setB = [0 for i in range(
            self.NetOrig.orig_network_size())]  # 存储该结点邻居结点
        self.flag_node_lower_std = [0 for i in range(
            self.NetOrig.orig_network_size())]
        self.node_degree_sequence = [0 for i in range(
            self.NetOrig.orig_network_size())]
        self.flag_for_whole_clique = [0 for i in range(
            self.NetOrig.orig_network_size())]
        self.CliqueCount = 0

    def BubbleSort(self):
        for i in range(self.NetOrig.orig_network_size()):
            for j in range(self.NetOrig.orig_network_size()-i-1):
                if self.NetOrig.orig_network_degree(self.node_degree_sequence[j]) > self.NetOrig.orig_network_degree(self.node_degree_sequence[j+1]):
                    temp = self.node_degree_sequence[j]
                    self.node_degree_sequence[j] = self.node_degree_sequence[j+1]
                    self.node_degree_sequence[j+1] = temp

    def MaxClique_Clique(self, k, m):

        return CLP[k]["MaxClique"][m]

    def MaxClique_size(self, k):

        return CLP[k]["num_of_cliques"]

    def intersection(self, num, num_set, num_setB):
        n = self.setB[num]
        if n == -1:
            return
        self.setA[num_set[0]] = n
        num_set[0] += 1
        self.setB[num] = -1
        num_set[1] -= 1

        if num_set[1] == 0:
            return

        for i in range(num_setB):
            x = self.setB[i]
            flag = 0
            if self.setB[i] == -1:
                continue
            for j in self.NetOrig.orig_network_Neighbor(n):
                if j == x:
                    flag = 1
                    break
                if j < x:
                    break

            if flag == 0:
                self.setB[i] = -1
                num_set[1] -= 1

    def Clique(self, node, sizeofclique, CLP):
        num1 = 0
        num2 = 0

        k = self.NetOrig.orig_network_degree(node) - sizeofclique + 1

        # 邻接结点有k-1个，但是度小于k-1的结点需要去除
        for m in self.NetOrig.orig_network_Neighbor(node):
            if num1 > k:
                return
            if self.flag_node[m] == 1:
                num1 += 1
                continue
            if self.NetOrig.orig_network_degree(m) < sizeofclique - 1:
                self.flag_node_lower_std[m] = 1
                num1 += 1
                if num1 > k:
                    return

        for m in self.NetOrig.orig_network_Neighbor(node):
            x = m
            num_intersection_node = 0

            if self.flag_node_lower_std[m] == 1 or self.flag_node[m] == 1:
                num2 += 1
                continue

            for n in self.NetOrig.orig_network_Neighbor(x):
                if self.flag_node_lower_std[n] == 1 or self.flag_node[n] == 1 or n == node:
                    continue

                for q in self.NetOrig.orig_network_Neighbor(node):
                    if self.flag_node_lower_std[q] == 1 or self.flag_node[q] == 1:
                        continue
                    if n == q:
                        num_intersection_node += 1
                        break
                    if n > q:
                        break

            if num_intersection_node < sizeofclique-2:
                num2 += 1
                self.flag_node_lower_std[x] = 1
            if num2 > k:
                return

        # 排除了不能构造clique的结点，结点将有两种可能性
        # 第一种情况，结点仅属于一个clique
        # c1 = 0
        # c2 = 0

        if (k == num2):
            # print("#####")
            for m in self.NetOrig.orig_network_Neighbor(node):
                if self.flag_node_lower_std[m] == 1 or self.flag_node[m] == 1:
                    # c1 += 1
                    continue
                for n in self.NetOrig.orig_network_Neighbor(node):
                    if (self.flag_node_lower_std[n] == 1 or self.flag_node[n] == 1 or m == n):
                        # c2 += 1
                        continue
                    if self.NetOrig.orig_network_AdjMatrix(m, n) == 0:
                        # print("c1 %d" % c1)
                        # print("c2 %d" % c2)
                        return

            Count1 = 1
            # 如何在不预设Maxclique结点集的情况下插入
            Count2 = CLP[sizeofclique-1]["num_of_cliques"]
            if Count2 >= len(CLP[sizeofclique-1]["MaxClique"]):
                CLP[sizeofclique -
                    1]["MaxClique"].append([0 for k in range(sizeofclique)])
            CLP[sizeofclique-1]["MaxClique"][Count2][0] = node

            for m in self.NetOrig.orig_network_Neighbor(node):
                if self.flag_node[m] == 1 or self.flag_node_lower_std[m] == 1:
                    continue
                CLP[sizeofclique-1]["MaxClique"][Count2][Count1] = m
                Count1 += 1

            CLP[sizeofclique-1]["num_of_cliques"] += 1
            self.flag_node[node] = 1

        # 第二种情况，一个结点属于多个clique
        else:
            num_exist_clique = 0
            num_node_for_set = [-1, -1]

            for m in self.NetOrig.orig_network_Neighbor(node):
                num = 0
                p = 0
                total_num_setB = 0

                if self.flag_node_lower_std[m] == 1 or self.flag_node[m] == 1:
                    continue

                num_node_for_set[0] = 2
                self.setA[0] = node
                self.setA[1] = m

                for n in self.NetOrig.orig_network_Neighbor(node):
                    if (self.flag_node_lower_std[n] == 1 or n == m or self.flag_node[n] == 1):
                        continue

                    for q in self.NetOrig.orig_network_Neighbor(m):
                        if n > q:
                            break
                        if n == q:
                            self.setB[p] = n
                            p += 1
                            break

                num_node_for_set[1] = p
                total_num_setB = p

                while (num_node_for_set[0] < sizeofclique) and (num_node_for_set[1] > 0):
                    self.intersection(num, num_node_for_set, total_num_setB)
                    num += 1

                if num_node_for_set[0] == sizeofclique:
                    # 构造新clique
                    Count1 = 1
                    Count2 = CLP[sizeofclique-1]["num_of_cliques"]
                    if Count2 >= len(CLP[sizeofclique-1]["MaxClique"]):
                        CLP[sizeofclique -
                            1]["MaxClique"].append([0 for k in range(sizeofclique)])
                    CLP[sizeofclique-1]["MaxClique"][Count2][0] = node

                    for i in range(1, sizeofclique):
                        CLP[sizeofclique-1]["MaxClique"][Count2][Count1] = self.setA[i]
                        Count1 += 1

                    CLP[sizeofclique-1]["num_of_cliques"] += 1
                    num_exist_clique += 1

            self.flag_node[node] = 1

    def maxclique(self, name):

        num_a = 0
        # 根据度升序排序结点
        for i in range(self.NetOrig.orig_network_size()):
            self.node_degree_sequence[i] = i

        self.BubbleSort()

        # CLP初始化
        self.CliqueCount = self.NetOrig.orig_network_degree(
            self.node_degree_sequence[self.NetOrig.orig_network_size()-1])+1

        # {'k': 1, 'num_of_cliques': 0, 'MaxClique': [[结点集], ...]}
        # 用来描述不同k的k-clique信息
        global CLP
        CLP = [{} for i in range(self.CliqueCount)]

        for i in range(self.CliqueCount):
            CLP[i]["k"] = i+1
            CLP[i]["num_of_cliques"] = 0
            CLP[i]["MaxClique"] = []
            CLP[i]["MaxClique"].append([0 for k in range(i+1)])

        # print("排序结束\n")

        # for i in range(self.NetOrig.orig_network_size()):
        #     print("结点 %d 的度是 %d " % (node_degree_sequence[i], self.NetOrig.orig_network_degree(node_degree_sequence[i])))

        # 寻找度为1的clique
        # m = 1
        # while m > 0:
        #     x = self.NetOrig.orig_network_degree(self.node_degree_sequence[m-1])

        #     print("------%d    %d------\n" % (x, self.node_degree_sequence[m-1]))

        #     if (x > 0):
        #         break
        #     elif x == 0:
        #         c = CLP[0]["num_of_cliques"]
        #         if c >= len(CLP[0]["MaxClique"]):
        #             CLP[0]["MaxClique"].append([self.node_degree_sequence[m-1]])
        #         else:
        #             CLP[0]["MaxClique"][c][0] = self.node_degree_sequence[m-1]
        #         CLP[0]["num_of_cliques"] += 1
        #         self.flag_for_whole_clique[self.node_degree_sequence[m-1]] = 1
        #     m += 1

        # Algorithm1
        for k in range(self.NetOrig.orig_network_degree(self.node_degree_sequence[self.NetOrig.orig_network_size()-1])+1, 2, -1):
        # for k in range(15, 0, -1):
            print("------%d-clique------\n" % k)

            # 将目标结点置0
            for p in range(self.NetOrig.orig_network_size()):
                self.flag_node[p] = 0

            c1 = 0
            for i in range(self.NetOrig.orig_network_size()-1, -1, -1):
                x = self.node_degree_sequence[i]
                # 结点的度小于k-1
                if (self.NetOrig.orig_network_degree(x) < k-1):
                    break

                # 结点不属于clique
                if (self.flag_for_whole_clique[x] == 1):
                    c1 += 1
                    continue
                else:
                    for p in range(self.NetOrig.orig_network_size()):
                        self.flag_node_lower_std[p] = 0
                        self.setA[p] = 0
                        self.setB[0] = 0

                    self.Clique(self.node_degree_sequence[i], k, CLP)

            # 删去重复clique
            if CLP[k-1]["num_of_cliques"] > 1:
                f = []
                for i in range(CLP[k-1]["num_of_cliques"]):
                    for j in range(i+1, CLP[k-1]["num_of_cliques"]):
                        if set(CLP[k-1]["MaxClique"][i]) == set(CLP[k-1]["MaxClique"][j]):
                            f.append(j)
                f = list(set(f))
                f.sort()

                for pos in range(len(f)-1, -1, -1):
                    del CLP[k-1]["MaxClique"][f[pos]]
                    CLP[k-1]["num_of_cliques"] -= 1

            # 输出clique
            if CLP[k-1]["num_of_cliques"] > 0:
                for m in range(CLP[k-1]["num_of_cliques"]):
                    print("the "+str(m+1)+" clique:", end=' ')
                    for n in range(k):
                        self.flag_for_whole_clique[CLP[k-1]["MaxClique"][m][n]] = 1
                        print("%d" % CLP[k-1]["MaxClique"][m][n], end='   ')
                    print('\n')

        # 输出所有clique
        # num_a = 1

        # f = open(name+"_clique_node.dat", 'w+', encoding='utf-8')

        # for k in range(self.NetOrig.orig_network_degree(self.node_degree_sequence[self.NetOrig.orig_network_size()-1])):
        #     print("the %d-clique--------number of clique: %d\n" % (k+1, CLP[k]["num_of_cliques"]))

        #     for m in range(CLP[k]["num_of_cliques"]):
        #         f.write(str(num_a)+": ")
        #         num_a += 1
        #         for n in range(k+1):
        #             f.write(str(CLP[k]["MaxClique"][m][n]+1) + "  ")
        #             print(str(CLP[k]["MaxClique"][m][n]+1) + "  ", end = '')
        #         f.write("\n")
        # f.close()
