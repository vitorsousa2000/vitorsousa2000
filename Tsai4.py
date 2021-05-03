'''
Código desenvolvido por Vitor Sousa para cálculo do critério de Tsai em Ligas de Alta Entropia, usando funções
criadas por Diego Santana.
'''
import numpy as np

def screening3(dx):
    composicoes = []
    for i in np.arange(0, 100+dx, dx):
        for j in np.arange(0, (100-i) + dx, dx):
            x0 = i/2
            x1 = j
            x2 = (100-i-j)
            x3 = i/2
            composicoes.append([x0, x1, x2, x3])
    composicoes = np.array(composicoes)
    return composicoes
comp3 = screening3(1)

#Neste exemplo, irei varrer o sistema VCrMnCo, com os pontos VCr, Mn, Co
#Aqui iremos colocar o número de elétrons de valência dos elementos
ve_el = [5,6,7,9] #Vanádio, Cromo, Manganês, Cobalto

#aqui iremos colocar se os elementos são A ou B (0 se forem A, 1 se forem B e 2 se não se encaixarem nesse critério)
PSFE_el = [0,0,2,1] #Vanádio, Cromo, Manganês, Cobalto

a={} #criamos o dicionário que será usado para plotar o gráfico
for k in range (len(comp3)): #loop para varrer os dados
    VEC = 0
    PSFE_a = 0
    PSFE_b = 0
    PSFE = 0
    CRIT = 0
    for w in range (4): #loop para varrer cada composição
        VEC += (comp3[k][w]*ve_el[w])/100 #soma parcial da VEC
        if(PSFE_el[w]==0): #aqui, caso o elemento seja A (=0), iremos somar sua % atômica em PSFE_a
            PSFE_a += comp3[k][w]
        elif(PSFE_el[w]==1): #aqui, caso o elemento seja B (=0), iremos somar sua % atômica em PSFE_b
            PSFE_b += comp3[k][w]
    if(PSFE_b>PSFE_a): #Como usamos o PSFE mínimo de A e B, tomamos o menor dos dois
        PSFE = 2*PSFE_a
    else:
        PSFE = 2*PSFE_b
    if(6.88<VEC<7.84):
        CRIT = 25
    if(PSFE>=45):
        if(6.88<VEC<7.84):
            CRIT = 100
        else:
            CRIT = 75
    a[comp3[k][0]+ comp3[k][3], comp3[k][1], comp3[k][2]] = CRIT #Aqui acrescentamos as composições ao dicionário juntamente com a informação
print(a)                                            #se haverá ou não fase sigma (CRIT=1 significa que há fase sigma, CRIT=0 que não)
a[0,0,0] = 100

import ternary 
figure, tax = ternary.figure(scale=100)

fontsize = 15

tax.right_corner_label("VCo", fontsize=fontsize, zorder=3)
tax.top_corner_label("Cr", fontsize=fontsize, zorder=3)
tax.left_corner_label("Mn", fontsize=fontsize, zorder=3)

# define os ticks do triangulo. podemos alterar tambem o seu tamanho
tax.ticks(axis='lbr', multiple=10, linewidth=0.5, offset=0.01, fontsize=8)

cb_kwargs = {'orientation': 'vertical', 'pad': 0.1, 'shrink': 0.85}

tax.heatmap(a, 100, cmap="Greys", cbarlabel = r"Criterio de Tsai", cb_kwargs=cb_kwargs)
tax.boundary(linewidth=2.0)

# desenha as linhas do triangulo interno
tax.gridlines(color="black", multiple=10, linewidth=0.5)
tax.clear_matplotlib_axis()

tax.show()