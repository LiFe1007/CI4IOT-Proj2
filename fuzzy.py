import simpful as sf


def create_rules(terms, predMU_rules, predLoad_rules, netAvailb_rules):
    # Memory usage x Memory usage variation
    predMU_rules = [
        f'IF (deltaMemUsage IS low_deltaMemUsage) AND (MemUsage IS low_MemUsage) THEN (pred_mem_usage IS LOW)'
        f'IF (deltaMemUsage IS low_deltaMemUsage) AND (MemUsage IS medium_MemUsage) THEN (pred_mem_usage IS LOW)'
        f'IF (deltaMemUsage IS low_deltaMemUsage) AND (MemUsage IS high_MemUsage) THEN (pred_mem_usage IS MEDIUM)'

        f'IF (deltaMemUsage IS medium_deltaMemUsage) AND (MemUsage IS low_MemUsage) THEN (pred_mem_usage IS LOW)'
        f'IF (deltaMemUsage IS medium_deltaMemUsage) AND (MemUsage IS medium_MemUsage) THEN (pred_mem_usage IS MEDIUM)'
        f'IF (deltaMemUsage IS medium_deltaMemUsage) AND (MemUsage IS high_MemUsage) THEN (pred_mem_usage IS HIGH)'

        f'IF (deltaMemUsage IS high_deltaMemUsage) AND (MemUsage IS low_MemUsage) THEN (pred_mem_usage IS MEDIUM)'
        f'IF (deltaMemUsage IS high_deltaMemUsage) AND (MemUsage IS medium_MemUsage) THEN (pred_mem_usage IS HIGH)'
        f'IF (deltaMemUsage IS high_deltaMemUsage) AND (MemUsage IS high_MemUsage) THEN (pred_mem_usage IS HIGH)'
    ]

    # Processor load x Processor load variation
    predLoad_rules = [
        f'IF (deltaLoad IS low_deltaLoad) AND (Load IS low_Load) THEN (predicted_processor_load IS LOW)'
        f'IF (deltaLoad IS low_deltaLoad) AND (Load IS medium_Load) THEN (predicted_processor_load IS LOW)'
        f'IF (deltaLoad IS low_deltaLoad) AND (Load IS high_Load) THEN (predicted_processor_load IS MEDIUM)'

        f'IF (deltaLoad IS medium_deltaLoad) AND (Load IS low_Load) THEN (pred_processor_load IS LOW)'
        f'IF (deltaLoad IS medium_deltaLoad) AND (Load IS medium_Load) THEN (pred_processor_load IS MEDIUM)'
        f'IF (deltaLoad IS medium_deltaLoad) AND (Load IS high_Load) THEN (pred_processor_load IS HIGH)'

        f'IF (deltaLoad IS high_deltaLoad) AND (Load IS low_Load) THEN (pred_processor_load IS MEDIUM)'
        f'IF (deltaLoad IS high_deltaLoad) AND (Load IS medium_Load) THEN (pred_processor_load IS HIGH)'
        f'IF (deltaLoad IS high_deltaLoad) AND (Load IS high_Load) THEN (pred_processor_load IS HIGH)'
    ]

    # Bandwidth x Latency
    netAvailb_rules = [
        f'IF (Bandwidth IS low_Bandwidth) AND (Latency IS high_Latency) THEN (network_availability IS LOW)'
        f'IF (Bandwidth IS medium_Bandwidth) AND (Latency IS medium_Latency) THEN (network_availability IS MEDIUM)'
        f'IF (Bandwidth IS high_Bandwidth) AND (Latency IS low_Latency) THEN (network_availability IS HIGH)'
    ]

    """
    
    # Predicted processor load x Predicted memory usage
    hwAvailb_rules = [
        f'IF (predicted_memory_usage IS low) AND (predicted_processor_load IS high) THEN (hardware_availability IS medium)'
        f'IF (predicted_memory_usage IS high) AND (predicted_processor_load IS low) THEN (hardware_availability IS medium)'
        f'IF (predicted_memory_usage IS low) AND (predicted_processor_load IS low) THEN (hardware_availability IS low)'
        f'IF (predicted_memory_usage IS high) AND (predicted_processor_load IS high) THEN (hardware_availability IS high'
    ]

    # Hardware availability x Network availability
    clpv_rules = [

    ]
    """

    return predMU_rules, predLoad_rules, netAvailb_rules


