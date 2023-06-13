import pandas as pd
import simpful as sf
from numpy import array, meshgrid, linspace
from simpful import *
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


def creating_FS():
    fs = sf.FuzzySystem()

    V_1 = sf.FuzzySet(points=[[0., 1.], [0.2, 1.], [0.3, 0]], term="decreasing")
    V_2 = sf.FuzzySet(points=[[0.2, 0], [0.3, 1.], [0.7, 1], [0.8, 0]], term="constant")
    V_3 = sf.FuzzySet(points=[[0.7, 0], [0.8, 1.], [1., 1.]], term="increasing")
    fs.add_linguistic_variable("memory_usage_value", sf.LinguisticVariable([V_1, V_2, V_3]))
    fs.add_linguistic_variable("processor_load_value", sf.LinguisticVariable([V_1, V_2, V_3]))

    Mu_1 = sf.FuzzySet(points=[[0., 1.], [30., 1.], [40., 0]], term="low")
    Mu_2 = sf.FuzzySet(points=[[30., 0], [40., 1.], [65., 1], [75., 0]], term="medium")
    Mu_3 = sf.FuzzySet(points=[[65., 0], [75., 1.], [100., 1.]], term="high")
    fs.add_linguistic_variable("memory_usage", sf.LinguisticVariable([Mu_1, Mu_2, Mu_3]))  # >70%

    Pl_1 = sf.FuzzySet(points=[[0., 1.], [40., 1.], [50., 0]], term="low")
    Pl_2 = sf.FuzzySet(points=[[40., 0], [50., 1.], [80., 1], [90., 0]], term="medium")
    Pl_3 = sf.FuzzySet(points=[[80., 0], [90., 1.], [100., 1.]], term="high")
    fs.add_linguistic_variable("processor_load", sf.LinguisticVariable([Pl_1, Pl_2, Pl_3]))  # > 85%

    Aob_1 = sf.FuzzySet(points=[[0., 1.], [0.75, 1.], [1., 0]], term="low")
    Aob_2 = sf.FuzzySet(points=[[75., 0], [1., 1.], [3.75, 1], [4.25, 0]], term="medium")
    Aob_3 = sf.FuzzySet(points=[[3.75, 0], [4.25, 1.], [5., 1.]], term="high")
    fs.add_linguistic_variable("available_bandwidth", sf.LinguisticVariable([Aob_1, Aob_2, Aob_3]))  # < 1Mbps

    L_1 = sf.FuzzySet(points=[[0., 1.], [40., 1.], [50., 0]], term="low")
    L_2 = sf.FuzzySet(points=[[40., 0], [50., 1.], [145., 1], [155., 0]], term="medium")
    L_3 = sf.FuzzySet(points=[[145., 0], [155., 1.], [200., 1.]], term="high")
    fs.add_linguistic_variable("latency", sf.LinguisticVariable([L_1, L_2, L_3]))  # > 150ms

    PMU = AutoTriangle(3, terms=['low', 'medium', 'high'], universe_of_discourse=[-1, 1])
    O_1 = sf.FuzzySet(points=[[-1., 1.], [-0.75, 1.], [-0.5, 0]], term="low")
    O_2 = sf.FuzzySet(points=[[-0.5, 0], [-0.25, 1.], [0.25, 1], [0.5, 0]], term="medium")
    O_3 = sf.FuzzySet(points=[[0.5, 0], [0.75, 1.], [1., 1.]], term="high")
    fs.add_linguistic_variable("predicted_memory_usage", sf.LinguisticVariable([O_1, O_2, O_3]))

    PPL = AutoTriangle(3, terms=['low', 'medium', 'high'], universe_of_discourse=[-1, 1])
    fs.add_linguistic_variable("predicted_processor_load", sf.LinguisticVariable([O_1, O_2, O_3]))

    HA = AutoTriangle(3, terms=['low', 'medium', 'high'], universe_of_discourse=[-1, 1])
    fs.add_linguistic_variable("hardware_availability", sf.LinguisticVariable([O_1, O_2, O_3]))

    NA = AutoTriangle(3, terms=['low', 'medium', 'high'], universe_of_discourse=[-1, 1])
    fs.add_linguistic_variable("network_availability", sf.LinguisticVariable([O_1, O_2, O_3]))

    CLP_V = AutoTriangle(3, terms=['decrease', 'maintain', 'increase'], universe_of_discourse=[-1, 1])
    fs.add_linguistic_variable("CLPVariation", CLP_V)

    fs.set_crisp_output_value("low", -1)
    fs.set_crisp_output_value("medium", 0)
    fs.set_crisp_output_value("high", 1)
    
    fs.set_crisp_output_value("decrease", -1)
    fs.set_crisp_output_value("maintain", 0)
    fs.set_crisp_output_value("increase", 1)

    return fs


