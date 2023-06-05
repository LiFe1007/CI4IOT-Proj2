import simpful as sf

# Create a fuzzy system.
FS = sf.FuzzySystem()

# Defining a list of points for each fuzzy set
points_list = [
    [[0., 1], [50., 1], [60., 0]],    # Points for 'low'
    [[20., 0], [50., 1], [80., 1], [85., 0]],   # Points for 'medium'
    [[75., 0], [90., 1], [100., 1]]   # Points for 'high'
]

# Defining fuzzy sets for each linguistic variable.
terms = ['low', 'medium', 'high']

# Linguistic variable: MemoryUsage
mem_vars = [sf.FuzzySet(points=points_list[i], term=f"{terms[i]}_memory")
            for i in range(3)]
FS.add_linguistic_variable("MemoryUsage", sf.LinguisticVariable(mem_vars))

# Linguistic variable: ProcessorLoad
load_vars = [sf.FuzzySet(points=points_list[i], term=f"{terms[i]}_load")
             for i in range(3)]
FS.add_linguistic_variable("ProcessorLoad", sf.LinguisticVariable(load_vars))

# Linguistic variable: Bandwidth
bw_vars = [sf.FuzzySet(points=points_list[i], term=f"{terms[i]}_bandwidth")
           for i in range(3)]
FS.add_linguistic_variable("Bandwidth", sf.LinguisticVariable(bw_vars))

# Linguistic variable: Latency
lat_vars = [sf.FuzzySet(points=points_list[i], term=f"{terms[i]}_latency")
            for i in range(3)]
FS.add_linguistic_variable("Latency", sf.LinguisticVariable(lat_vars))

# Define output functions.
FS.set_output_function("LOW", "-0.5*MemoryUsage - 0.5*ProcessorLoad - 0.5*Bandwidth - 0.5*Latency")
FS.set_output_function("MEDIUM", "MemoryUsage")
FS.set_output_function("HIGH", "0.5*MemoryUsage + 0.5*ProcessorLoad + 0.5*Bandwidth + 0.5*Latency")

# Define fuzzy rules.
rules = []
for term in terms:
    rules.append(f"IF (MemoryUsage IS {term}_memory) AND (ProcessorLoad IS {term}_load) AND "
                 f"(Bandwidth IS {term}_bandwidth) AND (Latency IS {term}_latency) "
                 f"THEN (CLPVariation IS {term.upper()})")
FS.add_rules(rules)

# Set antecedents values, perform Sugeno inference and print output values.
FS.set_variable("MemoryUsage", 60)
FS.set_variable("ProcessorLoad", 75)
FS.set_variable("Bandwidth", 40)
FS.set_variable("Latency", 30)
print(FS.Sugeno_inference(['CLPVariation']))
