from langdetect import detect


class TextTranslator:
    @staticmethod
    def translate_text(line, translator):
        if line and line.strip():
            try:
                detected_lang = detect(line)
                if detected_lang != "en":
                    return translator.translate(line, dest="en").text
                else:
                    return line
            except Exception as e:
                print(f"Error in translating text: {e}")
                return line
