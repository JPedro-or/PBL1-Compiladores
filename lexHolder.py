with open("input-lex.txt") as file:
    #data = file.readlines()
    text = file.read() #in case it can read token by token with this methods
###
# RUN
###
def run(text):
    lexer = Lexer(text)
    tokens, error = lexer.make_tokens()

    return tokens, error

###
# CONSTANTS
###
DIGITS = '0123456789'

###
# ERRORS
###
class Error:
    def __init__(self, error_name, details):
        self.error_name = error_name
        self.details = details
    
    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        return result

class IllegalCharError(Error):
    def __init__(self, details):
        super().__init__('illegal Character', details)

###
# TOKENS
###   
#
#DELIMITADORES
#
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
TT_LCURBRACK = 'CHAVE_E'
TT_RCURBRACK = 'CHAVE_D'
TT_LBRACK = 'COLCHETE_E'
TT_RBRACK = 'COLCHETE_D'
TT_SEMICOLON = 'PONTOV'
TT_COLON = 'VIRGULA'
TT_DOT = 'PONTO'
#
#PALAVRAS RESERVADAS
#
TT_INT = 'INTEIRO'
TT_FLOAT = 'FLOAT'
TT_REAL = 'REAL'
TT_BOOL = 'BOOLEANO'
TT_CHAR = 'CHAR'
TT_CHAIN = 'CADEIA'
TT_TRUE = 'VERDADEIRO'
TT_FALSE = 'FALSO'
TT_FOR = 'PARA'
TT_PRINT = 'ESCREVA'
TT_ALGO = 'ALGORITMO'
TT_VAR = 'VARIAVEIS'
TT_REG = 'REGISTO'
TT_FUNC = 'FUNCAO'
TT_RETURN = 'RETORNO'
TT_EMPTY = 'VAZIO'
TT_IF = 'SE'
TT_ELIF = 'SENAO'
TT_WHILE = 'ENQUANTO'
TT_READ = 'LEIA'
TT_WRTIE = 'ESCREVA'
TT_CONST = 'CONSTANTES'

#
# OPERADORES ARITMÉTICOS
#
TT_PLUS_PLUS = 'MAIS_MAIS'
TT_PLUS = 'MAIS'
TT_MINUS = 'MENOS'
TT_MULT = 'MULTIPLICA'
TT_DIV = 'DIVIDE'
TT_MINUS_MINUS = 'MENOS_MENOS'

#
# OPERADORES RELACIONAIS
#
TT_EQUAL = 'IGUAL'
TT_LTHAN = 'MENOR'
TT_GTHAN = 'MAIOR'
TT_NEQUAL = 'DIFERENTE'
TT_EQUALTO = 'IGUAL A'
TT_LTEQUAL = ''

class Token:
    def __init__(self, type_, value = None):
        self.type = type_
        self.value = value
    
    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'

###
# LEXER
###
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.current_char = None
        self.next_char()
    
    def next_char(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def make_tokens(self):
        tokens = []
        while self.current_char != None:
            #
            # ESPAÇO OU TAB
            #
            if self.current_char in ' \t':
                self.next_char()
            #
            # DIGITOS
            #
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            #
            # OPERADORES RELACIONAIS
            #
            elif self.current_char == '=':
                tokens.append(Token(TT_EQUAL))
                self.next_char()
            elif self.current_char == '<':
                tokens.append(Token(TT_LTHAN))
                self.next_char()
            elif self.current_char == '++':
                tokens.append(Token(TT_PLUS_PLUS))
                self.next_char()
            #
            # DELIMITADORES
            #
            elif self.current_char == ';':
                tokens.append(Token(TT_SEMICOLON))
                self.next_char()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN))
                self.next_char()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN))
                self.next_char()
            elif self.current_char == '{':
                tokens.append(Token(TT_LCURBRACK))
                self.next_char()
            elif self.current_char == '}':
                tokens.append(Token(TT_RCURBRACK)) 
                self.next_char()
            elif self.current_char == '[':
                tokens.append(Token(TT_RBRACK) 
                self.next_char()
            else:
                char = self.current_char
                self.next_char()
                return [], IllegalCharError("'" + char + "'")
        return tokens, None

    def make_number(self):
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
            return Token(TT_INT, int(num_str))
        else:
            return Token(TT_FLOAT, float(num_str))