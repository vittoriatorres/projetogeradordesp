import streamlit as st
import io
import os
import re
import datetime
import tempfile
from utils.pdf_generator import create_dispatch_pdf, merge_pdfs

st.set_page_config(page_title="Gerador de Despachos",
                   page_icon="📝",
                   layout="centered")

st.title("Gerador de Despachos")


# Function to sanitize filename
def sanitize_filename(filename):
    # Replace prohibited characters with periods
    sanitized = re.sub(r'[\\/*?:"<>|]', ".", filename)
    return sanitized


# Function to download PDF
def get_download_link(pdf_bytes, filename):
    b64_pdf = io.BytesIO(pdf_bytes)
    return b64_pdf


# Main form
with st.form("despacho_form"):
    st.subheader("Informações do Despacho")

    # Tipo de despacho
    tipo_despacho = st.selectbox(
        "Escolha o tipo de despacho:",
        ["Atualização de Base", "Imóvel Não Localizado", "Customizado"])

    # Informações comuns a todos os despachos
    numero_processo = st.text_input("Número do Processo")
    setor_destino = st.text_input("Setor de Destino")
    nome_usuario = st.text_input("Nome do Usuário")
    matricula_usuario = st.text_input("Matrícula do Usuário")

    # Campos específicos para cada tipo de despacho
    if tipo_despacho == "Atualização de Base":
        inscricao_tecnica = st.text_input("Inscrição Técnica")

    elif tipo_despacho == "Imóvel Não Localizado":
        tipo_logradouro = st.text_input("Tipo do Logradouro")
        logradouro = st.text_input("Logradouro")
        numero_porta = st.text_input("Número de Porta")
        complemento = st.text_input("Complemento")
        bairro = st.text_input("Bairro")

    elif tipo_despacho == "Customizado":
        texto_customizado = st.text_area("Texto Customizado", height=200)

    # Upload de documentos
    uploaded_files = st.file_uploader("Anexar documentos (opcional)",
                                      accept_multiple_files=True,
                                      type=["pdf"])

    submit_button = st.form_submit_button("Gerar Despacho")

# Processar o formulário quando enviado
if submit_button:
    # Verificar campos obrigatórios
    required_fields = [
        numero_processo, setor_destino, nome_usuario, matricula_usuario
    ]

    if tipo_despacho == "Atualização de Base":
        required_fields.append(inscricao_tecnica)
    elif tipo_despacho == "Imóvel Não Localizado":
        required_fields.extend(
            [tipo_logradouro, logradouro, numero_porta, bairro])
    elif tipo_despacho == "Customizado":
        required_fields.append(texto_customizado)

    if all(required_fields):
        try:
            # Data atual formatada
            data_atual = datetime.datetime.now().strftime("%d/%m/%Y")

            # Preparar o texto de acordo com o tipo de despacho
            if tipo_despacho == "Atualização de Base":
                texto_despacho = f"""Processo n°: {numero_processo}

{setor_destino},

Em retorno à Secretaria de origem. Base atualizada no Sistema SiGEO como técnica: {inscricao_tecnica}, de acordo com documentos e informações juntadas neste processo.
Para consultas de georreferenciamento acessar: https://www.sigeo.niteroi.rj.gov.br/pages/geoportal, clicar em portal do servidor >> Geoportal Privado >> acessar SSO.

SEREC, {data_atual}
{nome_usuario}
Matrícula {matricula_usuario}"""

            elif tipo_despacho == "Imóvel Não Localizado":
                texto_despacho = f"""Processo n°: {numero_processo}

{setor_destino},

Informo que, após pesquisas, não foi possível localizar a matrícula de IPTU referente ao imóvel situado à {tipo_logradouro} {logradouro}, n.º {numero_porta}, {complemento}, bairro {bairro}, visto que não existe essa numeração em nosso cadastro.
Para que possamos atender, solicito que seja enviada a localização do imóvel, a qual pode ser feita através de uma imagem do Google Maps com o imóvel hachurado/circulado, juntamente com sua foto de fachada e, se possível, suas coordenadas geográficas.

SEREC, {data_atual}
{nome_usuario}
Matrícula {matricula_usuario}"""

            elif tipo_despacho == "Customizado":
                texto_despacho = f"""Processo n°: {numero_processo}

{setor_destino},

{texto_customizado}

SEREC, {data_atual}
{nome_usuario}
Matrícula {matricula_usuario}"""

            # Criar PDF do despacho
            despacho_pdf = create_dispatch_pdf(texto_despacho)

            # Nome do arquivo final
            filename = f"{sanitize_filename(numero_processo)}_desp.pdf"

            # Se não houver documentos anexados, o despacho é o documento final
            if not uploaded_files:
                final_pdf = despacho_pdf
                st.success("Despacho gerado com sucesso!")
            else:
                # Se houver documentos anexados, mesclar com o despacho
                temp_files = []

                try:
                    # Salvar os arquivos carregados em arquivos temporários
                    for uploaded_file in uploaded_files:
                        temp_file = tempfile.NamedTemporaryFile(delete=False,
                                                                suffix='.pdf')
                        temp_file.write(uploaded_file.read())
                        temp_file.close()
                        temp_files.append(temp_file.name)

                    # Mesclar PDFs, colocando o despacho como a última folha
                    final_pdf = merge_pdfs(temp_files, despacho_pdf)
                    st.success(
                        "Despacho gerado e mesclado com os documentos anexados com sucesso!"
                    )

                finally:
                    # Limpar arquivos temporários
                    for temp_file in temp_files:
                        try:
                            os.unlink(temp_file)
                        except:
                            pass

            # Criar botão de download
            download_buffer = get_download_link(final_pdf, filename)
            st.download_button(label="Baixar Despacho",
                               data=download_buffer,
                               file_name=filename,
                               mime="application/pdf")

        except Exception as e:
            st.error(f"Erro ao gerar o despacho: {str(e)}")
    else:
        st.warning("Por favor, preencha todos os campos obrigatórios.")

st.markdown("---")
st.caption(
    "SEREC | Secretaria da Fazenda de Niterói\nElaborado por Vittoria Torres Silva"
)
