import json
import requests
from datetime import datetime
from excel_writer import salvar_venda_excel

CAMINHO_DADOS = "dados.json"


# 1) CARREGAR E SALVAR ARQUIVO JSON DE CREDENCIAIS

def carregar_dados():
    with open(CAMINHO_DADOS, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_dados(dados):
    with open(CAMINHO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)




# 2) GERAR NOVO ACCESS TOKEN USANDO O REFRESH TOKEN

def gerar_access_token(dados):
    url = "https://api.mercadolibre.com/oauth/token"

    payload = {
        "grant_type": "refresh_token",
        "client_id": dados["client_id"],
        "client_secret": dados["client_secret"],
        "refresh_token": dados["refresh_token"]
    }

    headers = {"content-type": "application/x-www-form-urlencoded"}

    r = requests.post(url, headers=headers, data=payload)

    if r.status_code != 200:
        print("❌ ERRO AO GERAR NOVO ACCESS TOKEN")
        print(r.text)
        raise Exception("Erro ao renovar o token")

    resposta = r.json()

    # Atualiza tokens no JSON
    dados["access_token"] = resposta["access_token"]
    dados["refresh_token"] = resposta["refresh_token"]

    salvar_dados(dados)
    print("🔄 Tokens atualizados e salvos no dados.json!\n")

    return resposta["access_token"]




# 3) BUSCAR VENDAS DO DIA PARA O USER ID INFORMADO

def buscar_vendas_hoje(access_token, user_id):
    hoje = datetime.now().strftime("%Y-%m-%dT00:00:00.000-03:00")

    url = (
        "https://api.mercadolibre.com/orders/search?"
        f"seller={user_id}&order.date_created.from={hoje}"
    )

    headers = {"Authorization": f"Bearer {access_token}"}

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print("❌ Erro ao buscar vendas:")
        print(r.text)

    return r.json()




# 4) PEGAR VALORES FINANCEIROS DE UMA VENDA / PAGAMENTO

def pegar_pagamento(order_id, access_token):
    url = f"https://api.mercadolibre.com/orders/{order_id}"
    headers = {"Authorization": f"Bearer {access_token}"}

    r = requests.get(url, headers=headers)
    dados = r.json()

    # Evita erro caso a venda não tenha pagamento ainda
    if not dados.get("payments"):
        return {
            "valor_produto": 0
        }

    pagamento = dados["payments"][0]

    valor_produto = pagamento["transaction_amount"]      # Preço do produto

    return {
        "valor_produto": valor_produto
    }

def pegar_tarifa_envio(order):
    tarifa_envio = 0

    if "fees" in order:
        for fee in order["fees"]:
            if fee.get("type") == "shipping":
                tarifa_envio = float(fee.get("amount", 0))
                break

    return tarifa_envio



# 5) MOSTRAR AS VENDAS E SALVAR NA PLANILHA DO EXCEL

def mostrar_vendas(vendas, access_token):
    print("📦 VENDAS DO DIA\n")

    for v in vendas.get("results", []):

        buyer_name = v["buyer"]["nickname"]
        sale_fee = v["order_items"][0]["sale_fee"]
        

        # produto principal
        item = v["order_items"][0]["item"]
        quantidade = v["order_items"][0]["quantity"]

        pagamento = pegar_pagamento(v["id"], access_token)

        #pegar tarifa de Envio do Mercado de Envios
        detalhes = requests.get(
            f"https://api.mercadolibre.com/orders/{v['id']}",
            headers={"Authorization": f"Bearer {access_token}"}
        ).json()

        # tarifa Mercado Envios (por sua conta)
        tarifa_envio = pegar_tarifa_envio(detalhes)

        lucro_liquido = pagamento['valor_produto'] - (sale_fee + tarifa_envio)

        # evitar divisão por zero
        if pagamento["valor_produto"] > 0:
            margem_lucro = (lucro_liquido / pagamento["valor_produto"]) * 100
        else:
            margem_lucro = 0

        print("----------------------------")
        print(f"👤 Comprador: {buyer_name}")
        print(f"ID da venda:  {v.get('id')}")
        print(f"Status:       {v.get('status')}")
        print(f"Data criação: {v.get('date_created')}")
        print("📦 Produto:", item["title"])
        print(f"📦 Quantidade: {quantidade}")
        print(f"💰 Valor do produto: R$ {pagamento['valor_produto']}")
        print(f"💰 Tarifa de venda: R$ {sale_fee}")
        print(f"Tarifa Mercado Envios (por sua conta): R$ {tarifa_envio:.2f}")
        print(f"💵 Total líquido(ML): R$ {lucro_liquido}")
        print(f"💵 Margem lucro(ML): {margem_lucro:.2f}%")
        print("----------------------------\n")

        venda_dict = {
            "comprador": buyer_name,
            "id_venda": v.get("id"),
            "status": v.get("status"),
            "data_criacao": v.get("date_created"),
            "produto": item["title"],
            "quantidade": quantidade,
            "valor_produto": pagamento["valor_produto"],
            "total_taxas": sale_fee,
            "total_envio": tarifa_envio,
            "liquido": lucro_liquido,
            "margem_lucro": round(margem_lucro, 2)
        }

        salvar_venda_excel(venda_dict)

    total = vendas.get("paging", {}).get("total", 0)
    print(f"Total de vendas hoje: {total}")




# 6) PROGRAMA PRINCIPAL

def main():
    dados = carregar_dados()

    # 1. Atualizar tokens
    access_token = gerar_access_token(dados)

    # 2. Buscar vendas do dia
    vendas = buscar_vendas_hoje(access_token, dados["user_id"])

    # 3. Mostrar e salvar excel
    mostrar_vendas(vendas, access_token)



if __name__ == "__main__":
    main()
