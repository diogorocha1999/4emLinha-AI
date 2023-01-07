import sys
import numpy

TABELA_TAM_X = 7 #Define o número de colunas
TABELA_TAM_Y = 6 #Define o número de linhas
PROFUNDIDADE_PESQUISA = 4 #Define a profundidade da procura em profundidade

COMPUTADOR = 1
HOMEM = -1

#
# Método que corre o algoritmo minimax e devolve a jogada e o resultado de cada jogada
#

def minimax(estadoJogo, profundidade, jogador, oponente):
    Jogadasdisponiveis = TABELA_TAM_X
    for i in range(0, TABELA_TAM_X):
        if estadoJogo[0][i] != 0:
            Jogadasdisponiveis -= 1

    if profundidade == 0 or Jogadasdisponiveis == 0:
        resultado = avaliaresultado(estadoJogo, jogador, oponente)
        return None, resultado

    melhorResultado = None
    melhorjogada = None

    for i in range(0, TABELA_TAM_X):
        # Se a jogada é inválida na coluna, passa á frente
        if estadoJogo[0][i] != 0:
            continue

        jogadaAtual = [0, i]

        for j in range(0, TABELA_TAM_Y - 1):
            if estadoJogo[j + 1][i] != 0:
                estadoJogo[j][i] = jogador
                jogadaAtual[0] = j
                break
            elif j == TABELA_TAM_Y - 2:
                estadoJogo[j+1][i] = jogador
                jogadaAtual[0] = j+1

        # Chama o minimax recursivo com Profundidade reduzida
        jogada, resultado = minimax(estadoJogo, profundidade - 1, oponente, jogador)

        estadoJogo[jogadaAtual[0]][jogadaAtual[1]] = 0

        if jogador == COMPUTADOR:
            if melhorResultado == None or resultado > melhorResultado:
                melhorResultado = resultado
                melhorjogada = jogadaAtual
        else:
            if melhorResultado == None or resultado < melhorResultado:
                melhorResultado = resultado
                melhorjogada = jogadaAtual

    return melhorjogada, melhorResultado

#
# Método que calcula o valor da heurística do estado do jogo.
# A heuristica adiciona um ponto ao jogador por cada lugar vazio na board que lhe consiga garantir a vitória
#

def avaliaresultado(estadoJogo, jogador, oponente):
    # Devolve infinito se um jogador ganhou numa board
    resultado = verificaVitoria(estadoJogo)

    if resultado == jogador:
        return float("inf")
    elif resultado == oponente:
        return float("-inf")
    else:
        resultado = 0

    for i in range(0, TABELA_TAM_Y):
        for j in range(0, TABELA_TAM_X):
            if estadoJogo[i][j] == 0:
                resultado += coordenadadoResultado(estadoJogo, i, j, jogador, oponente)

    return resultado

#
# Método que avalia se uma dada coordenada tem uma possibilidade de vitória para algum jogador.
# Cada coordenada avalia se uma possivel vitória poderá existir na vertical, horizontal e em ambas diagonais.
#

def coordenadadoResultado(estadoJogo, i, j, jogador, oponente):
    resultado = 0

    # Verifica a linha vertical
    resultado += resultadodaLinha(
                     estadoJogo=estadoJogo,
                     i=i,
                     j=j,
                     incrementoLinha=-1,
                     incrementoColuna=0,
                     condicaoprimeiraLinha=-1,
                     condicaosegundaLinha=TABELA_TAM_Y,
                     condicaoprimeiraColuna=None,
                     condicaosegundaColuna=None,
                     jogador=jogador,
                     oponente=oponente
                 )

    # Verifica a linha horizontal
    resultado += resultadodaLinha(
                     estadoJogo=estadoJogo,
                     i=i,
                     j=j,
                     incrementoLinha=0,
                     incrementoColuna=-1,
                     condicaoprimeiraLinha=None,
                     condicaosegundaLinha=None,
                     condicaoprimeiraColuna=-1,
                     condicaosegundaColuna=TABELA_TAM_X,
                     jogador=jogador,
                     oponente=oponente
                 )

    # verifica a diagonal para a direita /
    resultado += resultadodaLinha(
                     estadoJogo=estadoJogo,
                     i=i,
                     j=j,
                     incrementoLinha=-1,
                     incrementoColuna=1,
                     condicaoprimeiraLinha=-1,
                     condicaosegundaLinha=TABELA_TAM_Y,
                     condicaoprimeiraColuna=TABELA_TAM_X,
                     condicaosegundaColuna=-1,
                     jogador=jogador,
                     oponente=oponente
                 )

    # verifica a diagonal para a esquerda \
    resultado += resultadodaLinha(
                     estadoJogo=estadoJogo,
                     i=i,
                     j=j,
                     incrementoLinha=-1,
                     incrementoColuna=-1,
                     condicaoprimeiraLinha=-1,
                     condicaosegundaLinha=TABELA_TAM_Y,
                     condicaoprimeiraColuna=-1,
                     condicaosegundaColuna=TABELA_TAM_X,
                     jogador=jogador,
                     oponente=oponente
                 )

    return resultado

