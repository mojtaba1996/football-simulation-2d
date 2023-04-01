class Config:
    def __init__(self, path='config.txt'):
        file = open('config.txt')
        self.team1_name = file.readline().strip()
        self.team2_name = file.readline().strip()
        delay = file.readline().strip()
        self.delay_count = int(delay.split('*')[0])
        self.delay_amount = float(delay.split('*')[1])
        self.max_cycle = int(file.readline().strip())
        self.additional_delay = True if file.readline().strip().lower() == 'true' else False
        self.graphical_output = True if file.readline().strip().lower() == 'true' else False
