class fileReader:
    def __init__(self):
        self.input = "input-lex.txt"
    def read(self):
        with open(self.input) as file:
            #data = file.readlines()
            text = file.read()
        return text