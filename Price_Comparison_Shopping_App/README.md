# Comparador de Preços para Compras de Clientes

App em Flask para ajudar quem faz compras por encomenda: o cliente manda uma
foto e/ou descrição do produto, o app busca em vários sites e mostra onde
está mais barato, com o link direto para comprar.

## Como funciona

1. Você (ou o cliente) envia uma foto do produto e/ou uma descrição em texto.
2. Se houver uma foto e a variável `ANTHROPIC_API_KEY` estiver configurada, o
   app usa a Claude Vision para descrever o produto automaticamente (marca,
   modelo, características) e monta um termo de busca.
3. O termo de busca é consultado em paralelo em:
   - **Mercado Livre** — via [API pública oficial](https://api.mercadolibre.com/sites/MLB/search),
     estável e sem necessidade de chave de API.
   - **Amazon** e **Magazine Luiza** — via *web scraping* best-effort da
     página de busca (veja limitações abaixo).
4. Os resultados são ordenados por preço; o mais barato é destacado no topo.
   Se um site não retornar preços, o app ainda mostra um link de busca
   manual para aquele site, em vez de simplesmente omiti-lo.

## Rodando localmente

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # opcional, para habilitar a leitura de imagens
python run.py
```

Acesse http://127.0.0.1:5000.

## Testes

```bash
source .venv/bin/activate
pip install pytest
python -m pytest
```

Os testes usam respostas mockadas (não fazem chamadas de rede reais).

## Limitações importantes (leia antes de confiar 100% no app)

- **Amazon e Magazine Luiza usam scraping de HTML**, não uma API oficial.
  Isso é inerentemente frágil:
  - Os sites mudam o layout com frequência, o que pode quebrar o parsing
    a qualquer momento (os seletores usados estão comentados no código de
    cada scraper).
  - Alguns sites (a Magazine Luiza, em especial) renderizam os resultados
    via JavaScript no navegador — uma requisição HTTP simples pode não
    trazer nenhum produto. Para resolver isso de forma confiável seria
    necessário um navegador headless (Playwright/Selenium), o que não foi
    implementado aqui por simplicidade.
  - Fazer scraping pode estar em desacordo com os Termos de Uso desses
    sites. Para uso comercial contínuo e mais robusto, o recomendado é
    contratar uma API paga de comparação de preços (ex: SerpApi Google
    Shopping, ou a Amazon Product Advertising API oficial) — trocar isso
    é só substituir o conteúdo de `app/scrapers/amazon.py` e
    `app/scrapers/magazine_luiza.py`, a interface (`search(query) -> List[ProductResult]`)
    continua igual.
  - Quando o scraping falha ou não encontra nada, o app sempre devolve um
    link de busca manual para aquele site — o cliente nunca fica sem opção.
- **A leitura automática de imagem é opcional** e depende de uma chave da
  Anthropic (`ANTHROPIC_API_KEY`). Sem ela, o app pede uma descrição em
  texto do produto.
- Este projeto foi desenvolvido em um ambiente sandbox sem acesso à
  internet externa, então as chamadas reais ao Mercado Livre/Amazon/
  Magazine Luiza não puderam ser testadas ao vivo durante o
  desenvolvimento — apenas o fallback (quando a rede falha) foi validado
  de ponta a ponta. Ao rodar no seu computador com internet normal, teste
  uma busca real e ajuste os seletores de HTML em `amazon.py` /
  `magazine_luiza.py` se algum deles não estiver trazendo preços.

## Estrutura

```
app/
  config.py            # configuração via variáveis de ambiente
  scrapers/
    base.py             # ProductResult, parsing de preço em R$, fallback
    mercado_livre.py     # via API pública oficial
    amazon.py            # scraping best-effort
    magazine_luiza.py    # scraping best-effort
  services/
    search.py            # agrega e ordena resultados dos scrapers
    vision.py             # descrição de imagem via Claude (opcional)
  templates/, static/     # interface web
tests/                     # testes com respostas mockadas
```

## Próximos passos sugeridos

- Trocar Amazon/Magazine Luiza por uma API paga de comparação de preços
  para maior confiabilidade e conformidade legal.
- Adicionar mais lojas (Shopee, Americanas, etc.) seguindo o mesmo padrão
  de `search(query) -> List[ProductResult]`.
- Guardar um histórico de buscas por cliente (ex: SQLite) se for útil pro
  seu fluxo de trabalho.
