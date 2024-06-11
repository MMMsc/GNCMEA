import time
import argparse
from parameter import *
from clique_info import CliqueInfo
from clique_network import CliqueNet
from maxcliques import BuildClique
from population import Population
from evaluation import Evaluation
import numpy as np
from build_netInfo import build_netInfo
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from evaluate import *

def run():

    parser = argparse.ArgumentParser(
        description='read data from real or generate networks')
    parser.add_argument(
        '-a', '--attribute', help='real or generate network', required=True, default='r')
    parser.add_argument('-d', '--dataset',
                        help='select a suitable dataset', required=True)
    args = parser.parse_args()
    op1 = args.attribute
    op2 = args.dataset

    inputpath = ""
    inputcommunity = ""
    output_MOD = ""

    if op1 == 'r':
        N, E, M, S = read_net(inputpath)
    elif op1 == 'g':
        N, E, M, S = read_synnet(inputpath)

    varDim = N
    seed = np.random.rand(1, varDim)
    output_path = ""

    M2 = GNN(seed[0], N, M, S)

    buildNet = build_netInfo(N, E, M2)
    buildNet.build_netinfo()

    buildClique = BuildClique(buildNet)
    buildClique.maxclique(output_path)

    cliqueInfo = CliqueInfo(buildNet, buildClique)
    print("building clique network")
    cliqueInfo.construct_clique_network()
    # cliqueInfo.output_clique_network(output_path)

    cliqueNet = CliqueNet(cliqueInfo)
    cliqueNet.parameter_of_clique_network(varDim)

    population = Population(cliqueNet, cliqueInfo)
    evaluation = Evaluation(cliqueInfo, buildNet, population)

    for j in range(20):
        print("\ninitalizing population\n")

        population.init_population()

        for i in range(1, generation+1):
            print("---------------" "%3d/%-3d""---------------" % (i, generation))
            population.evolve_population()

        # population.dump_population(output_path, j)

        evaluation.uoModularity(population.pop, j, output_MOD)
        # real network不需要经过这一步
        if op1 == 'g':
            evaluation.gNMI(population.pop, inputcommunity, j, outputgNMI)

