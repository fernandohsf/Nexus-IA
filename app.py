import sys
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPainter, QImage, QMouseEvent
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTextEdit, QPushButton, QVBoxLayout
from chatbot import resposta_bot

class NexusApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Nexus')
        
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        ### Definindo o widget central
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setFixedWidth(400)

        self.layout = QVBoxLayout(self.central_widget)

        # Campo de exibição de mensagens
        self.conversa = QWidget(self)
        self.conversa.setStyleSheet("""
            background-color: #f0f0f0;
            border-radius: 10px;
            padding: 10px;
            font-size: 16px;
        """)
        self.layout.addWidget(self.conversa)

        ### Campo de entrada de texto
        self.entrada_usuario = QTextEdit(self)
        self.entrada_usuario.setPlaceholderText("Diga algo para o Nexus...")
        self.entrada_usuario.setStyleSheet("""
            background-color: white;
            border-radius: 10px;
            padding: 10px;
            font-size: 16px;
        """)
        self.entrada_usuario.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        self.layout.addWidget(self.entrada_usuario)

        # Botão de envio
        self.botao_enviar = QPushButton('Enviar', self)
        self.botao_enviar.setStyleSheet("""
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            padding: 10px;
            font-size: 16px;
        """)
        self.botao_enviar.clicked.connect(self.chatBot)
        self.layout.addWidget(self.botao_enviar)

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
        # Atualizando o tamanho dos widgets após o redimensionamento
        self.entrada_usuario.setFixedHeight(80)
        altura_conversa = self.height() - self.entrada_usuario.height() - 100
        self.conversa.setFixedHeight(altura_conversa)
        self.botao_enviar.setFixedHeight(50)

        posicao_x = self.width() - self.central_widget.width() - 190
        self.central_widget.move(posicao_x, 0)

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
            self.enviar_pergunta()

    def chatBot(self):
        pergunta = self.entrada_usuario.toPlainText().strip()
        if not pergunta:
            return

        # Exibe a pergunta do usuário na área de conversa
        self.conversa.append(f"Você: {pergunta}")
        self.entrada_usuario.clear()

        if pergunta.lower() == 'sair':
            self.close()
            return

        try:
            mensagens = [('user', pergunta)]
            resposta = resposta_bot(mensagens)
        except Exception as e:
            resposta = f"Desculpe, ocorreu um erro ao processar sua solicitação. {e}"

        # Exibe a resposta do bot na área de conversa
        self.conversa.append(f"Nexus: {resposta}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NexusApp()
    sys.exit(app.exec())