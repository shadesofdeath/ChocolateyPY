# import os
# import subprocess
# from colorama import Fore, Style, init
# init()
# print("────────────────────────────────────")
# print("  ChocolateyPY - Chocolatey Script")
# print("────────────────────────────────────")

# class ChocolateyPY:
#     choco_installed = os.path.exists(r"C:\ProgramData\chocolatey\choco.exe")
#     if not choco_installed:
#         print(Fore.RED + "Sisteminizde Chocolatey kurulu olmadığı tespit edildi." + Style.RESET_ALL)
#         install_choice = input("Chocolatey kurulsun mu? (E/H): ")
#         if install_choice.lower() == "e":
#             os.system("cls")
#             print(Fore.YELLOW + "Chocolatey kuruluyor..." + Style.RESET_ALL)
#             subprocess.call("powershell -Command \"Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))\"", shell=True)
#             os.system("cls")
#             print(Fore.GREEN + "Chocolatey kurulumu tamamlandı." + Style.RESET_ALL)
#             print()
#             print()
#             print(" ──────▄▌▐▀▀▀▀▀▀▀▀▀▀▀▀▌")
#             print(" ───▄▄██▌█░░░░░░░░░░░░▐")
#             print(" ▄▄▄▌▐██▌█░░░░░░░░░░░░▐")
#             print(" ███████▌█▄▄▄▄▄▄▄▄▄▄▄▄▌")
#             print(" ▀❍▀▀▀▀▀▀▀❍❍▀▀▀▀▀▀❍❍▀")
#         else:
#             os.system("cls")
#             print(Fore.RED + "Chocolatey kurulmadı. Bu uygulama çalışmayacaktır." + Style.RESET_ALL)
#             print(" ▄██████████████▄▐█▄▄▄▄█▌")
#             print(" ██████▌▄▌▄▐▐▌███▌▀▀██▀▀")
#             print(" ████▄█▌▄▌▄▐▐▌▀███▄▄█▌")
#             print(" ▄▄▄▄▄██████████████▀")
#             input()
#             exit()
#     os.system("cls")
#     print("────────────────────────────────────")
#     print("  ChocolateyPY - Chocolatey Script")
#     print("────────────────────────────────────")
#     app_name = input("İndirmek istediğiniz uygulamanın adını girin: ")
#     search_result = subprocess.check_output(f"choco search {app_name}", shell=True).decode("utf-8")
#     search_result = search_result.split("\n")
#     packages = []
#     for line in search_result:
#         if line.startswith("Chocolatey"):
#             continue
#         package_name = line.split("|")[0].strip()
#         packages.append(package_name)
#     print(Fore.CYAN + "Arama sonuçları:" + Style.RESET_ALL)
#     for i, package in enumerate(packages):
#         print(f"{Fore.YELLOW}{i + 1}. {package}{Style.RESET_ALL}")
#     print("────────────────────────────────────────────────")
#     package_choice = int(input("Kurmak istediğiniz uygulamanın numarasını girin: "))
#     package_to_install = packages[package_choice - 1]
#     subprocess.call(f"choco install {package_to_install} -y --force --ignore-checksums", shell=True)
# ChocolateyPY()
import sys
import subprocess
from PyQt6 import QtWidgets, QtCore, QtGui 
from PyQt6.QtWidgets import QMessageBox, QFileDialog

