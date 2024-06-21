import sys
import mysql.connector
from re import match
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSignal


conn_info = {}

class LoginBanco(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    login_successful = pyqtSignal(dict)
    
    def initUI(self):
        self.setWindowTitle('Login Banco de Dados de Placas')
        self.setFixedSize(300, 300)

        # Input do host
        self.host_label = QLabel('Host:', self)
        self.host_label.move(20, 20)

        self.host_input = QLineEdit(self)
        self.host_input.setGeometry(80, 20, 200, 20)
        self.host_input.setText('localhost')

        # Input da porta
        self.port_label = QLabel('Port:', self)
        self.port_label.move(20, 50)

        self.port_input = QLineEdit(self)
        self.port_input.setGeometry(80, 50, 200, 20)
        self.port_input.setText('3307')

        # Input do user
        self.user_label = QLabel('User:', self)
        self.user_label.move(20, 80)

        self.user_input = QLineEdit(self)
        self.user_input.setGeometry(80, 80, 200, 20)
        self.user_input.setText('root')

        # Input do database
        self.database_label = QLabel('Database:', self)
        self.database_label.move(20, 110)

        self.database_input = QLineEdit(self)
        self.database_input.setGeometry(80, 110, 200, 20)
        self.database_input.setText('banco_placas')

        # Input da senha
        self.password_label = QLabel('Senha:', self)
        self.password_label.move(20, 140)

        self.password_input = QLineEdit(self)
        self.password_input.setGeometry(80, 140, 200, 20)
        self.password_input.setEchoMode(QLineEdit.Password)

        # Botao para testar conexao
        self.btn_testar_conexao = QPushButton('Testar Conexão', self)
        self.btn_testar_conexao.setGeometry(100, 170, 100, 30)
        self.btn_testar_conexao.clicked.connect(self.testar_conexao)

    def testar_conexao(self):
        host = self.host_input.text()
        user = self.user_input.text()
        port = self.port_input.text()
        database = self.database_input.text()
        password = self.password_input.text()

        global conn_info
        conn_info = {
            'host': host,
            'user': user,
            'port': port,
            'password': password,
            'database': database,
        }
        try:
            conn = mysql.connector.connect(
                host=host,
                user=user,
                port=port,
                password=password,
                database=database,
            )
            self.login_successful.emit(conn_info)
            conn.close()
        
        except mysql.connector.Error as err:
            QMessageBox.critical(self, 'Erro', f'Erro ao conectar ao banco de dados: {err}')
            return None


class CadastroPlaca(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.conn_info = conn_info
    
    def initUI(self):
        self.setWindowTitle('Cadastro de Placas')
        self.setFixedSize(300, 150)

        # Input da placa
        self.placa_label = QLabel('Placa:', self)
        self.placa_label.move(20, 20)

        self.placa_input = QLineEdit(self)
        self.placa_input.setGeometry(80, 20, 200, 20)

        # Input da descricao
        self.descricao_label = QLabel('Descrição:', self)
        self.descricao_label.move(20, 50)

        self.descricao_input = QLineEdit(self)
        self.descricao_input.setGeometry(80, 50, 200, 20)

        # Botao de cadastrar
        self.btn_cadastrar = QPushButton('Cadastrar', self)
        self.btn_cadastrar.setGeometry(100, 80, 100, 30)
        self.btn_cadastrar.clicked.connect(self.cadastrar_placa)

    def cadastrar_placa(self, conn_info):
        pattern = r'^[A-Z]{3}\d[A-Z]\d{2}$'

        placa = self.placa_input.text()
        descricao = self.descricao_input.text()

        if not placa or not match(pattern, placa):
            QMessageBox.critical(self, 'Atenção', 'Por favor, insira uma placa válida!')
            return

        print('print conn_info: ', self.conn_info)
        try:
            conn = mysql.connector.connect(
                host=self.conn_info['host'],
                user=self.conn_info['user'],
                port=self.conn_info['port'],
                password=self.conn_info['password'],
                database=self.conn_info['database'],
            )
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO placas_registradas (placa, descricao) VALUES (%s, %s)",
                    (placa, descricao)
                )
            conn.commit()

            QMessageBox.information(self, 'Sucesso', 'Placa cadastrada com sucesso!')
            self.placa_input.clear()
            self.descricao_input.clear()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, 'Erro', f'Erro ao cadastrar placa: {err}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginBanco()
    cadastro_placa_window = None

    def show_cadastro_placa_window():
        global cadastro_placa_window
        login_window.close()
        cadastro_placa_window = CadastroPlaca()
        cadastro_placa_window.show()
    
    login_window.login_successful.connect(show_cadastro_placa_window)

    login_window.show()
    sys.exit(app.exec_())