def rules(fs):
    fs.add_rules([
        "IF (available_bandwidth IS medium) AND (latency IS high) THEN (network_availability IS low)",
        "IF (available_bandwidth IS medium) AND (latency IS medium) THEN (network_availability IS medium)",
        "IF (available_bandwidth IS medium) AND (latency IS low) THEN (network_availability IS high)",

        "IF (available_bandwidth IS high) AND (latency IS high) THEN (network_availability IS low)",
        "IF (available_bandwidth IS high) AND (latency IS medium) THEN (network_availability IS medium)",
        "IF (available_bandwidth IS high) AND (latency IS low) THEN (network_availability IS high)",

        "IF (available_bandwidth IS low) AND (latency IS high) THEN (network_availability IS low)",
        "IF (available_bandwidth IS low) AND (latency IS medium) THEN (network_availability IS low)",
        "IF (available_bandwidth IS low) AND (latency IS low) THEN (network_availability IS medium)"
    ])
    fs.add_rules([
        "IF (memory_usage_value IS increasing) AND (memory_usage IS low) THEN (predicted_memory_usage IS medium)",
        "IF (memory_usage_value IS increasing) AND (memory_usage IS medium) THEN (predicted_memory_usage IS high)",
        "IF (memory_usage_value IS increasing) AND (memory_usage IS high) THEN (predicted_memory_usage IS high)",

        "IF (memory_usage_value IS constant) AND (memory_usage IS low) THEN (predicted_memory_usage IS low)",
        "IF (memory_usage_value IS constant) AND (memory_usage IS medium) THEN (predicted_memory_usage IS medium)",
        "IF (memory_usage_value IS constant) AND (memory_usage IS high) THEN (predicted_memory_usage IS high)",

        "IF (memory_usage_value IS decreasing) AND (memory_usage IS low) THEN (predicted_memory_usage IS low)",
        "IF (memory_usage_value IS decreasing) AND (memory_usage IS medium) THEN (predicted_memory_usage IS low)",
        "IF (memory_usage_value IS decreasing) AND (memory_usage IS high) THEN (predicted_memory_usage IS medium)"
    ])
    fs.add_rules([
        "IF (processor_load_value IS increasing) AND (processor_load IS low) THEN (predicted_processor_load IS medium)",
        "IF (processor_load_value IS increasing) AND (processor_load IS medium) THEN (predicted_processor_load IS high)",
        "IF (processor_load_value IS increasing) AND (processor_load IS high) THEN (predicted_processor_load IS high)",

        "IF (processor_load_value IS constant) AND (processor_load IS low) THEN (predicted_processor_load IS low)",
        "IF (processor_load_value IS constant) AND (processor_load IS medium) THEN (predicted_processor_load IS medium)",
        "IF (processor_load_value IS constant) AND (processor_load IS high) THEN (predicted_processor_load IS high)",

        "IF (processor_load_value IS decreasing) AND (processor_load IS low) THEN (predicted_processor_load IS low)",
        "IF (processor_load_value IS decreasing) AND (processor_load IS medium) THEN (predicted_processor_load IS low)",
        "IF (processor_load_value IS decreasing) AND (processor_load IS high) THEN (predicted_processor_load IS medium)"
    ])
    fs.add_rules([
        "IF (predicted_memory_usage IS low) AND (predicted_processor_load IS high) THEN (hardware_availability IS medium)",
        "IF (predicted_memory_usage IS high) AND (predicted_processor_load IS low) THEN (hardware_availability IS medium)",
        "IF (predicted_memory_usage IS low) AND (predicted_processor_load IS low) THEN (hardware_availability IS low)",
        "IF (predicted_memory_usage IS high) AND (predicted_processor_load IS high) THEN (hardware_availability IS high)"
    ])
    fs.add_rules([
        "IF (network_availability IS high) AND (hardware_availability IS high) THEN (CLPVariation IS increase)",
        "IF (network_availability IS low) AND (hardware_availability IS low) THEN (CLPVariation IS maintain)",
        "IF ((network_availability IS high) OR (network_availability IS medium)) AND (hardware_availability IS low) THEN (CLPVariation IS decrease)",

        "IF ((hardware_availability IS high) OR (hardware_availability IS medium)) THEN (CLPVariation IS increase)",
    ])


