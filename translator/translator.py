from translate import Translator

translator= Translator(to_lang="ja")
try:
  with open('GitHub/Python/Python-exercises/translator/text.txt', mode='r') as my_file:
    txt = my_file.read()
    translation = (translator.translate(txt))
    with open('GitHub/Python/Python-exercises/translator/test-ja.txt', mode='w') as my_file2:
      my_file2.write(translation)
except FileNotFoundError as e:
  print('check your file path silly!')