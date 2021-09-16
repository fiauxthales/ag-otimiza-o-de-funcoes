#!/usr/bin/python
__author__ = "Fiaux"
__date__ = "$07/01/2015 14:09:45$"

from random import *
import random
import sys
import math
limite_populacao=100
total_de_geracoes=800
numero_de_genes = 2


def gerar_genotipo():    
  y=0
  genotipos_individuo = range(numero_de_genes)
  while y <=(numero_de_genes - 1):
      #genotipos_individuo[y] = randint(-512,512)
      genotipos_individuo[y] = uniform(-512,512.00001)
      genotipos_individuo[y] = round(genotipos_individuo[y],4)
      y = y+1
  fitness = calcular_fitness(genotipos_individuo)
  genotipos_individuo.insert(0,fitness)
  genotipos_individuo.insert(0,valor_ng)
  return genotipos_individuo



def calcular_fitness(x):
    #fitness = (x[5]*x[0]*x[1])+ ((x[2]*x[3])*(x[6] / (x[7]+1.0))) + ((2*(x[7]**2))-(5*(x[1])*(x[0]))) + 3*x[4]  #fitness_montanha, melhor fit = 140
    #fitness = 300 -x[0]**2 -x[1]**2 -x[2]**2 -x[3]**2 -x[4]**2 -x[5]**2 -x[6]**2 -x[7]**2 #fitness_esferico, array desejado = (0,0 ... 0). 
    '''
    i=0 #fitness_rosenbrock, array desejado = (1,1...1)
    fitness = 0
    while (i<7):
        fitness = fitness + 100 - (100* (x[i+1] - (x[i]**2))**2 + ((x[i]-1)**2))
        i=i+1
    '''
    fitness = - (-(x[1]+47)*math.sin(math.sqrt(abs(x[1]+(x[0]/2)+47))) - x[0]*math.sin(math.sqrt(abs(x[0]-(x[1]+47)))))
    fitness = round(fitness,4)
    return fitness


def crossover(ind1,ind2):
    individuos=range(2)
    individuos[0]=ind1
    individuos[1]=ind2
    y=0
    filho = range(numero_de_genes)
    for y in range(0,numero_de_genes):
        gene = randint(0,1)
        filho[y]=individuos[gene][y+2]
    return filho


def salvar_em_arquivo(x,k):
    try:
        file = open("teste","w+")
    except IOError, message:
        print >> sys.stderr, "File could not be opened:",message
        sys.exit(1)
    y=0
    z=0
    for y in range(0,k):
        for z in range(0,numero_de_genes + 2):
            print >> file, x[y][z],
        print >> file,"\n",
    file.close()


def recuperar_arquivo(k):    
    try:
        file = open("filhos.dat","r")
    except IOError:
        print >> sys.stderr,"file could not be opened"
        sys.exit(1)
    a=0
    for a in range(0,k-1):
        individuos[a]=file.readline()
        individuos[a]=individuos[a].split(" ")
        y=0
        for y in range(0,numero_de_genes + 2):
            if (y==1):
                individuos[a][y]=float(individuos[a][y])
            else:
                individuos[a][y]=int(individuos[a][y])
        individuos[a].pop()
    return individuos


def gerar_filho(ind1,ind2,g):
    filho = [range(numero_de_genes)]
    filho=crossover(ind1,ind2)
    filho=mutacao(filho)
    fitness = calcular_fitness(filho)
    filho.insert(0,fitness)
    filho.insert(0,g)
    return filho


def mutacao(x):
    for y in range(0,numero_de_genes):
        chances_de_mutacao=randint(1,4)
        if(chances_de_mutacao==1):
            x[y]=round(uniform(512,512.00001),4)
    return x


def zeresima_geracao():
    for y in range(0,limite_populacao):
        individuos[y]=gerar_genotipo()


def nova_geracao_completa():
    y=0
    while(y<(limite_populacao)):
        a = selecionar_pais()
        b = selecionar_pais()
        #while(a==b):
        #    b = selecionar_pais()
        novo_filho = gerar_filho(a,b,valor_ng)
        individuos.append(novo_filho)
        y=y+1
    y=0

