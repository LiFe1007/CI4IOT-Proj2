import simpful as sf
import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def initialize_fuzzy_dict():
    MU_pnts, deltaMU_pnts, Load_pnts, deltaLoad_pnts, BW_pnts, Ltncy_pnts, pMU_pnts, pLoad_pnts, hw_pnts, netAvailb_pnts = membershipFunctions()
    predMU_rules, predLoad_rules, netAvailb_rules, hwAvailb_rules, clpv_rules = create_rules()

    # Legenda do dicionario =
    # 'key' : Fuzzy_name_1, Fuzzy_name_2, points_list_1, points_list_2, sf.FuzzySystem(),
    # output function or value for low medium high, rules, output value result, input value 1, input value 2
    f_dict = {
        'predMemUsage': ['MemUsage', 'deltaMemUsage', MU_pnts, deltaMU_pnts, sf.FuzzySystem(show_banner=False),
                         [0, 50, 100], predMU_rules, None, None, None],

        'predLoad': ['Load', 'deltaLoad', Load_pnts, deltaLoad_pnts, sf.FuzzySystem(show_banner=False), [0, 50, 100],
                     predLoad_rules, None, None, None],

        'netAvailb': ['Bandwidth', 'Latency', BW_pnts, Ltncy_pnts, sf.FuzzySystem(show_banner=False), [0, 50, 100],
                      netAvailb_rules, None, None, None],

        'hwAvailb': ['predMemUsage', 'predLoad', pMU_pnts, pLoad_pnts, sf.FuzzySystem(show_banner=False), [0, 50, 100],
                     hwAvailb_rules, None],

        'CLPV': ['hwAvailb', 'netAvailb', hw_pnts, netAvailb_pnts, sf.FuzzySystem(show_banner=False), [0, 40, 90],
                 clpv_rules, None]
    }
    return f_dict


def membershipFunctions():
    MU_pnts_list = [
        [[0., 1], [20., 1], [60., 0]],  # Points for 'low'
        [[10., 0], [50., 1], [65., 1], [85., 0]],  # Points for 'medium'
        [[60., 0], [80., 1], [100., 1]]  # Points for 'high'
    ]

    deltaMU_pnts_list = [
        [[0., 0], [0., 1], [50., 0]],  # Points for 'low'
        [[10., 0], [50., 1], [50., 1], [90., 0]],  # Points for 'medium'
        [[50., 0], [100., 1], [100., 1]]  # Points for 'high'
    ]

    Load_pnts_list = [
        [[0., 1], [20., 1], [60., 0]],  # Points for 'low'
        [[10., 0], [50., 1], [75., 1], [95., 0]],  # Points for 'medium'
        [[70., 0], [90., 1], [100., 1]]  # Points for 'high'
    ]

    deltaLoad_pnts_list = [
        [[0., 0], [0., 1], [50., 0]],  # Points for 'low'
        [[10., 0], [50., 1], [50., 1], [90., 0]],  # Points for 'medium'
        [[50., 0], [100., 1], [100., 1]]  # Points for 'high'
    ]

    BW_pnts_list = [
        [[0., 1], [20., 1], [50., 0]],  # Points for 'low'
        [[10., 0], [45., 1], [55., 1], [90., 0]],  # Points for 'medium'
        [[50., 0], [80., 1], [100., 1]]  # Points for 'high'
    ]

    Ltncy_pnts_list = [
        [[0., 1], [20., 1], [50., 0]],  # Points for 'low'
        [[10., 0], [45., 1], [55., 1], [90., 0]],  # Points for 'medium'
        [[50., 0], [80., 1], [100., 1]]  # Points for 'high'
    ]

    pMU_pnts_list = [
        [[0., 1], [30., 1], [60., 0]],  # Points for 'low'
        [[10., 0], [50., 1], [65., 1], [90., 0]],  # Points for 'medium'
        [[60., 0], [80., 1], [100., 1]]  # Points for 'high'
    ]

    pLoad_pnts_list = [
        [[0., 1], [30., 1], [60., 0]],  # Points for 'low'
        [[10., 0], [50., 1], [65., 1], [90., 0]],  # Points for 'medium'
        [[60., 0], [80., 1], [100., 1]]  # Points for 'high'
    ]

    hw_pnts_list = [
        [[0., 1], [30., 1], [60., 0]],  # Points for 'low'
        [[10., 0], [50., 1], [65., 1], [100., 0]],  # Points for 'medium'
        [[60., 0], [80., 1], [100., 1]]  # Points for 'high'
    ]

    netAvailb_pnts_list = [
        [[0., 1], [30., 1], [60., 0]],  # Points for 'low'
        [[10., 0], [50., 1], [65., 1], [100., 0]],  # Points for 'medium'
        [[60., 0], [80., 1], [100., 1]]  # Points for 'high'
    ]

    return MU_pnts_list, deltaMU_pnts_list, Load_pnts_list, deltaLoad_pnts_list, BW_pnts_list, Ltncy_pnts_list, pMU_pnts_list, pLoad_pnts_list, hw_pnts_list, netAvailb_pnts_list


