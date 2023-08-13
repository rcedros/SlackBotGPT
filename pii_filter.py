import re
import validate_docbr as docbr
from creditcard_validate import check_issuer, check_card_number

##############################################################################################
#    Brazilian documents generates here => https://www.4devs.com.br/computacao               #
#                                                                                            # 
#    Credit Card: 5564 7813 7674 7251 | 5564781376747251                               #
#    CPF: 418.540.270-85 | 41854027085                                                       #
#    CNS: 03977291368                                                                        #
#    PIS: 76263869822 | 762.63869.82-2                                                       # 
#    RENAVAN: 18689900263                                                                    # 
#    TITULO ELEITOR: 348668162038                                                            #
#    EMAIL: lista_de_emails@gmail.com lista_de_emails@outlook.com lista_de_emails@inbox.com  #
#                                                                                            #
##############################################################################################

_RE_PIS = re.compile(r'\b\d{3}\.?\d{5}\.?\d{2}-?\d\b')
_RE_CCARD = re.compile(r'\b(?:\d[ -]*?){13,16}\b')
_RE_ELEITOR = re.compile(r'\b\d{12}\b')
_RE_CNH = re.compile(r'\b\d{11}\b')
_RE_CNS = re.compile(r'\b\d{15}\b')
_RE_CPF = re.compile(r'\d{3}\.?\d{3}\.?\d{3}-?\d{2}')
_RE_RENAVAN = re.compile(r'\b\d{11}\b')
_RE_TEL = re.compile(r'(?:\(\d{2}\)|\d{2})?\s?\d{5}-?\d{4}')
_RE_CEP = re.compile(r'\b(\d{5}-\d{3})\b')
_RE_MAIL = re.compile(r'\b[A-Za-z0-9._%+-]+@(?:gmail\.com|yahoo\.com|outlook\.com|hotmail\.com|aol\.com|protonmail\.com|zoho\.com|icloud\.com|mail\.com|gmx\.com|yandex\.com|msn\.com|live\.com|inbox\.com|fastmail\.com|hushmail\.com|lycos\.com|mail\.ru)\b')
_RE_CONTA = re.compile(r'\b(?:(?:\d{8}-\d)|(?:\d{8}\d))\b')
_RE_AGENCIA = re.compile(r'\b(?:0655)\b')

def remove_pii(text):
    # remove Cartão de Credito    
    FIND_CCARD = re.findall(_RE_CCARD, text)
    if FIND_CCARD:
        checkcardNumber = check_card_number(FIND_CCARD[0]) 
        checkIssuer = check_issuer(FIND_CCARD[0])
        if checkcardNumber is True and checkIssuer is not None:
            text = re.sub(FIND_CCARD[0], '[CARTAO DE CREDITO]', text)

    # Remove PIS: PIS/NIS/PASEP/NIT
    FIND_PIS = re.findall(_RE_PIS, text)
    if FIND_PIS:
        valid_PIS = [(docbr.PIS, FIND_PIS[0])]
        valid_PIS = docbr.validate_docs(valid_PIS)
        if valid_PIS[0] is True:
            text = re.sub(FIND_PIS[0], '[PIS/PASEP]', text)

    #remove Título eleitoral - Cadastro que permite cidadãos brasileiros votar
    FIND_ELEITOR = re.findall(_RE_ELEITOR, text)
    if FIND_ELEITOR:
        valid_ELEITOR = [(docbr.TituloEleitoral, FIND_ELEITOR[0])]
        valid_ELEITOR = docbr.validate_docs(valid_ELEITOR)
        if valid_ELEITOR[0] is True:
            text = re.sub(FIND_ELEITOR[0], '[TITULO DE ELEITOR]', text)

    # remove CPF - Cadastro de Pessoa Física
    FIND_CPF = re.findall(_RE_CPF, text)
    if FIND_CPF:
        valid_CPF = [(docbr.CPF, FIND_CPF[0])]
        valid_CPF = docbr.validate_docs(valid_CPF)
        if valid_CPF[0] is True:
            text = re.sub(FIND_CPF[0], '[CPF]', text)

    #remove CNH - Carteira Nacional de Habilitação
    FIND_CNH = re.findall(_RE_CNH, text)
    if FIND_CNH:
        valid_CNH = [(docbr.CNH, FIND_CNH[0])]
        valid_CNH = docbr.validate_docs(valid_CNH)
        if valid_CNH[0] is True:
            text = re.sub(FIND_CNH[0], '[CNH]', text)

    # remove CNS - cartão nacional de saúde
    FIND_CNS = re.findall(_RE_CNS, text)
    if FIND_CNS:
        valid_CNS = [(docbr.CNS, FIND_CNS[0])]
        valid_CNS = docbr.validate_docs(valid_CNH)
        if valid_CNS[0] is True:
            text = re.sub(FIND_CNS[0], '[CNS]', text)
  
    # remove RENAVAM - Registro Nacional de Veículos Automotores.
    FIND_RENAVAN = re.findall(_RE_RENAVAN, text)
    if FIND_RENAVAN:
        valid_RENAVAN = [(docbr.RENAVAM, FIND_RENAVAN[0])]
        valid_RENAVAN = docbr.validate_docs(valid_RENAVAN)
        if valid_RENAVAN[0] is True:
            text = re.sub(FIND_RENAVAN[0], '[RENAVAN]', text)

    # remove número de telefone:
    text = re.sub(_RE_TEL, '[TEL]', text)
    #remove cep:
    text = re.sub(_RE_CEP, '[CEP]', text)
    #remove email
    text = re.sub(_RE_MAIL, '[E-MAIL]', text)
    #remove conta bancária
    text = re.sub(_RE_CONTA, '[Nº CONTA CORRENTE]', text)
    #remove agencia bancária Neon
    text = re.sub(_RE_AGENCIA, '[AGENCIA NEON]', text)

    return text

def contains_prohibited(text):
    # lista Palavras proibidas
    keywords = [
                'key', 'token', 'senha', 'secret','secrets', 'passwd', 'password', 'username', 'client id', 'subscription key', 
                'api key', 'app key', 'swarm join token', 'swarm unlock key', 'api-token', 'user oauth token', 
                'client secret', 'access token', 'app id', 'app secret', 'api token', 'server key', 'personal access token', 
                'google_application_credentials', 'unseal key', 'secret access key', 'basic authentication credentials', 
                'private key', 'bind dn', 'bind password', 'ppk file', 'consumer key', 'consumer secret', 'smtp sername', 
                'smtp password', 'sonar_token', 'tfe_token', 'aws_secret_access_key', 'azure_devops_ext_pat', 
                'awsaccesskeyid', 'mwsauthtoken', 'aws_access_key_id', 'aws_access_key', 'azure_client_id', 
                'azure_client_secret', 'ibm_api_key', 'oracle_password', 'digitalocean_access_token'
    ]
    for word in keywords:
        if word in text.lower():
            return f"Sorry, we cannot process your message. It appears to contain the word: `{word}`. Please remove the word and its content. It is important to keep company and personal information secure. If you have any other questions or requests, I am here to help."
    return text
