from tkinter import *
from tkinter import messagebox
import Algoritmo as alg
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip
from pkg_resources import resource_filename


#Simulador Algoritmo do Banqueiro
#Autor: Herbert Fernandes de Oliveira
#LICOMP - 3º SEM

class Application(ttk.Window):
    def __init__(self, master):
        
        self.alg = alg.Algoritmo()
        self.valor_entrada = StringVar()
        self.valor_vazio=''
        self.valor_entrada.trace('w', self.verificaEntrada)
        self.valor_solicitar = StringVar()
        self.valor_solicitar.trace('w', self.verificaEntrada)


        self.app = ttk.Frame(master)
        self.app.grid()

        self.zona_titulo = ttk.Frame(self.app)
        self.zona_titulo.grid(row=0,pady=(20,0))
        self.zona_entrada = ttk.Frame(self.app, bootstyle=SECONDARY)
        self.zona_entrada.grid(row=1,padx=10)
        self.zona_botoes = ttk.Frame(self.app)
        self.zona_botoes.grid(row=2)

        ttk.Style().configure("TButton", font ="TkFixedFont 12")


        #Inicializando os ttk.Label's de informação.
        self.label_titulo = ttk.Label(self.zona_titulo, text="SIMULADOR ALGORITMO DO BANQUEIRO", font= ('arial',19,'bold'))
        self.label_titulo.grid(row=0, column=3, pady=(0,10))

        self.label_alocacao = ttk.Label(self.zona_entrada,text="Alocação",font=(None,15), bootstyle=(SECONDARY,INVERSE), justify=CENTER, cursor='question_arrow')
        self.label_alocacao.grid(row=0, column=2)

        self.label_max = ttk.Label(self.zona_entrada, text="Máximo", font= (None,15),bootstyle=(SECONDARY,INVERSE), cursor='question_arrow', )
        self.label_max.grid(row=0, column=3,padx=10)

        self.label_necessidade = ttk.Label(self.zona_entrada, text="Necessidade",bootstyle=(SECONDARY,INVERSE), font= (None,15), cursor='question_arrow')
        self.label_necessidade.grid(row=0, column=4,padx=(0,10))

        self.label_disponivel = ttk.Label(self.zona_entrada, text="Disponível",bootstyle=(SECONDARY,INVERSE) ,font= (None,15), cursor='question_arrow')
        self.label_disponivel.grid(row=0, column=5,padx=(2,10))

        self.label_estado = ttk.Label(self.zona_botoes,font= (None,12), text='Estado: ',cursor='question_arrow')
        self.label_estado.grid(row=0, column = 4)
        self.estado = StringVar()
        self.estado.set('Null')

        self.label_valor_estado = ttk.Label(self.zona_botoes,textvariable=self.estado,font= (None,12))
        self.label_valor_estado.grid(row=0, column = 5)

        self.label_ordem = ttk.Label(self.zona_botoes,font= (None,12),text= 'Ordem: ',cursor='question_arrow')
        self.label_ordem.grid(row=1, column = 4)
        self.ordem = StringVar()
        self.ordem.set('Null')
        self.label_valor_ordem = ttk.Label(self.zona_botoes,textvariable=self.ordem,font= (None,12))
        self.label_valor_ordem.grid(row=1, column = 5)

        self.label_msg = ttk.Label(self.zona_entrada, text= '', bootstyle='inverse-secondary',font=10)
        self.label_msg.grid(row=7, column=0,columnspan=6,pady=(10))


        # Inicializando indicadores de recursos (a,b,c,d):
        self.label_recursos = []
        for i in range(4):
            self.label_recursos.append(ttk.Label(self.zona_entrada,text='A  B  C  D', bootstyle=(SECONDARY,INVERSE),font= (None,9)))
            self.label_recursos[i].grid(row=1,column=i+2)

        # Inicializando ttk.Label's processos e os seus respectivos marcadores
        self.var = IntVar()
        self.label_processos = []
        self.radio_processos = []
        for x in range(2):
            self.label_processos.append(ttk.Label(self.zona_entrada,bootstyle=(SECONDARY,INVERSE), width=9, text=f"Processo {x}" ,font=15))
            self.Label = self.label_processos[x]
            self.Label.grid(row=x+2, column=0,padx=(10,0),ipady=3.6)

            self.radio_processos.append(ttk.Radiobutton(self.zona_entrada,state='disable', bootstyle='success-toolbutton',variable=self.var,value=x,cursor='hand2'))
            self.radio_processos[x].grid(row=x+2,column=1,pady=(0.5,0), padx=(3,5))

        
        #Inicializando a lista de strings da necessidade como vazia
        self.vetor_necessidade = []
        for x in range(2):
            self.vetor_necessidade.append(ttk.Label(self.zona_entrada, text='',bootstyle=(SECONDARY,INVERSE),font= (None,12),width=4))
            self.vetor_necessidade[x].grid(row=x+2, column=4)

        
        #Inicializando os verificadores que recebem as entradas de alocação e max
        self.verificadores_alocacao = []
        self.verificadores_max = []

        for x in range(5):
            self.verificadores_alocacao.append(StringVar())
            self.verificadores_alocacao[x].trace('w', self.verificaEntrada)
            self.verificadores_max.append(StringVar())
            self.verificadores_max[x].trace('w', self.verificaEntrada)
            

        #Inicializando entradas da Alocação e Max
        self.entry_alocacao = []
        self.entry_max = []
        for x in range(2):
            self.entry_alocacao.append(ttk.Entry(self.zona_entrada, width=4, justify=CENTER, font= (None,12), textvariable=self.verificadores_alocacao[x]))
            self.entry_max.append(ttk.Entry(self.zona_entrada, width=4,justify=CENTER, font= (None,12), textvariable=self.verificadores_max[x]))

            self.entry_alocacao[x].grid(row=x+2, column=2, ipadx=5, pady=5)
            self.entry_max[x].grid(row=x+2, column=3, ipadx=5)
        
        self.entry_disponivel = ttk.Entry(self.zona_entrada, width=4, justify=CENTER, font= (None,12), textvariable=self.valor_entrada)
        self.entry_disponivel.grid(row=2, column=5, ipadx=5)

        #Inicializa os botões
        # Botão calcular
        self.btn_calcular = ttk.Button(self.zona_botoes,command=self.imprimirNecessidade, text= 'Calcular', bootstyle=(SUCCESS),cursor='hand2')
        self.btn_calcular.grid(row=0, column=0, columnspan=1, pady=10,padx=10)

        # Botão Verificar
        self.btn_verificar = ttk.Button(self.zona_botoes, text='Verificar',command=self.exibirEstado,bootstyle=INFO, state='disable',cursor='hand2')
        
        self.btn_verificar.grid(row=1, column=0, columnspan=1,padx=10,pady=(0,10))

        #Botão Socilitar + entrada da solicitação
        self.entry_solicitar = ttk.Entry(self.zona_botoes, textvariable=self.valor_solicitar,font= 10,state='disable',justify=CENTER,width=4)
        self.entry_solicitar.grid(row=0, column=1, ipadx=15,padx=(0,10))

        self.btn_solicitar = ttk.Button(self.zona_botoes,command=self.executaSolicitacao,state='disable',text='Solicitar',bootstyle=WARNING,cursor='hand2')
        self.btn_solicitar.grid(row=1, column=1, columnspan=1,padx=(0,10), pady=(0,10))

        #Botão de adicionar processo: esse widget vai ter a função de adicionar mais processos no algoritmo.
        self.cell_btns_add = ttk.Frame(self.zona_entrada , bootstyle=SECONDARY)
        self.cell_btns_add.grid(row=0,column=0, padx=(10,0))

        self.btn_adicionar = ttk.Button(self.cell_btns_add, text='+',width=1, bootstyle=SUCCESS, command = self.adicionaProcesso,cursor='hand2')
        self.btn_adicionar.grid(row=0, column=0,pady=(10,0),padx=(10,2))

        self.btn_remover = ttk.Button(self.cell_btns_add, text='-',width=1, bootstyle=DANGER,command = self.removeProcesso,cursor='hand2')
        self.btn_remover.grid(row=0, column=1,pady=(10,0),padx=(2,0))

        
        # Nessa parte do código, os tooltips(dicas) são inicializados. Essas dicas servem para auxiliar o usuário durante a utilização do simulador
        ToolTip(self.btn_calcular,text='Calcula a Necessidade.')
        ToolTip(self.btn_verificar,text='Verifica o estado do sistema.')
        ToolTip(self.btn_solicitar,text='Executa a solicitação.')
        ToolTip(self.entry_solicitar,text='Informar os valores dos recursos que serão solicitados.\nObs.: Você deve marcar qual processo irá receber a solicitação.')
        ToolTip(self.btn_adicionar,text='Adiciona um processo.')
        ToolTip(self.btn_remover,text='Remove um processo.')


        ToolTip(self.label_disponivel, text='Indica o número de recursos disponíveis de cada tipo.')
        ToolTip(self.label_max, text='Define a demanda máxima de cada processo.')
        ToolTip(self.label_alocacao, text='Define o número de recursos de cada tipo correntemente alocados a cada processo.')
        ToolTip(self.label_necessidade, text='Indica os recursos remanescentes necessários a cada processo (Máximo - Alocação) .')
        ToolTip(self.label_estado, text='Indica o estado do sistema atual.')
        ToolTip(self.label_ordem, text='Indica uma ordem válida de processos, caso o sistema esteja seguro.')


    def verificaEntrada(self, *args):

        #Limpa os vetores antigos de alocação e max 
        self.alg.limpaAlocacao()
        self.alg.limpaMax()
        
        #Guarda os novos valores dos vetores
        self.guardaAlocacao()
        self.guardaMax()

        self.alg.setDisponivel(self.entry_disponivel.get()[0:4])
        
        for x in range(self.alg.getQtdProcessos()):
            valor_aloc = self.verificadores_alocacao[x].get()
            valor_max = self.verificadores_max[x].get()
            valor = self.valor_entrada.get()
            valor_solicitacao = self.valor_solicitar.get()

            if(len(valor_aloc)<4 or len(valor_max)<4 or len(valor)<4):
                self.btn_verificar.configure(state='disable')
                self.bloqueiaSolicitacao()

                if(self.estado.get()!='Null'):
                    self.ocultarNecessidade()
            
            if len(valor_aloc) > 4:
                self.verificadores_alocacao[x].set(valor_aloc[:4])
            if len(valor_max) > 4:
                self.verificadores_max[x].set(valor_max[:4])
            if len(valor_solicitacao) > 4:
                self.valor_solicitar.set(valor_solicitacao[:4])         


        if len(valor) > 4:
            self.valor_entrada.set(valor[:4])

    def guardaAlocacao(self):
        for x in range(self.alg.getQtdProcessos()):
            self.alg.addAlocacao(self.entry_alocacao[x].get()[0:4])

    def guardaMax(self):
        for x in range(self.alg.getQtdProcessos()):
            self.alg.addMax(self.entry_max[x].get()[0:4])
    
    def ocultarNecessidade(self):
        for x in range(self.alg.getQtdProcessos()):
            self.vetor_necessidade[x].configure(text='')

    # Verifica se os dados de Alocacao, Max e Necessidade estão válidos
    def verificaDados(self):

        flag = True
        for x in range(self.alg.getQtdProcessos()):
            if (len(self.verificadores_alocacao[x].get()) < 4 or self.verificadores_alocacao[x].get().isdigit() == False):
                self.entry_alocacao[x].configure(bootstyle= WARNING)
                self.label_msg.configure(text='Os valores das entradas devem possuir 4 digitos (ex: 1111).')
                flag = False
            else:
                self.entry_alocacao[x].configure(bootstyle= DARK)
            
            if (len(self.verificadores_max[x].get()) < 4 or self.verificadores_max[x].get().isdigit() == False):
                self.entry_max[x].configure(bootstyle= WARNING)
                    
                self.label_msg.configure(text='Os valores das entradas devem possuir 4 digitos (ex: 1111).')
                flag = False
            else:
                self.entry_max[x].configure(bootstyle= DARK)

        if len(self.alg.getDisponivel()) < 4 or self.valor_entrada.get().isdigit() == False:
            self.entry_disponivel.configure(bootstyle= WARNING)
            self.label_msg.configure(text='Os valores das entradas devem possuir 4 digitos (ex: 1111).')    
            flag = False
        else:
            self.entry_disponivel.configure(bootstyle= DARK)

        if flag:
            self.alg.calculaNecessidade()
            self.label_msg.configure(text='')
            for x in range(self.alg.getQtdProcessos()):
                for y in range(4):
                    if self.alg.getNecessidade()[x][y] == '-':
                        self.entry_max[x].configure(bootstyle= DANGER)
                        self.entry_alocacao[x].configure(bootstyle= DANGER)
                        self.label_msg.configure(text='O recurso alocado não pode ser maior do que o máximo requisidado.')
                        flag = False


        return flag

    def imprimirNecessidade(self):
        

        if(self.verificaDados()):
            self.btn_verificar.configure(state='active')
            self.ordem.set('Null')
            self.estado.set('Null')

            for x in range(self.alg.getQtdProcessos()):
                self.vetor_necessidade[x].configure(text=self.alg.getNecessidade()[x])
    
    def exibirEstado(self):
        if(self.verificaDados()):
            if(self.alg.verificaEstado()):
                self.label_valor_estado.configure(bootstyle=SUCCESS)
                self.estado.set('SEGURO')
                self.ordem.set(self.alg.getOrdem())

                self.liberaSolicitacao()


                messagebox.showinfo('Estado','O sistema está em estado seguro.')
            else:
                messagebox.showinfo('Estado','O sistema está em estado inseguro.')
                self.ordem.set('Null')
                self.label_valor_estado.configure(bootstyle=DANGER)
                self.estado.set('Inseguro')

    def liberaSolicitacao(self):
        self.btn_solicitar.configure(state = 'active')
        self.entry_solicitar.configure(state= 'normal')
                
        for x in range(self.alg.getQtdProcessos()):
            self.radio_processos[x].configure(state='normal')       
    
    def bloqueiaSolicitacao(self):
        self.btn_solicitar.configure(state = 'disable')
        self.entry_solicitar.configure(state= 'disable')
        for x in range(self.alg.getQtdProcessos()-1):
            self.radio_processos[x].configure(state='disable')  

    def executaSolicitacao(self):
        if self.verificaDados():
            self.label_msg.configure(text=self.alg.simulaSolicitacao(self.entry_solicitar.get(),self.var.get()))
            messagebox.showinfo('Solicitação',self.alg.simulaSolicitacao(self.entry_solicitar.get(),self.var.get()))


    def adicionaProcesso(self):
        if(self.alg.getQtdProcessos()<5):
            #Soma 1 na quantidade de processos do algoritmo
            self.alg.addProcesso()
            self.bloqueiaSolicitacao()
            #Adiciona um ttk.Label de Processo e seu respectivo marcador
            self.label_processos.append(ttk.Label(self.zona_entrada,bootstyle=(SECONDARY,INVERSE), width=9, text=f"Processo {self.alg.getQtdProcessos()-1}",font=15))
            self.label_processos[self.alg.getQtdProcessos()-1].grid(row=self.alg.getQtdProcessos()+1, column=0, padx=(10,0),ipady=3)

            self.radio_processos.append(ttk.Radiobutton(self.zona_entrada,state='disable',bootstyle='success-toolbutton', variable=self.var,value=self.alg.getQtdProcessos()-1,cursor='hand2'))
            self.radio_processos[self.alg.getQtdProcessos()-1].grid(row=self.alg.getQtdProcessos()+1,column=1,pady=(0.5,0))

            # Adiciona  as entradas de alocação e max do respectivo processo
            self.entry_alocacao.append(ttk.Entry(self.zona_entrada, width=4, justify=CENTER, font=10,
                                        textvariable=self.verificadores_alocacao[self.alg.getQtdProcessos()-1]))
            self.entry_max.append(ttk.Entry(self.zona_entrada, width=4, justify=CENTER,font= (None,12),textvariable=self.verificadores_max[self.alg.getQtdProcessos()-1]))

            self.entry_alocacao[self.alg.getQtdProcessos()-1].grid(row=self.alg.getQtdProcessos()+1, column=2, ipadx=5, pady=5)
            self.entry_max[self.alg.getQtdProcessos()-1].grid(row=self.alg.getQtdProcessos()+1, column=3, ipadx=5, pady=5)

            # Adiciona os campos da Necessidade:
            self.vetor_necessidade.append(ttk.Label(self.zona_entrada, text='', bootstyle=(SECONDARY,INVERSE),font= (None,12),width=4))
            self.vetor_necessidade[self.alg.getQtdProcessos()-1].grid(row=self.alg.getQtdProcessos()+1, column=4)



    def removeProcesso(self): # Remove o último processo adicionado
        if(self.alg.getQtdProcessos()>2): # Caso a quantidade de processos seja maior que dois, a operação de remover é válida.
            self.bloqueiaSolicitacao()
            self.alg.removerProcesso()
            self.label_processos[-1].grid_forget()
            self.radio_processos[-1].grid_forget()
            self.entry_alocacao[-1].grid_forget()
            self.entry_max[-1].grid_forget()
            self.vetor_necessidade[-1].grid_forget()

            self.label_processos.pop(-1)
            self.radio_processos.pop(-1)
            self.entry_alocacao.pop(-1)
            self.entry_max.pop(-1)
            self.vetor_necessidade.pop(-1)

                
tema='darkly'
root = ttk.Window(themename=tema)



def setTheme(tema):
    root.style.theme_use(tema)
    ttk.Style().configure("TButton", font ="TkFixedFont 12")
app = Application(root)

menuBar = Menu(root)
menuTema = Menu(menuBar, tearoff=0)

menuTema.add_command(label='Claro' ,command= lambda:setTheme('pulse'))
menuTema.add_command(label='Escuro',command= lambda:setTheme('darkly'))

menuBar.add_cascade(label='Tema', menu=menuTema)
# menuBar.add_command(label='Sair', command= lambda: quit())
root.config(menu = menuBar)
icone = resource_filename(__name__, 'ifba.ico')
root.resizable(0, 0)
root.title('Algoritmo do Banqueiro')
root.eval('tk::PlaceWindow . center')
root.iconbitmap(icone)
root.mainloop()
