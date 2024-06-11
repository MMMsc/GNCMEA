class Individual():

    def __init__(self, cliqueNet, community):

        self.community = community
        self.N = cliqueNet.network_size()

    def eval_individual(self, ind):

        n = ind["comm_n"]
        comm = ind["comm"]
        temp = 0.0
        ind["obj"] = [0.0, 0.0]

        for i in range(n):
            pin = comm[i]["Pin"]
            pout = comm[i]["Pout"]
            m = comm[i]["size"]
            temp += (pin/m)
            ind["obj"][1] += (pout/m)

        ind["obj"][0] = 2*(self.N-n) - temp

        return ind

    def new_individual(self, gene):

        ind = {}
        ind["gene"] = gene
        ind["comm"] = [{} for i in range(self.N)]
        # 为什么将新初始化的ind["comm"]传入
        # 通过label生成community
        gene, ind["comm"], ind["comm_n"] = self.community.label_to_community(gene, ind["comm"])

        self.eval_individual(ind)

        ind["refcount"] = 1
        return ind

    def set_individual(self, d):

        d["refcount"] += 1

        return d

    def tchebycheff(self, ind, ref, lamdba):

        lp = lamdba  # lambda_pos
        ln = 1 - lamdba  # lambda_neg as lp+ln===1
        fp = ind["obj"][0]  # f_pos_in
        fn = ind["obj"][1]  # f_neg_out
        rp = ref[0]  # f_pos_in_ref
        rn = ref[1]  # f_neg_out_ref

        t1 = lp * (fp-rp)
        t2 = ln * (fn-rn)

        if t1>t2:
            return t1
        else:
            return t2


