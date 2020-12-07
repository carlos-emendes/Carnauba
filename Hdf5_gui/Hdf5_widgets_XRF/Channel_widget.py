
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QGridLayout, QLineEdit, QLabel, QWidget, QCheckBox

import pyqtgraph as pg

def Channel_tab(window):
    #Cria QTable Widget Da aba de Canais#
    Channel_tab = QWidget()

    # Textos e areas para edicao do usuario#
    channel_chmin=QLabel('Min. ROI')
    channel_chmax=QLabel('Max ROI')
    channel_title=QLabel('Title')
    
    window.channel_chmin_edit=QLineEdit()
    window.channel_chmax_edit=QLineEdit()
    window.channel_title_edit=QLineEdit('New roi')
    
    window.Energy_check=QCheckBox('Energy axis')
        
    
    
    
    layout_roi=QVBoxLayout()
    Middle_roi=QGridLayout()
    
    channel_change_button=QPushButton('Change ROI') 
    Bot_roi=QPushButton('Add Roi')           

    #Permite mudar a cor do fundo e dos eixos
    pg.setConfigOption('background', 'w')
    pg.setConfigOption('foreground', 'k')
    pg.setConfigOptions(imageAxisOrder='row-major')
    
    # Cria uma janela de imagem
    sc_roi=pg.GraphicsWindow()
    window.p1=sc_roi.addPlot(title="XRF Intensity")
    window.lr=pg.LinearRegionItem([0,10])
    window.p1.setLogMode(False,True)
    
    
    
    Middle_roi.addWidget(channel_chmin,1,0)
    Middle_roi.addWidget(window.channel_chmin_edit,1,1)
    Middle_roi.addWidget(channel_chmax,1,2)
    Middle_roi.addWidget(window.channel_chmax_edit,1,3)
    Middle_roi.addWidget(channel_change_button,1,4)
    Middle_roi.addWidget(channel_title,2,0)
    Middle_roi.addWidget(window.channel_title_edit,2,1)
    Middle_roi.addWidget(window.Energy_check,2,2)
    
    
    
    

    layout_roi.addWidget(sc_roi)
    layout_roi.addLayout(Middle_roi)
    layout_roi.addWidget(Bot_roi)
    Channel_tab.setLayout(layout_roi)
    window.tabs.addTab(Channel_tab, 'Selection by ROI')
    
    #Funcoes acionadas quando botoes, abas sao acionadas#
    Bot_roi.clicked.connect(window.XRF_img)
    window.lr.sigRegionChanged.connect(window.update_channel_graph)
    channel_change_button.clicked.connect(window.update_channel_text)
    window.Energy_check.toggled.connect(window.change_axis_channel)