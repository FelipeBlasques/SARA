# Smart Automated Receive Application (SARA)

**SARA** é um aplicativo automatizado de recebimento de e-mails que permite verificar automaticamente os e-mails de uma caixa de entrada e exibi-los em uma interface gráfica. Ele também possui funcionalidade de log e atualização periódica.

## Sumário

1. [Pré-requisitos](#pré-requisitos)
2. [Instalação](#instalação)
3. [Uso](#uso)
4. [Estrutura do Projeto](#estrutura-do-projeto)
5. [Configuração Inicial](#configuração-inicial)
6. [Executável](#executável)
7. [Contribuindo](#contribuindo)

## Pré-requisitos

- **Python 3.8+**: Certifique-se de ter o Python instalado. Você pode baixá-lo [aqui](https://www.python.org/downloads/).
- **Pacotes Python**: As bibliotecas necessárias podem ser instaladas usando o `pip`.

## Instalação

1. Clone o repositório:
   ```
   git clone https://github.com/seu_usuario/seu_repositorio.git
   cd seu_repositorio
   ```
   
2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

   O arquivo requirements.txt deve conter as bibliotecas necessárias:

   ```
   imaplib
   keyring
   html2text
   pyinstaller
   ```

3. Execute o aplicativo:
   ```
   python script/main.py
   ```
   
## Uso
1. O aplicativo permite que você verifique seus e-mails de uma conta predefinida.
2. A interface gráfica exibe a lista de e-mails não lidos, e você pode clicar para visualizar o conteúdo.
3. O log do aplicativo é exibido na interface e atualizado automaticamente.


## Estrutura do Projeto
```
/meu_app
    ├── script
    │    ├── main.py         # Arquivo principal que inicia o aplicativo
    │    ├── email_handler.py # Funções para verificar e processar e-mails
    │    ├── gui.py           # Interface gráfica do aplicativo
    │    ├── logger.py        # Funções de log do aplicativo
    │    └── config.py        # Configurações, incluindo detalhes do e-mail
    ├── .gitignore            # Arquivos e pastas ignorados pelo Git
    ├── README.md             # Documentação do projeto
    └── requirements.txt      # Dependências do projeto
```

## Configuração Inicial
O arquivo config.py contém detalhes de configuração, como o servidor IMAP e o e-mail do usuário:
```
imap_server = "imap.gmail.com"
email_user = "seu_email@gmail.com"
email_destinatario = "seu_email@gmail.com"
```
O keyring é usado para armazenar a senha de e-mail de forma segura. Configure a senha com:
```
keyring.set_password("email", "seu_email@gmail.com", "sua_senha")
```
## Executável
Se você deseja criar um executável do aplicativo, siga os seguintes passos:

Instale o PyInstaller:

```
pip install pyinstaller
```
Gere o executável:

```
pyinstaller --onefile --windowed script/main.py
```
O executável será gerado na pasta dist/.

## Contribuindo
Contribuições são bem-vindas! Se você encontrar problemas ou quiser adicionar melhorias, sinta-se à vontade para abrir uma issue ou enviar um pull request.
