

def pluralize(word: str) -> str:
    if word.endswith('y') and word[-2] not in 'aeiou':
        return word[:-1] + 'ies'  # company → companies
    elif word.endswith(('s', 'sh', 'ch', 'x', 'z')):
        return word + 'es'        # bus → buses, match → matches
    
    return word + 's'         # role → roles, user → users
