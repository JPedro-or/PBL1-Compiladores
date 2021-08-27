with open("script-text.txt") as file:
            #data = file.readlines()
            text = file.read()
count = 0
while count != len(text):
    print(text[count])
    count += 1
print('\n')
print(len(text))


def q4(self, coment_str):
        if self.current_char ==  '%':
            while self.current_char != '\n' and self.pos.indx != len(self.text):#enquanto ele não chegar ao final da linha e consequentemente do comentário, 
                self.next_char()                                                #ou no final do arquivo, caso seja um comentário no final do arquivo
                                                                                #ele vai continuar lendo os caracteres até chegar o fim do comentário
        else:
            '''while self.pos.indx != len(self.text):
                if self.current_char == '#':
                    coment_str += self.current_char
                    self.next_char()
                    if self.current_char == '}':
                        coment_str+= self.current_char
                        self.next_char()
                        return None
                coment_str += self.current_char
                self.next_char()
            coment_str.replace(" ", "")
            return Token(CoMF, coment_str)'''
            return self.coment_loop_i(coment_str)

    def coment_loop_i(self, coment_str):
        '''while self.pos.indx != len(self.text):
            if self.current_char == '#': 
                coment_str += self.current_char
                return self.coment_loop_ii(coment_str)
            else:
                if self.next_char() != None:
                    coment_str += self.current_char
        return Token(CoMF, coment_str)'''
        if self.next_char != None:
            while self.pos.indx != len(self.text):
                coment_str += self.current_char
                if self.current_char == "#": 
                    return self.coment_loop_ii(coment_str)
                self.next_char()
        return Token(CoMF, coment_str)
    
    def coment_loop_ii(self, coment_str):
        '''return None
        self.next_char()
        if self.current_char != None:
            if self.current_char == "}":
                self.next_char()
                return None
            else: 
                return self.coment_loop_i(coment_str)
        return Token(CoMF, coment_str)'''
        if self.pos.indx != len(self.text):
            self.next_char()
            if self.current_char == "}":
                return None
            coment_str += self.current_char
            return self.coment_loop_i(coment_str)
        return Token(CoMF, coment_str)

        

    elif ord(self.current_char) in delComentario:
            if self.q4('') != None:
                tokens.append(self.pos.ln)
                tokens.append(self.q4(''))
            self.next_char()