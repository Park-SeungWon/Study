import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

from socket import *
import threading



form_class = uic.loadUiType("test.ui")[0]

port = 8080
ip = '127.0.0.1'
message = ''
received_msg = ''



class Client():
    print("불러오기 성공")
    global ip,port

    def send(sock):
        print("보내기 쓰레드 실행")
        global message
        while True:
            if len(message)>0 :
                sock.send(message.encode('utf-8'))
                message=''

    def receive(sock):
        print("받기 쓰레드 실행")

        while True:
            recvData = sock.recv(1024)
            print('상대방 :', recvData.decode('utf-8'))
            if len(recvData) > 0 :
                global received_msg
                received_msg = recvData
                print("야수야스"+ str(len(received_msg))+ "      " + str(len(recvData)))


    def connection(self):
        clientSock = socket(AF_INET, SOCK_STREAM)
        clientSock.connect((ip, port))
        sender = threading.Thread(target=Client.send, args=(clientSock,))
        receiver = threading.Thread(target=Client.receive, args=(clientSock,))
        sender.start()
        receiver.start()





class WindowClass (Client,QMainWindow, form_class) :
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
        global message
        message = self.messageEdit.toPlainText()
        self.messageEdit.clear()
        self.dialogView.append("나 : "+message)


    #연결버튼이 눌리면 동작할 부분
    def connectBtn_clicked(self):
        print("connectBtn Clicked")
        # ip,포트 값 가져오기
        global ip, port
        ip =self.iPEdit.text()
        port = int(self.portEdit.text())
        client = Client()
        try:
            client.connection()
            self.dialogView.append("채팅방에 입장하였습니다.")
            self.connectionState.setText(ip+" 에 연결하였습니다.")
            showMsg = threading.Thread(target=self.show_ReceivedMessage)
            showMsg.start()

        except Exception as ex :
            print("에러 발생 : "+ex)
            self.connectionState.setText("연결에 실패하였습니다.")

    #메시지를 채팅창에 보여주기
    def show_ReceivedMessage(self):
        global received_msg
        print("실행중!")
        print("msg: "+ received_msg + " 길이 : " + str(received_msg))
        while True :
            if len(received_msg) > 0:
                print("OK!!!!")
                self.dialogView.append(ip+" : "+str(received_msg.decode('utf-8')))
                received_msg = ''

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()