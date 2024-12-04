import sys
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPainter, QImage, QMouseEvent, QColor, QPainterPath
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton

from chatbot import resposta_bot

class NexusApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Nexus')
        
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        # Definindo o widget central
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Campo de entrada (inicialmente vazio)
        self.entrada_usuario = QLineEdit(self)
        self.entrada_usuario.setPlaceholderText("Diga algo para o Nexus...")
        self.entrada_usuario.setStyleSheet("background-color: white; border-radius: 10px; padding: 10px;")

        self.showFullScreen()
        self.drag_position = QPoint()

        # Variáveis para última pergunta e resposta
        self.resposta = ""

    def resizeEvent(self, event):
        entrada_largura = 400
        entrada_altura = 50

        # Calculando a posição para o canto inferior direito
        pos_x = self.width() - entrada_largura - 180  # 20px de margem da direita
        pos_y = self.height() - entrada_altura - 50  # 20px de margem inferior

        # Ajustando a posição e tamanho do campo de entrada
        self.entrada_usuario.setGeometry(pos_x, pos_y, entrada_largura, entrada_altura)

    def paintEvent(self, event):
        janela = QPainter(self)
        imagem_fundo = QImage("D:\\AutomacaoFapec\\Nexus IA\\imagens\\Nexus_v2.png")
        
        # Desenhar a imagem na posição calculada
        posicao_x = self.width() - 188
        posicao_y = self.height() - 255
        janela.drawImage(posicao_x, posicao_y, imagem_fundo)

        if hasattr(self, 'resposta') and self.resposta:
            mensagem = f"Nexus: {self.resposta}"
            self.balao_fala(janela, mensagem, posicao_x, posicao_y - 100)

        janela.end()

    def balao_fala(self, janela, texto, x, y):
        # Configurações de estilo
        margem = 20  # Margem ao redor do texto
        espacamento_linha = 10
        largura_maxima = 400
        cor_fundo = QColor("#e0f7fa")
        cor_contorno = QColor("#CCCCCC")
        sombra = QColor(0, 0, 0, 100)
        margem_sombra = 4

        # Divide o texto em linhas, respeitando a largura máxima
        font_metrics = janela.fontMetrics()
        palavras = texto.split()
        linhas = []
        linha_atual = ""

        for palavra in palavras:
            if font_metrics.horizontalAdvance(linha_atual + palavra) <= largura_maxima:
                linha_atual += palavra + " "
            else:
                linhas.append(linha_atual.strip())
                linha_atual = palavra + " "
        if linha_atual:
            linhas.append(linha_atual.strip())

        largura_texto = min(largura_maxima, max(font_metrics.horizontalAdvance(linha) for linha in linhas))
        altura_texto = len(linhas) * (font_metrics.height() + espacamento_linha)

        largura = largura_texto + 2 * margem
        altura = altura_texto + 2 * margem

        # Ajusta posição para manter o balão dentro da tela
        if x + largura > self.width():
            x = self.width() - largura - 150
        if y + altura > self.height():
            y = self.height() - altura - 10

        # Desenhar a sombra do balão
        sombra_path = QPainterPath()
        sombra_path.addRoundedRect(x + margem_sombra, y + margem_sombra, largura, altura, 20, 20)
        sombra_path.moveTo(x + largura - 60 + margem_sombra, y + altura + margem_sombra)
        sombra_path.lineTo(x + largura - 40 + margem_sombra, y + altura + margem_sombra + 20)
        sombra_path.lineTo(x + largura - 80 + margem_sombra, y + altura + margem_sombra)
        sombra_path.closeSubpath()

        janela.setBrush(sombra)
        janela.setPen(Qt.PenStyle.NoPen)
        janela.drawPath(sombra_path)

        # Desenhar o balão principal
        balao_path = QPainterPath()
        balao_path.addRoundedRect(x, y, largura, altura, 20, 20)
        balao_path.moveTo(x + largura - 60, y + altura)
        balao_path.lineTo(x + largura - 40, y + altura + 20)
        balao_path.lineTo(x + largura - 80, y + altura)
        balao_path.closeSubpath()

        janela.setBrush(cor_fundo)
        janela.setPen(cor_contorno)
        janela.drawPath(balao_path)

        # Desenhar o texto
        janela.setPen(QColor("#000000"))
        texto_y = y + margem
        for linha in linhas:
            janela.drawText(QPoint(x + margem, texto_y + font_metrics.ascent()), linha)
            texto_y += font_metrics.height() + espacamento_linha

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() & Qt.MouseButton.LeftButton:
            delta = event.globalPosition().toPoint() - self.drag_position
            self.move(self.pos() + delta)
            self.drag_position = event.globalPosition().toPoint()

    def keyPressEvent(self, event):
        if event.key() == 16777220:  # Código numérico para a tecla Enter
            self.enviar_pergunta()

    def enviar_pergunta(self):
        pergunta = self.entrada_usuario.text()
        if pergunta.lower() == 'sair':
            self.close()
            return

        try:
            mensagens = [('user', pergunta)]
            self.resposta = resposta_bot(mensagens)
        except Exception as e:
            self.resposta = f"Desculpe, ocorreu um erro ao processar sua solicitação. {e}"

        self.update()
        self.entrada_usuario.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NexusApp()
    sys.exit(app.exec())