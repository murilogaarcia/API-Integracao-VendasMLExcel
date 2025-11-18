import os
import pandas as pd

EXCEL_PATH = "vendas_ml.xlsx"

def salvar_venda_excel(venda_dict):
    # Converte a venda atual em DataFrame
    df_novo = pd.DataFrame([venda_dict])

    # Se a planilha ainda não existe, cria do zero
    if not os.path.exists(EXCEL_PATH):
        df_novo.to_excel(EXCEL_PATH, index=False)
        print("📗 Planilha criada com a primeira venda.")
        return

    # Caso já exista, carregamos ela
    df_antigo = pd.read_excel(EXCEL_PATH)

    # Verificar se a venda já existe para não duplicar
    if venda_dict["id_venda"] in df_antigo["id_venda"].astype(str).values:
        print(f"⚠️ Venda {venda_dict['id_venda']} já registrada. Ignorando...")
        return

    # Junta dados antigos com os novos
    df_final = pd.concat([df_antigo, df_novo], ignore_index=True)

    # Salva o arquivo atualizado
    df_final.to_excel(EXCEL_PATH, index=False)
    print(f"📗 Venda {venda_dict['id_venda']} registrada no Excel com sucesso!")
