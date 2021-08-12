import lexHolder

#reading the input file for the lexer
with open("input-lex.txt") as file:
    #data = file.readlines()
    text = file.read() #in case it can read token by token with this methods

result, error = lexHolder.run(text)

if error: print(error.as_string())
else: print(result)