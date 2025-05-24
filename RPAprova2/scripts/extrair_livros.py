import requests
from bs4 import BeautifulSoup
import sqlite3

def criar_banco_livros():
    conexao = sqlite3.connect("dados/livraria.db")
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS livros (
            titulo TEXT PRIMARY KEY,
            preco TEXT,
            avaliacao TEXT,
            disponibilidade TEXT
        )
    """)
    conexao.commit()
    return conexao, cursor

def extrair_avaliacao(classe):
    partes = classe.split()
    if len(partes) == 2:
        return partes[1]
    return "Não avaliado"

def buscar_livros():
    url = "https://books.toscrape.com/catalogue/page-1.html"
    resposta = requests.get(url)
    resposta.raise_for_status()
    soup = BeautifulSoup(resposta.text, 'html.parser')

    livros = []

    artigos = soup.find_all('article', class_='product_pod')[:10]  # só os 10 primeiros

    for art in artigos:
        titulo = art.h3.a['title']
        preco = art.find('p', class_='price_color').text.strip()
        avaliacao = extrair_avaliacao(art.p['class'][1])
        disponibilidade = art.find('p', class_='instock availability').text.strip()

        livros.append({
            "titulo": titulo,
            "preco": preco,
            "avaliacao": avaliacao,
            "disponibilidade": disponibilidade
        })

    return livros

def salvar_livros(cursor, livros):
    for livro in livros:
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO livros VALUES (
                    :titulo, :preco, :avaliacao, :disponibilidade
                )
            """, livro)
        except Exception as e:
            print(f"Erro ao salvar livro '{livro['titulo']}': {e}")

def executar_extracao_livros():
    print("📚 Iniciando extração dos livros...")
    conexao, cursor = criar_banco_livros()
    livros = buscar_livros()

    for livro in livros:
        print(f" - Livro: {livro['titulo']} (Preço: {livro['preco']}, Avaliação: {livro['avaliacao']})")

    salvar_livros(cursor, livros)
    conexao.commit()
    conexao.close()
    print("✅ Dados dos livros salvos em 'dados/livraria.db'.")

if __name__ == "__main__":
    executar_extracao_livros()
