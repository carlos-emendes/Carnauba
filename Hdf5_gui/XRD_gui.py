import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
from PyQt5 import QtGui
from Hdf5_gui.Carnauba_exp import hdf5File
from Hdf5_gui.Hdf5_widgets_XRD.Intro_widget import Intro_tab




class XRD_interface(QMainWindow):
    '''' Classe responsavel por gerar uma interface para estudo de '''
    def __init__(self):
        super().__init__()
        
        #Dados que serao obtidas pela funcao Carnauba e de inicialização
 
        self.Data=[] #arquivo HDF5
        self.filename=[] #Nome do arquivo HDF5
        self.Elements=[] #
        self.row=0 #linha em que a tabela se encontra
        self.last_b=0 #último botao pressionado na aba Periodic
        self.img_2d=[] #lista com as imagens 2D
        
        #Estrutura da GUI
        self.topo= 100
        self.esquerda=100
        self.largura= 1000
        self.altura= 700
        self.titulo= 'XRD Interface'
        
        self.tabs=QTabWidget()
        
        Intro_tab(self)
        
        
        self.setCentralWidget(self.tabs)
        
        self.Carregar()
        
    def Open_file(self): #Seleciona o arquivo HDF5
        filename=QtGui.QFileDialog.getOpenFileName(self,'Select File')
        if filename[0]!=[] and self.filename!=filename[0]:
            self.filename=filename[0]
            self.treeview.findHdf5TreeModel().clear()
            self.treeview.findHdf5TreeModel().appendFile(self.filename)
            
    def select_data(self):
        objects = list(self.treeview.selectedH5Nodes())
        obj=objects[0]
        # self.Elements=[]
        # self.row=0
        # self.last_b=0
        self.Data=hdf5File(self.filename,obj.name)
        
        self.Data.XRD_data()
        # self.Data.XRF_Energy_calib()
        # self.img_2d=[]
        
    def Carregar(self):
        #variáveis: a distância à esquerda, distância ao topo, largura e altura
        self.setGeometry(self.esquerda,self.topo,self.largura,self.altura)
        self.setWindowTitle(self.titulo)
        self.setWindowIcon(QtGui.QIcon("C:/Users/Carlos/Python_Estagio/Hdf5_gui/CNPEM.jpg"))
        self.show()

def XRD_gui():
    
    app=QApplication(sys.argv)
    j=XRD_interface()
    app.exec_()
    return j.Data


if __name__=="__main__":
    Data=XRD_gui()