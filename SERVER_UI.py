import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from socket import *
import threading
import time

port = 0
listen = False
form_class = uic.loadUiType("test.ui")[0]
class WindowClass (QMainWindow, form_class) :
    def __init__(self):
        
        super().__init__()
        self.setupUi(self)

        #버튼 부분
        #버튼 클릭 이벤트 감지  okButton은 Disigner에서 설정해준 버튼의 objectName
        self.okButton.clicked.connect(self.okBtn_clicked)
        self.connectButton.clicked.connect(self.connectBtn_clicked)

    #OK버튼이 눌리면 동작할 부분
    def okBtn_clicked(self):
        print("okBtn Clicked")
        message = self.messageEdit.toPlainText()
        self.messageEdit.clear()
        self.dialogView.append("나: "+message)

    #연결버튼이 눌리면 동작할 부분
    def connectBtn_clicked(self):
        print("connectBtn Clicked")
        # ip,포트 값 가져오기
        global port
        ip_value = self.iPEdit.text()
        port = int(self.portEdit.text())
        self.dialogView.append('%d번 포트로 접속 대기중...'%port)
        self.serverSock = socket(AF_INET, SOCK_STREAM)
        self.serverSock.bind(('', port))
        global listen
        listen = True
        self.t = threading.Thread(target=self.listener, args=(self.serverSock,))
        self.t.start()
        # print('Server Listening...')


    def listener(self, serverSock):
         if listen:
            serverSock.listen(1)
            try:
                 connectionSock, addr = serverSock.accept()
            except Exception as e:
                print('Accept() Error : ', e)
            else:                
                self.dialogView.append('에서 접속되었습니다.')
                self.dialogView.append(str(addr), '에서 접속되었습니다.')



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()