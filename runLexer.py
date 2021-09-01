import lexHolder_sm
import os.path

def read_write_file(file_value):
    with open('input\entrada' + str(file_value) + '.txt') as file:
                #data = file.readlines()
                text = file.read() #in case it can read token by token with this methods

    result, errors = lexHolder_sm.run(text)

    re_size = len(result)
    er_size = len(errors)

    open('output\saida' + str(file_value) + '.txt', 'w').close()#limpa o arquivo de saída para o novo output
    count = -1
    for i in range(re_size):
        count = count + 1
        if count == 2:#quebra de linha pra cada token
            count = 0
            with open('output\saida' + str(file_value) + '.txt', 'a') as file:
                file.write('\n')
        if count != 2:
            with open('output\saida' + str(file_value) + '.txt', 'a') as file:
                file.write(str(result[i]))
                file.write(' ')

    with open('output\saida' + str(file_value) + '.txt', 'a') as file:
        file.write('\n')

    for i in range(er_size):
        count = count + 1
        if count == 2:#quebra de linha pra cada token
            count = 0
            with open('output\saida' + str(file_value) + '.txt', 'a') as file:
                file.write('\n')
        if count != 2:
            with open('output\saida' + str(file_value) + '.txt', 'a') as file:
                file.write(str(errors[i]))
                file.write(' ')
    #print(result)

input_list = os.listdir('input')
output_list = os.listdir('output')
for j in range(len(output_list)):
    if j != 0:
        os.remove('output\saida' + str(j) + '.txt')
for j in range(len(input_list)):
    if j != 0:
        read_write_file(j)
