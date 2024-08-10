import yaml


class Config:
    def __init__(self, path='config.yaml'):
        try:
            with open(path, 'r') as file:
                data = yaml.safe_load(file)
                self.team1_name = data.get("team1_name", "team1")
                self.team2_name = data.get("team2_name", "team2")
                self.play_timeout = data.get("play_timeout", 0.5)
                self.max_cycle = data.get("max_cycle", 500)
                self.cycle_delay = data.get("cycle_delay", 0.03)
                self.additional_delay = data.get("additional_delay", True)
                self.graphical_output = data.get("graphical_output", True)
                self.print_decision_errors = data.get("print_decision_errors", True)
        except FileNotFoundError:
            print(f"Configuration file {path} not found. Using default values.")
            self.load_defaults()
        except yaml.YAMLError as e:
            print(f"Error parsing configuration file {path}: {e}. Using default values.")
            self.load_defaults()

    def load_defaults(self):
        self.team1_name = "team1"
        self.team2_name = "team2"
        self.play_timeout = 0.5
        self.max_cycle = 500
        self.cycle_delay = 0.03
        self.additional_delay = True
        self.graphical_output = True
        self.print_decision_errors = True
