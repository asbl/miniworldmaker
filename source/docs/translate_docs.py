import deepl
import os
import ../../../deepl_key.py as deepl_key

translator = deepl.Translator(os.getenv(deepl_key.KEY))

path = os.getcwd()
print(path)

for root, dirs, files in os.walk("./source/objectsfirst_german/"):
    for name in files:
        file = os.path.join(root, name)
        print(file)
        print(os.path.join(root, name))
        target_file = os.path.join(root, name).replace("german", "english")
        Translate a formal document from English to German 
        translator.translate_document_from_filepath(
            file,
            target_file,
            target_lang="EN-US",
        )
