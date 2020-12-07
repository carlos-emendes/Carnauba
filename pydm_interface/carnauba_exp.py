import numpy as np
import h5py
from math import log, sqrt
from scipy.constants import m_e, hbar
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import csv
from lmfit.models import QuadraticModel, LinearModel


#####################################
#Desenvolvedor: Carlos Eduardo Mendes
#Grupo: Carnaúba
#Contato: carlos.mendes@lnls.br

# O programa consiste em abrir o arquivo hdf5 gerado na linha experimental e extrair os dados dos detectores.
#Ademais, conta com funções de plot para XRF, XEOL e XAS (futuramente XRD) e imagem 2D para XRF #

###################################


class hdf5File:
    
    def __init__(self,filename,tree):
        self.file=filename
        plt.rcParams["figure.figsize"] = (5,10)
        self.tree=tree
        
        #Dados de XRF
        #self.xrf_stackdata
        #self.xrf_data
        #self.xrf_2d_img
        
        #Dados de XRD
        
        #Dados de XAS
        #self.Energy
        #self.I0
        #self.I1
        #self.xas_time
        #self.Abs
 

#RETIRAR APOS EXISTIR NOVO ARQUIVO hdf5
        #self.XRF_data()
        #self.XAS_data()
        
        
        
    #Experimento de Fluorescência
    def XRF_data(self):
        '''Funcao responsavel por retirar os dados de XRF (X-ray Fluorescensce) no formato hdf5.
        xrf_data: conjunto de dados de xrf em uma matriz da forma [nx,ny], onde cada par ordenado representa um pixel
        xrf_stackdata: somatoria dos dados de xrf de todos os pixels'''
        
        
        
        dados=0
        hdf_xrf=h5py.File(self.file,'r') 
        
        #Função responsável por retirar os dados
        # data=np.array(hdf_xrf['data_norm']) # Quando o novo formato for gerado, modificar onde é retirado os dados
        data=np.array(hdf_xrf[self.tree])
        # data=np.array(hdf_xrf['vortex'])
        # data=np.array(hdf_xrf['image1_001-norm']) # Ex:'C:/Users/Carlos/Desktop/Dados_Sirius/image1_001.hdf'
        
        
        for i in range(len(data)):
            for j in range(len(data[0])):
                dados=data[i,j]+dados
        
        #dados XRF        
        self.xrf_data=data
        self.xrf_stackdata=dados
        
    def XRF_exp(self):
        ''''Gera graficos dados de XRF, necessario utilizar a funcao XRF_data anteriormente. '''
        fig,(ax1,ax2)= plt.subplots(2)
        ax1.plot(self.xrf_stackdata)
        ax1.grid(color='k', linestyle='-', linewidth=.1)
        ax2.semilogy(self.xrf_stackdata)
        ax2.grid(color='k', linestyle='-', linewidth=.1)
        
        ax2.set_xlabel('Channel')
        ax1.set_ylabel('Counts')
        ax2.set_ylabel('Counts')
        plt.show()
        
    
    
    #Experimento de Difração
    def XRD_data(self):
        '''Funcao ainda nao implementada'''
        
        hdf_xrd=h5py.File(self.file,'r')
        data=hdf_xrd[self.tree]
        self.xrd_data=data
   
    
    #Experimento de Absorção        
    def XAS_data(self):
        '''Retira os dados de XAS (X-ray absortion Spectroscopy) de um arquivo em um formato tiff. Futuramente sera alterado para retirada em formato hdf5
        Energy: lista com valores do espectro Energia do experimento de XAS
        xas_time:  lista com os valores de tempo de cada aquisicao por ponto
        I0: Lista com os valores de intensidade de raio-x antes de incidir na amostra
        I1:Lista com os valores de intensidade de raio-x apos incidir a amostra
        Abs:Lista com os valores do log(I0/I1)'''
        
        #Variaveis iniciais para alocacao dos valores
        Energy=[]
        I0=[]
        I1=[]
        time=[]
        Abs1=[]
        
        dados=0
        fid=open(self.file)
        
        
        # Metodo deve ser alterado quando novo formato hdf5 for gerado.
        for i in range (13):
            fid.readline()
        for linha in fid:          
            dados=linha.split()
            if dados!=[]:
                Energy.append(float(dados[0]))
                time.append(float(dados[3]))
                I0.append(float(dados[4]))
                I1.append(float(dados[5]))
        for i in range(len(I0)):
            Abs1.append(log(I0[i]/I1[i]))
        
        #Dados XAS
        self.Energy=Energy
        self.xas_time=time
        self.I0=I0
        self.I1=I1
        self.Abs=Abs1
        
        
 
    def XAS_exp(self):
        ''' Gera grafico de XAS '''
        plt.plot(self.Energy,self.Abs)
        plt.xlabel('Energy [kev]')
        plt.ylabel('$\mu$(E)')
        plt.show()
        
 ###FUNÇOES DE PROCESSAMENTO DE DADOS PARA XRF####

    # def XRF_peaks(self,chmin,chmax):
    #     newdata=self.xrf_stackdata[chmin:chmax]
    #     logdata=[]
    #     x=[]
    #     j=0
    #     for i in range(len(newdata)):
    #         logdata.append(log(newdata[i]))
    #         x.append(chmin+j)
    #         j=j+1

    #     logdata=np.array(logdata)
    #     ind=detect_peaks(logdata, mph=9.5, mpd=28,show=False)
    #     xpeak=[]

    #     for i in range(len(ind)):
    #         xpeak.append(x[ind[i]])
    #     print('Peaks:',xpeak)    
    #     plt.plot(x,logdata)
    #     plt.plot(xpeak,logdata[ind],'x')
    #     plt.show()
    
  
       
        
        
    def XRF_2D_img(self,Chmin,Chmax,xpixel,ypixel,title,xlabel,ylabel):
        """Funcao responsavel por gerar imagem 2D dos dados de XRF, selecionando uma regiao de interesse(ROI) para obtencao da imagem. Funciona somente apos a funcao XRF_Data.
        Chmin: Canal onde comeca o ROI  
        Chmax:canal onde termina o ROI
        xpixel,ypixel: tamanho do pixel
        title: titulo do grafico
        eixox,eixoy: nome dos eixos x e y
        Ex: XRF_2D_img(300,320,0,02,0,02,'Fe','mm','mm')
        A imagem fica alocada em lista self.xrf_2d_img.
        """
        xrf_pixel=self.xrf_data
        xdata=np.arange(len(xrf_pixel[0]))
        ydata=np.arange(len(xrf_pixel))
        X,Y=np.meshgrid(xdata*xpixel,ydata*ypixel)  #X,Y: matriz com o tamanho  numero de pixel em x por numero de pixel em y. Necessario para gerar o grafico de cor
                 
        pixel=np.zeros([len(xrf_pixel),len(xrf_pixel[1])])


        for i in range(len(xrf_pixel)):
            for j in range(len(xrf_pixel[0])):
                intensity=0
                spectra=xrf_pixel[i][j]
                for k in range(Chmax-Chmin+1):
                     intensity=intensity+spectra[Chmin+k]
            
        
                pixel[i][j]=intensity #Intensidade do espectro do pixel

        
        
        self.xrf_2d_img=[X,Y,pixel] #mapa de cor
        fig,(ax1,ax2)=plt.subplots(2)    
        ax1.pcolor(X,Y,pixel, cmap='gray') #grafico de cor com escala de cor indicada em cmap.
        ax1.set_xlabel(xlabel)
        ax1.set_ylabel(ylabel)
        ax1.set_title(title)
        
        
        #Graficos verticais para representar a ROI selecionada
        ax2.semilogy(self.xrf_stackdata)
        ax2.axvline(Chmin,color='r')
        ax2.axvline(Chmax,color='r')
        plt.show()


    def plot_ROI(self,Roi):
        '''Gera n>=1 graficos de cores, de acordo com a Roi selecionada
        Roi: lista com o conjunto de ROI selecionado para os graficos de cores da forma Roi=[Roi1,Roi2,Roi3...Roin]. Cada Roin deve ser uma lista com  3 variaveis [Chmin,Chmax,cmap].
        Chmin: Canal onde comeca o ROI  
        Chmax:canal onde termina o ROI
        title: string com o titulo do grafico
        
        Ex: Roi1=[100,200,'Fe']
        Roi2=[50,60,'Co']
        plot_Roi([Roi1,Roi2])'''
        
        
        fig=plt.figure()
        axes=fig.subplots(2,len(Roi))


        xrf_pixel=self.xrf_data
        xdata=np.arange(len(xrf_pixel[0]))
        ydata=np.arange(len(xrf_pixel))
        # X,Y=np.meshgrid(xdata,ydata)
        
        for l in range(len(Roi)):
            Chmin=Roi[l][0]
            Chmax=Roi[l][1]
            pixel=np.zeros([len(xrf_pixel),len(xrf_pixel[1])])
            for i in range(len(xrf_pixel)):
                for j in range(len(xrf_pixel[0])):
                    intensity=0
                    spectra=xrf_pixel[i][j]
                    for k in range(Chmax-Chmin+1):
                        intensity=intensity+spectra[Chmin+k]


                    pixel[i][j]=intensity
                    
            
            #Caso especifico em que somente uma roi e selecionada
            if len(Roi)==1:
                axes[0].pcolor(pixel,cmap='gray')
                axes[1].semilogy(self.xrf_stackdata)
                axes[1].axvline(Chmin,color='r')
                axes[1].axvline(Chmax,color='r')
                axes[0].set_title(Roi[0][2])
            
                
                    
            else:        
                axes[0,l].pcolor(pixel,cmap='gray')
                axes[0,l].set_title(Roi[l][2])
                axes[1,l].semilogy(self.xrf_stackdata)
                axes[1,l].axvline(Chmin,color='r')
                axes[1,l].axvline(Chmax,color='r')
        
        
        
        plt.show()
        
    def plot_RGB(self,Roi,r_sat=[0,1],g_sat=[0,1],b_sat=[0,1],norm_cor=True):
        '''Gera 3 graficos de cores e 1 grafico RGB
        Roi: lista com 3 ROI selecionados para os graficos de cores da forma Roi=[Roi1,Roi2,Roi3]. Cada Roin deve ser uma lista com  3 variaveis [Chmin,Chmax,title].
        Chmin: Canal onde comeca o ROI  
        Chmax:canal onde termina o ROI
        title: string com o titulo do grafico de cor
        r_sat,g_sat,b_sat: [opcional] lista com nivel minimo e maximo de intensidade para as cores vermelho, verde e azul. Valor entre 0 e 1. Caso nao colocado na funcao, a lista fornecida para a cor sera [0,1] '''
        self.rgb=[]
        title=[]
        
        
        #variaveis de entrada para os graficos de cores
        pixel_len=0.02 #tamanho do pixel, alterar quando o valor for devidamente determinado
        label='mm'
        
        
        
        if len(Roi)==3:
            xrf_pixel=self.xrf_data
            xdata=np.arange(len(xrf_pixel[0]))
            ydata=np.arange(len(xrf_pixel))
            X,Y=np.meshgrid(xdata*pixel_len,ydata*pixel_len)
            for l in range(len(Roi)):
                Chmin=Roi[l][0]
                Chmax=Roi[l][1]
                title.append(Roi[l][2])
                pixel=np.zeros([len(xrf_pixel),len(xrf_pixel[1])])
                for i in range(len(xrf_pixel)):
                    for j in range(len(xrf_pixel[0])):
                        intensity=0
                        spectra=xrf_pixel[i][j]
                        for k in range(Chmax-Chmin+1):
                            intensity=intensity+spectra[Chmin+k]
                        pixel[i][j]=intensity
                self.rgb.append(pixel)
            
            r=self.rgb[0]
            g=self.rgb[1]
            b=self.rgb[2]
            
            
            cor=[r,g,b]
            
            #Valores de saturacao para cada cor
            sat=[r_sat,g_sat,b_sat]
            RGB = np.zeros([len(xrf_pixel), len(xrf_pixel[1]), 3], dtype="d")
            for i in range(3):
                cor[i][cor[i]<0]=0.
                
                if norm_cor==True:
                    cor[i]=cor[i]/cor[i].max()
                elif norm_cor==False:    
                    cor[i]=cor[i]/np.array(cor).max()
                
                #Aplicacao da saturacao
                slope=1/(sat[i][1]-sat[i][0])
                intercept=-sat[i][0]/(sat[i][1]-sat[i][0])
                
                #Saturacao linear
                cor[i]=slope*cor[i]+intercept
                
                    
                cor[i][cor[i]<0]=0.
                cor[i][cor[i]>1]=1
                
                
                RGB[:,:,i]=cor[i]
                
            
            #Parte responsável por gerar o histograma de cores em binagem 255
            
            
            hist_red=np.histogram(cor[0]*255,bins=np.arange(0,256,5))
            hist_green=np.histogram(cor[1]*255,bins=np.arange(0,256,5))
            hist_blue=np.histogram(cor[2]*255,bins=np.arange(0,256,5))
            
            
            ##Parte responsavel por gerar paletas de cor rgb
            
            
            
            red=[(0,0,0),(1,0,0)]
            green=[(0,0,0),(0,1,0)]
            blue=[(0,0,0),(0,0,1)]
            
            bins_r=255*(r_sat[1]-r_sat[0])
            bins_g=255*(g_sat[1]-g_sat[0])
            bins_b=255*(b_sat[1]-b_sat[0])
            
            
            map_Red = LinearSegmentedColormap.from_list('r',red, N=bins_r)
            map_Green= LinearSegmentedColormap.from_list('g',green, N=bins_g)
            map_Blue= LinearSegmentedColormap.from_list('b',blue, N=bins_b)
            
        
                
            fig=plt.figure(constrained_layout=True)
            gs = fig.add_gridspec(4, 3)
            
            
           
            ax1=fig.add_subplot(gs[0:-1,:-1])
            ax2=fig.add_subplot(gs[0,2])
            ax3=fig.add_subplot(gs[1,2])
            ax4=fig.add_subplot(gs[2,2])
            ax5=fig.add_subplot(gs[3,0])
            ax6=fig.add_subplot(gs[3,1])
            ax7=fig.add_subplot(gs[3,2])
            
            
            # ax = RGBAxes(fig, [0, 0, 1, 1])

            kwargs = dict(origin="lower", interpolation="none")
            
            #Gerar as Imagens RGB
            ax1.imshow(RGB,**kwargs)
            ax2.imshow(RGB[:,:,0],cmap=map_Red,**kwargs)
            ax3.imshow(RGB[:,:,1],cmap=map_Green,**kwargs)
            ax4.imshow(RGB[:,:,2],cmap=map_Blue,**kwargs)
            
            #Histograma de RGB
            bins_bar=np.arange(0,256,5)
            kwargs=dict(width=5)
            ax5.bar(bins_bar[:-1],hist_red[0],color=(1,0,0),**kwargs)
            ax6.bar(bins_bar[:-1],hist_green[0],color=(0,1,0),**kwargs)
            ax7.bar(bins_bar[:-1],hist_blue[0],color=(0,0,1),**kwargs)
            
            #Titulos e Eixos dos graficos
            ax1.set(title='RGB Plot',xlabel=label,ylabel=label)
            ax2.set(title=title[0])
            ax3.set(title=title[1])
            ax4.set(title=title[2])
            ax5.set(title='Red Color Histogram ', xlabel='Bin')
            ax6.set(title='Green Color Histogram', xlabel='Bin')
            ax7.set(title='Blue Color Histogram', xlabel='Bin')
            
            
            plt.show()
                
            
            
        else:
            print('Select Only 3 Rois to create the RGB plot')
            




        
    def XRF_save_img(self,Local_para_salvar_arquivo,resolucao_dpi,tittle,eixox,eixoy):
        plt.pcolor(self.xrf_2d_img[0],self.xrf_2d_img[1],self.xrf_2d_img[2],cmap='gray')
        plt.xlabel(eixox)
        plt.ylabel(eixoy)
        plt.title(tittle)
        plt.savefig(Local_para_salvar_arquivo,dpi=resolucao_dpi)
        
    
    
    def XRF_Energy_calib(self):
        x=[378,604,656]
        y=[3.6917,5.8987,6.4039]
        mod=QuadraticModel()
        pars=mod.guess(y,x=x)
        # quad_out=mod.fit(y,pars,x=x)
        
        # XRF_pixel=self.xrf_data
        XRF_dados=self.xrf_stackdata
        Energy=[]
        x=[]
        for i in range(len(XRF_dados)):
            x.append(i)
            Energy.append(pars['a'].value*i**2+pars['b'].value*i+pars['c'].value)
        
        self.Energy=Energy
        # plt.plot(Energy,XRF_dados)
        # plt.xlabel('Energy [KeV]')
        # plt.ylabel('Counts')
        # plt.show()


    # def XRF_fitting(self,ind):
    #     xrf_pixel=self.xrf_data
    #     # Data=self.xrf_data[0][0]
    #     Data=self.xrf_stackdata
    #     fit_data=np.zeros(len(Data))
    #     self.fit_pixel=np.zeros([len(xrf_pixel),len(xrf_pixel[1]),len(Data)])
        
    #     for i in range(len(ind)):
    #         Data1=Data[ind[i]-30:ind[i]+30]
    #         x=np.arange(ind[i]-30,ind[i]+30)
    #         mod=PseudoVoigtModel()
    #         pars=mod.guess(Data1,x=x)
    #         voigt=mod.fit(Data1,pars,x=x)
    #         fit_data[ind[i]-30:ind[i]+30]=voigt.best_fit
    #         for j in range(len(xrf_pixel)):
    #             for k in range(len(xrf_pixel[1])):
    #                 spec=xrf_pixel[j][k][ind[i]-30:ind[i]+30]
    #                 spec_fit=mod.fit(spec,pars,x=x)
    #                 self.fit_pixel[j][k][ind[i]-30:ind[i]+30]=spec_fit.best_fit
                    
        
        
        
    #     plt.semilogy(self.xrf_stackdata,'b-')
    #     plt.semilogy(fit_data,'r')
    #     plt.show()
        

