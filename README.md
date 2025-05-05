# Gerador de Despacho

#### 📄 Descrição
Gerar despachos administrativos em PDF com base em informações inseridas pelo usuário. Também permite o anexo de documentos PDF, que são mesclados ao despacho final em um único arquivo consolidado.

#### 🎯 Objetivo 
Facilitar e padronizar a criação de despachos administrativos, otimizando o tempo e garantindo uniformidade nos documentos.

### 🔧 Dependências
- Python 3.11

- Streamlit 1.44.1

- PyPDF2 3.0.1

- ReportLab 4.3.1

- E outras listadas em `requirements.txt` ou `pyproject.toml.`

### 📂 Estrutura do Projeto

```
├── app.py                       # Arquivo principal para rodar o Streamlit
├── assets
│   └── niteroi_cabecalho.jpg    # Imagem utilizada no cabeçalho do despacho
├── pyproject.toml               # Arquivo de configuração do Poetry (se utilizado)
├── render.yaml                  # Configuração de deploy no Render
├── requirements.txt             # Dependências do projeto
└── utils
    └── pdf_generator.py         # Funções auxiliares para geração e manipulação de PDFs
```

### 🚀 Deploy no Render

1. Acesse [Render.com](https://render.com/) e crie uma conta (se ainda não tiver).
2. Após o login, clique em "New +" e escolha **Web Service**.
3. Conecte sua conta do GitHub (ou GitLab/Bitbucket) ao Render.
4. Escolha o repositório do seu projeto **Gerador de Despachos**.
5. Configurar o Serviço de Web

- **Nome do Serviço**: Escolha um nome para o seu serviço (ex: `gerador-despachos`).
- **Branch**: Selecione o branch principal (normalmente `main`).
- **Build Command**:
  ```
  pip install -r requirements.txt
  ```
  - **Start Command:**
  ```
  streamlit run app.py
  ```

### 🛠️ Uso
1. Escolha o tipo de despacho;
- Atualização de Base
- Imóvel Não Localizado
- Customizado

2. Preencha os campos obrigatórios;

3. (Opcional) Anexe arquivos PDF adicionais;

4. Clique em "Gerar Despacho" e faça o download do PDF final (anexos + despacho).

### 👩‍💻 Autoria

Desenvolvido por **Vittoria Torres Silva**