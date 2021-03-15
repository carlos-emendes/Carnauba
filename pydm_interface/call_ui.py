import os
import pyqtgraph as pg
from PyMca5.PyMcaPhysics.xrf import Elements
from PyQt5 import QtGui
from PyQt5.QtWidgets import QTableWidgetItem, QVBoxLayout, QMainWindow, QWidget, QLabel
from pydm import Display
import numpy as np
from carnauba_exp import hdf5File


class XRF_display(Display):
    # PyDM Application pass parameters to Display.
    # You can use them according to your needs.
    def __init__(self, parent=None, args=None, macros=None, ui_filename=None):
        super(XRF_display, self).__init__(ui_filename='XRF_gui.ui', macros=macros)
        # Connecting the button to a routine

        self.Data=[] #arquivo HDF5
        self.filename=[] #Nome do arquivo HDF5
        self.Elements=[] #
        self.row=0 #linha em que a tabela se encontra
        self.last_b=0 #último botao pressionado na aba Periodic
        self.img_2d=[] #lista com as imagens 2D
        self.edge_b = [self.ui.bot_Ka, self.ui.bot_Kb, self.ui.bot_La, self.ui.bot_Lb]
        self.lr = pg.LinearRegionItem([0, 10])
        self.lr_image = pg.LinearRegionItem(movable=False, pen='r')

        self.ui.table.setRowCount(20)  # Numero de linhas
        self.ui.table.setColumnCount(3)  # numero de colunas
        self.ui.table.setHorizontalHeaderLabels(['Chmin', 'Chmax', 'Title'])  # titulo das colunas



        #First Tab Commands
        self.ui.open_file_button.clicked.connect(self.Open_file)
        self.ui.select_data_button.clicked.connect(self.select_data)

        #Second Tab Commands

        self.ui.f.table.sigElementClicked.connect(self.Check_Energy)
        self.ui.bot_Ka.clicked.connect(self.Energy_edge)
        self.ui.bot_Kb.clicked.connect(self.Energy_edge)
        self.ui.bot_La.clicked.connect(self.Energy_edge)
        self.ui.bot_Lb.clicked.connect(self.Energy_edge)
        self.ui.bot1.clicked.connect(self.Energy_line)
        self.ui.bot2.clicked.connect(self.cleargraph)


        #Third Tab Commands
        self.ui.Bot_roi.clicked.connect(self.XRF_img)
        self.lr.sigRegionChanged.connect(self.update_channel_graph)
        self.ui.channel_change_button.clicked.connect(self.update_channel_text)
        self.ui.Energy_check.toggled.connect(self.change_axis_channel)


        #Fourth Tab Commands
        self.ui.table.cellClicked.connect(self.show_img)
        self.ui.Rgb_button.clicked.connect(self.rgb_show)
        self.ui.image_button.clicked.connect(self.img_show_window)
        self.ui.delete_table.clicked.connect(self.delete_table_function)



    def Open_file(self): #Seleciona o arquivo HDF5
        filename=QtGui.QFileDialog.getOpenFileName(self,'Select File')
        if filename[0]!=[] and self.filename!=filename[0]:
            self.filename=filename[0]
            self.ui.treeview.findHdf5TreeModel().clear()
            self.ui.treeview.findHdf5TreeModel().appendFile(self.filename)

    def select_data(self):
        objects = list(self.treeview.selectedH5Nodes())
        obj=objects[0]

        self.Elements=[]
        self.row=0
        self.last_b=0
        self.Data= hdf5File(self.filename,obj.name)
        self.Data.XRF_data()
        self.Data.xrf_stackdata+=1 #Adiciona uma contagem para todos os canais, apenas para que o gráfico no pyqtgraph em escala log funcione.
        self.Data.XRF_Energy_calib()
        self.img_2d=[]

        self.ui.table.clear()
        self.ui.table.setHorizontalHeaderLabels(['Chmin','Chmax','Title'])
        self.row=0

        self.ui.sc.clear()
        self.ui.sc.plot(self.Data.Energy,self.Data.xrf_stackdata, pen='r')

        self.ui.p1.clear()
        self.ui.p2.clear()
        self.ui.p3.clear()


        self.ui.p1.plot(self.Data.xrf_stackdata, pen='b')
        self.ui.p1.setLabel('bottom',"Channel")
        self.ui.p1.addItem(self.lr)

        self.ui.p2.ui.roiBtn.hide()
        self.ui.p2.ui.menuBtn.hide()
        self.ui.p2.ui.histogram.hide()

        self.ui.p3.plot(self.Data.xrf_stackdata, pen='b')
        self.ui.p3.addItem(self.lr_image)

    def Check_Energy(self): #Verifica se o Elemento em questao possui nivel de energia acessivel
        Element=self.ui.f.lastElement
        if Element != None:
        #Mostra os tipos de fluorescencia que ocorrem

            xrays=Elements.Element[Element]
            #Habilita e desabilita os botoes

            if('KL2' in xrays)==True:
                self.ui.bot_Ka.setEnabled(True)
            else:
                self.ui.bot_Ka.setEnabled(False)
                self.ui.bot_Ka.setChecked(False)


            if('KM2' in xrays)==True:
                self.ui.bot_Kb.setEnabled(True)
            else:
                self.ui.bot_Kb.setEnabled(False)
                self.ui.bot_Kb.setChecked(False)


            if ('L3M5' in xrays)==True:
                self.ui.bot_La.setEnabled(True)
            else:
                self.ui.bot_La.setEnabled(False)
                self.ui.bot_La.setChecked(False)

            if ('L2M4' in xrays)==True:
                self.ui.bot_Lb.setEnabled(True)
            else:
                self.ui.bot_Lb.setEnabled(False)
                self.ui.bot_Lb.setChecked(False)
        else:
            pass

    def Energy_edge(self): #Responsavel por impedir que dois botoes de energia sejam pressionados
        state=[]
        a=0 #contador
        for bot in self.edge_b:
            if bot.isChecked():
                a+=1

        for bot in self.edge_b:
            if bot.isChecked() and a==1: #apenas um botao apertado
                self.last_b=bot
                state.append(True)
            elif bot.isChecked() and a==2: #quando o segundo botao for apertado
                if bot!=self.last_b:
                    state.append(True) # o ultimo botao acionado e pressionado e o o anterior volta ao estado 0
                else:
                    state.append(False)
            else:
                state.append(False)
        #Muda a cor dos botoes quando ativados/desativados
        for i in  range(len(self.edge_b)):
            self.edge_b[i].setChecked(state[i])
            if state[i]==True:
                self.last_b=self.edge_b[i]

    def Energy_line(self):
        Bclick=[]
        Bclick.append(self.ui.f.lastElement)
        if Bclick == [None]:
            print('Select an Element')
        else: #ADICIONA A LISTA O NIVEL DE ENERGIA SELECIONADO
            if self.ui.bot_Ka.isChecked():
                Bclick.append('KL2')
                Bclick.append('K\u03b1')
            if self.ui.bot_Kb.isChecked():
                Bclick.append('KM2')
                Bclick.append('K\u03b2')
            if self.ui.bot_La.isChecked():
                Bclick.append('L3M5')
                Bclick.append('L\u03b1')
            if self.ui.bot_Lb.isChecked():
                Bclick.append('L2M4')
                Bclick.append('L\u03b2')



            if len(Bclick)>1: #Caso um  nivel de energia for escolhido
                vertical_line=pg.InfiniteLine(pos=Elements.Element[Bclick[0]][Bclick[1]]['energy'],angle=90,pen='b', movable=False)
                self.ui.sc.addItem(vertical_line)

                if (Bclick in self.Elements)==False: #Caso o elemento selecionado ainda nao foi escolhido pelo usuario
                    self.Elements.append(Bclick)
                    self.add_roi(Bclick,self.row,1) #o segundo número é para saber em qual aba ele se encontra
            else:
                print('Select an energy level')

    def cleargraph(self):
        #Limpa o grafico e limpa os elementos selecionados
        self.Elements=[]
        self.ui.sc.clear()
        self.sc.plot(self.Data.Energy, self.Data.xrf_stackdata, pen='r')

    def add_roi(self,data,row,mod):
        if mod==1:
            Energy=np.asarray(self.Data.Energy)
            Elementos=data
            binding=Elements.Element[Elementos[0]][Elementos[1]]['energy']
            idx = (np.abs(Energy - binding)).argmin()
            if (min(np.abs(Energy - binding)))<1:
                chmin=idx-1
                chmax=idx+1
                title= 'Element: '+ Elementos[0]+'  Transition: '+Elementos[2]
                # roi=[chmin,chmax,title]
                self.ui.table.setItem(row,0,QTableWidgetItem(str(chmin)))
                self.ui.table.setItem(row,1,QTableWidgetItem(str(chmax)))
                self.ui.table.setItem(row,2,QTableWidgetItem(title))
                for i in range(3):
                    self.ui.table.item(row,i).setBackground(QtGui.QColor(255,51,51))
                img=np.zeros([len(self.Data.xrf_data),len(self.Data.xrf_data[0])])
                for i in range(len(self.Data.xrf_data)):
                    for j in range(len(self.Data.xrf_data[0])):
                        intensity=0
                        for k in range(chmax-chmin+1):
                              intensity=intensity+self.Data.xrf_data[i][j][chmin+k]
                        img[i][j]=intensity

                self.img_2d.append(img)
                self.row+=1
        if mod==2:
            chmin=data[0]
            chmax=data[1]
            title=self.ui.channel_title_edit.text()
            self.ui.table.setItem(row,0,QTableWidgetItem(str(chmin)))
            self.ui.table.setItem(row,1,QTableWidgetItem(str(chmax)))
            self.ui.table.setItem(row,2,QTableWidgetItem(title))
            for i in range(3):
                self.ui.table.item(row,i).setBackground(QtGui.QColor(153,153,255))

            img=np.zeros([len(self.Data.xrf_data),len(self.Data.xrf_data[0])])
            for i in range(len(self.Data.xrf_data)):
                for j in range(len(self.Data.xrf_data[0])):
                    intensity=0
                    for k in range(chmax-chmin+1):
                          intensity=intensity+self.Data.xrf_data[i][j][chmin+k]
                    img[i][j]=intensity

            self.img_2d.append(img)
            self.row+=1

    def XRF_img(self):
        [Chmin,Chmax]=self.lr.getRegion()
        if self.ui.Energy_check.isChecked()==0:
            Chmin=round(Chmin)
            Chmax=round(Chmax)
        else:
            Energy=np.asarray(self.Data.Energy)
            Chmin=(np.abs(Energy - Chmin)).argmin()
            Chmax=(np.abs(Energy - Chmax)).argmin()
        self.add_roi([Chmin,Chmax], self.row, 2)

    def update_channel_graph(self):
        if self.ui.Energy_check.isChecked() == 0:
            [Chmin, Chmax] = self.lr.getRegion()
            self.ui.channel_chmin_edit.setText(str(round(Chmin)))
            self.ui.channel_chmax_edit.setText(str(round(Chmax)))
        else:
            [Chmin, Chmax] = self.lr.getRegion()
            self.ui.channel_chmin_edit.setText(str(round(Chmin,2)))
            self.ui.channel_chmax_edit.setText(str(round(Chmax,2)))

    def update_channel_text(self):
        chmin = self.ui.channel_chmin_edit.text()
        chmax = self.ui.channel_chmax_edit.text()
        if self.ui.Energy_check.isChecked() == 0:
            Chmin = int(chmin)
            Chmax = int(chmax)
        else:
            Chmin = float(chmin)
            Chmax = float(chmax)

        self.lr.setRegion([Chmin, Chmax])

    def change_axis_channel(self):
        self.ui.p1.clear()
        self.ui.p1.addItem(self.lr)
        if self.ui.Energy_check.isChecked()==1:
            self.ui.p1.plot(self.Data.Energy,self.Data.xrf_stackdata, pen='b', )
            self.ui.p1.setLabel('bottom',"Energy",units='Kev')
        else:
            self.ui.p1.plot(self.Data.xrf_stackdata, pen='b')
            self.ui.p1.setLabel('bottom',"Channel", units='')

    def delete_table_function(self):
        row_selected = []
        rows = self.ui.table.selectionModel().selectedRows()

        for i in sorted(rows):
            row_selected.append(i.row())
        row_selected.reverse()  # remover as linhas de baixo para cima

        # self.row-=1
        self.row -= len(row_selected)
        # row=self.table.currentRow()
        for row in row_selected:
            self.ui.table.removeRow(row)
            try:
                del self.img_2d[row]
            except IndexError:
                pass
        self.ui.table.setRowCount(20)

    def show_img(self):
        row=self.ui.table.currentRow()
        try:
            img=pg.ImageItem(self.img_2d[row])


            self.ui.p2.addItem(img)
            Chmin=int((self.ui.table.item(row,1).text()))
            Chmax=int((self.ui.table.item(row,0).text()))
            self.lr_image.setRegion([Chmin,Chmax])
        except IndexError:
            pass

    def rgb_show(self):
        a=self.ui.table.selectionModel().selectedRows()

        layout=QVBoxLayout()

        if len(a)==3:
            try:
                rows=[a[0].row(),a[1].row(),a[2].row()]
                Title_red=self.ui.table.item(rows[0],2).text()
                Title_green=self.ui.table.item(rows[1],2).text()
                Title_blue=self.ui.table.item(rows[2],2).text()


                r=self.img_2d[rows[0]]
                g=self.img_2d[rows[1]]
                b=self.img_2d[rows[2]]

                cor=[r,g,b]
                RGB = np.zeros([len(r), len(r[1]), 3], dtype="d")
                for i in range(3):
                    cor[i][cor[i]<0]=0.
                    cor[i]=cor[i]/cor[i].max()
                    RGB[:,:,i]=cor[i]

                win =QMainWindow(self)
                widget=QWidget()
                win.setWindowTitle('RGB Image')




                #Titulo
                string1="<b style='color:red'>Red: </b>" + "<a>%s</a> <br>" %Title_red
                string2="<b style='color:green'>Green: </b>" + "<a>%s</a> <br>" %Title_green
                string3="<b style='color:blue'>Blue: </b>" + "<a>%s</a>" %Title_blue
                Elementos=string1+string2+string3
                title=QLabel(Elementos)
                title.setFont(QtGui.QFont('Arial',12))

                #Imagem
                imv = pg.ImageView(view=pg.PlotItem())
                imv.view.invertY(False)


                layout.addWidget(title)
                layout.addWidget(imv)

                widget.setLayout(layout)
                win.setCentralWidget(widget)

                win.show()
                imv.setImage(RGB*255, levelMode='rgba')
                image=imv.getView()

                def hoverEvent(event): #funcao para obter o pixel do mouse
                 if event.isExit():

                     return
                 else:
                     pos = event.pos()
                     i, j = pos.y(), pos.x()
                     i = int(np.clip(i, 0, RGB.shape[0] - 1))
                     j = int(np.clip(j, 0, RGB.shape[1] - 1))
                     val_red = RGB[i][j][0]*255
                     val_green= RGB[i][j][1]*255
                     val_blue= RGB[i][j][2]*255

                     image.setTitle('pixel: (%d, %d) &nbsp;&nbsp;&nbsp; Value[R,G,B]: (%d,%d,%d)' % (j, i, val_red,val_green,val_blue))


                imv.imageItem.hoverEvent=hoverEvent
            except IndexError:
                pass

    def img_show_window(self):
        a=self.ui.table.selectedItems()
        layout=QVBoxLayout()



        try:
            row=a[0].row()
            img=(self.img_2d[row])

            win =QMainWindow(self)
            widget=QWidget()
            win.setWindowTitle('XRF Image')
            Elemento=self.ui.table.item(row,2).text()
            title=QLabel(Elemento)
            # title.setFont(QtGui.QFont('Arial',12))
            imv = pg.ImageView(view=pg.PlotItem())
            imv.view.invertY(False)
            layout.addWidget(title)
            layout.addWidget(imv)
            spectra_window=pg.GraphicsWindow()
            p1=spectra_window.addPlot(title="XRF Intensity")
            p1.setLogMode(False,True)
            layout.addWidget(spectra_window)
            layout.setStretch(0,5)
            layout.setStretch(1,65)
            layout.setStretch(2,30)



            widget.setLayout(layout)
            win.setCentralWidget(widget)
            win.show()
            imv.setImage(img)
            image=imv.getView()
            imv.ui.roiBtn.hide()
            imv.ui.menuBtn.hide()

            def hoverEvent(event): #funcao para obter o pixel do mouse
             if event.isExit():
                #Manter os dados ao tirar o mouse da imagem
                 return
             else:
                 pos = event.pos()
                 i, j = pos.y(), pos.x()
                 i = int(np.clip(i, 0, img.shape[0] - 1))
                 j = int(np.clip(j, 0, img.shape[1] - 1))
                 val = img[i, j]
                 p1.clear()
                 p1.setLabel('bottom',"Energy[Kev]")
                 logdata=self.Data.xrf_data[i,j]
                 logdata+=1 #Caso nao seja modificado, o plot pelo pyqtgraph nao aparece em escala log

                 p1.plot(self.Data.Energy, logdata, pen='b')
                 image.setTitle('pixel: (%d, %d) &nbsp;&nbsp;Value: %d' % (j, i, val))


            imv.imageItem.hoverEvent=hoverEvent
        except IndexError:
            pass

def xrf_linux():
    os.system("pydm call_ui.py")

if __name__=="__main__":

    os.system("pydm call_ui.py")
