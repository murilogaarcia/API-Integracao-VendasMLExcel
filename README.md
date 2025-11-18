📦 API Mercado Livre – Consulta de Vendas + Exportação para Excel

Este projeto foi criado para automatizar a consulta de vendas diárias no Mercado Livre, calcular taxas, obter valores líquidos e exportar tudo para uma planilha Excel.
A motivação veio do fato de que muitos micro e pequenos sellers ainda utilizam Excel para controle de vendas, então a automação ajuda a reduzir erros e economizar tempo.

⸻

🚀 Funcionalidades
	•	Busca automática das vendas do dia via API do Mercado Livre
	•	Cálculo de:
	•	Valor do produto
	•	Tarifa de venda (sale fee)
	•	Tarifas de envio (shipping fee) quando disponíveis
	•	Total líquido
	•	Margem de lucro
	•	Consulta do pagamento da venda
	•	Exportação automática para Excel (um registro por linha)
	•	Atualização automática do access token via refresh token
	•	Organização clara dos dados no terminal

⸻

🛠 Estrutura do Projeto:
/API-VendasML
│
├── dados.json              # Tokens e credenciais
├── search_orderML.py       # Código principal
├── requirements.txt
└── vendas.xlsx             # Arquivo gerado com as vendas

🔑 1. Criando a Aplicação no Mercado Livre
	1.	Acesse: https://developers.mercadolivre.com.br
	2.	Vá em Minhas Aplicações
	3.	Crie uma nova aplicação
	4.	Defina:
  	•	Redirect URI
  	•	Nome da aplicação
	5.	Copie:
  	•	APP_ID (Client ID)
  	•	Client Secret

Esses dados serão usados para gerar os tokens.
⸻

🔐 2. Gerando o Access Token e Refresh Token (via CURL)

Após autorizar a aplicação, o Mercado Livre fornece um code na URL.

Use o comando abaixo para trocar o code pelos tokens:
curl -X POST: "https://api.mercadolibre.com/oauth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code" \
  -d "client_id=SEU_APP_ID" \
  -d "client_secret=SEU_CLIENT_SECRET" \
  -d "code=SEU_CODE" \
  -d "redirect_uri=SUA_REDIRECT_URI"
  
Será retornado:
	•	access_token
	•	refresh_token
	•	expires_in

Salve isso no arquivo dados.json
{
    "client_id": "xxxxxxxxxxxxxxxxx",
    "client_secret": "yyyyyyyyyyyyyyyyyy",
    "user_id": "zzzzzzzzzzzzzzz",
    "access_token": "APP_USR-XXXXXXXXXXXXXX",
    "refresh_token": "TG-YYYYYYYYYYYYYY"
}
⸻

🔄 3. Atualização automática de tokens

Quando o access token expira, o script usa o refresh token:

curl -X POST: "https://api.mercadolibre.com/oauth/token" \
  -H 'Accept: application/json' \
  -d "grant_type=refresh_token" \
  -d "client_id=..." \
  -d "client_secret=..." \
  -d "refresh_token=..."

O código já faz isso sozinho.

⸻

📥 4. Consulta das vendas do dia

O script usa:
GET /orders/search?seller=SEU_ID&order.date_created.from=...

ada venda retorna dados como:
	•	comprador
	•	produtos
	•	sale_fee
	•	status
	•	date_created
	•	ordem de envio (se existir)

⸻

💳 5. Consulta dos pagamentos

Para cada venda:
De lá pegamos:
	•	valor pago pelo cliente
	•	valor recebido pelo seller

⸻

📦 6. Cálculo das taxas

O código calcula automaticamente:
	•	Tarifa de venda (sale_fee)
	•	Tarifa de envio (shipping fee) quando disponível
	•	Total líquido
	•	Margem de lucro

⸻

📊 7. Exportação para Excel

Cada venda é registrada com:
	•	ID
	•	Comprador
	•	Produto
	•	Quantidade
	•	Valor do produto
	•	Tarifas
	•	Total líquido
	•	Margem
	•	Data

Isso facilita muito o controle para quem usa Excel no dia a dia.

⸻

▶ 8. Como executar
	1.	Instale as dependências:
  -pip install -r requirements.txt

  2.	Adicione suas credenciais no dados.json.
	3.	Execute: python search_orderML.py

✔ 9. Melhorias futuras
	•	Dashboard em Power BI
	•	Integração com Google Sheets
	•	Inclusão das etiquetas de envio
	•	Inserção de cálculo real da tarifa do Mercado Envios (quando liberado pela API)




