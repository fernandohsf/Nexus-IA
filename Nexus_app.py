import sys
from PyQt6.QtCore import Qt, QPoint, QFile, QTextStream, QTimer
from PyQt6.QtGui import QPainter, QImage, QMouseEvent
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTextEdit, QScrollArea, QVBoxLayout, QPushButton
from chatbot import resposta_bot
from mensagens import MensagemWidget

class NexusApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Nexus')
        
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        ### Definindo o widget central
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # ScrollArea para conversa
        self.scroll_area = QScrollArea(self.central_widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("scroll_area")
        self.scroll_area.setStyleSheet("border: none;")

        # Área de conversa
        self.conteudo_scroll = QWidget(self)
        self.layout_conversa = QVBoxLayout(self.conteudo_scroll)
        self.conteudo_scroll.setLayout(self.layout_conversa)
        self.scroll_area.setWidget(self.conteudo_scroll)

        self.layout_enviar = QVBoxLayout()
        # Botão de envio
        self.botao_enviar = QPushButton('Enviar', self.central_widget)
        self.botao_enviar.setObjectName("botao_enviar")
        self.botao_enviar.clicked.connect(self.chatBot)

        ### Área de entrada de texto
        self.entrada_usuario = QTextEdit(self.central_widget)
        self.entrada_usuario.setPlaceholderText("Diga algo para o Nexus...")
        self.entrada_usuario.setObjectName("entrada_usuario")
        self.entrada_usuario.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)

        self.carregar_css()
        self.showMaximized()
        self.drag_position = QPoint()

    def paintEvent(self, event):
        janela_nexus = QPainter(self)
        imagem_fundo = QImage("C:\\Automações Fapec\\Nexus IA\\imagens\\Nexus_v2.png")
        
        ### Posicionamento do Nexus
        posicao_x = self.width() - imagem_fundo.width() 
        posicao_y = self.height() - imagem_fundo.height()
        janela_nexus.drawImage(posicao_x, posicao_y, imagem_fundo)

        janela_nexus.end()

    def resizeEvent(self, event):
        ### Posicionamento e tamanho da entrada_usuario
        self.entrada_usuario.setFixedSize(350, 80)
        posicao_x_entrada = self.width() - self.entrada_usuario.width() - 240
        posicao_y_entrada = self.height() - self.entrada_usuario.height() - 25
        self.entrada_usuario.move(posicao_x_entrada, posicao_y_entrada)

        self.botao_enviar.setFixedSize(45, 80)
        posicao_x_botao = self.width() - self.botao_enviar.width() - 190
        posicao_y_botao = self.height() - self.botao_enviar.height() - 25
        self.botao_enviar.move(posicao_x_botao, posicao_y_botao)

        ### Posicionamento e tamanho da área de conversa
        altura_conversa = self.height() - self.entrada_usuario.height() - 20
        self.scroll_area.setFixedSize(455, altura_conversa)
        posicao_x_scroll = self.width() - self.scroll_area.width() - 162
        posicao_y_scroll = 0
        self.scroll_area.move(posicao_x_scroll, posicao_y_scroll)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() & Qt.MouseButton.LeftButton:
            delta = event.globalPosition().toPoint() - self.drag_position
            self.move(self.pos() + delta)
            self.drag_position = event.globalPosition().toPoint()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return and event.modifiers() == Qt.KeyboardModifier.NoModifier:
            self.chatBot()

    def chatBot(self):
        pergunta = self.entrada_usuario.toPlainText().strip()
        if not pergunta:
            return

        # Adicionar pergunta como widget no layout
        pergunta_widget = MensagemWidget(f"Você: {pergunta}", "usuario", self)
        self.layout_conversa.addWidget(pergunta_widget)
        self.entrada_usuario.clear()

        if pergunta.lower() == "sair":
            self.close()
            return

        try:
            mensagens = [("user", pergunta)]
            resposta = resposta_bot(mensagens)  # Substitua com sua função de chatbot
        except Exception as e:
            resposta = f"Desculpe, ocorreu um erro ao processar sua solicitação. {e}"

        # Adicionar resposta como widget no layout
        resposta_widget = MensagemWidget(f"Nexus: {resposta}", "nexus", self)
        self.layout_conversa.addWidget(resposta_widget)

        QTimer.singleShot(10, self.scroll_to_bottom)
    
    def carregar_css(self):
        arquivo_css = QFile("css\\style_nexus_app.css")
        if arquivo_css.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(arquivo_css)
            css = stream.readAll()
            self.setStyleSheet(css)
            arquivo_css.close()

    def scroll_to_bottom(self):
        # Rolar automaticamente para a última mensagem
        self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NexusApp()
    sys.exit(app.exec())