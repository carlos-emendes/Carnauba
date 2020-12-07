

from Hdf5_gui.Pymca_func.ElementsInfo import ElementsInfo
from PyQt5.QtWidgets import QPushButton,QVBoxLayout,QHBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


def Periodic_tab(window):
    periodic_tab = QWidget()
    window.f=ElementsInfo()
    layout=QVBoxLayout()
    Botoes=QHBoxLayout()
    
          
    #BOTOES DE ENERGIA DE LIGACAO
    window.bot_Ka=QPushButton('K\u03b1') #botao Ka
    window.bot_Kb=QPushButton('K\u03b2') #botao Kb
    window.bot_La=QPushButton('L\u03b1') #botao L
    window.bot_Lb=QPushButton('L\u03b2') #botao L
   
    window.bot_Ka.setCheckable(True)
    window.bot_Kb.setCheckable(True)
    window.bot_La.setCheckable(True)
    window.bot_Lb.setCheckable(True)
    
    window.edge_b=[window.bot_Ka,window.bot_Kb,window.bot_La,window.bot_Lb] #Lista responsável por impedir que dois
    #botoes sejam pressionados. Caso um novo botao seja adicionado, colocar aqui
    
    
    
    
    #Adiciona os botoes no layout
    bot1=QPushButton('Add Roi and Show Energy Line',window)
    bot2=QPushButton('Clear Graph',window)
    Botoes.addWidget(window.bot_Ka)
    Botoes.addWidget(window.bot_Kb)
    Botoes.addWidget(window.bot_La)
    Botoes.addWidget(window.bot_Lb)
    
    Botoes.addWidget(bot1)
    Botoes.addWidget(bot2)

    #widget3
    window.sc = MplCanvas(window, width=5, height=4, dpi=100)
    
         
    layout.addWidget(window.f)
    
    layout.addLayout(Botoes)
    layout.addWidget(window.sc)
    periodic_tab.setLayout(layout)
    window.tabs.addTab( periodic_tab,'Periodic Table')
    
    
    
    window.f.table.sigElementClicked.connect(window.Check_Energy)
    window.bot_Ka.clicked.connect(window.Energy_edge)
    window.bot_Kb.clicked.connect(window.Energy_edge)
    window.bot_La.clicked.connect(window.Energy_edge)
    window.bot_Lb.clicked.connect(window.Energy_edge)
    bot1.clicked.connect(window.Energy_line)
    bot2.clicked.connect(window.cleargraph)

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)