from mnemonic import Mnemonic

mnemonic_phrase = "abandon zoo enhance young join maximum fancy call minimum code spider olive toilet system also share birth profit horn bargain beauty media rapid"
words = mnemonic_phrase.split()

mnemo = Mnemonic("english")
wordlist = mnemo.wordlist
first_23_words = words

found_24th_word = None
for word in wordlist:
    full_mnemonic = " ".join(first_23_words + [word])
    if mnemo.check(full_mnemonic):
        found_24th_word = word
        break

if found_24th_word:
    print(f"A 24ª palavra BIP39 válida é: {found_24th_word}")
else:
    print("Não foi possível encontrar uma 24ª palavra válida para as 23 palavras fornecidas.")





