
###
# RUN
###
from typing import Counter


def run(text):
    lexer = Lexer(text)
    tokens, error = lexer.make_tokens()

    return tokens

###
# CONSTANTS
###
DIGITS = '0123456789'
#unicode de cada linha da tabela
opAritmeticos = [42, 43, 45, 47]
delimitadores = [91, 93, 123, 125, 40, 41, 59, 44, 46]
opLogicos = [38, 124, 33]
delComentario = [37]

###
# ERRORS
###
#class Error:
#    def __init__(self, pos_start, pos_end, error_name, details):
#        self.pos_start = pos_start
#        self.pos_end = pos_end
#        self.error_name = error_name
#        self.details = details
#    
#    def as_string(self):
#        result = f'{self.error_name}: {self.details}'
#       return result

#class IllegalCharError(Error):
#    def __init__(self, details):
#        super().__init__('illegal Character', details)

###
# TOKEN SIGLAS
###   
PRE = 'PRE'
IDE = 'IDE'
NRO = 'NRO'
DEL = 'DEL'
REL = 'REL'
LOG = 'LOG'
ART = 'ART'
SIB = 'SIB'
SII = 'SII'
CMF = 'CMF'
NMF = 'NMF'
CAR = 'CAR'
CaMF = 'CaMF'
CoMF = 'CoMF'
OpMF = 'OpMF'
CAD = 'CAD'


class Token:
    def __init__(self, type_, value = None):
        self.type = type_
        self.value = value
    
    def __repr__(self):
        if self.value: return f'{self.type}: {self.value}'
        return f'{self.type}'

class Position:#mantem o valor da linha e coluna
    def __init__(self, indx, ln, col):
        self.indx = indx
        self.ln = ln
        self.col = col
    
    def advance(self, current_char):
        self.indx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0
        return self
    
    def retreat(self, current_char):
        if self.col != 0:
            self.indx -= 1 
            self.col -= 1
        return self
    
    def copy(self):
        return Position(self.indx, self.ln, self.col)


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = Position(-1, 0, -1)
        self.current_char = None
        self.next_char()
    
    def next_char(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.indx] if self.pos.indx < len(self.text) else None
    
    def prev_char(self):
        self.pos.retreat(self.current_char)
        self.current_char = self.text[self.pos.indx] 

    def make_tokens(self):# função que vai iniciar a máquina de estados no estado q0
        tokens = []
        errors = []
        while self.current_char != None:
            self.q0(tokens, errors)
        return tokens, None   
    
    def q0(self, tokens, errors):#q0 vai ser o node inicial da máquina e vai chamar os outros nodes. 
                         #Cada node vai corresponder a uma classificação na tabela de expressão regular (ex. Operadores aritméticos é o node q2)
        #                         
        # ESPAÇO OU TAB
        #
        if self.current_char in ' \t\n':
            self.next_char()
        #
        # DIGITOS
        #
        elif self.current_char in DIGITS:
            tk_out_str = ""
            tokens.append(self.pos.ln)
            tokens.append(self.q1())
        #
        # OPERADORES ARITMÉTICOS
        #
        elif ord(self.current_char) in opAritmeticos:
            tokens.append(self.pos.ln) 
            tokens.append(self.q2())
            self.next_char()
        
        elif ord(self.current_char) in delimitadores:
            tokens.append(self.pos.ln)
            tokens.append(self.q3())
            self.next_char()
        
        elif ord(self.current_char) in delComentario:
            if self.q4() != None:
                tokens.append(self.pos.ln)
                tokens.append(self.q4())
            self.next_char()
            
        elif ord(self.current_char) in opLogicos:
            tokens.append(self.pos.ln)
            tokens.append(self.q5())
            self.next_char()

        elif self.current_char == 'EOF':
            print("Hello")
        
        else:
            errors.append(self.pos.ln)
            errors.append(self.q14())
            self.next_char()
            
        #return tokens, None

    def q1(self):# Vai definir os tokens de digitos, ints e pontos flutuantes
        num_str = ''
        dot_count = 0

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count +=1
                num_str += '.'
            else: 
                num_str += self.current_char
            self.next_char()
        
        if dot_count == 0:
            return Token(NRO, int(num_str))
        else:
            return Token(NRO, float(num_str))

    def q2(self):#vai definir os operadores aritméticos
        if self.current_char == '+':
            token_str = self.current_char
            self.next_char()
            if self.current_char == '+':
                token_str += self.current_char
                return Token(ART, token_str)
            else:
                self.prev_char()
                return Token(ART, token_str)
        elif self.current_char == '-':
            token_str = self.current_char
            self.next_char()
            if self.current_char == '-':
                token_str += self.current_char
                return Token(ART, token_str)
            else:
                self.prev_char()
                return Token(ART, token_str)
        elif self.current_char == '/':
            return Token(ART, self.current_char)
        elif self.current_char == '*':
            return Token(ART, self.current_char)
        else:
            return self.q14()
        
    def q3(self):#vai definir os delimitadores
        if self.current_char == ';':
            return Token(DEL, self.current_char)
        elif self.current_char == ',':
            return Token(DEL, self.current_char)
        elif self.current_char == '.':
            return Token(DEL, self.current_char)
        elif self.current_char == '[':
            return Token(DEL, self.current_char)
        elif self.current_char == ']':
           return Token(DEL, self.current_char)
        elif self.current_char == '(':
            return Token(DEL, self.current_char)
        elif self.current_char == ')':
            return Token(DEL, self.current_char)
        elif self.current_char == '{':
            if self.next_char() == '#':
                return self.q4()#mudar o número quando for comentário de bloco
            else:
                self.prev_char()
                return Token(DEL, self.current_char)
        elif self.current_char == '}':
            return Token(DEL, self.current_char)
    
    def q4(self):
        if self.current_char ==  '%':
            while self.current_char != '\n' and self.pos.indx != len(self.text):#enquanto ele não chegar ao final da linha e consequentemente do comentário, 
                                                                                #ou no final do arquivo, caso seja um comentário no final do arquivo
                                                                                #ele vai continuar lendo os caracteres até chegar o fim do comentário
                self.next_char()
        return None
        
    def q14(self):#Erro de símbolo inválido
        return Token(SII, self.current_char)