def nova_geracao_completa_recompensa4():
    taxa_superaptos = 5 #reproduzem 5 vezes, os 10% melhores
    taxa_aptos = 4      #reproduzem 4, proximos 20%
    taxa_medios = 3     #reproduzem 3, proximos 60%
    taxa_inaptos = 1    #reproduzem 1, proximos 10%
    
    novos_filhos = range(int(3.2*limite_populacao)) 
    
    geracao = obter_geracao(valor_ng-1)
    geracao.sort(lambda x, y: cmp(x[1],y[1]))
    geracao.sort(reverse=True)
    
    y=0
    x=0
    z=0
    
    #superaptos
    while(y<(0.1*limite_populacao)):
	while (x<taxa_superaptos):
	  a = geracao[y]
	  b = random.choice(geracao)
	  novo_filho = gerar_filho(a,b,valor_ng)
	  novos_filhos[z] = novo_filho
	  x=x+1
	  #print "\ngerando filho superapto de", y, novos_filhos[z]
	  z=z+1
	y=y+1
	x=0
	
    #aptos
    while(y<(0.3*limite_populacao)):
	while (x<taxa_aptos):
	  a = geracao[y]
	  b = random.choice(geracao)
	  novo_filho = gerar_filho(a,b,valor_ng)
	  novos_filhos[z] = novo_filho
	  x=x+1
	  #print "\ngerando filho apto", y, novos_filhos[z]
	  z=z+1
	y=y+1
	x=0
	
        
    #medios
    while(y<(0.9*limite_populacao)):
	while (x<taxa_medios):
	  a = geracao[y]
	  b = random.choice(geracao)
	  novo_filho = gerar_filho(a,b,valor_ng)
	  novos_filhos[z] = novo_filho
	  x=x+1
	  #print "\ngerando filho medio", y, novos_filhos[z]
	  z=z+1
	y=y+1
	x=0
	
  
    #inaptos
    while(y<(limite_populacao)):
	while (x<taxa_inaptos):
	  a = geracao[y]
	  b = random.choice(geracao)
	  novo_filho = gerar_filho(a,b,valor_ng)
	  novos_filhos[z] = novo_filho
	  x=x+1
	  #print "\ngerando filho inapto", y, novos_filhos[z]
	  z=z+1
	y=y+1
	x=0

    novos_filhos.sort()
    novos_filhos.sort(reverse=True)
    
    y=0
    while(y<(limite_populacao)):
        individuos.append(novos_filhos[y])
        y=y+1
    y=0
    
    
def nova_geracao_parcial():
    y=0
    while(y<(limite_populacao*0.9)):
        a = selecionar_pais()
        b = selecionar_pais()
        #while(a==b):
        #   b = selecionar_pais()
        novo_filho = gerar_filho(a,b,valor_ng)
        individuos.append(novo_filho)
        y=y+1
    y=0


def selecionar_pais():
    geracao = obter_geracao(valor_ng-1)
    geracao.sort(lambda x, y: cmp(x[1],y[1]))
    media_fitness=(geracao[0][1]+geracao[-1][1])/2
    geracao_len = len(geracao)
    i = 0
    while (i<2):
        ind_aleatorio = randint(0,geracao_len-1)
        if(geracao[ind_aleatorio][1] > media_fitness):
            return geracao[ind_aleatorio]
        i=i+1
    ind_aleatorio = randint(0,geracao_len-1)
    return geracao[ind_aleatorio]

def obter_geracao(geracao_procurada):
    geracao = []
    l = len(individuos)
    geracao_procurada = geracao_procurada
    for x in range(0,l-1):
        if(individuos[x][0]==geracao_procurada):
            geracao.insert(0,individuos[x])
    return geracao

def eliminar_menos_adaptados():
    numero_de_ind_eliminados = limite_populacao / 5
    k=0
    y=0
    while y < ((len(individuos))-1):
        if (individuos[y][0]==valor_ng):
            while(k < numero_de_ind_eliminados):
                individuos.pop(y)
                k=k+1
            break
        y=y+1
                

def migrantes():
    y=0
    while(y<(limite_populacao*0.2)):
        individuo_migrador = gerar_genotipo()
        individuos.append(individuo_migrador)
        y=y+1

individuos=[range(10)]*limite_populacao
valor_ng = 0
zeresima_geracao()
valor_ng = 1
x=0
while(x<(total_de_geracoes-1)):
# todos reproduzem, analisando os filhos: mata os filhos menos adaptados, e deixa imigrantes se misturarem aos filhos
    individuos.sort()
    eliminar_menos_adaptados()
    migrantes()
    nova_geracao_completa_recompensa4()
    valor_ng=valor_ng + 1
    x=x+1

# blablabla
    #nova_geracao_completa()
    #individuos.sort()
    #eliminar_menos_adaptados()
    #valor_ng=valor_ng + 1
    #migrantes()
    #x=x+1

individuos.sort()
numero_de_individuos = len(individuos)
salvar_em_arquivo(individuos,numero_de_individuos)