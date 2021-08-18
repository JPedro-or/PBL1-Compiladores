CONST = '1, 2, 32'

with open("input-lex.txt") as file:
    #data = file.readlines()
    text = file.read()
if text in CONST:
    print(text)