import networkx as nx
import random
import math
#import matplotlib.pyplot as plt
#import mplcursors
from colorama import Fore, Back, Style, init

init() #Para Colorama

Semilla = random.seed(37) #Para reproducir ejemplos

############################################################################
#Funciones para hacer la digráfica mas estetica y ejemplificar la generación de texto
############################################################################

def calculate_positions(G, QN, UnoAbs, DosAbs):
    positions = {}
    num_nodes = len(G.nodes)
    for i, node in enumerate(G.nodes):
        if node in QN:
            theta = (num_nodes / (2 * math.pi)) + (i / (2 * math.pi))
            positions[node] = (3 * math.cos(theta), 3 * math.sin(theta))
        elif node in UnoAbs:
            theta = (num_nodes / (2 * math.pi)) + (i / (2 * math.pi))
            positions[node] = (2 * math.cos(theta), 2 * math.sin(theta))
        elif node in DosAbs:
            theta = (num_nodes / (2 * math.pi)) + (i / (2 * math.pi))
            positions[node] = (math.cos(theta), math.sin(theta))
    return positions

def Color(texto):
  color = ''
  if texto in QN:
     color = Back.BLUE
  elif texto in UnoAbs:
     color = Back.RED
  elif texto in DosAbs:
     color = Back.GREEN
  return color

############################################################################
#Creación de la digráfica de co-ocurrencia
############################################################################

def SepararTexto(texto):
    l = []
    x = ''

    for palabra in texto:
        if palabra == " ":
            x += palabra
        #elif palabra == ".":
        #    if x:
        #        l.append(x)
        #        x = ""
        #    l.append(".")
        else:
            if x and x[-1] == " ":
                l.append(x)
                x = ""
            x += palabra
    
    if x:
       l.append(x)

    l[-1] += ' '

    return l

def DiGraCo(A):
  Aa = [SepararTexto(A[i]) for i in range(len(A))]

  G = nx.DiGraph()

  for i in range(len(A)):
      for j in range(len(Aa[i])-1):
          G.add_edge(Aa[i][j],Aa[i][j+1])

  return G

A = [
        "Un gato ve un gato.",
        "Vi un gato. Es naranja.",
        "Es raro ver el color naranja. Excepto en un gato."
    ]

G = DiGraCo(A)

############################################################################
#Funciones para calcular quasi-núcleo
############################################################################

nodes = list(G.nodes())

def ConjIndMax(DiGra):
    con = set()
    nodos = list(DiGra.nodes())

    while nodos:
        node = nodos.pop()
        con.add(node)
        nodos = [n for n in nodos if not (n in DiGra[node] or node in DiGra[n])]

    return con

def PropDosAbs(G, S):
    for nodo in set(G.nodes) - S:
        if all(nx.shortest_path_length(G, nodo, s) > 2 for s in S if nx.has_path(G, nodo, s)):
            return False
    return True

def QuasiNucleo(G):
    S = ConjIndMax(G)
    while not PropDosAbs(G, S):
        S = ConjIndMax(G)
    return S

############################################################################
#Calcular un quasi-nucleo de la sub-digrafica
############################################################################

NodosEliminar = []

def SubDiGra(G):
  Nodos = list(reversed(nodes))

  H = G.copy()

  for n in range(0,len(nodes)-5):
      v = Nodos[n]
      Pred_v = G.predecessors(v)

      H_nodes = list(H.nodes())

      if v in H_nodes:
          NodosEliminar.append(v)
          H.remove_node(v)
          H.remove_nodes_from(Pred_v)

  return H

H = SubDiGra(G)

QN = set()

if not len(H) == 0:
  if nx.is_weakly_connected(H):
    QN = QuasiNucleo(H)
  else:
    for C in nx.weakly_connected_components(H):
      QN.update(QuasiNucleo(H.subgraph(list(C))))

############################################################################
#Completar el quasi-nucleo
############################################################################

Invertir_NodosEliminar = list(reversed(NodosEliminar))

for n in range(0,len(NodosEliminar)):

    QN_copy = QN.copy()

    if any(G.has_edge(Invertir_NodosEliminar[n],s) or G.has_edge(s,Invertir_NodosEliminar[n]) for s in QN_copy):
        continue
    else:
        QN.add(Invertir_NodosEliminar[n])

UnoAbs = set(v for v in set(G.nodes-QN) if any(nx.shortest_path_length(G, v, s) == 1 for s in QN if nx.has_path(G, v, s)))

DosAbs = set(v for v in set(G.nodes-QN-UnoAbs) if any(nx.shortest_path_length(G, v, s) == 2 for s in QN if nx.has_path(G, v, s)))

def SigNodo(Nodo1, QNucleo, DiGra):
    if Nodo1 in QNucleo:
        Vecinos = [vecino for vecino in DiGra[Nodo1] if vecino not in QNucleo and set(Nodo1)]
        if Vecinos:
            return random.choice(Vecinos)
    elif Nodo1 in UnoAbs:
        Vecinos = [vecino for vecino in DiGra[Nodo1] if vecino in QNucleo]
        if Vecinos:
            return random.choice(Vecinos)
    elif Nodo1 in DosAbs:
        Vecinos = [vecino for vecino in DiGra[Nodo1] if vecino in UnoAbs]
        if Vecinos:
            return random.choice(Vecinos)
    return None

############################################################################
# Para vizualizar la digráfica
############################################################################

#pos = calculate_positions(G, QN, UnoAbs, DosAbs)

#node_colors = ["skyblue" if node in QN else "red" if node in UnoAbs else "green" for node in G.nodes]
#bbox_params = {
#    'boxstyle': "round,pad=0.3",  
#    'ec': "black",               
#    'fc': "lightyellow",         
#    'alpha': 0.7                 
#}

#nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=40) # nx.draw_networkx_labels(G, pos, font_size=10, font_color='black', font_weight='bold', bbox=bbox_params) # 
#nx.draw_networkx_edges(G, pos, arrowsize=10, alpha=0.3)
#plt.axis("off")

#crs = mplcursors.cursor(hover=True)

#crs.connect("add", lambda sel: sel.annotation.set_text(f'{list(G.nodes)[sel.target.index]}'))

#plt.show()

############################################################################
# Cerrar la ventana de la gráfica para ejecutar el resto del código
############################################################################

print("Escriba 'Salir' para acabar el programa.")

while True:
    texto_input = input("Usuario: ")

    if texto_input.lower() == 'salir':
        print("Cerrando el programa")
        break

    B = [texto_input]

    #

    Bb = SepararTexto(B[0]) #B[0].split(' ') #

    UltNodo = Bb[-1]

    Continuator = [B[0]+' ']
    
    for _ in range(50):
        next_node = SigNodo(UltNodo, QN, G)
        if next_node is None:
            break
        elif "." == next_node or "?" in next_node or "!" in next_node:
            Continuator.append(next_node)
            UltNodo = next_node
            break

        Continuator.append(next_node)
        UltNodo = next_node

    Continuator = [Color(Continuator[i]) + Fore.BLACK + Continuator[i] + Style.RESET_ALL for i in range(len(Continuator))]

    if len(Continuator) == 0:
      print('Continuator : Perdón no se como responder.')
    else:
      print(f'Continuator: {"".join(Continuator)}')