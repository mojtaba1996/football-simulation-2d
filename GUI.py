import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import subprocess, threading, shutil, os, glob
from genericpath import isdir
from os import listdir
from os.path import join
import xlsxwriter

class Command():
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None
        self.out, self.err = '', ''

    def run(self, timeout, input = b'', cwd = None):
        def target():
            if len(input) != 0:
                self.process = subprocess.Popen(self.cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
                self.out, self.err = self.process.communicate(input)
            else:
                self.process = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
                self.out, self.err = self.process.communicate()

        thread = threading.Thread(target=target)
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            self.process.terminate()
            thread.join()

def Make_Result_File(Teams, Location):
    if len(Teams) == 0:
        return
    workbook = xlsxwriter.Workbook(Location + 'Results.xlsx')
    worksheet = workbook.add_worksheet('Results')

    default_format = workbook.add_format({
        'font_name': 'Times New Roman',
        'font_size':  14,
    })

    default_red_format = workbook.add_format({
        'font_name': 'Times New Roman',
        'font_color': 'red',
        'font_size':  14,
    })

    default_yellow_format = workbook.add_format({
        'font_name': 'Times New Roman',
        'font_color': 'yellow',
        'font_size':  14,
    })

    default_green_format = workbook.add_format({
        'font_name': 'Times New Roman',
        'font_color': 'green',
        'font_size':  14,
    })

    worksheet.add_table(0, 0, len(Teams), 8, \
                        {'columns': [{'header': 'Team Name', 'header_format': default_format}, \
                                     {'header': 'Games Played', 'header_format': default_format}, \
                                     {'header': 'Win', 'header_format': default_format}, \
                                     {'header': 'Draw', 'header_format': default_format}, \
                                     {'header': 'Lost', 'header_format': default_format}, \
                                     {'header': 'Goals For', 'header_format': default_format}, \
                                     {'header': 'Goals Against', 'header_format': default_format}, \
                                     {'header': 'Goal Difference', 'header_format': default_format}, \
                                     {'header': 'Points', 'header_format': default_format}]})
    row = 1
    max_width = [9, 12, 3, 4, 4, 9, 13, 15, 6]
    for Team in Teams:
        worksheet.write(row, 0, Team['TeamName'], default_format)
        worksheet.write(row, 1, Team['GamesPlayed'], default_format)
        worksheet.write(row, 2, Team['Win'], default_green_format)
        worksheet.write(row, 3, Team['Draw'], default_yellow_format)
        worksheet.write(row, 4, Team['Lost'], default_red_format)
        worksheet.write(row, 5, Team['GoalsFor'], default_format)
        worksheet.write(row, 6, Team['GoalsAgainst'], default_format)
        if Team['GoalDifference'] > 0:
            write_format = default_green_format
        elif Team['GoalDifference'] < 0:
            write_format = default_red_format
        else:
            write_format = default_yellow_format
        worksheet.write(row, 7, Team['GoalDifference'], write_format)
        if Team['Points'] > 0:
            write_format = default_green_format
        elif Team['Points'] < 0:
            write_format = default_red_format
        else:
            write_format = default_yellow_format
        worksheet.write(row, 8, Team['Points'], default_format)

        if len(Team['TeamName']) > max_width[0]:
            max_width[0] = len(Team['TeamName'])
        row += 1
    for i in range(len(max_width)):
        worksheet.set_column(i, i, max_width[i]+5)
    worksheet.ignore_errors()
    workbook.close()

def RunMatch(Team1, Team2, Delay_Count, Delay_Amount, Max_Cycle):
    # create config file
    file = open('config.txt', 'w')
    file.write(Team1['TeamName']+ '\n')
    file.write(Team2['TeamName']+ '\n')
    file.write(str(Delay_Count) + '*' + str(Delay_Amount) + '\n')
    file.write(str(Max_Cycle)+ '\n')
    file.write('True\n' if (Delay.get() == 1 and Graphical.get() == 1) else 'False\n')
    file.write('True\n' if Graphical.get() == 1 else 'False\n')
    file.close()
    
    # copy files
    shutil.copyfile(Team1['FileAddress'], './team1/team1.py')
    shutil.copyfile(Team2['FileAddress'], './team2/team2.py')

    # remove previous results
    try:
        os.remove('result.txt')
    except:
        pass

    # run simulation
    command = Command(["python", 'main.py'])
    TimeOut = Max_Cycle
    command.run(TimeOut) 

    # return results
    if command.process.returncode == 0:
        file = open('result.txt')
        Results = file.read().split()
        file.close()

        return int(Results[0]), int(Results[1])

def RunPrograms():
    FileNames = Files_lstbx.get(0, tk.END)
    Teams = []
    for File in FileNames:
        Temp = {}
        Temp['FileAddress'] = File
        Temp['TeamName'] = File.split('/')[-1][:-3]
        Temp['GamesPlayed'] = 0
        Temp['GoalDifference'] = 0
        Temp['GoalsFor'] = 0
        Temp['GoalsAgainst'] = 0
        Temp['Points'] = 0
        Temp['Win'] = 0
        Temp['Lost'] = 0
        Temp['Draw'] = 0
        Teams.append(Temp)

    RunMatches(Teams, './')

def RunGroupMatches():
    FolderPath = './Groups/'    
    Groups = [f for f in listdir(FolderPath) if isdir(join(FolderPath, f))]
    
    for Group in Groups:
        print(Group)
        Path = FolderPath  + Group + '/'
        FileNames = glob.glob(Path + '*.py')
        Teams = []
        for File in FileNames:
            Temp = {}
            Temp['FileAddress'] = File
            Temp['TeamName'] = File.split('\\')[-1][:-3]
            Temp['GamesPlayed'] = 0
            Temp['GoalDifference'] = 0
            Temp['GoalsFor'] = 0
            Temp['GoalsAgainst'] = 0
            Temp['Points'] = 0
            Temp['Win'] = 0
            Temp['Lost'] = 0
            Temp['Draw'] = 0
            Teams.append(Temp)
        
        RunMatches(Teams, Path)

def RunMatches(Teams, ResultsLocation):
    try:
        Delay_Amount = float(Delay_Amount_ent.get())
    except:
        showinfo(title='Error', message="Delay Amount not right")

    try:
        Delay_Count = int(Delay_Count_ent.get())
    except:
        showinfo(title='Error', message="Delay Count not right")

    try:
        Max_Cycle = int(Max_Cycle_ent.get())
    except:
        showinfo(title='Error', message="Max Cycle not right")

    for i in range(len(Teams)):
        for j in range(len(Teams)):
            if i != j:
                Result = RunMatch(Teams[i], Teams[j], Delay_Count, Delay_Amount, Max_Cycle)
                if Result != None:
                    if Result[0] > Result[1]:
                        Teams[i]['Win'] += 1
                        Teams[j]['Lost'] += 1
                    elif Result[0] < Result[1]:
                        Teams[j]['Win'] += 1
                        Teams[i]['Lost'] += 1
                    else:
                        Teams[i]['Draw'] += 1
                        Teams[j]['Draw'] += 1
                    
                    Teams[i]['GoalsFor'] += Result[0]
                    Teams[i]['GoalsAgainst'] += Result[1]
                    Teams[j]['GoalsFor'] += Result[1]
                    Teams[j]['GoalsAgainst'] += Result[0]

                    Teams[i]['GoalDifference'] = Teams[i]['GoalsFor'] - Teams[i]['GoalsAgainst']
                    Teams[j]['GoalDifference'] = Teams[j]['GoalsFor'] - Teams[j]['GoalsAgainst']

                    Teams[i]['Points'] = Teams[i]['Win'] * 3 + Teams[i]['Draw']
                    Teams[j]['Points'] = Teams[j]['Win'] * 3 + Teams[j]['Draw']
                    Teams[i]['GamesPlayed'] += 1
                    Teams[j]['GamesPlayed'] += 1
    
    for i in range(len(Teams)-1):
        for j in range(i+1,len(Teams)):
            if Teams[i]['Points'] < Teams[j]['Points']:
                Teams[i], Teams[j] = Teams[j], Teams[i]
            elif Teams[i]['Points'] == Teams[j]['Points'] and Teams[i]['GoalDifference'] < Teams[j]['GoalDifference']:
                Teams[i], Teams[j] = Teams[j], Teams[i]
            elif Teams[i]['Points'] == Teams[j]['Points'] and Teams[i]['GoalDifference'] == Teams[j]['GoalDifference'] and Teams[i]['GoalsAgainst'] == Teams[j]['GoalsAgainst']:
                Teams[i], Teams[j] = Teams[j], Teams[i]

    Make_Result_File(Teams, ResultsLocation)

def AddFile():
    filetypes = (('python files', '*.py'), ('All files', '*.*'))    
    filename = fd.askopenfilenames(title='Open a file', initialdir='./', filetypes=filetypes)
    Last_Index = Files_lstbx.size()
    for i in range(Last_Index, len(filename)+Last_Index):
        Files_lstbx.insert(i, filename[i-Last_Index])

def DeleteFile():
    Index = Files_lstbx.curselection()
    for i in Index[::-1]:
        Files_lstbx.delete(i)

def ChangeGraphical():
    if Graphical.get() == 0:
        Additional_Delay_chk.config(state='disabled')
    else:
        Additional_Delay_chk.config(state='normal')

window = tk.Tk()
window.title('Football Simulation GUI')
window.resizable(False, False)
window.geometry('400x320')

HScroll = ttk.Scrollbar(window, orient='horizontal')
VScroll = ttk.Scrollbar(window, orient='vertical')
Files_lstbx = tk.Listbox(window, selectmode='multiple', yscrollcommand=VScroll.set, xscrollcommand=HScroll.set)
HScroll.config(command=Files_lstbx.xview)
VScroll.config(command=Files_lstbx.yview)
Add_File_btn = tk.Button(window, text= "Add File", command= AddFile)
Delete_File_btn = tk.Button(window, text= "Delete File", command= DeleteFile)
Start_btn = tk.Button(window, text= "Start", command= RunPrograms)
Group_btn = tk.Button(window, text= "Start Group Matchs", command= RunGroupMatches)

Graphical = tk.IntVar()
Graphical.set(1)
Delay = tk.IntVar()
if Graphical.get() == 1:
    Delay.set(1)

Graphical_chk = tk.Checkbutton(window, text= 'Graphical Output', variable=Graphical, command=ChangeGraphical)
Additional_Delay_chk = tk.Checkbutton(window, text= 'Additional Delay', variable=Delay)

Delay_Count_ent = tk.Entry(window, width = 10)
Delay_Amount_ent = tk.Entry(window)
Max_Cycle_ent = tk.Entry(window)

HScroll.place(x= 0, y= 201, width=375, height=25)
VScroll.place(x= 376, y= 0, width= 25, height= 200)
Files_lstbx.place(x=0, y=0, width= 375, height= 200)
Add_File_btn.place(x=20, y=280)
Delete_File_btn.place(x=100, y=280)
Start_btn.place(x= 190, y= 280, width= 70)
Group_btn.place(x= 270, y= 280)
Graphical_chk.place(x= 0, y=250)
Additional_Delay_chk.place(x= 150, y=250)
tk.Label(window, text='Delay Count: ').place(x= 0, y= 226)
Delay_Count_ent.place(x= 79, y=228, width= 30)
tk.Label(window, text='Delay Amount: ').place(x= 125, y= 226)
Delay_Amount_ent.place(x= 215, y=228, width= 30)
tk.Label(window, text='Max Cycle: ').place(x= 260, y= 226)
Max_Cycle_ent.place(x= 328, y=228, width= 30)

Delay_Count_ent.insert(-1, '8')
Delay_Amount_ent.insert(-1, '0.07')
Max_Cycle_ent.insert(-1, '500')

window.mainloop()