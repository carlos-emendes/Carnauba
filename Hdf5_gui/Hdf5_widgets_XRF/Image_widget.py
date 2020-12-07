
from PyQt5.QtWidgets import   QPushButton,QVBoxLayout,QHBoxLayout,QGridLayout, QLabel, QWidget
from PyQt5 import  QtCore
import pyqtgraph as pg


def Image_tab(window):
    image_tab=QWidget()
    Layout_Data_Vis=QVBoxLayout()
    Bottom_roi=QHBoxLayout()
    grid_layout=QGridLayout()
    
    cor_periodic=QLabel()
    cor_periodic.setStyleSheet("background-color: rgb(255, 51, 51)")
    cor_periodic.setFixedSize(20,20)
    
    cor_channel=QLabel()
    cor_channel.setStyleSheet("background-color: rgb(153,153,255)")
    cor_channel.setFixedSize(20,20)
    
    
    sc_image=pg.GraphicsWindow()
    window.p2=sc_image.addViewBox(enableMouse=False)
    sc_image.nextRow()
    window.p3=sc_image.addPlot(title="XRF Intensity",movable=True) 

    window.p3.setLogMode(False,True)
    window.lr_image=pg.LinearRegionItem(movable=False, pen='r')
    
    Rgb_button=QPushButton('RGB')
    image_button=QPushButton('Image Preview')
    
    delete_table=QPushButton('Delete Row')
    
    
    grid_layout.addWidget(cor_periodic,0,0)
    grid_layout.addWidget(QLabel('Periodic Table'),0,1)
    grid_layout.addWidget(cor_channel,1,0)
    grid_layout.addWidget(QLabel('Selection by Channel'),1,1)
    grid_layout.addWidget(Rgb_button,2,1)
    grid_layout.addWidget(image_button,3,1)
    grid_layout.addWidget(delete_table,4,1)  
    grid_layout.setAlignment(QtCore.Qt.AlignTop)
    

    
    Bottom_roi.addWidget(sc_image)
    Bottom_roi.addWidget(window.table)
    Bottom_roi.addLayout(grid_layout)
    Bottom_roi.setStretch(0,6)
    Bottom_roi.setStretch(1,2)
    Bottom_roi.setStretch(2,1)
    
    Layout_Data_Vis.addLayout(Bottom_roi)
    image_tab.setLayout(Layout_Data_Vis)
    
    
    
    window.tabs.addTab(image_tab, 'Data visualization')
    
    window.table.cellClicked.connect(window.show_img)
    Rgb_button.clicked.connect(window.rgb_show)
    image_button.clicked.connect(window.img_show_window)
    delete_table.clicked.connect(window.delete_table_function)