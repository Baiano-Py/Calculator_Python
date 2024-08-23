# Parte das importações, biblioteca e modulos
from PySide6.QtWidgets import QPushButton, QGridLayout
from files.variables_ import *
from files.utils import *
from math import pi
import json

# criação da class botão
class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()
    
    #configuração do estilho do button: muda o tamanho da font-size, adicionar font e ajustar o tamanho 
    def configStyle(self):
        font = self.font()
        font.setPixelSize(SMALL_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(75, 55)

#criação dos buttons da calculadora, todos os numeros e operações matematicas
class ButtonsGrid(QGridLayout):
    def __init__(self, display, info,  window, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        #Simbolo de todos os botões da calculadora:
        self._grindMask =  [
            ['C', '/', '^', '◀'], # coluna 1 da interface de botões
            ['7', '8', '9', '*'], # coluna 2 da interface de botões
            ['4', '5', '6', '-'], # coluna 3 da interface de botões
            ['1', '2', '3', '+'], # coluna 4 da interface de botões
            ['H', '0', '.', '='], # coluna 5 da interface de botões
        ]
        #setas todas as variaveis iniciais:
        self.window = window # pega o arquivo window da inicialização
        self._left = None # a primeira opção de numeros do display
        self._right = None # a segunda opção de numeros do display
        self._operator = None # operador da conta
        self.display = display # display: tela onde aparece os numeros escolhidos
        self.info = info # info: aparece as resposta das contas fica em cima display
        self._makeGrind() #ativa a função de colocar os botões

    # função onde pega as informações dadas e coloca no Info:
    @property
    def equation(self):
        return self._equation
    
    @equation.setter
    def equation(self, value):
        self._equation = value # seta o valor do label
        self.info.setText(value)# coloca o valor na info

    # função dos botoes, essa parte ira estilizar eles e colocar na interface:
    def _makeGrind(self):
        for row_num, row in enumerate(self._grindMask): # pega a linha do simbulo
            for column_num, button_text in enumerate(row): # pega a coluna do simbolo
                button = Button(button_text) # a variavel button pega o valor do simbolo adicionado
                
                if isNumOrDot(button_text): # uma variavel do files.variables / verifica numeros de 0 a 9
                    button.setStyleSheet(button_theme) #seta o tema dos botões que não são operadores
                else:
                    button.setProperty('cssClass', 'specialButton') #adiciona o tem dos operadores
                    self._configSpecialButton(button) #Ativa a função dos operadores
                    
                self.addWidget(button, row_num, column_num) #adiciona na interface

                slot = self._makeSlot(self._InsertButtonTextDisplay, button) # coloca algo no display
                self._connectButtonClicked(button, slot) # faz uma coneção de click com o slot

    # função de conectar o click
    def _connectButtonClicked(self, button, slot):
        button.clicked.connect(slot)
    
    # função de conectar os operadores
    def _configSpecialButton(self, button):
        text = button.text()
        
        # quando clicar no botão c, aivar a função de clear
        if text == 'C':
            button.clicked.connect(self._clear)

        # ativar função de operadores
        elif text in '+-/*^':
            button.clicked.connect(lambda: self._operatorClicked(button))
        
        #ativa a função de carregar a resposta 
        elif text == '=':
            button.clicked.connect(self._calculation)
        
        # ativar a função do pi
        elif text == 'H':
            button.clicked.connect(lambda: history_cont(self))
        
        # ativar a função de apagar a ultima mensagem digitada
        elif text == '◀':
            button.clicked.connect(self._backspace)

    #criar a função do slot
    def _makeSlot(self, func, *args, **kwargs):
        def realSlot():
            func(*args, **kwargs)
        return realSlot

    #função de dar o valor do pi

    # função de colocar no display
    def _InsertButtonTextDisplay(self, button):
        button_text = button.text() # pega o texto do botão
        newDisplayValue = self.display.text() + button_text # adiciona o texto do botão no display

        if not isValidNumber(newDisplayValue):
            return
        
        self.display.insert(button_text) # inseri no display o valor do botão

    #funçãodo clear
    def _clear(self):
        self._left = None # reseta a variavel pra none
        self._right = None # reseta a variavel pra none
        self._operator = None # reseta a variavel pra none
        self.equation = '' #reseta o label da info
        self.display.clear() # da clear no dislay
    
    #funções dos botões de operações matematica
    def _operatorClicked(self, button):
        buttonText = button.text() #pega o texto do botão
        displayText = self.display.text() # pega o texto do display
        
        if isValidNumber(displayText): # verifica se é um numero valido
            self._left = displayText # seta o valor do DisplayText
            self._operator = buttonText # seta o operador com o valor do ButtonText
            self.display.clear() # da clear no display
            self.equation = f'{self._left} {self._operator} ??' # adiciona na info o texto modificado
        else:
            self._ShowError('ERROR: Digite um numero antes') # mostrar o error

    
    #função de calcular o resultado
    def _calculation(self):
        displayText = self.display.text() #pega o texto do display

        if not isValidNumber(displayText) and (self._right is None or self._operator is None):
            self._ShowError('ERROR: Você não digitou os parametros')
            return

        if self._right is None: #verifica se o numero 2 já tem valor
            self._right = displayText #da o valor para o numero direito
        
        self.equation = f'{self._left} {self._operator} {self._right}' # formato da informação

        result = 'error' #resultado começa com erro

        try:
            if '^' in self.equation: # se escolher a opção de elevado
                result = eval(self.equation.replace('^', '**')) # troca o simbolo de ^ por **
                salvarArquivo(f'{self.equation} = {result}')
            else:
                result = eval(self.equation) # faz a conta normal
                salvarArquivo(f'{self.equation} = {result}')

        except ZeroDivisionError: # se dividir pro zero da erro
            self._ShowError('ERROR: Numero não pode ser divisivel por zero')
            return

        except OverflowError: # se a resposta for muito grande
            self._ShowError('ERROR: Numero muito frande para a calculadora')
            return

        except Exception as e: # se acontecer algum outro problema setar um error global:
            self.info.setText('error') #setar erro na info
            self._ShowError('ERROR: Tente novamente... Erro desconhecido')
            return # fazer a conta não passar daqui

        self.display.clear() # limpar o display
        self.info.setText(f'{self.equation} = {result}') # setar a informação da resposta na info
        self._left = result # deixar o resultado da esquerda como o resultado da conta anterior 
        self._right = None # lado direito é setado None

        if result == 'error': # se der erro:
            self._left = None # valor numerico da esquerda vira None
    
    #função de apagar o ultimo item
    def _backspace(self): 
        displayText = self.display.text() # pegar o display Texto
        
        if displayText: # se tiver texto no display]
            nextTextDisplay = displayText[:-1] #fazer uma nova vatriavel de display com uma letra a menos
            self.display.setText(nextTextDisplay) # setar a nova variavel no display

    def _ShowError(self, text):
        mensageBox = self.window.makeMensageBox()
        mensageBox.setText(text)
        mensageBox.setIcon(mensageBox.Icon.Critical)
        mensageBox.exec()
    