def create_rules():
    # Memory usage x Memory usage variation
    predMU = [
        f'IF (deltaMemUsage IS low_deltaMemUsage) AND (MemUsage IS low_MemUsage) THEN (predMemUsage IS LOW)',
        f'IF (deltaMemUsage IS low_deltaMemUsage) AND (MemUsage IS medium_MemUsage) THEN (predMemUsage IS LOW)',
        f'IF (deltaMemUsage IS low_deltaMemUsage) AND (MemUsage IS high_MemUsage) THEN (predMemUsage IS MEDIUM)',

        f'IF (deltaMemUsage IS medium_deltaMemUsage) AND (MemUsage IS low_MemUsage) THEN (predMemUsage IS LOW)',
        f'IF (deltaMemUsage IS medium_deltaMemUsage) AND (MemUsage IS medium_MemUsage) THEN (predMemUsage IS MEDIUM)',
        f'IF (deltaMemUsage IS medium_deltaMemUsage) AND (MemUsage IS high_MemUsage) THEN (predMemUsage IS HIGH)',

        f'IF (deltaMemUsage IS high_deltaMemUsage) AND (MemUsage IS low_MemUsage) THEN (predMemUsage IS MEDIUM)',
        f'IF (deltaMemUsage IS high_deltaMemUsage) AND (MemUsage IS medium_MemUsage) THEN (predMemUsage IS HIGH)',
        f'IF (deltaMemUsage IS high_deltaMemUsage) AND (MemUsage IS high_MemUsage) THEN (predMemUsage IS HIGH)'
    ]

    # Processor load x Processor load variation
    predLoad = [
        f'IF (deltaLoad IS low_deltaLoad) AND (Load IS low_Load) THEN (predLoad IS LOW)',
        f'IF (deltaLoad IS low_deltaLoad) AND (Load IS medium_Load) THEN (predLoad IS MEDIUM)',
        f'IF (deltaLoad IS low_deltaLoad) AND (Load IS high_Load) THEN (predLoad IS HIGH)',

        f'IF (deltaLoad IS medium_deltaLoad) AND (Load IS low_Load) THEN (predLoad IS LOW)',
        f'IF (deltaLoad IS medium_deltaLoad) AND (Load IS medium_Load) THEN (predLoad IS MEDIUM)',
        f'IF (deltaLoad IS medium_deltaLoad) AND (Load IS high_Load) THEN (predLoad IS HIGH)',

        f'IF (deltaLoad IS high_deltaLoad) AND (Load IS low_Load) THEN (predLoad IS MEDIUM)',
        f'IF (deltaLoad IS high_deltaLoad) AND (Load IS medium_Load) THEN (predLoad IS HIGH)',
        f'IF (deltaLoad IS high_deltaLoad) AND (Load IS high_Load) THEN (predLoad IS HIGH)'
    ]

    # Bandwidth x Latency
    netAvailb = [
        f'IF (Bandwidth IS low_Bandwidth) AND (Latency IS high_Latency) THEN (netAvailb IS LOW)',
        f'IF (Bandwidth IS medium_Bandwidth) AND (Latency IS medium_Latency) THEN (netAvailb IS MEDIUM)',
        f'IF (Bandwidth IS high_Bandwidth) AND (Latency IS low_Latency) THEN (netAvailb IS HIGH)',

        f'IF (Bandwidth IS low_Bandwidth) AND (Latency IS low_Latency) THEN (netAvailb IS LOW)',
        f'IF (Bandwidth IS low_Bandwidth) AND (Latency IS medium_Latency) THEN (netAvailb IS LOW)',

        f'IF (Bandwidth IS medium_Bandwidth) AND (Latency IS low_Latency) THEN (netAvailb IS HIGH)',
        f'IF (Bandwidth IS medium_Bandwidth) AND (Latency IS high_Latency) THEN (netAvailb IS LOW)',

        f'IF (Bandwidth IS high_Bandwidth) AND (Latency IS high_Latency) THEN (netAvailb IS MEDIUM)',
        f'IF (Bandwidth IS high_Bandwidth) AND (Latency IS medium_Latency) THEN (netAvailb IS MEDIUM)'

    ]

    # Predicted processor load x Predicted memory usage
    hwAvailb = [
        f'IF (predMemUsage IS low_predMemUsage) AND (predLoad IS low_predLoad) THEN (hwAvailb IS HIGH)',
        f'IF (predMemUsage IS low_predMemUsage) AND (predLoad IS medium_predLoad) THEN (hwAvailb IS MEDIUM)',
        f'IF (predMemUsage IS low_predMemUsage) AND (predLoad IS high_predLoad) THEN (hwAvailb IS LOW)',

        f'IF (predMemUsage IS medium_predMemUsage) AND (predLoad IS low_predLoad) THEN (hwAvailb IS HIGH)',
        f'IF (predMemUsage IS medium_predMemUsage) AND (predLoad IS medium_predLoad) THEN (hwAvailb IS MEDIUM)',
        f'IF (predMemUsage IS medium_predMemUsage) AND (predLoad IS high_predLoad) THEN (hwAvailb IS LOW)',

        f'IF (predMemUsage IS high_predMemUsage) AND (predLoad IS low_predLoad) THEN (hwAvailb IS LOW)',
        f'IF (predMemUsage IS high_predMemUsage) AND (predLoad IS medium_predLoad) THEN (hwAvailb IS LOW)',
        f'IF (predMemUsage IS high_predMemUsage) AND (predLoad IS high_predLoad) THEN (hwAvailb IS LOW)'
    ]

    # Hardware availability x Network availability
    clpv = [
        f'IF (hwAvailb IS low_hwAvailb) AND (netAvailb IS low_netAvailb) THEN (CLPV IS MEDIUM)',
        f'IF (hwAvailb IS low_hwAvailb) AND (netAvailb IS medium_netAvailb) THEN (CLPV IS LOW)',
        f'IF (hwAvailb IS low_hwAvailb) AND (netAvailb IS high_netAvailb) THEN (CLPV IS LOW)',

        f'IF (hwAvailb IS medium_hwAvailb) AND (netAvailb IS low_netAvailb) THEN (CLPV IS HIGH)',
        f'IF (hwAvailb IS medium_hwAvailb) AND (netAvailb IS medium_netAvailb) THEN (CLPV IS HIGH)',
        f'IF (hwAvailb IS medium_hwAvailb) AND (netAvailb IS high_netAvailb) THEN (CLPV IS MEDIUM)',

        f'IF (hwAvailb IS high_hwAvailb) AND (netAvailb IS low_netAvailb) THEN (CLPV IS HIGH)',
        f'IF (hwAvailb IS high_hwAvailb) AND (netAvailb IS medium_netAvailb) THEN (CLPV IS HIGH)',
        f'IF (hwAvailb IS high_hwAvailb) AND (netAvailb IS high_netAvailb) THEN (CLPV IS HIGH)'
    ]

    return predMU, predLoad, netAvailb, hwAvailb, clpv


