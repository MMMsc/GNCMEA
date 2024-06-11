from parameter import *
import pandas as pd
import math, time
import random, gc


class Evaluation():

    def __init__(self, cliqueInfo, netOrig, population):

        self.N = cliqueInfo.orig_network_size()
        self.population = population
        self.netOrig = netOrig
        self.MAX_NUM_COMMUNITY_REAL = 3000
        self.MAX_NUM_COMMUNITY_EVAL = 3000
        self.NUM_OF_COMMUNITY = 1000


    '''
    该函数用来评估Modularity作为实验结果
    pop:社区发现的结果
    seq:为了得到稳定的结果，所有网络将会运行无数次，用这个参数来记录运行次数
    mod_name:存储Modularity的运算结果
    '''
    def uoModularity(self, pop, seq, mod_name):

        maxlengthofcomm = 0
        numofnode = 0
        node_overlapping_membership = [0 for i in range(self.N)]
        Mod = [0 for i in range(popsize)]

        path = "%s_%d.dat" % (mod_name, seq)
        f = open(path, 'w+')

        for i in range(popsize):
            Mod[i] = 0
            if maxlengthofcomm < pop[i]["ind"]["comm_n"]:
                maxlengthofcomm = pop[i]["ind"]["comm_n"]

        evalcomm = [{} for i in range(maxlengthofcomm)]

        for i in range(maxlengthofcomm):
            evalcomm[i]["comm"] = [0 for j in range(self.MAX_NUM_COMMUNITY_EVAL)]
            evalcomm[i]["size"] = 0

        for i in range(popsize):
            print("------------calculating Modularity %d / %d--------------" % (i, popsize))
            for j in range(self.N):
                node_overlapping_membership[j] = 0

            # 将community中的clique转换回原始网络形式
            for j in range(pop[i]["ind"]["comm_n"]):
                numofnode, sets = self.population.convert_clique_to_node(pop[i]["ind"]["comm"][j], evalcomm[j]["comm"])
                evalcomm[j]["size"] = numofnode

            for k in range(pop[i]["ind"]["comm_n"]):
                for j in range(evalcomm[k]["size"]):
                    node_overlapping_membership[evalcomm[k]["comm"][j]] += 1

            # 输出划分的community
            # for i in range(maxlengthofcomm):
            #     print(evalcomm[i]["comm"][:evalcomm[i]["size"]])

            A = 0
            for k in range(pop[i]["ind"]["comm_n"]):
                for m in range(evalcomm[k]["size"]):
                    for n in range(evalcomm[k]["size"]):
                        A = 0
                        if m == n:
                            continue
                        if self.netOrig.orig_network_AdjMatrix(evalcomm[k]["comm"][m], evalcomm[k]["comm"][n]) > 0:
                            tmp1 = self.netOrig.orig_network_degree(
                                evalcomm[k]["comm"][m]) * self.netOrig.orig_network_degree(evalcomm[k]["comm"][n])
                            tmp2 = node_overlapping_membership[evalcomm[k]["comm"][m]] * node_overlapping_membership[evalcomm[k]["comm"][n]]
                            A = (self.netOrig.orig_network_AdjMatrix(evalcomm[k]["comm"][m], evalcomm[k]["comm"][n]) - tmp1 / (2*self.netOrig.orig_network_nEdge())) / tmp2

                        Mod[i] += A

            lengthofevalcomm = 0
            for j in range(len(evalcomm)):
                if evalcomm[j]["size"] > 0:
                    lengthofevalcomm += 1

            f.write("%lf\n" % (Mod[i]/(2*self.netOrig.orig_network_nEdge())))

        f.close()

        del Mod
        del node_overlapping_membership
        del evalcomm
        gc.collect()


    def HX_f(self, k):

        p = k / self.N
        if p == 0 or p == 1:
            return 0
        else:
            return -p*math.log(p)-(1-p)*math.log(1-p)


    def intersection_size(self, real, eval):

        num = 0
        m = real["size"]
        n = eval["size"]
        for i in range(m):
            for j in range(n):
                if real["comm"][i] == eval["comm"][j]:
                    num += 1
                    break

        return num


    def gNMI(self, pop, name, seq, gNMI_name):

        max_lengthofvalcomm = 0
        numofnode = 0
        P00 = 0
        P10 = 0
        P01 = 0
        P11 = 0
        H00 = 0
        H10 = 0
        H01 = 0
        H11 = 0
        HX1Y2 = 0
        HY2X1 = 0
        HXY = 0
        HYX = 0
        ave_gNMI = 0

        num = 0
        num1 = 0
        num2 = 0

        k = 0
        realcomm = [{} for i in range(self.NUM_OF_COMMUNITY)]

        path = "%s_%d.dat" % (gNMI_name, seq)

        f = pd.read_csv(name, sep='\t', header=None, names=["Node1", "Node2"])

        fp = open(path, 'w+')

        for i in range(self.NUM_OF_COMMUNITY):
            realcomm[i]["comm"] = [
                0 for j in range(self.MAX_NUM_COMMUNITY_REAL)]
            realcomm[i]["size"] = 0

        lengthofrealcomm = 0

        for i, j in zip(f["Node1"], f["Node2"]):
            num = realcomm[j-1]["size"]
            if j > lengthofrealcomm:
                lengthofrealcomm = j
            realcomm[j-1]["comm"][num] = i - 1
            realcomm[j-1]["size"] += 1

        # 计算所有population中最大的community
        for i in range(popsize):
            if max_lengthofvalcomm < pop[i]["ind"]["comm_n"]:
                max_lengthofvalcomm = pop[i]["ind"]["comm_n"]

        # 初始化evaluations并且存储到evalcomm中
        evalcomm = [{} for i in range(max_lengthofvalcomm)]
        for i in range(max_lengthofvalcomm):
            evalcomm[i]["comm"] = {}
            evalcomm[i]["size"] = 0

        # 初始化NMI的计算参数
        HX = [0 for i in range(max_lengthofvalcomm)]
        HY = [0 for i in range(lengthofrealcomm)]
        nbestc1 = [0 for i in range(max_lengthofvalcomm)]
        nbestc2 = [0 for i in range(lengthofrealcomm)]
        minHXY = [0 for i in range(max_lengthofvalcomm)]
        minHYX = [0 for i in range(lengthofrealcomm)]
        gNMI = [0 for i in range(popsize)]

        for j in range(lengthofrealcomm):
            HY[j] = self.HX_f(realcomm[j]["size"])

        for j in range(max_lengthofvalcomm):
            minHXY[j] = random.randint(32767, 2147483647)

        for j in range(lengthofrealcomm):
            minHYX[j] = random.randint(32767, 2147483647)

        for i in range(popsize):
            print("------------calculating gNMI %d / %d--------------" % (i, popsize))
            if i > 1:
                for c1 in range(pop[i-1]["ind"]["comm_n"]):
                    for j in range(evalcomm[c1]["size"]):
                        evalcomm[c1]["comm"][j] = 0
                    evalcomm[c1]["size"] = 0

            if i > 1:
                for c1 in range(pop[i-1]["ind"]["comm_n"]):
                    HX[c1] = 0
                    minHXY[c1] = random.randint(32767, 2147483647)
                    nbestc1[c1] = 0
                for c2 in range(lengthofrealcomm):
                    minHYX[c2] = random.randint(32767, 2147483647)
                    nbestc2[c2] = 0

            # 将community network转为node networks
            for c1 in range(pop[i]["ind"]["comm_n"]):
                numofnode, _ = self.population.convert_clique_to_node(pop[i]["ind"]["comm"][c1], evalcomm[c1]["comm"])
                evalcomm[c1]["size"] = numofnode
                print(evalcomm[c1])

            for c1 in range(pop[i]["ind"]["comm_n"]):
                HX[c1] = self.HX_f(evalcomm[c1]["size"])

            for c1 in range(pop[i]["ind"]["comm_n"]):
            # for c1 in range(lengthofevalcomm):
                num1 = evalcomm[c1]["size"]
                for c2 in range(lengthofrealcomm):
                    P00 = 0
                    P01 = 0
                    P10 = 0
                    P11 = 0
                    H00 = 0
                    H01 = 0
                    H10 = 0
                    H11 = 0
                    HXY = 0
                    HY2X1 = 0

                    num2 = realcomm[c2]["size"]
                    num = self.intersection_size(evalcomm[c1], realcomm[c2])
                    P11 = (num)/self.N
                    P10 = (num1 - num)/self.N
                    P01 = (num2 - num)/self.N
                    P00 = (self.N - (num1 + num2 - num))/self.N

                    if P11 > 0:
                        H11 = -P11 * math.log(P11)
                    else:
                        H11 = 0
                    if P10 > 0:
                        H10 = -P10 * math.log(P10)
                    else:
                         H10 = 0
                    if P01 > 0:
                        H01 = -P01 * math.log(P01)
                    else:
                        H01 = 0
                    if P00 > 0:
                        H00 = -P00 * math.log(P00)
                    else:
                        H00 = 0

                    HX1Y2 = (H11+H10+H01+H00) - HY[c2]
                    HY2X1 = (H11+H10+H01+H00) - HX[c1]

                    if (H11+H00) > (H01+H10):
                        nbestc1[c1] += 1
                        if HX1Y2 < minHXY[c1]:
                            minHXY[c1] = HX1Y2
                            nbestc2[c2] += 1
                        if HY2X1 < minHYX[c2]:
                            minHYX[c2] = HY2X1

            # 计算H(X|Y)和H(Y|X)
            for c1 in range(k):
                if nbestc1[c1]>0 and HX[c1]>0:
                    HXY = HXY + minHXY[c1] / HX[c1]
                else:
                    HXY = HXY + 1
            HXY = HXY / (pop[i]["ind"]["comm_n"])

            for c2 in range(lengthofrealcomm):
                if nbestc2[c2]>0 and HY[c2]>0:
                    HYX = HYX + minHYX[c2] / HY[c2]
                else:
                    HYX = HYX + 1
            HYX = HYX / lengthofrealcomm

            gNMI[i] = 1 - (HXY + HYX) / 2
            gNMI[i] *= math.exp(-(abs(lengthofrealcomm-pop[i]["ind"]["comm_n"])/lengthofrealcomm))

            fp.write("%lf\n" % gNMI[i])

        # for i in range(popsize):
        #     ave_gNMI += gNMI[i]
        # ave_gNMI = ave_gNMI / popsize

        # fp.write("%lf\n" % ave_gNMI)

        # fp.close()

        del HX
        del HY
        del nbestc1
        del nbestc2
        del minHXY
        del minHYX
        del gNMI
        del realcomm
        del evalcomm
        gc.collect()
