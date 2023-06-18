import simpful as sf
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def membershipFunctions():
    MU_pnts_list = [
        [[0., 1], [50., 1], [60., 0]],  # Points for 'low'
        [[20., 0], [50., 1], [80., 1], [85., 0]],  # Points for 'medium'
        [[75., 0], [90., 1], [100., 1]]  # Points for 'high'
    ]

    deltaMU_pnts_list = [
        [[0., 1], [50., 1], [60., 0]],  # Points for 'low'
        [[20., 0], [50., 1], [80., 1], [85., 0]],  # Points for 'medium'
        [[75., 0], [90., 1], [100., 1]]  # Points for 'high'
    ]

    Load_pnts_list = [
        [[0., 1], [50., 1], [60., 0]],  # Points for 'low'
        [[20., 0], [50., 1], [80., 1], [85., 0]],  # Points for 'medium'
        [[75., 0], [90., 1], [100., 1]]  # Points for 'high'
    ]

    deltaLoad_pnts_list = [
        [[0., 1], [50., 1], [60., 0]],  # Points for 'low'
        [[20., 0], [50., 1], [80., 1], [85., 0]],  # Points for 'medium'
        [[75., 0], [90., 1], [100., 1]]  # Points for 'high'
    ]

    BW_pnts_list = [
        [[0., 1], [50., 1], [60., 0]],  # Points for 'low'
        [[20., 0], [50., 1], [80., 1], [85., 0]],  # Points for 'medium'
        [[75., 0], [90., 1], [100., 1]]  # Points for 'high'
    ]

    Ltncy_pnts_list = [
        [[0., 1], [50., 1], [60., 0]],  # Points for 'low'
        [[20., 0], [50., 1], [80., 1], [85., 0]],  # Points for 'medium'
        [[75., 0], [90., 1], [100., 1]]  # Points for 'high'
    ]

    pMU_pnts_list = [
        [[0., 1], [50., 1], [60., 0]],  # Points for 'low'
        [[20., 0], [50., 1], [80., 1], [85., 0]],  # Points for 'medium'
        [[75., 0], [90., 1], [100., 1]]  # Points for 'high'
    ]

    pLoad_pnts_list = [
        [[0., 1], [50., 1], [60., 0]],  # Points for 'low'
        [[20., 0], [50., 1], [80., 1], [85., 0]],  # Points for 'medium'
        [[75., 0], [90., 1], [100., 1]]  # Points for 'high'
    ]

    hw_pnts_list = [
        [[0., 1], [50., 1], [60., 0]],  # Points for 'low'
        [[20., 0], [50., 1], [80., 1], [85., 0]],  # Points for 'medium'
        [[75., 0], [90., 1], [100., 1]]  # Points for 'high'
    ]

    netAvailb_pnts_list = [
        [[0., 1], [50., 1], [60., 0]],  # Points for 'low'
        [[20., 0], [50., 1], [80., 1], [85., 0]],  # Points for 'medium'
        [[75., 0], [90., 1], [100., 1]]  # Points for 'high'
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
        f'IF (deltaLoad IS low_deltaLoad) AND (Load IS medium_Load) THEN (predLoad IS LOW)',
        f'IF (deltaLoad IS low_deltaLoad) AND (Load IS high_Load) THEN (predLoad IS MEDIUM)',

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
        f'IF (Bandwidth IS low_Bandwidth) AND (Latency IS medium_Latency) THEN (netAvailb IS MEDIUM)',

        f'IF (Bandwidth IS medium_Bandwidth) AND (Latency IS low_Latency) THEN (netAvailb IS HIGH)',
        f'IF (Bandwidth IS medium_Bandwidth) AND (Latency IS high_Latency) THEN (netAvailb IS LOW)',

        f'IF (Bandwidth IS high_Bandwidth) AND (Latency IS high_Latency) THEN (netAvailb IS LOW)',
        f'IF (Bandwidth IS high_Bandwidth) AND (Latency IS medium_Latency) THEN (netAvailb IS MEDIUM)'

    ]

    # Predicted processor load x Predicted memory usage
    hwAvailb = [
        f'IF (predMemUsage IS low_predMemUsage) AND (predLoad IS low_predLoad) THEN (hwAvailb IS HIGH)',
        f'IF (predMemUsage IS low_predMemUsage) AND (predLoad IS medium_predLoad) THEN (hwAvailb IS MEDIUM)',
        f'IF (predMemUsage IS low_predMemUsage) AND (predLoad IS high_predLoad) THEN (hwAvailb IS MEDIUM)',

        f'IF (predMemUsage IS medium_predMemUsage) AND (predLoad IS low_predLoad) THEN (hwAvailb IS HIGH)',
        f'IF (predMemUsage IS medium_predMemUsage) AND (predLoad IS medium_predLoad) THEN (hwAvailb IS MEDIUM)',
        f'IF (predMemUsage IS medium_predMemUsage) AND (predLoad IS high_predLoad) THEN (hwAvailb IS LOW)',

        f'IF (predMemUsage IS high_predMemUsage) AND (predLoad IS low_predLoad) THEN (hwAvailb IS MEDIUM)',
        f'IF (predMemUsage IS high_predMemUsage) AND (predLoad IS medium_predLoad) THEN (hwAvailb IS LOW)',
        f'IF (predMemUsage IS high_predMemUsage) AND (predLoad IS high_predLoad) THEN (hwAvailb IS LOW)'
    ]

    # Hardware availability x Network availability
    clpv = [
        f'IF (hwAvailb IS low_hwAvailb) AND (netAvailb IS low_netAvailb) THEN (CLPV IS MEDIUM)',
        f'IF (hwAvailb IS low_hwAvailb) AND (netAvailb IS medium_netAvailb) THEN (CLPV IS HIGH)',
        f'IF (hwAvailb IS low_hwAvailb) AND (netAvailb IS high_netAvailb) THEN (CLPV IS HIGH)',

        f'IF (hwAvailb IS medium_hwAvailb) AND (netAvailb IS low_netAvailb) THEN (CLPV IS LOW)',
        f'IF (hwAvailb IS medium_hwAvailb) AND (netAvailb IS medium_netAvailb) THEN (CLPV IS MEDIUM)',
        f'IF (hwAvailb IS medium_hwAvailb) AND (netAvailb IS high_netAvailb) THEN (CLPV IS MEDIUM)',

        f'IF (hwAvailb IS high_hwAvailb) AND (netAvailb IS low_netAvailb) THEN (CLPV IS LOW)',
        f'IF (hwAvailb IS high_hwAvailb) AND (netAvailb IS medium_netAvailb) THEN (CLPV IS MEDIUM)',
        f'IF (hwAvailb IS high_hwAvailb) AND (netAvailb IS high_netAvailb) THEN (CLPV IS LOW)'
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

        """        
        fuzz_dict[key][1].set_crisp_output_value("LOW", dict[key][2][0])
        fuzz_dict[key][1].set_crisp_output_value("MEDIUM", dict[key][2][1])
        fuzz_dict[key][1].set_crisp_output_value("HIGH", dict[key][2][2])
        """
    return fuzz_dict


def set_rules(fuzz_dict):
    for fuzz_key in fuzz_dict:
        fuzz_dict[fuzz_key][4].add_rules(fuzz_dict[fuzz_key][6])

    return fuzz_dict


def aggregate_fuzzies(aggr_dict):
    for fuzz_key in aggr_dict:
        fuzzy_one_vars = [sf.FuzzySet(points=aggr_dict[fuzz_key][0], term=f'{aggr_dict[fuzz_key][3]}')]
        fuzzy_two_vars = [sf.FuzzySet(points=aggr_dict[fuzz_key][1], term=f'{aggr_dict[fuzz_key][4]}')]

        aggr = sf.fuzzy_aggregation.FuzzyAggregator(verbose=True)
        aggr.add_variables(*fuzzy_one_vars, *fuzzy_two_vars)

        aggr.set_variable(aggr_dict[fuzz_key][3], aggr_dict[fuzz_key][5])
        aggr.set_variable(aggr_dict[fuzz_key][4], aggr_dict[fuzz_key][6])

        aggr_dict[fuzz_key][2] = aggr.aggregate([aggr_dict[fuzz_key][3], aggr_dict[fuzz_key][4]],
                                                aggregation_fun='arit_mean')

        print(f'aggr === {aggr_dict[fuzz_key][2]}')

    return aggr_dict


if __name__ == '__main__':
    terms = ['low', 'medium', 'high']
    MU_pnts, deltaMU_pnts, Load_pnts, deltaLoad_pnts, BW_pnts, Ltncy_pnts, pMU_pnts, pLoad_pnts, hw_pnts, netAvailb_pnts = membershipFunctions()

    FS_MU = sf.FuzzySystem()
    FS_Load = sf.FuzzySystem()
    FS_netAvailb = sf.FuzzySystem()
    FS_hw = sf.FuzzySystem()
    FS_clpv = sf.FuzzySystem()

    # just creating output variables 4 each fuzzy
    pMU_result = 0
    pLoad_result = 0
    netAvailb_result = 0
    hwAvailb_result = 0
    clpv_result = 0

    predMU_rules, predLoad_rules, netAvailb_rules, hwAvailb_rules, clpv_rules = create_rules()

    # Legenda do dicionario =
    # 'key' : Fuzzy_name_1, Fuzzy_name_2, points_list_1, points_list_2, sf.FuzzySystem(),
    # output function or value for low medium high, rules, output value result
    fuzzy_dict = {
        'predMemUsage': ['MemUsage', 'deltaMemUsage', MU_pnts, deltaMU_pnts, FS_MU, [5, 25, 100],
                         predMU_rules, pMU_result],
        
        'predLoad': ['Load', 'deltaLoad', Load_pnts, deltaLoad_pnts, FS_Load, [7, 27, 98], predLoad_rules,
                     pLoad_result],

        'netAvailb': ['Bandwidth', 'Latency', BW_pnts, Ltncy_pnts, FS_netAvailb, [8, 28, 97], netAvailb_rules,
                      netAvailb_result],

        'hwAvailb': ['predMemUsage', 'predLoad', pMU_pnts, pLoad_pnts, FS_hw, [8, 28, 97], hwAvailb_rules,
                     hwAvailb_result],

        'CLPV': ['hwAvailb', 'netAvailb', hw_pnts, netAvailb_pnts, FS_clpv, [8, 28, 97], clpv_rules,
                 clpv_result]
    }

    create_fuzzies(fuzzy_dict, terms)
    set_rules(fuzzy_dict)

    for fuzzkey in fuzzy_dict:
        fuzzy_dict[fuzzkey][4].set_variable(fuzzy_dict[fuzzkey][0], 10)
        fuzzy_dict[fuzzkey][4].set_variable(fuzzy_dict[fuzzkey][1], 10)

        if fuzzkey == 'hwAvailb':
            fuzzy_dict[fuzzkey][4].set_variable(fuzzy_dict[fuzzkey][0], fuzzy_dict['predMemUsage'][7])
            fuzzy_dict[fuzzkey][4].set_variable(fuzzy_dict[fuzzkey][1], fuzzy_dict['predLoad'][7])

        elif fuzzkey == 'CLPV':
            fuzzy_dict[fuzzkey][4].set_variable(fuzzy_dict[fuzzkey][0], fuzzy_dict['hwAvailb'][7])
            fuzzy_dict[fuzzkey][4].set_variable(fuzzy_dict[fuzzkey][1], fuzzy_dict['netAvailb'][7])

        fuzzy_dict[fuzzkey][7] = fuzzy_dict[fuzzkey][4].Sugeno_inference([fuzzkey])[fuzzkey]
        print(f'======{fuzzy_dict[fuzzkey][7]}')

    fuzzy_dict['CLPV'][4].plot_surface(variables=['hwAvailb', 'netAvailb'], output='CLPV', detail=40, color_map='plasma')
    plt.show()


    """
        hw_pnts_list_1 = [[0., 1], [40., 1], [60., 0]]
        hw_pnts_list_2 = [[0., 1], [50., 1], [60., 0.5], [100., 0]]
        clpv_pnts_list_1 = [[0., 1], [50., 1], [80., 1], [85., 0]]
        clpv_pnts_list_2 = [[0., 1], [50., 1], [60., 0]]
     
    # Agregattion--------------------------------------------------------------------
    
    FS_HW = sf.fuzzy_aggregation.FuzzyAggregator()
    FS_CLPV = sf.FuzzySystem()

    aggregated_dict_1 = {
        'hwAvailb': [hw_pnts_list_1, hw_pnts_list_2, FS_HW, 'predMemUsage', 'predLoad', fuzzy_dict['predMemUsage'][7],
                     fuzzy_dict['predLoad'][7]]
    }

    aggregated_dict_final = {
        'CLPV': [clpv_pnts_list_1, clpv_pnts_list_2, FS_CLPV, 'hwAvailb', 'netAvailb', fuzzy_dict['netAvailb'][7],
                 aggregated_dict_1['hwAvailb'][6]]
    }

    aggregate_fuzzies(aggregated_dict_1)
    aggregate_fuzzies(aggregated_dict_final)
    """
