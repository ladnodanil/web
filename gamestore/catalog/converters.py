import re

class GameSlugConverter:
    regex = "[A-Za-z0-9-]+"  # Добавлена поддержка цифр

    def to_python(self, value):
        """Преобразование из URL в Python-значение"""
        return re.sub(r"-+", " ", value).strip().lower()  # Заменяем один или несколько дефисов пробелом

    def to_url(self, value):
        """Преобразование из Python-значения в URL"""
        return re.sub(r"\s+", "-", value.strip())  # Убираем лишние пробелы и заменяем пробелы на дефисы
