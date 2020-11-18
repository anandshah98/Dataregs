from PyQt5 import QtCore, QtWidgets, QtGui
import sys
import ctypes
import database
import subprocess


class Dataregs(QtWidgets.QMainWindow):

    def __init__(self, parent=None):        # create a basic template for the application
        try:
            QtWidgets.QMainWindow.__init__(self, parent)
            with open("styles.stylesheet", "r") as f:
                self.setStyleSheet(f.read())

            self.stack = QtWidgets.QStackedWidget(self)
            user32 = ctypes.windll.user32
            self.X, self.Y = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

            self.layout = QtWidgets.QWidget()
            self.layout.setObjectName("main")

            self.layout1 = QtWidgets.QWidget()
            self.layout1.setObjectName("table")

            self.tableWidget = QtWidgets.QTableWidget(self.layout1)

            self.titlelab = QtWidgets.QLabel("Dataregs", self.layout)
            self.titlelab.setGeometry(self.X/2 - 270, 0, 550, 175)
            self.titlelab.setObjectName("tl")

            self.frame = QtWidgets.QFrame(self.layout)
            self.frame.setGeometry(self.X/2 - 400, self.Y/2 - 380, 800, 800)

            self.item_name_text = QtWidgets.QLineEdit(self.frame)

            self.company_text = QtWidgets.QLineEdit(self.frame)

            self.affiliate_text = QtWidgets.QLineEdit(self.frame)

            self.quantity_text = QtWidgets.QLineEdit(self.frame)
            self.unit_select = QtWidgets.QComboBox(self.frame)

            self.amount_text = QtWidgets.QLineEdit(self.frame)
            self.currency_select = QtWidgets.QComboBox(self.frame)

            self.cash_flow = QtWidgets.QLabel("Cash flow", self.frame)
            self.cash_flow_select = QtWidgets.QComboBox(self.frame)

            self.transac_type = QtWidgets.QLabel("Transaction", self.frame)
            self.transac_type_select = QtWidgets.QComboBox(self.frame)

            self.item_type = QtWidgets.QLabel("Item type", self.frame)
            self.item_type_select = QtWidgets.QComboBox(self.frame)

            self.search_button = QtWidgets.QPushButton("Search", self.frame)
            self.insert_button = QtWidgets.QPushButton("Insert", self.frame)
            self.quit_button = QtWidgets.QPushButton("Quit", self.frame)
            self.reset_button = QtWidgets.QPushButton("Reset", self.frame)

            self.db = database.connect()
            database.open(self.db)

            self.setFocus()
            self.createform()

        except Exception as e:
            print(f"Error starting the application: {e}")
            sys.exit(-1)

    def createform(self):                       # create the startup page (page 1) of the application

        self.setWindowTitle("Dataregs-Transaction tracker")
        self.setWindowIcon(QtGui.QIcon("dataregs.png"))

        self.item_name_text.setGeometry(50, 40, 300, 75)
        self.item_name_text.setPlaceholderText("Item name")

        self.company_text.setGeometry(450, 40, 300, 75)
        self.company_text.setPlaceholderText("Company")

        self.quantity_text.setGeometry(50, 165, 175, 65)
        self.quantity_text.setValidator(QtGui.QDoubleValidator())
        self.quantity_text.setToolTip("Only Numeric entry allowed")
        self.quantity_text.setObjectName("qtext")
        self.quantity_text.setPlaceholderText("Quantity")
        self.quantity_text.setAlignment(QtCore.Qt.AlignCenter)

        self.unit_select.setGeometry(235, 165, 115, 65)
        self.unit_select.setObjectName("unitsel")
        self.unit_select.addItem("")
        self.unit_select.addItem("Unit(s)")
        self.unit_select.addItem("Kg(s)")
        self.unit_select.addItem("Lt(s)")

        self.amount_text.setGeometry(450, 165, 220, 65)
        self.amount_text.setValidator(QtGui.QDoubleValidator())
        self.amount_text.setToolTip("Only Numeric entry allowed")
        self.amount_text.setObjectName("amt")
        self.amount_text.setPlaceholderText("Amount")
        self.amount_text.setAlignment(QtCore.Qt.AlignCenter)

        self.currency_select.setGeometry(680, 165, 70, 65)
        self.currency_select.setObjectName("curr")
        self.currency_select.addItem("")
        self.currency_select.addItem("₹")
        self.currency_select.addItem("$")
        self.currency_select.addItem("€")
        self.currency_select.addItem("£")

        self.affiliate_text.setGeometry(50, 280, 300, 60)
        self.affiliate_text.setPlaceholderText("Affiliate")

        self.cash_flow.setGeometry(450, 280, 150, 60)
        self.cash_flow.setAlignment(QtCore.Qt.AlignCenter)
        self.cash_flow_select.setGeometry(610, 280, 140, 60)

        self.cash_flow_select.addItem("")
        self.cash_flow_select.addItem("Inflow")
        self.cash_flow_select.addItem("Outflow")
        self.cash_flow_select.addItem("Transfer")
        self.cash_flow_select.setProperty("cssClass", "combo")

        self.transac_type.setGeometry(50, 395, 160, 60)
        self.transac_type.setAlignment(QtCore.Qt.AlignCenter)
        self.transac_type_select.setGeometry(220, 395, 130, 60)
        self.transac_type_select.setProperty("cssClass", "combo")
        self.transac_type_select.addItem("")
        self.transac_type_select.addItem("Cash")
        self.transac_type_select.addItem("Card")
        self.transac_type_select.addItem("Cheque")
        self.transac_type_select.addItem("UPI")
        self.transac_type_select.addItem("Online")

        self.item_type.setGeometry(450, 395, 140, 60)
        self.item_type.setAlignment(QtCore.Qt.AlignCenter)
        self.item_type_select.setGeometry(600, 395, 155, 60)
        self.item_type_select.setProperty("cssClass", "combo")
        self.item_type_select.addItem("")
        self.item_type_select.addItem("Food")
        self.item_type_select.addItem("Luxury")
        self.item_type_select.addItem("Stationary")
        self.item_type_select.addItem("Fuel")
        self.item_type_select.addItem("Grocery")
        self.item_type_select.addItem("Others")
        self.item_type_select.addItem("Withdrawal")
        self.item_type_select.addItem("N.A.")

        splitter = QtWidgets.QSplitter(self.frame)
        splitter.setGeometry(0, 500, 800, 1)

        self.insert_button.setGeometry(150, 575, 200, 70)
        self.insert_button.setToolTip("Press Enter")
        self.insert_button.setShortcut(QtCore.Qt.Key_Return)
        self.insert_button.clicked.connect(self.insertentry)
        self.insert_button.setProperty("cssClass", "button")

        self.search_button.setGeometry(150, 700, 200, 70)
        self.search_button.setToolTip("Ctrl + F")
        self.search_button.setShortcut(QtGui.QKeySequence("Ctrl+F"))
        self.search_button.clicked.connect(self.refresh)
        self.search_button.setProperty("cssClass", "button")

        self.reset_button.setGeometry(445, 575, 200, 70)
        self.reset_button.setToolTip("Ctrl + R")
        self.reset_button.setShortcut(QtGui.QKeySequence("Ctrl+R"))
        self.reset_button.clicked.connect(self.resetapp)
        self.reset_button.setProperty("cssClass", "button")

        self.quit_button.setGeometry(445, 700, 200, 70)
        self.quit_button.setToolTip("Ctrl + Q")
        self.quit_button.setShortcut(QtGui.QKeySequence("Ctrl+Q"))
        self.quit_button.clicked.connect(self.quitapp)
        self.quit_button.setProperty("cssClass", "button")

        help_button = QtWidgets.QPushButton("?", self.frame)
        help_button.setShortcut(QtGui.QKeySequence("Ctrl+H"))
        help_button.clicked.connect(self.dialogs)
        help_button.setToolTip("Ctrl + H")
        help_button.setObjectName("help")
        help_button.setGeometry(775, 0, 25, 25)

        self.layout.setTabOrder(self.item_name_text, self.company_text)
        self.layout.setTabOrder(self.company_text, self.quantity_text)
        self.layout.setTabOrder(self.quantity_text, self.unit_select)
        self.layout.setTabOrder(self.unit_select, self.amount_text)
        self.layout.setTabOrder(self.amount_text, self.currency_select)
        self.layout.setTabOrder(self.currency_select, self.affiliate_text)
        self.layout.setTabOrder(self.affiliate_text, self.cash_flow_select)
        self.layout.setTabOrder(self.cash_flow_select, self.transac_type_select)
        self.layout.setTabOrder(self.transac_type_select, self.item_type_select)
        self.layout.setTabOrder(self.item_type_select, self.search_button)
        self.layout.setTabOrder(self.search_button, self.insert_button)
        self.layout.setTabOrder(self.insert_button, self.reset_button)
        self.layout.setTabOrder(self.reset_button, self.quit_button)
        self.layout.setTabOrder(self.quit_button, help_button)
        self.layout.setTabOrder(help_button, self.item_name_text)

        self.setGeometry(0, 40, self.X, self.Y)
        self.setFixedSize(QtCore.QSize(self.X, self.Y))

        self.stack.addWidget(self.layout)
        self.setCentralWidget(self.stack)
        self.item_name_text.setFocus()
        self.stack.setCurrentIndex(0)
        self.show()

    def quitapp(self):                  # function to quite app

        choice = QtWidgets.QMessageBox.question(self, "Quit", "Are you sure?", QtWidgets.QMessageBox.Yes,
                                                QtWidgets.QMessageBox.No)
        if choice == QtWidgets.QMessageBox.Yes:
            sys.exit()

        else:
            pass

    def resetapp(self):                # function to reset details on startup page

        self.amount_text.setText('')
        self.item_name_text.setText('')
        self.quantity_text.setText('')
        self.company_text.setText('')
        self.affiliate_text.setText('')
        self.cash_flow_select.setCurrentIndex(0)
        self.transac_type_select.setCurrentIndex(0)
        self.item_type_select.setCurrentIndex(0)
        self.currency_select.setCurrentIndex(0)
        self.unit_select.setCurrentIndex(0)
        self.item_name_text.setFocus()

    def dialogs(self):

        subprocess.Popen(["notepad.exe", "help1.txt"])

    def dialogs1(self):

        subprocess.Popen(["notepad.exe", "help2.txt"])

    def changewindow(self):                     # change from details page to home page

        choice = QtWidgets.QMessageBox.question(self, "Confirm", "Return to Insert page?",
                                                QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if choice == QtWidgets.QMessageBox.Yes:
            self.stack.setCurrentIndex(0)
            self.item_name_text.setFocus()

    def insertentry(self):                      # function to handle data insertion
        item = self.item_name_text.text().upper()
        comp = self.company_text.text().upper()
        quant = self.quantity_text.text()
        unit = self.unit_select.currentText().upper()
        amt = self.amount_text.text()
        currency = self.currency_select.currentText()
        aff = self.affiliate_text.text().upper()
        flow = self.cash_flow_select.currentText().upper()
        stat = self.transac_type_select.currentText().upper()
        itemtype = self.item_type_select.currentText().upper()

        try:
            if item != '' and not (amt == '' or amt == 0) and type(float(amt)) not in [str, dict, list] and not (quant == '' or quant == 0) and type(float(quant)) not in [str, dict, list] and unit != "" and currency != "" and flow != "" and stat != "" and itemtype != "":
                details = {'item': item, 'comp': comp, 'quant': quant, 'unit': unit, 'amt': amt, 'currency': currency,
                           'aff': aff, 'flow': flow, 'stat': stat, 'itemtype': itemtype}
                database.insert(self.db, details)
                self.resetapp()
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Only Affiliate and Company field can be empty", QtWidgets.QMessageBox.Ok)

        except:
            QtWidgets.QMessageBox.warning(self, "Error", "Information doesn't satisfy requirements", QtWidgets.QMessageBox.Ok)

    def searchitems(self):                  # create 'Details' (page 2) page based on the search results

        with open("button.stylesheet", "r") as f:
            buttons = f.read()
        self.layout1.setStyleSheet(buttons)
        self.setGeometry(0, 40, self.X, self.Y)
        self.setFixedSize(QtCore.QSize(self.X, self.Y))

        back = QtWidgets.QPushButton("Back", self.layout1)
        back.setGeometry(self.X - 140, 130, 105, 60)
        back.setShortcut(QtGui.QKeySequence("Ctrl+B"))
        back.setToolTip("Ctrl + B")
        back.clicked.connect(self.changewindow)

        ref = QtWidgets.QPushButton("Refresh", self.layout1)
        ref.setGeometry(self.X - 140, 330, 105, 60)
        ref.setShortcut(QtGui.QKeySequence("Ctrl+R"))
        ref.setToolTip("Ctrl + R")
        ref.clicked.connect(self.refresh)

        helpb = QtWidgets.QPushButton("Help", self.layout1)
        helpb.setGeometry(self.X - 140, 530, 105, 60)
        helpb.setShortcut(QtGui.QKeySequence("Ctrl+H"))
        helpb.setToolTip("Ctrl + H")
        helpb.clicked.connect(self.dialogs1)

        quitb = QtWidgets.QPushButton("Quit", self.layout1)
        quitb.setGeometry(self.X - 140, 730, 105, 60)
        quitb.setShortcut(QtGui.QKeySequence("Ctrl+Q"))
        quitb.clicked.connect(self.quitapp)

        self.tableWidget.setGeometry(100, 50, self.X - 270, self.Y - 150)
        self.tableWidget.setFixedSize(QtCore.QSize(self.X - 270, self.Y - 150))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(14)
        self.tableWidget.setFocus()
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.CurrentChanged)

        results = self.searchentry()
        self.tableWidget.setRowCount(len(results))

        for i, query in enumerate(results):
            for j in range(11):
                temp = QtWidgets.QTableWidgetItem()
                if j in [3, 5, 7, 8, 9, 10]:
                    temp.setFlags(QtCore.Qt.ItemIsEditable)
                if j in [0, 1, 6]:
                    temp.setText(query[j + 1].title())
                elif j == 10:
                    temp.setText(query[j + 1].split(".")[0])
                else:
                    temp.setText(str(query[j + 1]))
                temp.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setItem(i, j, temp)

            but1 = QtWidgets.QPushButton(self.layout1)
            but1.clicked.connect(self.delitems)
            but1.setToolTip("Ctrl + D")
            but1.setProperty("cssClass", "deled")
            but1.setText("Delete")
            self.tableWidget.setCellWidget(i, 11, but1)

            but2 = QtWidgets.QPushButton(self.layout1)
            but2.clicked.connect(self.edititems)
            but2.setToolTip("Press Enter")
            but2.setProperty("cssClass", "deled")
            but2.setText("Edit")
            self.tableWidget.setCellWidget(i, 12, but2)

            idtag = QtWidgets.QTableWidgetItem()
            idtag.setText(str(query[0]))
            self.tableWidget.setItem(i, 13, idtag)

        self.tableWidget.hideColumn(13)
        edit = QtWidgets.QShortcut(QtCore.Qt.Key_Return, self.layout1)
        edit.activated.connect(self.edititems)
        delete = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+D"), self.layout1)
        delete.activated.connect(self.delitems)

        self.tableWidget.setHorizontalHeaderLabels(['Name', 'Company', 'Quantity', 'Unit', 'Amount', '', 'Affiliate', 'Cash Flow', 'Transaction in', 'Item type', 'Time', 'Click to\ndelete', 'Click to\nedit'])
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.setColumnWidth(0, 250)
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.setColumnWidth(2, 80)
        self.tableWidget.setColumnWidth(3, 100)
        self.tableWidget.setColumnWidth(4, 100)
        self.tableWidget.setColumnWidth(5, 50)
        self.tableWidget.setColumnWidth(6, 80)
        self.tableWidget.setColumnWidth(7, 120)
        self.tableWidget.setColumnWidth(8, 140)
        self.tableWidget.setColumnWidth(9, 110)
        self.tableWidget.setColumnWidth(10, 203)
        self.tableWidget.setColumnWidth(11, 75)
        self.tableWidget.setColumnWidth(12, 75)

        self.stack.addWidget(self.layout1)
        self.stack.setCurrentIndex(1)
        self.show()

    def refresh(self):                          # function to refresh details page
        self.stack.removeWidget(self.layout1)
        self.layout1 = QtWidgets.QWidget()
        self.layout1.setObjectName("table")
        self.tableWidget = QtWidgets.QTableWidget(self.layout1)
        self.searchitems()

    def delitems(self):                         # handles delete operation for page 2
        row = self.tableWidget.currentIndex().row()
        self.tableWidget.selectRow(row)
        choice = QtWidgets.QMessageBox.question(self, "Confirm", "Are you sure you want to delete the highlighted row?", QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if choice == QtWidgets.QMessageBox.Yes:
            row = self.tableWidget.currentIndex().row()
            idtag = self.tableWidget.item(row, 13).text()
            database.delete(self.db, idtag)
            self.tableWidget.removeRow(row)
            QtWidgets.QMessageBox.information(self.layout1, "Success", "Item deleted")

    def edititems(self):                        # handles edit operation for page 2

        row = self.tableWidget.currentIndex().row()
        self.tableWidget.selectRow(row)
        choice = QtWidgets.QMessageBox.question(self, "Confirm", "Are you sure you want to update the changes\nin the highlighted row?", QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)

        try:
            if choice == QtWidgets.QMessageBox.Yes:
                idtag = self.tableWidget.item(row, 13).text()
                item = self.tableWidget.item(row, 0).text().upper()
                company = self.tableWidget.item(row, 1).text().upper()
                quantity = self.tableWidget.item(row, 2).text().upper()
                unit = self.tableWidget.item(row, 3).text().upper()
                amount = self.tableWidget.item(row, 4).text().upper()
                curr = self.tableWidget.item(row, 5).text().upper()
                aff = self.tableWidget.item(row, 6).text().upper()
                cashflow = self.tableWidget.item(row, 7).text().upper()
                transac = self.tableWidget.item(row, 8).text().upper()
                itemtype = self.tableWidget.item(row, 9).text().upper()
                vals = [item, company, quantity, unit, amount, curr, aff, cashflow, transac, itemtype]

                if database.edit(self.db, vals, idtag):
                    self.tableWidget.item(row, 0).setText(item.title())
                    self.tableWidget.item(row, 1).setText(company.title())
                    self.tableWidget.item(row, 2).setText(quantity)
                    self.tableWidget.item(row, 3).setText(unit)
                    self.tableWidget.item(row, 4).setText(amount)
                    self.tableWidget.item(row, 5).setText(curr)
                    self.tableWidget.item(row, 6).setText(aff.title())
                    self.tableWidget.item(row, 7).setText(cashflow)
                    self.tableWidget.item(row, 8).setText(transac)
                    self.tableWidget.item(row, 9).setText(itemtype)
                    self.tableWidget.clearFocus()
                    QtWidgets.QMessageBox.information(self.layout1, "Success", "Item edited")

                else:
                    QtWidgets.QMessageBox.information(self.layout1, "Error", "Only Company and Affiliate columns can be empty.\nReverting to details window")
                    self.refresh()

        except:
            QtWidgets.QMessageBox.information(self.layout1, "Error", "Only numeric entry accepted in Amount and Quantity fields")
            self.searchitems()

    def searchentry(self):                          # function to help retrieve results based on search criteria

        item = self.item_name_text.text().upper()
        comp = self.company_text.text().upper()
        quant = self.quantity_text.text()
        unit = self.unit_select.currentText().upper()
        amt = self.amount_text.text()
        currency = self.currency_select.currentText()
        aff = self.affiliate_text.text().upper()
        flow = self.cash_flow_select.currentText().upper()
        stat = self.transac_type_select.currentText().upper()
        itemtype = self.item_type_select.currentText().upper()

        vals = [item, comp, quant, unit, amt, currency, aff, flow, stat, itemtype]
        queryresult = database.search(self.db, vals)
        return queryresult


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Main = QtWidgets.QMainWindow()
    startd = Dataregs(Main)
    sys.exit(app.exec_())