def create_fuzzies(fuzz_dict, terms):
    for fuzz_key in fuzz_dict:
        key_vars_1 = [sf.FuzzySet(points=fuzz_dict[fuzz_key][2][i], term=f"{terms[i]}_{fuzz_dict[fuzz_key][0]}")
                      for i in range(3)]

        key_vars_2 = [sf.FuzzySet(points=fuzz_dict[fuzz_key][3][i], term=f"{terms[i]}_{fuzz_dict[fuzz_key][1]}")
                      for i in range(3)]

        fuzz_dict[fuzz_key][4].add_linguistic_variable(fuzz_dict[fuzz_key][0], sf.LinguisticVariable(key_vars_1))
        fuzz_dict[fuzz_key][4].add_linguistic_variable(fuzz_dict[fuzz_key][1], sf.LinguisticVariable(key_vars_2))

        for i, term in enumerate(terms):
            fuzz_dict[fuzz_key][4].set_crisp_output_value(term.upper(), fuzz_dict[fuzz_key][5][i])

        """        
        fuzz_dict[key][1].set_crisp_output_value("LOW", dict[key][2][0])
        fuzz_dict[key][1].set_crisp_output_value("MEDIUM", dict[key][2][1])
        fuzz_dict[key][1].set_crisp_output_value("HIGH", dict[key][2][2])
        """
    return fuzz_dict


def set_rules(fuzz_dict):
    for fuzz_key in fuzz_dict:
        fuzz_dict[fuzz_key][4].add_rules(fuzz_dict[fuzz_key][6])


def aggregate_fuzzies(aggr_dict):

    for fuzz_key in aggr_dict:
        print(f'OLAAAA = {aggr_dict[fuzz_key][0]}')
        fuzzy_one_vars = [sf.FuzzySet(points=aggr_dict[fuzz_key][0], term=f'{aggr_dict[fuzz_key][3]}')]
        fuzzy_two_vars = [sf.FuzzySet(points=aggr_dict[fuzz_key][1], term=f'{aggr_dict[fuzz_key][4]}')]

        aggr = sf.fuzzy_aggregation.FuzzyAggregator(verbose=True)
        aggr.add_variables(*fuzzy_one_vars, *fuzzy_two_vars)

        aggr.set_variable(aggr_dict[fuzz_key][3], aggr_dict[fuzz_key][5])
        aggr.set_variable(aggr_dict[fuzz_key][4], aggr_dict[fuzz_key][6])

        aggr_dict[fuzz_key][2] = aggr.aggregate([aggr_dict[fuzz_key][3], aggr_dict[fuzz_key][4]], aggregation_fun='arit_mean')

    return aggr_dict


if __name__ == '__main__':
    terms = ['low', 'medium', 'high']

    MU_pnts_list = [
        [[0., 1], [50., 1], [60., 0]],  # Points for 'low'
        [[20., 0], [50., 1], [80., 1], [85., 0]],  # Points for 'medium'
        [[75., 0], [90., 1], [100., 1]]  # Points for 'high'
    ]

    pMU_pnts_list = [
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

    hw_pnts_list_1 = [[75., 0], [90., 1], [100., 1]]

    hw_pnts_list_2 = [[20., 0], [50., 1], [80., 1], [85., 0]]

    clpv_pnts_list_1 = [[20., 0], [50., 1], [80., 1], [85., 0]]

    clpv_pnts_list_2 = [[0., 1], [50., 1], [60., 0]]

    FS_MU = sf.FuzzySystem()
    FS_Load = sf.FuzzySystem()
    FS_netAvailb = sf.FuzzySystem()

    # 1st round
    predMU_rules = []
    predLoad_rules = []
    netAvailb_rules = []

    # 2nd round (aggregation)
    hwAvailb_rules = []

    # final round (2nd round's aggregation)
    clpv_rules = []

    create_rules(terms, predMU_rules, predLoad_rules, netAvailb_rules)

    # Legenda do dicionario =
    # 'key' : Fuzzy_name_1, Fuzzy_name_2, points_list_1, points_list_2, sf.FuzzySystem(),
    # output function or value for low medium high, rules
    first_dict = {
        'predMemUsage': ['MemUsage', 'deltaMemUsage', MU_pnts_list, pMU_pnts_list, FS_MU, [5, 25, 100], predMU_rules],
        'predLoad': ['Load', 'deltaLoad', Load_pnts_list, deltaLoad_pnts_list, FS_Load, [7, 27, 98], predLoad_rules],
        'netAvailb': ['Bandwidth', 'Latency', BW_pnts_list, Ltncy_pnts_list, FS_netAvailb, [8, 28, 97], netAvailb_rules]
    }

    create_fuzzies(first_dict, terms)
    set_rules(first_dict)

    FS_HW = sf.fuzzy_aggregation.FuzzyAggregator()
    FS_CLPV = sf.FuzzySystem()

    # mudar isto amanha
    sugeno1 = 10
    sugeno2 = 32

    aggregated_dict = {
        'hwAvailb': [hw_pnts_list_1, hw_pnts_list_2, FS_HW, 'predMemUsage', 'predLoad', sugeno1, sugeno2],

        'CLPV': [clpv_pnts_list_1, clpv_pnts_list_2, FS_CLPV, 'hwAvailb', 'netAvailb', sugeno1, sugeno2]
    }

    aggregate_fuzzies(aggregated_dict)
