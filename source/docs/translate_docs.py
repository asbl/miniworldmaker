import deepl
import os
from pathlib import Path
import deepl_key
translator = deepl.Translator(deepl_key.KEY)
path = os.getcwd()

for root, dirs, files in os.walk("./source/objectsfirst_german/"):
    for name in files:
        file = os.path.join(root, name)
        target_file = os.path.join(root, name).replace("german", "english")
        txt_de = Path(file).read_text()
        txt_en = translator.translate_text(txt_de, target_lang="EN-US")
        output = open(target_file, 'w')
        output.write(str(txt_en))
        output.close()
