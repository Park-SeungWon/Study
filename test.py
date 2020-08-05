import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

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
        ip_value =self.iPEdit.text()
        port = self.portEdit.text()







if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()