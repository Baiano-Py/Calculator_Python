import re
from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import Qt
import json
from files.variables_ import *

NUM_OR_DOT_REGEX = re.compile(r'^[0-9.]$')

def isNumOrDot(string: str) -> bool:
    return bool(NUM_OR_DOT_REGEX.search(string))

def isValidNumber(string: str) -> bool:
    try:
        float(string)
        return True
    except ValueError:
        return False

def salvarArquivo(resultado: str) -> None:

    try:
        with open(caminho_history, 'r') as file:
            history = json.load(file)
            if len(history) >= 10:
                history.pop(0)
    except FileNotFoundError:
        history = []

    history.append(resultado)

    with open(caminho_history, 'w', encoding='utf8') as file:
        json.dump(history, file, indent=2)


def history_cont(self):
    with open(caminho_history, 'r') as file:
        history = json.load(file)
    if not history:
        self._ShowError('O histórico está vazio.')
        return
    history = [conta for conta in history if conta.strip()]

    # Formata o histórico em uma string para exibir na mensagem
    formatted_history = "\n".join([f"{conta}" for indice, conta in enumerate(history)])
    historyInfo(self, formatted_history)

def historyInfo(self, text):
    mensageBox = self.window.makeMensageBox()
    formatted_text = f"<p style='text-align: center;'>{text.replace('\n', '<br>')}</p>"
    mensageBox.setText(formatted_text)
    mensageBox.setStyleSheet(info_theme)
    mensageBox.setIcon(QMessageBox.Information)
    mensageBox.exec()