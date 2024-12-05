from PyQt6.QtCore import Qt, QFile, QTextStream
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class MensagemWidget(QWidget):
    def __init__(self, texto, tipo, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        label = QLabel(texto, self)
        label.setWordWrap(True)

        if tipo == "usuario":
            label.setObjectName("mensagem_usuario")
            label.adjustSize()
            layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        elif tipo == "nexus":
            label.setObjectName("mensagem_nexus")
            label.adjustSize()
            layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        layout.addWidget(label)
        self.setLayout(layout)
        self.carregar_css()

    def carregar_css(self):
        arquivo_css = QFile("css\\style_mensagens.css")
        if arquivo_css.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(arquivo_css)
            css = stream.readAll()
            self.setStyleSheet(css)
            arquivo_css.close()