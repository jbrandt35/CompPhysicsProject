import Parser

options = Parser.parse_config("SimFiles/config.JSON")

planets = Parser.parse_objects(options["Planets"])