def create_fuzzies(fuzz_dict, terms):
    for fuzz_key in fuzz_dict:
        key_vars_1 = [sf.FuzzySet(points=fuzz_dict[fuzz_key][2][i], term=f"{terms[i]}_{fuzz_dict[fuzz_key][0]}")
                      for i in range(3)]

        key_vars_2 = [sf.FuzzySet(points=fuzz_dict[fuzz_key][3][i], term=f"{terms[i]}_{fuzz_dict[fuzz_key][1]}")
                      for i in range(3)]

        fuzz_dict[fuzz_key][4].add_linguistic_variable(fuzz_dict[fuzz_key][0], sf.LinguisticVariable(key_vars_1))
        fuzz_dict[fuzz_key][4].add_linguistic_variable(fuzz_dict[fuzz_key][1], sf.LinguisticVariable(key_vars_2))

        for i, term in enumerate(terms):
            if isinstance(fuzz_dict[fuzz_key][5][i], int) or isinstance(fuzz_dict[fuzz_key][5][i], float):
                fuzz_dict[fuzz_key][4].set_crisp_output_value(term.upper(), fuzz_dict[fuzz_key][5][i])
            elif isinstance(fuzz_dict[fuzz_key][5][i], str):
                fuzz_dict[fuzz_key][4].set_output_function(term.upper(), fuzz_dict[fuzz_key][5][i])

        fuzz_dict[fuzz_key][4].add_rules(fuzz_dict[fuzz_key][6])
        """        
        fuzz_dict[key][1].set_crisp_output_value("LOW", dict[key][2][0])
        fuzz_dict[key][1].set_crisp_output_value("MEDIUM", dict[key][2][1])
        fuzz_dict[key][1].set_crisp_output_value("HIGH", dict[key][2][2])
        """
    return fuzz_dict


