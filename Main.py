import Parser
import Simulator as NbodySimulator

options = Parser.parse_config("SimFiles/config.JSON")

planets = Parser.parse_objects(options)

print(f"Starting N-body simulator with dt={options['dt']} seconds for {options['Runtime']} seconds...")
NbodySimulator.RunSim(planets, options)




