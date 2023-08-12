import logging
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from secret_access import SLACK_APP_TOKEN, SLACK_BOT_TOKEN
from refatorador import process_code, process_message, info

app = App(token=SLACK_BOT_TOKEN, name="neon-gpt")
logger = logging.getLogger(__name__)

@app.message(r"@hibot")
def start_conversation(message, say):
    user_id = message['user']
    info[user_id] = {'type': 'random', 'thread': message['ts']}
    say("Olá, Como posso ajudar?", thread_ts=message['ts'])

@app.message(r"@code-security")
def ask_security_questions(message, say):
    user_id = message['user']
    info[user_id] = {'type': 'security', 'thread': message['ts']}
    say("Qual é o nome da vulnerabilidade encontrada?", thread_ts=message['ts'])

@app.message(r"@code-refactor")
def ask_security_questions(message, say):
    user_id = message['user']
    info[user_id] = {'type': 'refactor', 'thread': message['ts']}
    say("Qual a linguagem utilizada?", thread_ts=message['ts'])

@app.message("")
def handle_message(message, say):
    user_id = message['user']

    if user_id in info:
        if 'type' in info[user_id]:
            if info[user_id]['type'] == 'random':
                say("Aguarde, estamos processando sua mensagem!", thread_ts=message['ts'])
                process_message(message, say) # Chama a função correta
            elif info[user_id]['type'] == 'security':
                process_security(message, say)
            elif info[user_id]['type'] == 'refactor':
                process_refactor(message, say)

def process_security(message, say):
    user_id = message['user']
    thread_ts = info[user_id]['thread']

    if 'vulnerability' not in info[user_id]:
        info[user_id]['vulnerability'] = message['text']
        say("Qual é a linguagem do código utilizada?", thread_ts=message['ts'])
    elif 'language' not in info[user_id]:
        info[user_id]['language'] = message['text']
        say("Qual é o código?", thread_ts=thread_ts)
    elif 'code' not in info[user_id]:
        info[user_id]['code'] = message['text']
        say("Aguarde, estamos processando sua mensagem!", thread_ts=thread_ts)
        process_code(message, say, 'security')
    elif 'satisfied' in info[user_id]:
        if message['text'].lower() in ['não', 'nao', 'no']:
            say("Por favor, Qual a alteração desejada?", thread_ts=thread_ts)
            del info[user_id]['satisfied']
        elif message['text'].lower() in ['sim', 'yes']:
            del info[user_id]
            say("Obrigado!", thread_ts=thread_ts)
    else:
        info[user_id]['alteration'] = message['text']
        info[user_id]['satisfied'] = False
        say("Aguarde, estamos processando sua mensagem!", thread_ts=message['ts'])
        process_code(message, say, 'security')

def process_refactor(message, say):
    user_id = message['user']
    thread_ts = info[user_id]['thread']

    if 'language' not in info[user_id]:
        info[user_id]['language'] = message['text']
        say("Qual é o código?", thread_ts=thread_ts)
    elif 'code' not in info[user_id]:
        info[user_id]['code'] = message['text']
        say("Aguarde, estamos processando sua mensagem!", thread_ts=thread_ts)
        process_code(message, say, 'refactor')
    elif 'satisfied' in info[user_id]:
        if message['text'].lower() in ['não', 'nao', 'no']:
            say("Por favor, Qual a alteração desejada?", thread_ts=thread_ts)
            del info[user_id]['satisfied']
        elif message['text'].lower() in ['sim', 'yes']:
            del info[user_id]
            say("Obrigado!", thread_ts=thread_ts)
    else:
        info[user_id]['alteration'] = message['text']
        info[user_id]['satisfied'] = False
        say("Aguarde, estamos processando sua mensagem!", thread_ts=message['ts'])
        process_code(message, say, 'refactor')


@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)

def main():
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()

if __name__ == "__main__":
    main()
