
    def comment_loop_i(self, comment_str):
        #if self.current_char != None:
        self.next_char()
        while self.current_char != None:
            comment_str += self.current_char
            if self.current_char == '#':
                self.comment_loop_ii(comment_str)
            else:
                self.next_char()
        return Token(CoMF, comment_str)
    
    def comment_loop_ii(self, comment_str):
        self.next_char()
        if self.current_char != None and self.current_char == "}":
            print(comment_str)
            return 'comentario de bloco'
        elif self.current_char != None: comment_str += self.current_char
        return self.comment_loop_i(comment_str)