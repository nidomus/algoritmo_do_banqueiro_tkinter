    

# Referência utilizada para a construção deste programa:
# SILBERSCHATZ, Abraham; GALVIN, Peter; GAGNE,
# Greg. Fundamentos de sistemas operacionais. 8.
# ed. Rio de Janeiro: LTC Editora, 2010.

class Algoritmo(): 
    # A classe Algoritmo possui como atributos, todos os vetores necessários para o funcionamento da simulação do Algoritmo do Banqueiro.
    # Esses vetores/matrizes foram implementados com base na explicação de como construir o algoritmo,
    # presente nos subtópicos 7.5.3.1 e 7.5.3.2, intitulados respectivamente como 'Algoritmo de Segurança' 
    # e 'Algoritmo de Solicitação de Recursos', do livro referenciado.

    def __init__(self): # Construtor da classe de Algoritmo

        self.alocacao = [] # inicializa a matriz de alocação de recursos de cada processo.
        self.trabalho = '' # inicializa a variável trabalho, utilizada na verificação de estado.
        self.max = [] # inicializa a matriz que guarda máximo dos recursos de cada processo.
        self.disponivel = [] # inicializa a variável que vai receber o valor disponível de recursos.
        self.necessidade = [] # Inicializa a matriz de necessidade de recursos de cada processo.
        self.ordem = [] # Inicializa a variável que vai armazenar uma ordem válida dos processos para um sistema seguro.
        self.estado = ''
        self.qtd_processos = 2# Inicia a quantidade de processos do sistema como 2(mínimo).
    
    # Set's e Get's:
    def setAlocacao(self, lista):
        self.alocacao = lista[0:5]

    def getAlocacao(self):
        return self.alocacao
    
    def setMax(self, lista):
        self.max = lista[0:5]
    
    def getMax(self):
        return self.max

    def setDisponivel(self,string):
        self.disponivel = list(string)[0:4]
    
    def getDisponivel(self):
        return self.disponivel
    
    def getOrdem(self):
        return self.ordem

    def getNecessidade(self):
        return self.necessidade

    #Métodos gerais utilizados na lógica do Algoritmo:
    def limpaAlocacao (self):
        self.alocacao.clear()
    
    def addMax(self,string):
        self.max.append(list(string))

    def limpaNecessidade(self):
        self.necessidade = []

    def addAlocacao(self,string):
        self.alocacao.append(list(string))

    def limpaMax(self):
        self.max.clear()
    
    def addProcesso(self):
        self.qtd_processos+=1
    
    def removerProcesso(self):
        self.qtd_processos-=1
    
    def getQtdProcessos(self):
        return self.qtd_processos
    
    def confereValores (self,lista1,lista2):
        # Esse método verifica se os valores dos recursos presentes no primeiro elemento são menores que o do segundo.
        for x in range(4):# Percorre cada recurso dos elementos
            if int(lista1[x]) > int(lista2[x]):
                return False
        return True

    def adicionarRecursos(self,lista,lista2):
        aux = []
        for x in range(4):
            aux.append(int(lista[x]) + int(lista2[x]))
        return aux

    def removerRecursos (self,lista1, lista2):
        aux = []
        for x in range(4):
            aux.append(str(int(lista1[x]) - int(lista2[x])))
        return aux
    
    #Métodos específicos do algoritmo
    def calculaNecessidade (self):
        # Essa função calcula a necessidade com base na subtração de Máx - Alocação.
        self.necessidade.clear() #Limpa os valores antigos presentes na matriz Necessidade
        for x in range(self.qtd_processos):
            valor = '' # O valor irá guardar o resultado da subtração de cada elemento dos vetores de max e alocação
            for y in range(4):
                valor +=  str(int(self.max[x][y]) - int(self.alocacao[x][y])) # Subtração dos elementos da posição (x,y) de cada matriz
            self.necessidade.append(valor)# Adciona o valor que representa a necessidade do processo (identificado pelo índice).
        return self.necessidade #Retorna a matriz necessidade preenchida com os valores.



    def verificaEstado(self):
        # Esse método foi construido com base no algoritmo de segurança apresentado no livro referenciado.

        trabalho = self.disponivel[0:4] # Atribui a quantidade de recursos disponíveis na variável trabalho
        termino = [] #Inicializa o vetor que irá guardar o estado(TRUE, FALSE) de atendimento de cada processo
        
        for x in range(self.qtd_processos):#Define a situação inicial, indicando que nenhum processo foi atendido
            termino.append(False)
        termino_antigo = [] # Icializa a variável que guarda a situação anterior do vetor termino.
        self.ordem = [] #Reseta o vetor de ordem
        flag = False # Inicializa a variável que será retornada no final, indicando se o estado do sistema é seguro(TRUE) ou inseguro(FALSE)
        rpt = 0 # Inicializa a variável que irá indicar quantas vezes o laço repetiu, com ou sem alteração
        
        x = 0 #Inicializa a variável que irá percorrer os vetores/matrizes
        while flag == False: # O laço while irá repetir enquanto todos os processos não tiverem sidos atendidos (no caso de um sistema seguro)
            termino_antigo = termino[0:5] # Guarda o estado atual do vetor termino
            
            if termino[x]== False and self.confereValores(list(self.necessidade[x]),trabalho):
                # Caso o estado de atendimento do processo [x] for FALSE e o mesmo possa ser atendido
                # Os recursos alocados por esse processo são adicionados na variavel trabalho

                trabalho = self.adicionarRecursos(list(trabalho),list(self.alocacao[x]))[0:4]# Adiciona os recursos de forma separada
                termino[x] = True  # E seu estado de atendimento é indicado como TRUE
                self.ordem.append(f'P{x}')# Como o processo foi atendido, ele é adicionado na ordem válida do sistema
            
            x +=1 # Adiciona mais um no contador que percorre

            if termino.count(False)==0: # Se não forem encontrados nenhum processo que não foi atendido, o sistema está seguro
                flag = True # Nesse caso, a variável flag recebe TRUE e o laço é finalizado

            elif x == self.qtd_processos: # Se o laço percorreu todos os processos do sistema

                x=0 # O contador que percorre é resetado
                rpt+=1 # É adicionado +1 na variável, indicando que o laço já percorreu todos os processos

            if rpt>=2 and termino_antigo == termino:
                # Se o laço já percorreu todos os processos mais de uma vez e não foi possível atender mais nenhum processo
                #,ou seja, o vetor termino antigo continua igual ao vetor termino atual, isso indica que o sistema é inseguro
                # Nesse caso o laço é interrompido e a flag mantém seu estado como FALSE.
                break
        return flag
            
    def simulaSolicitacao(self,solicitacao,x):
        # O método simulaSolicitacao foi construído com base no subtópico 7.5.3.2,'Algoritmo de Solicitação de Recursos', do livro referenciado.
        # Esse método recebe como parâmetro o valor da solicitação (solicitacao) e qual processo irá recebe-la(x). 
        # Esse método tem o objetivo de testar se, primeiramente, a solicitação que será simulada atende os requisitos 
        # dos recursos presentes no sitema.

        if self.confereValores(solicitacao,self.necessidade[x]):#Verifica se o valor solicitado não excede a necessidade desse processo
            if self.confereValores(solicitacao, self.disponivel): #Verifica se o valor solicitado não excede os recursos diponíveis

                disponivel_backup= self.disponivel[0:4]# Faz um backup do valor do atributo disponível do sistema
                alocacao_backup = self.alocacao[x] # Faz um backup do valor de alocação do processo específico
                necessidade_backup = self.necessidade[x] # Faz um backup do valor de necessidade do processo específico

                # Nessa etapa do método são executadas todas as alterações citadas no subtópico necessárias para a simulação

                self.disponivel = self.removerRecursos(list(self.disponivel),list(solicitacao)) # Os recursos solicitados são removidos dos recursos disponíveis.
                self.alocacao[x] = self.adicionarRecursos(self.alocacao[x],solicitacao) # Os recursos solicitados são adicionados nos recursos alocados do processo.
                self.necessidade[x] = self.removerRecursos(self.necessidade[x],solicitacao)# Os recursos solicitados são removidos da necessidade do processo.

                flag = self.verificaEstado() # A variável flag irá guardar o retorno (TRUE,FALSE) da verificação do estado do sistema após as alterações da solicitação

                # Os valores que foram armazenados antes das alterações são atribuidos nos seus respectivos atributos, retornando ao estado antes da simulação.
                self.disponivel = disponivel_backup
                self.alocacao[x] = alocacao_backup
                self.necessidade[x] = necessidade_backup

                #Obs.: O retorno da função é uma string, pois a mesma será utilizada no GUI para informar o resultado da simulação ao usuário.
                if flag: #Se após a simulação o sistema continuar seguro, a solicitação é válida.
                    return 'A solicitação é válida.' 
                
                else: #Se após a simulação o sistema ficar inseguro, a solicitação é inválida.
                    return 'A solicitação é inválida.'
            else:# Caso o valor solicitado exceda a disponibilidade do sistema, o processo deve esperar
                return f'O processo P{x} deve esperar.'
        else: # Caso o valor solicitado exceda a necessidade do processo, a solicitação é interrompida
            return 'Erro: O processo excedeu sua requisição máxima!'        



    
    
            

