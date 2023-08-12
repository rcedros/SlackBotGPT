
import json
from datetime import datetime


def save_conversation(thread_id, conversation):
    current_dateTime = datetime.now().isoformat(timespec='minutes')
    # Convertendo a conversa para JSON para ter uma representação legível
    conversation_json = json.dumps(conversation, indent=4)
    
    # Criando um nome de arquivo com base no user_id e thread_id
    filename = f"_{thread_id}_{current_dateTime}.txt"
    
    # Escrevendo a conversa no arquivo
    with open(filename, 'w') as f:
        f.write(conversation_json)