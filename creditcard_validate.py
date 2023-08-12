import re

# Algoritmo Luhn para identificação de números de cartão de crédito válidos.

def sum_digits(n):
    return sum(int(digit) for digit in str(n))

def check_card_number(card_number):
    digits = [int(digit) for digit in re.findall(r'\d', card_number)]

    for i in range(len(digits) - 2, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
    return sum(digits) % 10 == 0

# Identify card issuer based on card number regex
def check_issuer(card_number):
    card_number = card_number.replace(" ","")
    issuer_dict = {
        "Amex": "^3[47][0-9]{13}$",
        "BCGlobal": "^(6541|6556)[0-9]{12}$",
        "Carte Blanche Card": "^389[0-9]{11}$",
        "Diners Club Card": "^3(?:0[0-5]|[68][0-9])[0-9]{11}$",
        "Discover Card": "^65[4-9][0-9]{13}|64[4-9][0-9]{13}|6011[0-9]{12}|(622(?:12[6-9]|1[3-9][0-9]|[2-8][0-9][0-9]|9[01][0-9]|92[0-5])[0-9]{10})$",
        "Insta Payment Card": "^63[7-9][0-9]{13}$",
        "JCB Card": "^(?:2131|1800|35\d{3})\d{11}$",
        "KoreanLocalCard:": " ^9[0-9]{15}$",
        "Laser Card": "^(6304|6706|6709|6771)[0-9]{12,15}$",
        "Maestro Card": "^(5018|5020|5038|6304|6759|6761|6763)[0-9]{8,15}$",
        "Mastercard": "^5[1-5][0-9]{14}$}",
        "Solo Card": "^(6334|6767)[0-9]{12}|(6334|6767)[0-9]{14}|(6334|6767)[0-9]{15}$",
        "Switch Card": "^(4903|4905|4911|4936|6333|6759)[0-9]{12}|(4903|4905|4911|4936|6333|6759)[0-9]{14}|(4903|4905|4911|4936|6333|6759)[0-9]{15}|564182[0-9]{10}|564182[0-9]{12}|564182[0-9]{13}|633110[0-9]{10}|633110[0-9]{12}|633110[0-9]{13}$",
        "Union Pay Card": "^(62[0-9]{14,17})$",
        "Visa Card": "^4[0-9]{12}(?:[0-9]{3})?$",
        "Visa Master Card": "^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14})$"
    }
    
    for card, regex in issuer_dict.items():
        if re.search(regex, card_number):
            return card