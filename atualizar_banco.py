import json
import os
import glob

# Configurações de pastas
ARQUIVO_MESTRE = "banco_final.json"
PASTA_EXTRACOES = "extrações"

def processar_banco():
    # 1. Tenta carregar o banco que você já tem
    banco_dados = {} # Usamos um dicionário para garantir IDs únicos
    
    if os.path.exists(ARQUIVO_MESTRE):
        with open(ARQUIVO_MESTRE, 'r', encoding='utf-8') as f:
            try:
                lista_existente = json.load(f)
                # Transforma a lista em dicionário: { "3057536": {dados}, ... }
                for q in lista_existente:
                    banco_dados[str(q['id'])] = q
            except:
                print("Aviso: Banco mestre estava vazio ou corrompido. Iniciando do zero.")

    print(f"Estado atual: {len(banco_dados)} questões únicas no banco.")

    # 2. Varre a pasta de novas extrações
    arquivos_novos = glob.glob(os.path.join(PASTA_EXTRACOES, "*.json"))
    
    if not arquivos_novos:
        print("Nenhuma nova extração encontrada na pasta 'extrações'.")
        return

    novas_adicionadas = 0
    repetidas_ignoradas = 0

    for arquivo in arquivos_novos:
        print(f"Lendo arquivo: {arquivo}")
        with open(arquivo, 'r', encoding='utf-8') as f:
            try:
                dados_arquivo = json.load(f)
                for questao in dados_arquivo:
                    id_q = str(questao['id'])
                    
                    # O FOCO: Verificar se a QUESTÃO é repetida, não o arquivo
                    if id_q not in banco_dados:
                        banco_dados[id_q] = questao
                        novas_adicionadas += 1
                    else:
                        repetidas_ignoradas += 1
            except Exception as e:
                print(f"Erro ao processar {arquivo}: {e}")

    # 3. Salva o resultado de volta em formato de lista para o seu Visualizador HTML
    lista_final = list(banco_dados.values())
    
    with open(ARQUIVO_MESTRE, 'w', encoding='utf-8') as f:
        json.dump(lista_final, f, indent=2, ensure_ascii=False)

    print("\n" + "="*40)
    print(f"PROCESSAMENTO CONCLUÍDO")
    print(f"Questões NOVAS adicionadas: {novas_adicionadas}")
    print(f"Questões REPETIDAS ignoradas: {repetidas_ignoradas}")
    print(f"Total de questões ÚNICAS agora: {len(lista_final)}")
    print("="*40)

    # 4. Limpeza opcional
    limpar = input("\nDeseja apagar os arquivos da pasta 'extrações' para a próxima rodada? (s/n): ")
    if limpar.lower() == 's':
        for arquivo in arquivos_novos:
            os.remove(arquivo)
        print("Pasta de extrações limpa.")

if __name__ == "__main__":
    processar_banco()