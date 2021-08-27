
###
# RUN
###
from typing import Counter


def run(text):
    lexer = Lexer(text)
    tokens = lexer.make_tokens()

    return tokens

###
# CONSTANTS
###
DIGITS = '0123456789'
LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
#unicode de cada linha da tabela
opAritmeticos = [42, 43, 45, 47]
delimitadores = [91, 93, 123, 125, 40, 41, 59, 44, 46]
opLogicos = [38, 124, 33]
opRelacionais = [60, 61, 62]
delComentario = [37]
reserved_words = ["algoritmo", "variaveis", "constantes", "registro",
"funcao", "retorno", "vazio", "se", "senao", "enquanto",
"para", "leia", "escreva", "inteiro", "real", "booleano", "char",
"cadeia", "verdadeiro", "falso"]
simboloNaoIncluso = [34, 39]

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

''' def verificaLetra(caracter):
    caracter = ord(caracter)
    if(caracter >= 65 and caracter <= 90):
        return True
    elif(caracter >= 97 and caracter <= 122):
        return True
    return False '''

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
        self.pos = Position(-1, 1, -1)
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
        return tokens   
    
    def q0(self, tokens, errors):#q0 vai ser o node inicial da máquina e vai chamar os outros nodes. 
                         #Cada node vai corresponder a uma classificação na tabela de expressão regular (ex. Operadores aritméticos é o node q2)
        #                         
        # ESPAÇO OU TAB
        #
        if self.current_char in ' \t\n':
            self.next_char()
        #
        # IDENTIFICADORES
        #
        elif self.current_char in LETTERS:
            tokens.append(self.pos.ln)
            tk_out_str = self.identificador()
            tokens.append(tk_out_str)
        #
        # DIGITOS
        #
        elif self.current_char in DIGITS:
            tk_out_str = ""
            tokens.append(self.pos.ln)
            tk_out_str = self.q1()
            tokens.append(tk_out_str)
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
            tokens.append(self.pos.ln)
            tokens.append(self.q4(''))
            self.next_char()
            
        elif ord(self.current_char) in opLogicos:
            tokens.append(self.pos.ln)
            tokens.append(self.q5())
            self.next_char()
        
        elif ord(self.current_char) in opRelacionais:
            tokens.append(self.pos.ln)
            tokens.append(self.operadorRelacional())
            self.next_char()

        elif ord(self.current_char) >= 32 and ord(self.current_char) <= 255:
            tokens.append(self.pos.ln)
            tokens.append(self.simbolos())
            self.next_char()


        
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
            return Token(NRO, num_str)
        else:
            return Token(NRO, num_str)

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
        elif self.current_char   == ')':
            return Token(DEL, self.current_char)
        elif self.current_char == '{':
            comment_str = self.current_char
            self.next_char()
            if self.current_char == '#':
                return self.q4(comment_str)
            self.prev_char()
            return Token(DEL, self.current_char)
        elif self.current_char == '}':
            return Token(DEL, self.current_char)
    
    def q4(self, comment_str):
        if self.current_char ==  '%':
            while self.current_char != '\n' and self.pos.indx != len(self.text):#enquanto ele não chegar ao final da linha e consequentemente do comentário, 
                self.next_char()
            return 'comentario de linha'                                               #ou no final do arquivo, caso seja um comentário no final do arquivo
                                                                                #ele vai continuar lendo os caracteres até chegar o fim do comentário
        elif self.current_char == '#':
            comment_str += self.current_char
            return self.comment_loop_i(comment_str)

    def comment_loop_i(self, comment_str):
       while self.current_char != None:
           self.next_char()
           if self.current_char != None and self.current_char == "#":
               comment_str += self.current_char
               return self.comment_loop_ii(comment_str)
           elif self.current_char != None:
                comment_str += self.current_char
       return Token(CoMF, comment_str)
    
    def comment_loop_ii(self, comment_str):
        self.next_char()
        if self.current_char != None and self.current_char == "}":
            return 'comentario de bloco'
        elif self.current_char != None: 
            comment_str += self.current_char
        return self.comment_loop_i(comment_str)

    def q5(self):
        if self.current_char ==  '&':
            lex = self.current_char
            self.next_char()
            if self.current_char == '&':
               lex += self.current_char
               return Token(LOG, lex)
            self.prev_char()
            return Token(OpMF, lex)

        elif self.current_char ==  '|':
            lex = self.current_char
            self.next_char()
            if self.current_char == '|':
               lex += self.current_char
               return Token(LOG, lex)
            self.prev_char()
            return Token(OpMF, lex)

        elif self.current_char == '!':
            lex = self.current_char
            self.next_char()
            if self.current_char == '=':
                lex += self.current_char
                return Token(REL, lex)
            self.prev_char()
            return Token(LOG, lex)

        return None



    def identificador(self):
        lex = self.current_char
        
        self.next_char()
        while self.current_char in LETTERS or self.current_char in DIGITS or self.current_char == '_':
            lex += self.current_char
            self.next_char()
            if(self.current_char == None):
                break


        if(lex in reserved_words):
            return Token(PRE, lex)
        return Token(IDE, lex)

    def operadorRelacional(self):
        if self.current_char ==  '=':
            lex = self.current_char
            self.next_char()
            if self.current_char == '=':
               lex += self.current_char
               return Token(REL, lex)
            self.prev_char()
            return Token(REL, self.current_char)

        elif self.current_char ==  '>':
            lex = self.current_char
            self.next_char()
            if self.current_char == '=':
               lex += self.current_char
               return Token(REL, lex)
            self.prev_char()
            return Token(REL, self.current_char)

        elif self.current_char == '<':
            lex = self.current_char
            self.next_char()
            if self.current_char == '=':
               lex += self.current_char
               return Token(REL, lex)
            self.prev_char()
            return Token(REL, self.current_char)

            

    def simbolos(self):
        if ord(self.current_char) >= 32 and ord(self.current_char) <= 126 and ord(self.current_char) not in simboloNaoIncluso:
            return Token(SIB, self.current_char)
        else:
            return Token(SII, self.current_char)
        
    def q14(self):#Erro de símbolo inválido
        return Token(SII, self.current_char)