#
# Método que pesquisa através de uma linha (vertical, horizontal ou diagonal)
# para achar o valor da heurística de uma dada coordenada.
#

def resultadodaLinha(
    estadoJogo,
    i,
    j,
    incrementoLinha,
    incrementoColuna,
    condicaoprimeiraLinha,
    condicaosegundaLinha,
    condicaoprimeiraColuna,
    condicaosegundaColuna,
    jogador,
    oponente
):
    resultado = 0
    linhaAtual = 0
    valoresLinha = 0
    valoresLinhaPrev = 0

    # Repete num lado da linha até uma jogada do outro jogador ou um espaço livre for encontrado.
    linha = i + incrementoLinha
    coluna = j + incrementoColuna
    primeiroLoop = True
    while (
        linha != condicaoprimeiraLinha and
        coluna != condicaoprimeiraColuna and
        estadoJogo[linha][coluna] != 0
    ):
        if primeiroLoop:
            linhaAtual = estadoJogo[linha][coluna]
            primeiroLoop = False
        if linhaAtual == estadoJogo[linha][coluna]:
            valoresLinha += 1
        else:
            break
        linha += incrementoLinha
        coluna += incrementoColuna

    # Repete no segundo lado da linha
    linha = i - incrementoLinha
    coluna = j - incrementoColuna
    primeiroLoop = True
    while (
        linha != condicaosegundaLinha and
        coluna != condicaosegundaColuna and
        estadoJogo[linha][coluna] != 0
    ):
        if primeiroLoop:
            primeiroLoop = False

            # Verifica se o lado anterior da linha garante uma vitória na coordenada.
            # Caso não se verifique, continua a contar para verificar se certa coordenada consegue completar
            # uma linha a partir do meio. 
            if linhaAtual != estadoJogo[linha][coluna]:
                if valoresLinha == 3 and linhaAtual == jogador:
                    resultado += 1
                elif valoresLinha == 3 and linhaAtual == oponente:
                    resultado -= 1
            else:
                valoresLinhaPrev = valoresLinha

            valoresLinha = 0
            linhaAtual = estadoJogo[linha][coluna]

        if linhaAtual == estadoJogo[linha][coluna]:
            valoresLinha += 1
        else:
            break
        linha -= incrementoLinha
        coluna -= incrementoColuna

    if valoresLinha + valoresLinhaPrev >= 3 and linhaAtual == jogador:
        resultado += 1
    elif valoresLinha + valoresLinhaPrev >= 3 and linhaAtual == oponente:
        resultado -= 1

    return resultado

#
# Método que executa a primeira execução do método minimax e devolve
# a jogada para ser executada pelo computador.
# Também verifica se alguma vitória ou derrota está presente.
#

