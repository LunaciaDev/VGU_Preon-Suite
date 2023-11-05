from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Slot, Signal
from packages.ui.applicationControllerClass import Ui_MainWindow

from packages.passwordWindow import PasswordWindow
from packages.homeWindow import HomeWindow

from packages.password_tasks import password_tasks as PasswordTask

from packages.scheduler import SchedulerController

class ApplicationController(QMainWindow):
    terminateThread = Signal()

    def __init__(self):
        super(ApplicationController, self).__init__()
        self.ui = Ui_MainWindow();
        self.ui.setupUi(self)

        self.homeWindow = HomeWindow()
        self.passwordWindow = PasswordWindow()

        self.ui.applicationStack.addWidget(self.passwordWindow)
        self.ui.applicationStack.addWidget(self.homeWindow)

        self.passwordTask = PasswordTask()

        self.passwordTask.loginStatus.connect(self.passwordWindow.onValidationCompleted)
        self.passwordTask.registerStatus.connect(self.passwordWindow.onAccountRegistrated)
        self.passwordWindow.validateCredential.connect(self.passwordTask.login)
        self.passwordWindow.createCredential.connect(self.passwordTask.register)
        self.passwordWindow.loggedIn.connect(self.onLoggedIn)

        self.ui.applicationStack.setCurrentIndex(0)
    
    @Slot()
    def onLoggedIn(self):
        self.ui.applicationStack.setCurrentIndex(1)
        self.schedulerWorker.mailTask.signIn()
    
    def initScheduler(self):
        self.schedulerWorker = SchedulerController()
        self.terminateThread.connect(self.schedulerWorker.terminateThread)

        #temporary var for quick access
        mailWindow = self.homeWindow.mailWindow
        SCHMail = self.schedulerWorker.mailTask

        #Wiring for Mail Module
        mailWindow.googleRegistration.connect(SCHMail.generateToken)
        mailWindow.sendEmail.connect(SCHMail.sendEmail)
        mailWindow.refreshPage.connect(SCHMail.CheckInbox)

        SCHMail.credentialsValidity.connect(mailWindow.onGotLoginStatus)
        SCHMail.inboxPayload.connect(mailWindow.setEmailList)
        SCHMail.sentEmail.connect(mailWindow.onSentEmail)
        
        self.schedulerWorker.run()

    @Slot()
    def quit(self):
        self.terminateThread.emit()