def normalize(value, min_value=0, max_value=100):
    for i in range(101):
        normalized_value = (2 * (value - min_value) / (max_value - min_value)) - 1
    return normalized_value


def TestMe(filename):
    df = pd.read_csv(filename)
    return df


if __name__ == '__main__':

    rows = TestMe("Project2_SampleData.csv")

    terms = ['low', 'medium', 'high']

    fuzzy_dict = initialize_fuzzy_dict()
    create_fuzzies(fuzzy_dict, terms)

    for i in range(len(rows.index)):  # Itinerate the file to calculate the CLPV for each line

        print(f'-------------{i+1}---------------')

        fuzzy_dict['predMemUsage'][8] = rows["MemoryUsage"][i] * 100
        fuzzy_dict['predMemUsage'][9] = rows["V_MemoryUsage"][i] * 100

        fuzzy_dict['predLoad'][8] = rows["ProcessorLoad"][i] * 100
        fuzzy_dict['predLoad'][9] = rows["V_ProcessorLoad"][i] * 100

        fuzzy_dict['netAvailb'][8] = rows["OutBandwidth"][i] * 100
        fuzzy_dict['netAvailb'][9] = rows["Latency"][i] * 100

        for fuzzkey in fuzzy_dict:

            if fuzzkey == 'hwAvailb':
                fuzzy_dict[fuzzkey][4].set_variable(fuzzy_dict[fuzzkey][0], fuzzy_dict['predMemUsage'][7])
                fuzzy_dict[fuzzkey][4].set_variable(fuzzy_dict[fuzzkey][1], fuzzy_dict['predLoad'][7])

            elif fuzzkey == 'CLPV':
                fuzzy_dict[fuzzkey][4].set_variable(fuzzy_dict[fuzzkey][0], fuzzy_dict['hwAvailb'][7])
                fuzzy_dict[fuzzkey][4].set_variable(fuzzy_dict[fuzzkey][1], fuzzy_dict['netAvailb'][7])

            else:
                fuzzy_dict[fuzzkey][4].set_variable(fuzzy_dict[fuzzkey][0], fuzzy_dict[fuzzkey][8])
                fuzzy_dict[fuzzkey][4].set_variable(fuzzy_dict[fuzzkey][1], fuzzy_dict[fuzzkey][9])

            fuzzy_dict[fuzzkey][7] = fuzzy_dict[fuzzkey][4].Sugeno_inference([fuzzkey])[fuzzkey]
            fuzzy_dict[fuzzkey][7] = math.floor(fuzzy_dict[fuzzkey][7] * 100) / 100
            print(f'======{fuzzkey} = {fuzzy_dict[fuzzkey][7]}')

        normalized = normalize(fuzzy_dict['CLPV'][7])
        # print(f'CLPV variation = {normalized}\n\n\n\n')
        print(f'CLPV calculated = {normalized}')
        if "CLPVariation" in rows:
            print(f'CLPV expected = {rows["CLPVariation"][i]}')
        print("\n\n\n\n")

    # fuzzy_dict['predMemUsage'][4].plot_variable('MemUsage')
    # fuzzy_dict['predMemUsage'][4].plot_variable('deltaMemUsage')
    #
    # fuzzy_dict['predLoad'][4].plot_variable('Load')
    # fuzzy_dict['predLoad'][4].plot_variable('deltaLoad')
    #
    # fuzzy_dict['netAvailb'][4].plot_variable('Bandwidth')
    # fuzzy_dict['netAvailb'][4].plot_variable('Latency')
    #
    # fuzzy_dict['hwAvailb'][4].plot_variable('predMemUsage')
    # fuzzy_dict['hwAvailb'][4].plot_variable('predLoad')
    #
    # fuzzy_dict['CLPV'][4].plot_variable('netAvailb')
    # fuzzy_dict['CLPV'][4].plot_variable('hwAvailb')

    # fuzzy_dict['CLPV'][4].plot_surface(variables=['hwAvailb', 'netAvailb'], output='CLPV')
    # plt.show()

