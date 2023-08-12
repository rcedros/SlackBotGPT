# SlackBotGPT

This Chatbot integrates with slack and openAI, performs PII filter and access key types filter. 

To make the bot more secure I implemented some security measures:

The bot validates if the user inserted in the thread any Brazilian document such as: CPF, CHN, CNS, RENAVAM, PIS, Voter's Title, Credit Card and e-mail. In this case, the bot makes a parse of the document number by the name of the document type. The idea is that it forwards to openAI, but does not forward the actual document number, example: 

* Sent by user: `CPF = 777.888.999-92`
* Sent to openAI: `CPF = [CPF]`

To do this parse, I am using the [validate_docbr](https://github.com/alvarofpp/validate-docbr/tree/main) library.

Another security validation is blocking of most commonly used sensetive secrets. In this case, the bot returns a response for the user to evaluate or replace the value, example: `key`, `token`, `password`, `secret`, `passwd`, `password`.

You will find details here: [chatbot_pii.py](https://github.com/rcedros/SlackBotGPT/blob/main/filter_pii.py).

### Commands in Slackbot:
You can use it like a ChatGPT starting commands:

* `@Hibot`: Opens a chat conversation like a chatbot in the same thread.
* `@code-refactor`: Refactor the code based on the information entered by the user in the same thread.
* `@code-security`: Refactor the code based on the vulnerability and the information entered by the user in the same thread.

## Let's Implementations

### Slack

1. Access [api.slack.com](https://api.slack.com) and login in your workspace.
2. Click in `Your Apps` and `Create an app`, select `From Scratch` option.
3. Create a App and select your workspace option.

**Menu (Settings and Features)**

1.  **Basic Information:** create a App-Level Tokens, choose all scoles (connections:write, authorizations:read, app_configurations:write). Copy and save the Token: `xapp-1-...`

3.  **Socket Mode:** Enable Socket Mode and click in `Event Subscriptions` to enable.
  
5.   **Event Subscriptions:** In Subscribe to bot events: add Event Name:`app_mention`, `im_history_changed`, `message.channels` and `message.im`.
   
7.   **App Home:** Config `App Display Name` to give bot name and change enable `Messages Tab` and mark checkbox: `Allow users to send Slash commands and messages from the messages tab` in Show Tabs.
   
9.   **OAuth & Permissions:** create and copy the `Bot User OAuth Token`: `xoxb-...` and in `Scopes` option add: `app_mentions:read`, `channels:history`, `channels:read`, `chat:write`, `im:history`, `im:read`.
    
11.   **Install App:** Click for Install to Workspace.

### OpenAI setep

1. Create Account in [openai.com](https://openai.com)
2. In menu, click in view API Keys
3. Create new secret key, give a name and copy and save secret key: 'sk-...'

### Configuration Keys setup:

1. Update secrets keys in [secret_acces.py](https://github.com/rcedros/SlackBotGPT/blob/main/secret_access.py) with keys that saved.
```
SLACK_APP_TOKEN = 'xapp-1-...'
SLACK_BOT_TOKEN = 'xoxb-...'
OPEN_IA_TOKEN = 'sk-...'
```
2. Then, you can run `chatbot_slack_gpt.py` directly or,
3. Use dockerfile to create a image and run container.
```
docker build -t slackBotGPT .
docker run -d slackBotGPT slackBotGPT
```


