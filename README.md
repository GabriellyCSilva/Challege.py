# Challege.py
Este projeto é um sistema automatizado que escuta a voz do médico, transforma a fala em texto, usa a API da OpenAI para gerar uma receita médica, cria um PDF e envia por e-mail para o paciente.

📚 Funcionalidades

Escuta a voz do médico via microfone

Converte a fala em texto com Speech Recognition

Gera a receita com a IA do ChatGPT (OpenAI API)

Cria um PDF com as informações da receita

Envia o PDF por e-mail para o paciente

📁 Estrutura do Projeto

ReceitaMedica/
├── main.py

⚙️ Bibliotecas utilizadas

speech_recognition: converte voz em texto

openai: usa a API do ChatGPT para gerar a receita

fpdf: gera o PDF

smtplib, email: para envio de e-mails com anexo

os, mimetypes: manipula arquivos e caminhos

📆 Como funciona o sistema (explicação por partes)

1. Importações

Importa todas as bibliotecas necessárias para fala, IA, PDF, envio de e-mail, etc.

2. Chave da OpenAI

Configura a chave da API para acessar o ChatGPT.

3. ouvir_medico()

Escuta o que o médico fala e converte para texto usando o microfone e o Google.

4. gerar_receita(transcricao)

Envia o texto da fala para a IA e retorna uma receita formatada.

5. gerar_pdf_receita(texto_receita, nome_paciente)

Gera um PDF com o nome do paciente e a receita médica gerada.

6. enviar_email(destinatario, caminho_pdf, nome_paciente)

Envia o PDF como anexo para o e-mail do paciente.

7. sistema_prescricao()

Menu principal com 3 opções:

Criar nova receita

Ver receitas anteriores

Sair

🚀 Como executar

Instale as dependências:

pip install speechrecognition openai fpdf

Rode o sistema:

python main.py

🚨 Observação importante

A biblioteca speech_recognition depende do PyAudio para funcionar. Se estiver com problemas de instalação no Windows, considere substituir por outra biblioteca de captura de áudio (ex: sounddevice).
