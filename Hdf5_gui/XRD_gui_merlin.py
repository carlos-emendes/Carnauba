from PyMca5.PyMcaPhysics.xrf import Elements
import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QVBoxLayout, QTabWidget, QLabel, QWidget, \
    QTableWidget, QTableWidgetItem, QAbstractItemView
import matplotlib
from PyQt5 import QtGui
import pyqtgraph as pg
import numpy as np
# from Carnauba_exp import hdf5File
from Hdf5_gui.Hdf5_widgets_XRD.Intro_widget import Intro_tab
import h5py


class XRD_interface(QMainWindow):
    ''' Classe responsavel por gerar uma interface para estudo de '''

    def __init__(self):
        super().__init__()

        # Dados que serao obtidas pela funcao Carnauba e de inicialização

        self.Data = []  # arquivo HDF5
        self.filename = []  # Nome do arquivo HDF5
        self.Elements = []  #
        self.row = 0  # linha em que a tabela se encontra
        self.last_b = 0  # último botao pressionado na aba Periodic
        self.img_2d = []  # lista com as imagens 2D

        # Estrutura da GUI
        self.topo = 100
        self.esquerda = 100
        self.largura = 1000
        self.altura = 700
        self.titulo = 'XRD Interface'

        self.tabs = QTabWidget()

        Intro_tab(self)

        self.setCentralWidget(self.tabs)

        self.Carregar()

    def Open_file(self):  # Seleciona o arquivo HDF5
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Select File')
        if filename[0] != [] and self.filename != filename[0]:
            self.filename = filename[0]
            self.treeview.findHdf5TreeModel().clear()
            self.treeview.findHdf5TreeModel().appendFile(self.filename)

    def select_data(self):
        c = ['entry_0000', 'entry_0001', 'entry_0002', 'entry_0003', 'entry_0004', 'entry_0005', 'entry_0006',
             'entry_0007', 'entry_0008', 'entry_0009', 'entry_0010', 'entry_0011', 'entry_0012', 'entry_0013',
             'entry_0014', 'entry_0015', 'entry_0016', 'entry_0017', 'entry_0018', 'entry_0019', 'entry_0020',
             'entry_0021', 'entry_0022', 'entry_0023', 'entry_0024', 'entry_0025', 'entry_0026', 'entry_0027',
             'entry_0028', 'entry_0029', 'entry_0030', 'entry_0031', 'entry_0032', 'entry_0033', 'entry_0034',
             'entry_0035', 'entry_0036', 'entry_0037', 'entry_0038', 'entry_0039', 'entry_0040', 'entry_0041',
             'entry_0042', 'entry_0043', 'entry_0044', 'entry_0045', 'entry_0046', 'entry_0047', 'entry_0048',
             'entry_0049', 'entry_0050']
        hdf_xrd = h5py.File(self.filename, 'r')
        a = np.zeros([51, 51, 515, 515], dtype=np.float)
        stack = np.zeros([51, 51], dtype=np.float)

        for i in range(51):
            dados = np.array(hdf_xrd[c[i] + '/instrument/Merlin/data'][()])
            # dados = np.array(hdf_xrd[c[i] + '/instrument/xspress3/data'][()])


            for j in range(51):
                a[i][j] = dados[j]
                stack[i][j] = a[i][j].sum()
        self.dados = a
        self.stack = stack

    def mostrar_xrd(self):
        layout = QVBoxLayout()

        try:
            img = (self.stack)
            win = QMainWindow(self)
            widget = QWidget()
            win.setWindowTitle('XRD Image')

            imv = pg.ImageView(view=pg.PlotItem())
            imv.view.invertY(False)
            layout.addWidget(imv)
            imv2 = pg.ImageView()
            layout.addWidget(imv2)
            layout.setStretch(0, 5)
            layout.setStretch(1, 5)

            widget.setLayout(layout)
            win.setCentralWidget(widget)
            win.show()
            imv.setImage(img)
            imv.ui.roiBtn.hide()
            imv.ui.menuBtn.hide()

            def hoverEvent(event):  # funcao para obter o pixel do mouse
                if event.isExit():

                    return
                else:
                    pos = event.pos()
                    i, j = pos.y(), pos.x()
                    i = int(np.clip(i, 0, img.shape[0] - 1))
                    j = int(np.clip(j, 0, img.shape[1] - 1))
                    val = img[i, j]

                    imv2.setImage(self.dados[i][j], levels=[0, 1])

            imv.imageItem.hoverEvent = hoverEvent


        except IndexError:
            pass

    def Carregar(self):
        # variáveis: a distância à esquerda, distância ao topo, largura e altura
        self.setGeometry(self.esquerda, self.topo, self.largura, self.altura)
        self.setWindowTitle(self.titulo)
        self.setWindowIcon(QtGui.QIcon("C:/Users/Carlos/Python_Estagio/Hdf5_gui/CNPEM.jpg"))
        self.show()


def XRD_gui():
    app = QApplication(sys.argv)
    j = XRD_interface()
    app.exec_()
    return j.Data


if __name__ == "__main__":
    Data = XRD_gui()
