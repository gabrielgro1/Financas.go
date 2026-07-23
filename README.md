# Financas API

API REST para controle financeiro pessoal, criada como um projeto de aprendizado com uma organizacao proxima de um projeto profissional em Flask.

A ideia deste projeto foi construir uma API real aos poucos, entendendo cada decisao: ambiente virtual, instalacao de pacotes, rotas HTTP, JSON, validacao, PostgreSQL, organizacao em camadas, autenticacao com token e tratamento de erros.

## O que a API faz  

- Cadastro de usuarios com senha protegida por hash.
- Login com retorno de token JWT.
- Cadastro e listagem de categorias por usuario autenticado.
- CRUD de transacoes por usuario autenticado.
- Resumo financeiro com receitas, despesas e saldo.
- Validacoes de entrada antes de gravar no banco.
- Tratamento de erros de banco e conexao.

## Aprendizados aplicados.

- Criacao e uso de `venv`.
- Instalacao de dependencias com `pip`.
- Conceito de API REST.
- Metodos HTTP: `GET`, `POST`, `PUT` e `DELETE`.
- Codigos de status: `200`, `201`, `400`, `401`, `404`, `500` e `503`.
- Envio e recebimento de JSON.
- Testes manuais com `curl`.
- Variaveis de ambiente com `.env`.
- Conexao com PostgreSQL usando `psycopg2`.
- Migrations SQL para criar tabelas.
- Relacionamentos com `REFERENCES`.
- Organizacao em camadas: routes, services, repositories e validators.
- Hash de senha com Werkzeug.
- Autenticacao com JWT.
- Protecao de rotas com decorator.
- Uso de `.gitignore` para nao publicar dados locais ou segredos.

## Estrutura

```txt
app/
  routes/          # Entrada HTTP da API
  services/        # Regras de negocio
  repositories/    # Acesso ao banco de dados
  validators/      # Validacao dos dados de entrada
  database.py      # Conexao com PostgreSQL
  errors.py        # Tratamento global de erros
  security.py      # JWT e protecao de rotas
migrations/
  001_create_tables.sql
main.py
requirements.txt
```

## Variaveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/financas
SECRET_KEY=troque_essa_chave
PORT=8000
DEBUG=0
```



## Como rodar localmente

Ative o ambiente virtual:

```bash
source venv/bin/activate
```

Instale as dependencias:

```bash
pip install -r requirements.txt
```

Execute a migration no PostgreSQL:

```bash
psql -U financas_user -d financas -f migrations/001_create_tables.sql
```

Inicie a API:

```bash
python main.py
```

A API ficara disponivel em:

```txt
http://127.0.0.1:8000
```

## Rotas principais

### Usuarios

```http
POST /usuarios
```

Cria um usuario:

```json
{
  "nome": "Gabriel",
  "email": "gabriel@email.com",
  "senha": "123456"
}
```

### Login

```http
POST /login
```

Retorna um token JWT:

```json
{
  "email": "gabriel@email.com",
  "senha": "123456"
}
```

### Categorias

Rotas protegidas por token:

```http
GET /categorias
POST /categorias
```

Exemplo:

```bash
curl -X POST "http://127.0.0.1:8000/categorias" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN" \
  -d '{"nome":"Mercado"}'
```

### Transacoes

Rotas protegidas por token:

```http
GET /transacoes
POST /transacoes
GET /transacoes/<id>
PUT /transacoes/<id>
DELETE /transacoes/<id>
```

Exemplo:

```bash
curl -X POST "http://127.0.0.1:8000/transacoes" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN" \
  -d '{"tipo":"despesa","valor":50.90,"descricao":"Mercado","categoria_id":1}'
```

### Resumo

```http
GET /resumo
```

Retorna:

```json
{
  "total_receitas": 0.0,
  "total_despesas": 50.9,
  "saldo": -50.9
}
```

## Status do projeto

Este projeto esta em fase de MVP. A base principal esta funcionando: usuario, login, categorias, transacoes e resumo financeiro autenticado.

Proximos passos possiveis:

- Testes automatizados.
- Paginar listagem de transacoes.
- Melhorar filtros por data.
- Criar atualizacao e remocao de categorias.
- Preparar deploy em ambiente externo.
