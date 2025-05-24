import requests
import sqlite3

def criar_banco_paises():
    conexao = sqlite3.connect("dados/paises.db")
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS paises (
            nome_comum TEXT PRIMARY KEY,
            nome_oficial TEXT,
            capital TEXT,
            continente TEXT,
            regiao TEXT,
            sub_regiao TEXT,
            populacao INTEGER,
            area REAL,
            moeda_nome TEXT,
            moeda_simbolo TEXT,
            idioma TEXT,
            fuso_horario TEXT,
            url_bandeira TEXT
        )
    """)
    conexao.commit()
    return conexao, cursor

def buscar_dados_pais(nome_pais):
    url = f"https://restcountries.com/v3.1/name/{nome_pais}"
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
        dados = resposta.json()[0]

        # Extraindo informações necessárias com tratamento para campos ausentes
        nome_comum = dados.get("name", {}).get("common", "N/A")
        nome_oficial = dados.get("name", {}).get("official", "N/A")
        capital = dados.get("capital", ["N/A"])[0]
        continente = dados.get("continents", ["N/A"])[0]
        regiao = dados.get("region", "N/A")
        sub_regiao = dados.get("subregion", "N/A")
        populacao = dados.get("population", 0)
        area = dados.get("area", 0.0)

        moedas = dados.get("currencies", {})
        if moedas:
            moeda_nome = list(moedas.values())[0].get("name", "N/A")
            moeda_simbolo = list(moedas.values())[0].get("symbol", "N/A")
        else:
            moeda_nome = "N/A"
            moeda_simbolo = "N/A"

        idiomas = dados.get("languages", {})
        idioma = list(idiomas.values())[0] if idiomas else "N/A"

        fuso_horario = dados.get("timezones", ["N/A"])[0]
        url_bandeira = dados.get("flags", {}).get("png", "N/A")

        return (
            nome_comum,
            nome_oficial,
            capital,
            continente,
            regiao,
            sub_regiao,
            populacao,
            area,
            moeda_nome,
            moeda_simbolo,
            idioma,
            fuso_horario,
            url_bandeira
        )

    except requests.exceptions.HTTPError as e:
        if resposta.status_code == 404:
            print(f"❌ País '{nome_pais}' não encontrado. Tente outro nome (em inglês).")
            return None
        else:
            print(f"Erro ao buscar '{nome_pais}': {e}")
            return None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None

def solicitar_paises():
    paises_validos = []
    while len(paises_validos) < 3:
        nome = input(f"Digite o nome do {len(paises_validos)+1}º país (em inglês): ").strip()
        dados = buscar_dados_pais(nome)
        if dados:
            paises_validos.append(dados)
        else:
            print("Vamos tentar novamente.")
    return paises_validos

def salvar_paises(cursor, paises):
    for pais in paises:
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO paises VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, pais)
            print(f"✅ {pais[0]} salvo com sucesso!")
        except Exception as e:
            print(f"Erro ao salvar {pais[0]}: {e}")

def executar_extracao_paises():
    print("🌍 Bem-vindo ao Extrator de Dados de Países!")
    conexao, cursor = criar_banco_paises()
    paises = solicitar_paises()
    salvar_paises(cursor, paises)
    conexao.commit()
    conexao.close()
    print("📦 Todos os países foram salvos em 'dados/paises.db'!")

if __name__ == "__main__":
    executar_extracao_paises()