def melhorjogada(estadoJogo, jogador, oponente):
    for i in range(0, TABELA_TAM_X):
        # Caso não se possa fazer jogadas na coluna, passa á frente
        if estadoJogo[0][i] != 0:
            continue

        jogadaAtual = [0, i]

        for j in range(0, TABELA_TAM_Y - 1):
            if estadoJogo[j + 1][i] != 0:
                estadoJogo[j][i] = jogador
                jogadaAtual[0] = j
                break
            elif j == TABELA_TAM_Y - 2:
                estadoJogo[j+1][i] = jogador
                jogadaAtual[0] = j+1

        vencedor = verificaVitoria(estadoJogo)
        estadoJogo[jogadaAtual[0]][jogadaAtual[1]] = 0

        if vencedor == COMPUTADOR:
            return jogadaAtual[1]

    for i in range(0, TABELA_TAM_X):
        # Se a jogada não pode ser feita na coluna, passa á frente.
        if estadoJogo[0][i] != 0:
            continue

        jogadaAtual = [0, i]

        for j in range(0, TABELA_TAM_Y - 1):
            if estadoJogo[j + 1][i] != 0:
                estadoJogo[j][i] = oponente
                jogadaAtual[0] = j
                break
            elif j == TABELA_TAM_Y - 2:
                estadoJogo[j+1][i] = oponente
                jogadaAtual[0] = j+1

        vencedor = verificaVitoria(estadoJogo)
        estadoJogo[jogadaAtual[0]][jogadaAtual[1]] = 0

        if vencedor == HOMEM:
            return jogadaAtual[1]

    jogada, resultado = minimax(estadoJogo, PROFUNDIDADE_PESQUISA, jogador, oponente)
    return jogada[1]

#
# Método que verifica se a atual board está em condições de vitória para
# algum jogador, retornando infinito se esse é o caso.
#

def verificaVitoria(estadoJogo):
    atual = 0
    atualContagem = 0
    computador_ganha = 0
    oponente_ganha = 0

    # Verifica vitórias na horizontal
    for i in range(0, TABELA_TAM_Y):
        for j in range(0, TABELA_TAM_X):
            if atualContagem == 0:
                if estadoJogo[i][j] != 0:
                    atual = estadoJogo[i][j]
                    atualContagem += 1
            elif atualContagem == 4:
                if atual == COMPUTADOR:
                    computador_ganha += 1
                else:
                    oponente_ganha += 1
                atualContagem = 0
                break
            elif estadoJogo[i][j] != atual:
                if estadoJogo[i][j] != 0:
                    atual = estadoJogo[i][j]
                    atualContagem = 1
                else:
                    atual = 0
                    atualContagem = 0
            else:
                atualContagem += 1

        if atualContagem == 4:
            if atual == COMPUTADOR:
                computador_ganha += 1
            else:
                oponente_ganha += 1
        atual = 0
        atualContagem = 0

    # Verifica vitórias na vertical
    for j in range(0, TABELA_TAM_X):
        for i in range(0, TABELA_TAM_Y):
            if atualContagem == 0:
                if estadoJogo[i][j] != 0:
                    atual = estadoJogo[i][j]
                    atualContagem += 1
            elif atualContagem == 4:
                if atual == COMPUTADOR:
                    computador_ganha += 1
                else:
                    oponente_ganha += 1
                atualContagem = 0
                break
            elif estadoJogo[i][j] != atual:
                if estadoJogo[i][j] != 0:
                    atual = estadoJogo[i][j]
                    atualContagem = 1
                else:
                    atual = 0
                    atualContagem = 0
            else:
                atualContagem += 1

        if atualContagem == 4:
            if atual == COMPUTADOR:
                computador_ganha += 1
            else:
                oponente_ganha += 1
        atual = 0
        atualContagem = 0

    # Verifica vitórias nas diagonais
    np_matriz = numpy.array(estadoJogo)
    diags = [np_matriz[::-1,:].diagonal(i) for i in range(-np_matriz.shape[0]+1,np_matriz.shape[1])]
    diags.extend(np_matriz.diagonal(i) for i in range(np_matriz.shape[1]-1,-np_matriz.shape[0],-1))
    diags_list = [n.tolist() for n in diags]

    for i in range(0, len(diags_list)):
        if len(diags_list[i]) >= 4:
            for j in range(0, len(diags_list[i])):
                if atualContagem == 0:
                    if diags_list[i][j] != 0:
                        atual = diags_list[i][j]
                        atualContagem += 1
                elif atualContagem == 4:
                    if atual == COMPUTADOR:
                        computador_ganha += 1
                    else:
                        oponente_ganha += 1
                    atualContagem = 0
                    break
                elif diags_list[i][j] != atual:
                    if diags_list[i][j] != 0:
                        atual = diags_list[i][j]
                        atualContagem = 1
                    else:
                        atual = 0
                        atualContagem = 0
                else:
                    atualContagem += 1

            if atualContagem == 4:
                if atual == COMPUTADOR:
                    computador_ganha += 1
                else:
                    oponente_ganha += 1
            atual = 0
            atualContagem = 0

    if oponente_ganha > 0:
        return HOMEM
    elif computador_ganha > 0:
        return COMPUTADOR
    else:
        return 0

