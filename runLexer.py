import lexHolder_sm


with open("input-lex.txt") as file:
            #data = file.readlines()
            text = file.read() #in case it can read token by token with this methods

result = lexHolder_sm.run(text)

print(result)