def graphs(fs):
    # fs.plot_surface = plot_surface_edited
    FS.set_variable("available_bandwidth", 2)
    FS.set_variable("latency", 80)

    FS.set_variable("memory_usage", 50)
    FS.set_variable("processor_load", 50)

    FS.set_variable("memory_usage_value", 0)
    FS.set_variable("processor_load_value", 0)

    FS.set_variable("predicted_memory_usage", 0)
    FS.set_variable("predicted_processor_load", 0)
    FS.set_variable("network_availability", 0)
    FS.set_variable("hardware_availability", 0)
    FS.set_variable("CLPVariation", 0)

    # res = fs.inference(["predicted_memory_usage", "predicted_processor_load"])
    # FS.set_variable("predicted_memory_usage", res["predicted_memory_usage"])
    # FS.set_variable("predicted_processor_load", res["predicted_processor_load"])
    #
    # res = fs.inference(["network_availability", "hardware_availability"])
    # FS.set_variable("network_availability", res["network_availability"])
    # FS.set_variable("hardware_availability", res["hardware_availability"])
    #
    # print(fs.inference(["hardware_availability", "network_availability", "CLPVariation"]))

    def plot_surface_edited(self, variables, output, detail=40, color_map="plasma"):
        """
        Plots the surface induced by the rules.

        Args:
            variables: a pair of linguistic variables for the x and y axis.
            output: the output variable to be computed.
            detail: number of subdivisions along each axis.
            color_map: the color map to be used for the plot.

        Returns:
            a matplotlib figure object.
        """

        if len(variables) != 2:
            print("ERROR: please specify the two variables for the surface plot")
            return None

        v1, v2 = variables

        min_v1, max_v1 = self._lvs[v1].get_universe_of_discourse()
        min_v2, max_v2 = self._lvs[v2].get_universe_of_discourse()

        A = linspace(min_v1, max_v1, detail)
        B = linspace(min_v2, max_v2, detail)
        C = []

        for a in A:
            temp = []
            for b in B:
                self.set_variable(self._lvs[v1]._concept, a)
                self.set_variable(self._lvs[v2]._concept, b)
                res = self.inference()[output]
                temp.append(res)
            C.append(temp)
        C = array(C)

        A, B = meshgrid(A, B)

        fig = plt.figure(figsize=(8, 6))
        ax = plt.axes(projection='3d')

        v = ax.plot_surface(A, B, C, shade=True, cmap=color_map)
        ax.set_xlabel(self._lvs[v1]._concept)
        ax.set_ylabel(self._lvs[v2]._concept)
        ax.set_zlabel(output)
        plt.colorbar(v, ax=ax)
        fig.tight_layout()
        return fig

    FS.plot_surface = plot_surface_edited

    # fs.plot_surface(FS, {"hardware_availability", "network_availability"}, "CLPVariation")
    plt.show()


def calculate(inputs):
    CLPVariation = 0
    FS.set_variable("available_bandwidth", inputs["available_bandwidth"])
    FS.set_variable("latency", inputs["latency"])
    FS.set_variable("memory_usage", inputs["memory_usage"])
    FS.set_variable("processor_load", inputs["processor_load"])

    FS.set_variable("memory_usage_value", inputs["memory_usage_value"])
    FS.set_variable("processor_load_value", inputs["processor_load_value"])

    FS.set_variable("predicted_memory_usage", inputs["memory_usage"])
    FS.set_variable("predicted_processor_load", inputs["memory_usage"])
    FS.set_variable("network_availability", inputs["memory_usage"])
    FS.set_variable("hardware_availability", inputs["memory_usage"])

    FS.set_variable("CLPVariation", inputs["memory_usage"])

    return CLPVariation


def results(df, FS):
    res = []
    for idx, row in df.iterrows():
        inputs = {'memory_usage': row['MemoryUsage'], 'memory_usage_value': row['V_MemoryUsage'],
                  'processor_load': row['ProcessorLoad'], 'processor_load_value': row['V_ProcessorLoad'],
                  'available_bandwidth': row['OutBandwidth'], 'latency': row['Latency'], }
        output = calculate(inputs)
        res.append(output)

    # Add the results to the DataFrame
    df['CLPVariation'] = res
    print(df['CLPVariation'])


if __name__ == '__main__':
    df = pd.read_csv("Lab10-Proj2_TestS.csv")
    FS = creating_FS()
    rules(FS)
    graphs(FS)
    results(df, FS)
