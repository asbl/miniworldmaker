import deepl
import os
from pathlib import Path
translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))
path = os.getcwd()

for root, dirs, files in os.walk("./source/processing_german/"):
    for name in files:
        file = os.path.join(root, name)
        print(file)
        target_file = os.path.join(root, name).replace("german", "english")
        txt_de = Path(file).read_text()
        txt_en = translator.translate_text(txt_de, target_lang="EN-US")
        txt_en_str = str(txt_en)
        txt_en_str = txt_en_str.replace("\n`` python", "\n``` python")
        txt_en_str = txt_en_str.replace("\n``python", "\n``` python")
        txt_en_str = txt_en_str.replace("\n`` {", "\n``` {")
        txt_en_str = txt_en_str.replace("\n``{", "\n``` {")
        output = open(target_file, 'w')
        output.write(txt_en_str)
        output.close()
