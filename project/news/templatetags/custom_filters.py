from django import template
from datetime import datetime
register = template.Library()


@register.filter
def censorship(value, words_to_censor):
    words = value.split()  # Разделяем текст на слова
    censored_text = []

    for word in words:
        clean_word = word.strip('.,!?;:')  # Удаляем знаки препинания в конце слова для точного сравнения
        if clean_word.lower() in words_to_censor:  # Сравниваем без учета регистра
            censored_word = clean_word[0] + '*' * (len(clean_word) - 1)
            censored_text.append(word.replace(clean_word, censored_word))  # Возвращаем знаки препинания на место
        else:
            censored_text.append(word)

    return ' '.join(censored_text)


