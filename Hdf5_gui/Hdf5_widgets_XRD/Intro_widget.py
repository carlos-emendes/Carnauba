

from PyQt5.QtWidgets import  QPushButton,QVBoxLayout,QGridLayout, QLabel, QWidget 
from PyQt5.QtGui import QPixmap
import silx.gui.hdf5





def Intro_tab(window):
    ''' a variavel window é a classe Periodic_gui, desta forma sera como entrada 'self' '''
#######################LAYOUT DA ABA INTRO TAB################################
    intro_tab=QWidget()
    layout_intro=QVBoxLayout()
    Middle_intro=QGridLayout()
    
    open_file_button=QPushButton('Open File') #Botao de abrir arquivos
    select_data_button=QPushButton('Select Data')
    logo=QLabel()    #Logo
    pixmap=QPixmap("Hdf5_gui/_images/logo.jpg")
    logo.setPixmap(pixmap)
    
    
    window.treeview=silx.gui.hdf5.Hdf5TreeView(window)
    
    
    developer_label=QLabel("<b>Developer: Carlos Eduardo Mendes <br>"
    "Contact: <i>carlos.mendes@lnls.br</i></b><br>"
    "<b>Beamline Group: <i>Carnauba</i></b>")

    show_window = QPushButton('Show XRD Image')
    show_window.clicked.connect(window.mostrar_xrd)


    
    
    help_link= QLabel("<a href=http://www.cnpem.br> Click here to open the User Guide </a>") #contem link para tutorial        
    help_link.setOpenExternalLinks(True)
    layout_intro.addWidget(open_file_button)
    layout_intro.addWidget(window.treeview)
    layout_intro.addWidget(select_data_button)
    layout_intro.addWidget(show_window)
    
    Middle_intro.addWidget(developer_label,1,1)
    Middle_intro.addWidget(logo,3,1)
    Middle_intro.addWidget(help_link,4,1)


    
    
    layout_intro.addLayout(Middle_intro)
    intro_tab.setLayout(layout_intro)
    window.tabs.addTab(intro_tab,'Introduction')

##############################################################################
    
    open_file_button.clicked.connect(window.Open_file)
    # window.treeview.activated.connect(window.test)
    select_data_button.clicked.connect(window.select_data)
    
    