class ChocolateyInstaller(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.label = QtWidgets.QLabel('Uygulama adını girin:')
        self.input = QtWidgets.QLineEdit()
        self.button = QtWidgets.QPushButton('Ara')
        self.listWidget = QtWidgets.QListWidget()
        self.logOutput = QtWidgets.QPlainTextEdit()
        self.outputLabel = QtWidgets.QLabel("Çıktı:")
        self.packageInfo = QtWidgets.QLabel()

        # burada önce self.updateButton öğesini tanımlamamız gerekiyor.
        self.updateButton = QtWidgets.QPushButton('Tüm Uygulamaları Güncelle')
        self.updateButton.clicked.connect(self.updateAll)

        self.button.clicked.connect(self.searchChocolatey)
        self.listWidget.itemClicked.connect(self.installPackage)
        
        inputLayout = QtWidgets.QHBoxLayout()
        inputLayout.addWidget(self.label)
        inputLayout.addWidget(self.input)
        inputLayout.addWidget(self.button)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addLayout(inputLayout)
        mainLayout.addWidget(self.packageInfo)
        mainLayout.addWidget(self.listWidget)
        mainLayout.addWidget(self.outputLabel)
        mainLayout.addWidget(self.logOutput)
        mainLayout.addWidget(self.updateButton)
        
        self.setLayout(mainLayout)
        self.setStyleSheet("""
            QLineEdit {
                border: 1.0px solid #D8D8D8;
                border-radius: 10px;
                font-family: Verdana;
                padding: 5px 10px;
                
            }

            QPushButton {
                background-color: #943126   ;
                color: white;
                font-family: Verdana;
                border-radius: 10px;
                padding: 5px 15px;
                border: 1.0px solid #D8D8D8;
            }

            QPushButton:hover {
                background-color: #7B241C ;
                font-family: Verdana;
                border: 1.0px solid #D8D8D8;
                border-radius: 10px;
                
            }
            QPlainTextEdit {
                font-size: 10px;
                border-radius: 10px;
                font-family: Verdana;
                border: 0.5px solid #D8D8D8;
            }

            QPlainTextEdit[lineNumber=true] > QPlainTextEditViewport {
                border-right-color: #ccc;
                border-right-width: 1px;
                font-family: Verdana;
                border-right-style: solid;
                border-radius: 10px;
                line-number-color: #999;
                line-number-background-color: #f7f7f7;
                line-number-width: 40px;
            }

            QPlainTextEdit {
                font-size: 10px;
                font-family: Verdana;
                background-color: #f7f7f7;
                border: 0.5px solid #D8D8D8;
                padding: 5px;
                border-radius: 10px;
            }
            QListWidget {
                font-size: 10px;
                font-family: Verdana;
                background-color: #f7f7f7;
                border: 0.5px solid #D8D8D8;
                padding: 5px;
                border-radius: 9px;
            }
            QLabel {
                font-size: 13px;
                font-family: Verdana;
            }
        """)
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.setWindowTitle('ChocolateyPY v1.0')
        self.setWindowIcon(QtGui.QIcon('logo.ico'))
        self.setGeometry(450, 200, 550, 500)
        self.show()

    def searchChocolatey(self):
        package_name = self.input.text()
        result = subprocess.check_output(
            ['choco', 'search', package_name], encoding='ISO-8859-1')
        lines = result.split('\n')
        packages = []
        for line in lines:
            if package_name.lower() in line.lower():
                package = line.split(' ')[0].strip()
                if package:
                    packages.append(package)

        self.listWidget.clear()
        self.listWidget.addItems(packages)

    def installPackage(self, item):
        package_name = item.text()
        reply = QtWidgets.QMessageBox.question(self, 'Uygulama Kurulumu', f"{package_name} Uygulamayı yüklemek istediğinizden emin misiniz?",QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No, QtWidgets.QMessageBox.StandardButton.No)
        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            self.progress = QtWidgets.QProgressDialog(
                "Uygulama Kurulumu", "iptal", 0, 100, self)
            self.progress.setWindowModality(
                QtCore.Qt.WindowModality.ApplicationModal)
            self.progress.show()

            process = subprocess.Popen(['choco', 'install', package_name, '-y', '--force','--ignore-checksums'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            while True:
                output = process.stdout.readline().decode(sys.stdout.encoding, errors='ignore')
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.progress.setValue(self.progress.value() + 1)
                    self.logOutput.appendPlainText(output.strip())
                    if 'Reading package info' in output:
                        self.packageInfo.setText(output.strip())
            self.progress.setValue(100)

    def updateAll(self):
        reply = QtWidgets.QMessageBox.question(self, 'Tüm Uygulamaları Güncelle', "Tüm uygulamaları güncellemek istediğinizden emin misiniz?", QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No, QtWidgets.QMessageBox.StandardButton.No)
        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            self.progress = QtWidgets.QProgressDialog("Tüm Uygulamaları Güncelle", "İptal", 0, 100, self)
            self.progress.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
            self.progress.show()

            process = subprocess.Popen(['choco', 'upgrade', 'all', '-y','--force', '--ignore-checksums'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            while True:
                output = process.stdout.readline().decode(sys.stdout.encoding, errors='ignore')
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.progress.setValue(self.progress.value() + 1)
                    self.logOutput.appendPlainText(output.strip())
                    if 'Reading package info' in output:
                        self.packageInfo.setText(output.strip())
            self.progress.setValue(100)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('logo.ico'))
    ex = ChocolateyInstaller()
    sys.exit(app.exec())
