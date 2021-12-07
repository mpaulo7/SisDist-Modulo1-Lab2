# Exemplo basico socket (lado passivo)

import socket
import os.path

TERMO_NAO_ENCONTRADO = "Termo não encontrado no arquivo" # Mensagem padrão para termo não encontrado no arquivo
ARQUIVO_NAO_ENCONTRADO = "Arquivo não encontrado" # Mensagem padrão para arquivo não encontrado

HOST = ''    # '' possibilita acessar qualquer endereco alcancavel da maquina local
PORTA = 5000  # porta onde chegarao as mensagens para essa aplicacao

# cria um socket para comunicacao
sock = socket.socket() # valores default: socket.AF_INET, socket.SOCK_STREAM  

# vincula a interface e porta para comunicacao
sock.bind((HOST, PORTA))

# define o limite maximo de conexoes pendentes e coloca-se em modo de espera por conexao
sock.listen(5) 

# aceita a primeira conexao da fila (chamada pode ser BLOQUEANTE)
novoSock, endereco = sock.accept() # retorna um novo socket e o endereco do par conectado
print ('Conectado com: ', endereco)

while True:
    # depois de conectar-se, espera o nome do arquivo (chamada pode ser BLOQUEANTE))
    nomeArquivo = novoSock.recv(1024)
    
    # espera o termo de busca
    termo = novoSock.recv(1024)
    
    if not nomeArquivo: break 
    else:
        # verifica se o arquivo existe
        if os.path.isfile(nomeArquivo):
            # abre o arquivo e o lê na variável conteudo, fechando-o em seguida
            arquivo = open(nomeArquivo)
            conteudo = arquivo.read()
            arquivo.close()
            
            # conta quantas vezes o termo está presente no arquivo, montando o resultado
            qtd = conteudo.count(str(termo,  encoding='utf-8'))
            if qtd > 0:
                resultado = "Termo encontrado " + str(qtd) + " vezes no arquivo."
            else:
                # termo não encontrado no arquivo
                resultado = TERMO_NAO_ENCONTRADO
        else:
            # arquivo não existe
            resultado = ARQUIVO_NAO_ENCONTRADO
            
    
    # envia mensagem de resposta
    novoSock.send(bytes(resultado, 'utf-8')) 

# fecha o socket da conexao
novoSock.close() 

# fecha o socket principal
sock.close() 
