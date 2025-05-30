import random

def generate_text(corpus, length=100):
  """
  Генерирует текст на основе корпуса текста, используя цепи Маркова.

  Args:
    corpus: Текст, на основе которого генерируется новый текст.
    length: Желаемая длина сгенерированного текста (количество слов).

  Returns:
    Сгенерированный текст.
  """

  # Создаем словарь, где ключ - слово, а значение - список слов,
  # которые следуют за ним в корпусе.
  markov_chain = {}
  words = corpus.split()

  for i in range(len(words) - 1):
    current_word = words[i]
    next_word = words[i+1]
    if current_word in markov_chain:
      markov_chain[current_word].append(next_word)
    else:
      markov_chain[current_word] = [next_word]

  # Начинаем генерацию с произвольного слова из корпуса.
  current_word = random.choice(words)
  generated_text = [current_word]

  # Генерируем текст, выбирая следующее слово из списка возможных
  # слов, которые следуют за текущим словом.
  for _ in range(length - 1):
    if current_word in markov_chain:
      next_word = random.choice(markov_chain[current_word])
      generated_text.append(next_word)
      current_word = next_word
    else:
      # Если текущего слова нет в цепи Маркова, выбираем произвольное
      # слово из корпуса, чтобы продолжить генерацию.
      current_word = random.choice(words)
      generated_text.append(current_word)

  return " ".join(generated_text)


# Пример использования:
corpus = """
The quick brown fox jumps over the lazy dog.
The lazy dog sleeps.
The quick fox runs.
"""

generated_text = generate_text(corpus, length=20)
print(generated_text)