#
# Função que imprime a board do jogo, representando o jogador como 0 e o computador como X.
#

def printTabela(estadoJogo):
    for i in range(1, TABELA_TAM_X + 1):
        sys.stdout.write(" %d " % i)

    print ("")
    print ("_" * (TABELA_TAM_X * 3))
    for i in range(0, TABELA_TAM_Y):
        for j in range(0, TABELA_TAM_X):

            if estadoJogo[i][j] == 1:
                sys.stdout.write("|X|")
            elif estadoJogo[i][j] == -1:
                sys.stdout.write("|O|")
            else:
                sys.stdout.write("|-|")

        print ("")

    print ("_" * (TABELA_TAM_X * 3))
    print ("")

#
# Método que devolve o main flow do jogo, perguntando ao jogador para fazer
# a jogada, e due depois dá a oportunidade do computador fazer a sua.
# 
# Depois de cada turno, o método verifica se a board está cheia ou se algum 
# jogador ganhou.
# 

def playGame():
    estadoJogo = [[0 for col in range(TABELA_TAM_X)] for linha in range(TABELA_TAM_Y)]
    jogadaVertical = [0] * TABELA_TAM_X
    jogador = COMPUTADOR
    oponente = HOMEM
    vencedor = 0
    fimJogo = False
    colunasRestantes = TABELA_TAM_X
    print ("= BEM-VINDO AO 4 EM LINHA! =")
    printTabela(estadoJogo)


    while True:

        while True:
            try:
                jogada = int(input("Escolha a coluna onde quer jogar? (escolhe entre 1 e %d)" % TABELA_TAM_X))
            except ValueError:
                print ("Escolha ERRADA! Tente novamente.")
                continue
            if jogada < 1 or jogada > TABELA_TAM_X:
                print ("Essa jogada não é válida. Tente novamente.")
            elif jogadaVertical[jogada - 1] == TABELA_TAM_Y:
                print ("A Coluna escolhida já está cheia. Tente novamente.")
            else:
                break

        jogadaVertical[jogada - 1] += 1
        estadoJogo[TABELA_TAM_Y - jogadaVertical[jogada - 1]][jogada - 1] = oponente
        printTabela(estadoJogo)

        if jogadaVertical[jogada - 1] == TABELA_TAM_Y:
            colunasRestantes -= 1
        if colunasRestantes == 0:
            fimJogo = True
        if fimJogo:
            break

        resultado = verificaVitoria(estadoJogo)
        if resultado == jogador:
            vencedor = jogador
            break
        elif resultado == oponente:
            vencedor = oponente
            break
        else:
            resultado = 0

        print ("Agora é a vez do COMPUTADOR! AGUARDA!")
        jogada = melhorjogada(estadoJogo, jogador, oponente)
        if jogada == None:
            break

        jogadaVertical[jogada] += 1
        estadoJogo[TABELA_TAM_Y - jogadaVertical[jogada]][jogada] = jogador
        printTabela(estadoJogo)

        if jogadaVertical[jogada] == TABELA_TAM_Y:
            colunasRestantes -= 1
        if colunasRestantes == 0:
            fimJogo = True
        if fimJogo:
            break

        resultado = verificaVitoria(estadoJogo)
        if resultado == jogador:
            vencedor = jogador
            break
        elif resultado == oponente:
            vencedor = oponente
            break
        else:
            resultado = 0

    return vencedor

#
# O Main do Jogo. É executado até o jogador decidir parar.
#

if __name__ == "__main__":
    playing = True
    while playing:
        vencedor = playGame()
        if vencedor == COMPUTADOR:
            print ("CARAGO! PERDESTE!")
        elif vencedor == HOMEM:
            print ("Cum Catano! GANHASTE!")
        else:
            print ("Tá tudo CHEIO. É um EMPATE!")

        while True:
            try:
                option = input("Queres jogar novamente? (S/N)")
            except ValueError:
                print ("Opção inválida. Tente novamente.")
                continue
            if option == 'S' or option == 's':
                break
            elif option == 'N' or option == 'n':
                playing = False
                break
            else:
                print ("Por favor Introduz S(s) ou N(n)!!!")
