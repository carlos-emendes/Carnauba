
from PyQt5.QtWidgets import  QLineEdit, QLabel, QWidget ,QGridLayout
from PyQt5.QtGui import QPixmap


def Info_tab(window):
    info_tab= QWidget()
    layout_info = QGridLayout()
    Int_text=QLabel()
    Int_text.setText('<p>Intensity(I0)</p>')
    I0_label=QLineEdit()
    
    
    


    layout_info.addWidget(Int_text,0,0)
    layout_info.addWidget(I0_label,0,1)


    info_tab.setLayout(layout_info)

    
    window.tabs.addTab(info_tab, 'Information')