### FUNÇÕES PARA PROCESSAMENTO DE DADOS XANES###

    def XANES_exp(self):
        background=[]
        k=[]
        #Obtenção do background
        x=self.Energy[0:50]
        y=self.Abs[0:50]
        mod=LinearModel()
        pars=mod.guess(y,x=x)
        
        
        ang_const=pars['slope'].value
        lin_const=pars['intercept'].value
        
        for i in range(len(self.Energy)):
            background.append(ang_const*self.Energy[i]+lin_const)
        
        background=np.array(background)

        #Absorcao sem o background
        Abs2=self.Abs-background

        # derivada discreta do dado sem background
        diff=np.diff(self.Abs)

        #indice do maximo da derivada
        index_max=np.where(diff==max(diff))
        
        #Valor E_0
        E0=self.Energy[index_max[0][0]]

        #valor delta de absorcao
        abs_E0=self.Abs[index_max[0][0]]
        Back_E0=ang_const*E0+lin_const
        
        delta_Abs=abs_E0-Back_E0


        #Absorcao normalizada
        Abs_norm=Abs2/delta_Abs
        
        Xanes_Energy=self.Energy[index_max[0][0]+1::]
        Xanes_abs=Abs_norm[index_max[0][0]+1::]
        
        #Calculo do vetor de onda:
        for i in range(len(Xanes_Energy)):
            Energy_j=1000*Xanes_Energy[i]*1.602176565e-19
            E0_j=1000*E0*1.602176565e-19
            wnumber=sqrt(2*m_e*(Energy_j-E0_j))/hbar
            k.append(wnumber)

        k=np.array(k)/10**10
        
        fig,(ax1,ax2,ax3,)=plt.subplots(3) 
        ax1.plot(self.Energy,self.Abs)
        ax1.plot(self.Energy,background,'r--')
        ax1.plot(E0,abs_E0,'o')
        ax2.plot(self.Energy,Abs_norm)
        ax3.plot(k,Xanes_abs)

        ax1.set_xlabel('Energy [Kev]')
        ax1.set_ylabel('$\mu$(E)')
        ax2.set_xlabel('Energy [Kev]')
        ax2.set_ylabel('Normalized $\chi$(E)')

        ax3.set_xlabel('wavenumber [$\AA^{-1}]$' )
        ax3.set_ylabel('$\chi$(k)')
        plt.show()
        
    def save_csv(self):
        pixel=self.xrf_2d_img[2]
        f=open('C:/Users/Carlos/Desktop/Dados_Sirius/file.mca','w')
        writer = csv.writer(f,delimiter=',')
        writer.writerow(self.xrf_stackdata)
        #for i in range(len(self.xrf_stackdata)):
            #f.write(str(self.xrf_stackdata[i])+'\n')
        f.close()
        f=open('C:/Users/Carlos/Desktop/Dados_Sirius/pixel.csv','w')

        with f:
            writer = csv.writer(f)
            for i in range(len(pixel)):
                row=[]
                
                for j in range(len(pixel[1])):                
                    row.append(pixel[i][j])
                writer.writerow(row)
                                                                   
        f.close()
        


    
            
    



            
        
        
        
        
        
