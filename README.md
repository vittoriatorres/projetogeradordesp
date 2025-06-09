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
PROJETOGERADORDESP/
├── .streamlit/
│   └── config.toml
├── assets/
│   └── niteroi_cabecalho.jpg
├── utils/
│   └── pdf_generator.py
├── .gitignore
├── app.py
├── Dockerfile
├── pyproject.toml
├── README.md
├── requirements.txt
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