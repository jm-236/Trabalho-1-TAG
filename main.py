import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import random
import glob 

# --- 1. Construir o Grafo Completo ---
G_completo = nx.Graph()

# Encontra todos os arquivos .edges na pasta 'facebook/'
caminho_dados = 'facebook/*.edges'
arquivos_arestas = glob.glob(caminho_dados)

print(f"Construindo o grafo completo a partir de {len(arquivos_arestas)} arquivos de ego-networks...")

for arquivo in arquivos_arestas:
    # Extrai o ID do nó ego a partir do nome do arquivo
    try:
        # Tenta extrair o número do nome do arquivo. Ex: 'facebook/107.edges' -> 107
        ego_node = int(arquivo.split('/')[-1].split('.')[0])
    except ValueError:
        continue # Pula arquivos que não têm um ID numérico

    # Lê as conexões entre os amigos do ego
    df_arestas = pd.read_csv(arquivo, sep=' ', header=None)

    # Adiciona as arestas entre os amigos ao grafo completo
    for index, row in df_arestas.iterrows():
        G_completo.add_edge(row[0], row[1])

    # Encontra todos os amigos únicos mencionados no arquivo
    amigos_do_ego = set(df_arestas[0]).union(set(df_arestas[1]))

    # Adiciona a conexão do ego a cada um de seus amigos
    for amigo in amigos_do_ego:
        G_completo.add_edge(ego_node, amigo)

print("\n--- Grafo Completo Construído ---")
print(f"Número total de nós: {G_completo.number_of_nodes()}")
print(f"Número total de arestas: {G_completo.number_of_edges()}")


# --- 2. Extrair a Amostra e Criar o Subgrafo ---
populacao_de_nos = list(G_completo.nodes())
tamanho_da_amostra = 2000

amostra_aleatoria = random.sample(populacao_de_nos, tamanho_da_amostra)
G_subgrafo = G_completo.subgraph(amostra_aleatoria)

print("\n--- Subgrafo Aleatório Criado ---")
print(f"Nós no subgrafo: {G_subgrafo.number_of_nodes()}")
print(f"Arestas no subgrafo: {G_subgrafo.number_of_edges()}")

# --- 3. Analise de comunidades




# --- 3. Visualizar o Subgrafo ---
print("\nGerando a visualização...")
plt.figure(figsize=(14, 14))
pos = nx.spring_layout(G_subgrafo, iterations=30)
nx.draw(G_subgrafo, pos, with_labels=False, node_size=15, width=0.3, node_color='skyblue')
plt.title(f"Visualização do Subgrafo com {tamanho_da_amostra} Nós Aleatórios")
plt.show()