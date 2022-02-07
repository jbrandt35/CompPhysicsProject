import Parser
from NBodySims import JoshSim as NbodySimulator

options = Parser.parse_config("SimFiles/config.JSON")

planets = Parser.parse_objects(options["Planets"])

#Example of starting N-body simulator
NbodySimulator.RunSim(planets, options)

