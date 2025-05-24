from scripts.extrair_paises import executar_extracao_paises
from scripts.extrair_livros import executar_extracao_livros
from scripts.gerar_relatorio import gerar_relatorio

def main():
    print("🚀 Iniciando processo completo...")

    executar_extracao_paises()

    executar_extracao_livros()

    nome_aluno = input("Digite seu nome para o relatório final: ")
    gerar_relatorio(nome_aluno)

    print("🎉 Processo finalizado! Relatório criado com sucesso.")

if __name__ == "__main__":
    main()
