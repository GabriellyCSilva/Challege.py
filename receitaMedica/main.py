
#Importações das bibliotecas
import speech_recognition as sr #escuta e converte voz em texto
import openai #conecta com a API da OpenAI (ChatGPT)
from fpdf import FPDF #cria arquivos PDF
import os #mexe com arquivos e caminhos no sistema
import smtplib #envia e-mails
from email.message import EmailMessage #cria mensagens de e-mail com anexo
import mimetypes #identifica o tipo de arquivo (PDF, imagem, etc.)

#chave para poder usar o chat gpt no codigo
openai.api_key = ""

#Função para escutar o médico
def ouvir_medico():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
#Cria o objeto que vai reconhecer a fala (recognizer) e usa o microfone como fonte
    with mic as source:
        print("\n[INFO] Ajustando ruído...")
        recognizer.adjust_for_ambient_noise(source)
        print("[INFO] Pode falar a prescrição agora:")
        audio = recognizer.listen(source)
#ajusta para o ruído do ambiente e escuta o que o médico fala
    try:
        texto = recognizer.recognize_google(audio, language="pt-BR")
        print(f"\n[TRANSCRIÇÃO] Você disse: {texto}")
        return texto
    except sr.UnknownValueError:  #Tenta converter a fala em texto usando o Google // Retorna a transcrição da fala
        print("[ERRO] Não entendi o que você falou.")
        return ""
    except sr.RequestError as e:
        print(f"[ERRO] Problema no serviço de reconhecimento: {e}")
        return ""


#Função gera a receita com IA
def gerar_receita(transcricao):
    if transcricao == "":
        return "[AVISO] Nenhuma informação foi fornecida."  #Se não tiver texto (fala vazia), avisa
#Monta a mensagem (prompt) que será enviada ao ChatGPT
    prompt = f"""
    Organize uma receita médica de forma estruturada, com base nessa transcrição do médico:

    "{transcricao}"

    O resultado deve conter o nome do medicamento, a posologia e a frequência, caso haja.
    """
#Envia o prompt para a OpenAI e recebe uma resposta
    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente que escreve receitas médicas."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=300
    )

    receita_formatada = resposta['choices'][0]['message']['content'] #Extrai a resposta formatada e retorna
    return receita_formatada 


#Função gerar pdf da receita
def gerar_pdf_receita(texto_receita, nome_paciente):
#Cria um novo arquivo PDF e adiciona uma página
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
#Adiciona o título "Receita Médica" e o nome do paciente
    pdf.cell(200, 10, txt="Receita Médica", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Paciente: {nome_paciente}", ln=True, align='L')
    pdf.ln(10)
#Quebra a receita em linhas e escreve cada uma no PDF
    for linha in texto_receita.split('\n'):
        pdf.multi_cell(0, 10, linha)
#Salva o PDF na mesma pasta do projeto
    nome_arquivo = f"receita_{nome_paciente.replace(' ', '_')}.pdf"
    caminho_arquivo = os.path.join(os.getcwd(), nome_arquivo)
    pdf.output(caminho_arquivo)
#Informa o nome do arquivo e retorna o caminho
    print(f"\n✅ PDF gerado com sucesso: {caminho_arquivo}")
    return caminho_arquivo

#Enviar a receita (PDF) por e-mail
def enviar_email(destinatario, caminho_pdf, nome_paciente):
#Define o e-mail de origem e a senha do app (do Gmail com verificação em 2 etapas)
    remetente = 'gabriellycasilva@gmail.com'
    senha = ''
#Cria a estrutura do e-mail (assunto, remetente, destinatário)
    mensagem = EmailMessage()
    mensagem['Subject'] = f'Receita Médica - {nome_paciente}'
    mensagem['From'] = remetente
    mensagem['To'] = destinatario
#Escreve o conteúdo da mensagem
    mensagem.set_content(f'Olá, {nome_paciente}!\n\nSegue em anexo sua receita médica.\n\nAtenciosamente,\nHospital XPTO')
#Lê o PDF e anexa no e-mail
    with open(caminho_pdf, 'rb') as arquivo:
        tipo_mime, _ = mimetypes.guess_type(caminho_pdf)
        mime_tipo, mime_subtipo = tipo_mime.split('/')
        mensagem.add_attachment(arquivo.read(), maintype=mime_tipo, subtype=mime_subtipo, filename=os.path.basename(caminho_pdf))
#Tenta enviar usando o servidor do Gmail
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(remetente, senha)
            smtp.send_message(mensagem)
        print(f'\n✅ E-mail enviado com sucesso para {destinatario}!')
    except Exception as e:
        print(f'\n❌ Falha ao enviar e-mail: {e}')

#Menu principal do sistema (chama as funções e executa)
def sistema_prescricao():
    lista_receitas = [] #Começa o sistema e cria uma lista pra armazenar o histórico

    while True: #Mostra o menu e pede uma opção
        print("\n======= SISTEMA DE PRESCRIÇÃO =======")
        print("1 - Criar nova receita")
        print("2 - Ver receitas anteriores")
        print("3 - Sair")

        opcao = input("Escolha uma opção: ")
        #Coleta nome, e-mail, escuta a voz e gera a receita com a IA
        if opcao == "1":
            nome_paciente = input("Digite o nome do paciente: ")
            email_paciente = input("Digite o e-mail do paciente: ")

            transcricao = ouvir_medico()
            receita = gerar_receita(transcricao)
            #Adiciona ao histórico
            lista_receitas.append({
                "paciente": nome_paciente,
                "receita": receita
            })
            #Mostra a receita, gera o PDF e envia por e-mail
            print("\n===== RECEITA GERADA =====")
            print(receita)

            caminho_pdf = gerar_pdf_receita(receita, nome_paciente)
            enviar_email(email_paciente, caminho_pdf, nome_paciente)
        #Exibe todas as receitas já criadas
        elif opcao == "2":
            print("\n===== HISTÓRICO DE RECEITAS =====")
            if len(lista_receitas) == 0:
                print("Nenhuma receita foi criada ainda.")
            else:
                for idx, item in enumerate(lista_receitas):
                    print(f"\nReceita {idx + 1} - Paciente: {item['paciente']}")
                    print(item['receita'])
        #Encerra o programa
        elif opcao == "3":
            print("\nSaindo do sistema... Até logo!")
            break
        #Trata erro se digitar algo diferente de 1, 2 ou 3
        else:
            print("\n[ERRO] Opção inválida! Tente novamente.")


sistema_prescricao() #inicia o sistema chamando a função

