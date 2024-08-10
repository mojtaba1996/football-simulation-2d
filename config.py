class Config:
    def __init__(self, path='config.txt'):
        file = open('config.txt')
        self.team1_name = file.readline().strip()
        self.team2_name = file.readline().strip()
        self.play_timeout = float(file.readline().strip())
        self.max_cycle = int(file.readline().strip())
        self.cycle_delay = float(file.readline().strip())
        self.additional_delay = True if file.readline().strip().lower() == 'true' else False
        self.graphical_output = True if file.readline().strip().lower() == 'true' else False
