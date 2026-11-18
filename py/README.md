# 📁 Upload & Download API

API REST desenvolvida em **Flask** para upload e download de arquivos, pronta para deploy em produção no **Render**.

---

## 📋 Descrição

Esta API permite que clientes enviem arquivos via HTTP (`multipart/form-data`) e os recuperem pelo nome. Os metadados dos arquivos são persistidos em um banco de dados SQLite e os arquivos físicos são armazenados na pasta `uploads/`.

---

## 🗂️ Estrutura de Pastas

```
upload+download/
├── app.py                          # Ponto de entrada da aplicação Flask
├── Procfile                        # Comando de inicialização para o Render/Gunicorn
├── requirements.txt                # Dependências do projeto
├── .gitignore                      # Arquivos ignorados pelo Git
├── README.md                       # Esta documentação
│
├── database/
│   └── db.py                       # Conexão e inicialização do banco SQLite
│
├── models/
│   ├── upload_model.py             # Operações de escrita no banco (save, find)
│   └── download_model.py           # Operações de leitura no banco (find)
│
├── controllers/
│   ├── upload_controller.py        # Lógica de negócio para upload
│   └── download_controller.py      # Lógica de negócio para download
│
├── routes/
│   ├── upload_route.py             # Blueprint e rotas de upload
│   └── download_route.py           # Blueprint e rotas de download
│
└── uploads/                        # Pasta gerada automaticamente para armazenar arquivos
```

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia      | Versão   | Descrição                                      |
|-----------------|----------|------------------------------------------------|
| Python          | 3.14+    | Linguagem base                                 |
| Flask           | 3.1.3    | Framework web WSGI                             |
| Flask-CORS      | 5.0.1    | Suporte a Cross-Origin Resource Sharing (CORS) |
| Werkzeug        | 3.1.9    | Utilitários WSGI (usado pelo Flask)            |
| Gunicorn        | 23.0.0   | Servidor WSGI para produção                    |
| SQLite          | built-in | Banco de dados leve via módulo `sqlite3`       |

---

## ⚙️ Instalação e Execução Local

### Pré-requisitos

- Python 3.10 ou superior
- `pip` atualizado

### Passo a passo

**1. Clone o repositório**

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd upload+download
```

**2. Crie e ative o ambiente virtual**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

**3. Instale as dependências**

```bash
pip install -r requirements.txt
```

**4. Execute a aplicação**

```bash
# Modo simples (desenvolvimento)
python app.py

# Modo produção com Gunicorn (Linux/macOS)
gunicorn app:app --bind 0.0.0.0:5000
```

A API estará disponível em: `http://localhost:5000`

---

## 🔌 Endpoints da API

### 📤 Upload de Arquivo

| Campo          | Valor                              |
|----------------|------------------------------------|
| **Método**     | `POST`                             |
| **URL**        | `/uploads/upload`                  |
| **Formato**    | `multipart/form-data`              |
| **Campo**      | `file` — o arquivo a ser enviado   |

**Tipos de arquivo permitidos:** `png`, `jpg`, `jpeg`, `gif`, `pdf`, `txt`

**Tamanho máximo:** 30 KB

**Exemplo com `curl`:**

```bash
curl -X POST http://localhost:5000/uploads/upload \
  -F "file=@/caminho/para/seu/arquivo.pdf"
```

**Resposta de sucesso (`200 OK`):**

```json
{
  "mensagem": "Arquivo salvo com sucesso!",
  "arquivo": "documento.pdf"
}
```

**Respostas de erro:**

```json
// 400 — Nenhum arquivo enviado
{ "erro": "Nenhum arquivo enviado" }

// 400 — Nome vazio
{ "erro": "Nome do arquivo vazio" }

// 400 — Arquivo muito grande
{ "erro": "Arquivo excede o tamanho máximo permitido (30 KB)" }

// 400 — Extensão não permitida
{
  "erro": "Tipo de arquivo não permitido!",
  "tipos_permitidos": ["png", "jpg", "jpeg", "gif", "pdf", "txt"]
}
```

---

### 📥 Download de Arquivo

| Campo          | Valor                                      |
|----------------|--------------------------------------------|
| **Método**     | `GET`                                      |
| **URL**        | `/downloads/download/<filename>`           |
| **Parâmetro**  | `filename` (na URL) — nome exato do arquivo|

**Exemplo com `curl`:**

```bash
curl -OJ http://localhost:5000/downloads/download/documento.pdf
```

**Resposta de sucesso (`200 OK`):**
O arquivo é retornado diretamente como download (`Content-Disposition: attachment`).

**Resposta de erro:**

```json
// 404 — Arquivo não encontrado
{ "erro": "Arquivo não encontrado" }
```

---

## 🚀 Deploy no Render

### Variáveis de ambiente

Nenhuma variável é obrigatória. O Render injeta `PORT` automaticamente e a aplicação já a lê.

> **Atenção:** O Render usa um **filesystem efêmero**. Os arquivos enviados para a pasta `uploads/` são perdidos a cada novo deploy. Para persistência real em produção, integre um serviço de armazenamento externo como **AWS S3**, **Cloudflare R2** ou **Supabase Storage**.

### Passos para deploy

1. Faça o push do projeto para um repositório GitHub
2. Acesse [render.com](https://render.com) e crie um novo **Web Service**
3. Conecte o repositório
4. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Environment:** `Python 3`
5. Clique em **Deploy**

---

## 🌐 Link da API em Produção

```
https://seu-servico.onrender.com
```

> Substitua pela URL gerada pelo Render após o deploy.

**Endpoints em produção:**

```
POST https://seu-servico.onrender.com/uploads/upload
GET  https://seu-servico.onrender.com/downloads/download/<filename>
```

---

## 📝 Logs

A aplicação gera o arquivo `uploads.log` na raiz do projeto com registros de cada operação de upload (sucesso e falha), incluindo o IP do cliente e o timestamp.

---

## 📄 Licença

Este projeto está sob a licença MIT.

