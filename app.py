import sys
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QMainWindow

class NexusApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Nexus')
        self.setGeometry(100, 100, 800, 600)
        
        # Tornando a janela transparente
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlag(Qt.FramelessWindowHint)

        # Configurando o WebEngineView
        self.web_view = QWebEngineView(self)
        self.web_view.setGeometry(0, 0, 800, 600)
        self.web_view.setAttribute(Qt.WA_TranslucentBackground)
        self.web_view.setStyleSheet("background: transparent;")

        # Convertendo o caminho para QUrl e carregando o arquivo HTML
        file_path = "D:/AutomacaoFapec/Nexus_IA/web/index.html"
        self.web_view.load(QUrl.fromLocalFile(file_path))
        
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NexusApp()
    sys.exit(app.exec_())
