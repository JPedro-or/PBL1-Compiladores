import lexHolder_sm
import os.path

with open("input-lex.txt") as file:
            #data = file.readlines()
            text = file.read() #in case it can read token by token with this methods

result = lexHolder_sm.run(text)

re_size = len(result)
open('out-lex.txt', 'w').close()#limpa o arquivo de saída para o novo output
count = -1
for i in range(re_size):
    count = count + 1
    if count == 2:#quebra de linha pra cada token
        count = 0
        with open('out-lex.txt', 'a') as file:
            file.write('\n')
    if count != 2:
        with open('out-lex.txt', 'a') as file:
            file.write(str(result[i]))
            file.write(' ')
print(result)