import random, gc, time
from parameter import *
from operators import Operator
from individual import Individual
from community import Community


class Population():

    def __init__(self, cliqueNet, cliqueInfo):

        self.cliqueNet = cliqueNet
        self.cliqueInfo = cliqueInfo
        self.community = Community(cliqueNet)
        self.individual = Individual(cliqueNet, self.community)
        self.operator = Operator(cliqueNet, self.community, self.individual)

        self.n = self.cliqueNet.network_size()
        self.orig_n = self.cliqueInfo.orig_network_size()
        self.pop = [{} for i in range(popsize)]

        self.perm = [i for i in range(self.n)]
        self.ref = [-1, -1]

    def shuffle(self):

        for i in range(self.n):
            try:
                j = random.randint(i, self.n-i+1)
                if i != j:
                    self.perm[i], self.perm[j] = self.perm[j], self.perm[i]
            except (ValueError, IndexError):
                continue

    def population_info(self, p):

        print("[%04d]" % p["id"], end = '  ')
        print("(%.5lf) " % p["lambda"], end='  ')
        print("f=(%.2lf,%.2lf) " %
              (p["ind"]["obj"][0], p["ind"]["obj"][1]), end='  ')
        print("#%-5d" % p["ind"]["comm_n"])

    def init_population(self):

        self.lamdba = [random.random() for i in range(popsize)]
        self.lamdba.sort()

        for i in range(popsize):
            random.shuffle(self.perm) # 随机初始化
            self.pop[i]["id"] = i
            self.pop[i]["ind"] = self.operator.decode(self.perm)

            self.pop[i]["lambda"] = self.lamdba[i]
            self.pop[i]["neighbor"] = []
            # print("------------gene: after decoding--------------")
            # print(self.pop[i]["ind"]["gene"])

        # 设置邻居的范围i-T/2~i+T/2
        for i in range(popsize):

            l = int(i - T / 2)
            h = int(i + T / 2)

            if l < 0:
                l = 0
                h = T-1
            if h >= popsize:
                h = popsize - 1
                l = popsize - T

            # 寻找lambda更好的neighbor范围
            while l > 0 and (self.pop[i]["lambda"]-self.pop[l-1]["lambda"] < self.pop[h]["lambda"]-self.pop[i]["lambda"]):
                l -= 1
                h -= 1

            while h < popsize-1 and (self.pop[i]["lambda"]-self.pop[l]["lambda"] > self.pop[h+1]["lambda"]-self.pop[i]["lambda"]):
                l += 1
                h += 1

            self.pop[i]["neighbor"] = [i for i in range(l, popsize)]

        self.ref[0] = self.pop[0]["ind"]["obj"][0]
        self.ref[1] = self.pop[0]["ind"]["obj"][1]

        for i in range(1, popsize):

            if self.pop[i]["ind"]["obj"][0] < self.ref[0]:
                self.ref[0] = self.pop[i]["ind"]["obj"][0]

            if self.pop[i]["ind"]["obj"][1] < self.ref[1]:
                self.ref[1] = self.pop[i]["ind"]["obj"][1]

        # for i in range(popsize):
        #     self.population_info(self.pop[i])

        print("KKM: %f" % (self.ref[0]))
        print("RC: %f\n" % (self.ref[1]))


    def update_pop_neighbor(self, pop_tmp, ind):

        # nbs是neighbor构成的list，根据id在self.pop中查询邻居信息
        nbs = pop_tmp["neighbor"]

        for i in range(T):
            lamdba = self.pop[nbs[i]]["lambda"]

            f_old = self.individual.tchebycheff(self.pop[nbs[i]]["ind"], self.ref, lamdba)
            f_new = self.individual.tchebycheff(ind, self.ref, lamdba)

            if f_new<f_old:
                self.pop[nbs[i]]["ind"] = self.individual.set_individual(self.pop[nbs[i]]["ind"])

                # self.population_info(self.pop[nbs[i]])

        return pop_tmp

    def evolve_population(self):

        for i in range(popsize):
            # 随机选择一个交叉
            j = random.randint(0, T-1)
            while(i == j or j > len(self.pop[i]["neighbor"])):
                j = random.randint(0, T-1)

            # 随机neighbor在list中的位置
            n_pos = self.pop[i]["neighbor"][j]

            child = self.operator.crossover(self.pop[i]["ind"], self.pop[n_pos]["ind"])
            child = self.operator.mutation(child)

            # 存在child为tuple，暂时不清楚产生原因
            if type(child) == tuple:
                child = child[0]

            if child["obj"][0] < self.ref[0]:
                self.ref[0] = child["obj"][0]
            if child["obj"][1] < self.ref[1]:
                self.ref[1] = child["obj"][1]

            self.pop[i] = self.update_pop_neighbor(self.pop[i], child)

            del(child)
            gc.collect()


    def convert_clique_to_node(self, comm, set):

        num = 0

        for i in range(self.cliqueInfo.num_of_clique_node(comm["member"][0])):
            set[num] = self.cliqueInfo.node_of_clique(comm["member"][0])[i]
            num += 1

        for pos in range(1, len(comm["member"])):
            tmp = 0

            for i in range(self.cliqueInfo.num_of_clique_node(comm["member"][pos])):
                flag = 0
                for j in range(num):
                    if self.cliqueInfo.node_of_clique(comm["member"][pos])[i] == set[j]:
                        flag = 1
                        break
                if flag == 1:
                    continue
                else:
                    set[num+tmp] = self.cliqueInfo.node_of_clique(comm["member"][pos])[i]
                    tmp += 1

            num += tmp

        return num, set


    def dump_pop(self, path, pop, set):

        f = open(path, 'w+')

        f.write("#id       %d\n" % (pop["id"]))
        f.write("#lambda   %lf\n" % (pop["lambda"]))
        f.write("#comm_in  %lf\n" % (pop["ind"]["obj"][0]))
        f.write("#comm_out %lf\n" % (pop["ind"]["obj"][1]))
        f.write("#number   %d\n" % (pop["ind"]["comm_n"]))

        for j in range(pop["ind"]["comm_n"]):
            numofnode = 0
            for k in range(self.orig_n):
                set[k] = 0

            numofnode, set = self.convert_clique_to_node(
                pop["ind"]["comm"][j], set)

            f.write("#community %d size %d\n" % (j, numofnode))

            for k in range(numofnode):
                f.write("%d\n" % (set[k]+1))

        f.close()

    # 存储population
    def dump_population(self, output_path, m):

        set_output = [0 for i in range(self.orig_n)]

        for i in range(popsize):

            self.population_info(self.pop[i])
            print("-------------saving  %d  population-----------" % (i+1))
            path = "%s_%04d_%02d.dat" % (output_path, i, m)
            self.dump_pop(path, self.pop[i], set_output)

        del set_output
        gc.collect()


