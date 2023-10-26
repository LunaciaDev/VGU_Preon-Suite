from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal, Slot
from packages.ui.passwordWindow.passwordLoginWindowClass import Ui_passwordLoginWindow

class PasswordLoginWindow(QWidget):
    validateCredential = Signal(str, str)
    createCredential = Signal(str, str)
    loggedIn = Signal()

    def __init__(self):
        super(PasswordLoginWindow, self).__init__()
        self.ui = Ui_passwordLoginWindow();
        self.ui.setupUi(self)
        
        self.ui.registerButton.clicked.connect(self.onRegisterButtonClicked)
        self.ui.loginButton.clicked.connect(self.onLoginButtonClicked)
        self.ui.passwordLoginButton.clicked.connect(self.onSwitchToCredentalLoginClicked)

        self.ui.loginStack.setCurrentIndex(0)

        self.ui.wrongCredentialLabel.hide()
        self.ui.notMatchingPasswordLabel.hide()
        self.ui.instructionLabel.hide()

    # Registration Control #
    @Slot()
    def onCreateAccountButtonClicked(self):
        if (self.ui.createPasswordInput.text() == self.ui.confirmPasswordInput.text()):
            self.ui.createUsernameInput.setText("")
            self.ui.createPasswordInput.setText("")
            self.ui.confirmPasswordInput.setText("")
            self.ui.notMatchingPasswordLabel.hide()
            self.createCredential.emit(self.ui.createUsernameInput.text(), self.ui.createPasswordInput.text())
            return

        self.ui.notMatchingPasswordLabel.show()

    @Slot()
    def onAccountRegistrationSuccessful(self):
        self.loggedIn.emit()
    ######

    # User Interface Control #
    @Slot()
    def onSwitchToCredentalLoginClicked(self):
        self.ui.loginStack.setCurrentIndex(1)

    @Slot()
    def onRegisterButtonClicked(self):
        self.ui.loginStack.setCurrentIndex(2)
    ######

    # Login Control #
    @Slot()
    def onLoginButtonClicked(self):
        self.validateCredential.emit(self.ui.usernameInput, self.ui.passwordInput)

    @Slot(bool, str)
    def onValidationCompleted(self, success, labelValue):
        if (success):
            self.ui.usernameInput.setText("")
            self.ui.passwordInput.setText("")
            self.ui.wrongCredentialLabel.hide()
            self.loggedIn.emit()
            return
        
        #Just in case if they wanted it
        self.ui.wrongCredentialLabel.setText(labelValue)
        self.ui.wrongCredentialLabel.show()
    ######