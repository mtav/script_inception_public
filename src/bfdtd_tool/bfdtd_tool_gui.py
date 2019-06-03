#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import (pyqtSignal, QAbstractListModel, QDir, QLibraryInfo, QModelIndex, Qt, QSettings)
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit, QListView, QSizePolicy, QTextBrowser, QWidget, QFileDialog, QMessageBox, QTableWidgetItem, QTableWidgetSelectionRange)
from PyQt5.QtCore import QAbstractListModel, QStringListModel, QItemSelectionModel, QVariant
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QListWidgetItem

from bfdtd_tool_mainwindow import Ui_MainWindow

import os
import sys
import tempfile

from bfdtd.bfdtd_parser import BFDTDobject
from constants.physcon import get_c0
from utilities.harminv import getFrequencies

# Notes:
# Generate new .py file from .ui file using:
#  pyuic5 bfdtd_tool.ui -o bfdtd_tool_mainwindow.py
#  pyuic5 bfdtd_tool.ui -o bfdtd_tool_mainwindow.py && ./bfdtd_tool_gui.py

# To force terminate:
#  ps aux | grep bfdtd_tool_gui | grep -v grep | awk '{print $2}' | xargs kill

# Use assistant or assistant-qt5 for help/documentation. (Add new .qch files via edit->preferences->documentation)

# TODO: How to select rows?

def selectRow(table_widget, row):
  #item = table_widget.item(row, 0)
  #table_widget.setCurrentItem(item, QItemSelectionModel.Rows)
  table_widget.selectRow(row)

  #for col in range(table_widget.columnCount()):
    #item = table_widget.item(row, col)
    #table_widget.setCurrentItem(item, QItemSelectionModel.Rows)
  #myrange = QTableWidgetSelectionRange(row, 0, row, self.tableWidget_Frequencies.columnCount())
  #self.tableWidget_Frequencies.setRangeSelected(myrange, True)
  return

def getRowFloat(table_widget, row):
  row_contents = table_widget.columnCount()*[0]
  for col in range(table_widget.columnCount()):
    row_contents[col] = float(table_widget.item(row, col).text())
  return row_contents

def setRowFloat(table_widget, row, row_contents):

    #freq = self.tableWidget_Frequencies.rowCount()-1
    #wavelength = self.tableWidget_Frequencies.rowCount()-1
    #freq_item = QTableWidgetItem()
    #wavelength_item = QTableWidgetItem()
    #freq_item.setData(Qt.DisplayRole, freq)
    #wavelength_item.setData(Qt.DisplayRole, wavelength)
    #self.tableWidget_Frequencies.setItem(self.tableWidget_Frequencies.rowCount()-1, 0, freq_item )
    #self.tableWidget_Frequencies.setItem(self.tableWidget_Frequencies.rowCount()-1, 1, wavelength_item )

  for col in range(table_widget.columnCount()):
    item = QTableWidgetItem()
    item.setData(Qt.DisplayRole, float(row_contents[col]))
    table_widget.setItem(row, col, item)
    
    #item = table_widget.item(row, col)
  return

def getRow(table_widget, row):
  row_contents = table_widget.columnCount()*[0]

  #for col in range(table_widget.columnCount()):
    #row_contents[col] = float(table_widget.item(row, col).text())

  row_contents[0] = float(table_widget.item(row, 0).text())
  row_contents[1] = float(table_widget.item(row, 1).text())
  row_contents[2] = table_widget.item(row, 2).text()

  return row_contents

def setRow(table_widget, row, row_contents):
  item = QTableWidgetItem()
  item.setData(Qt.DisplayRole, row_contents[0])
  table_widget.setItem(row, 0, item)

  item = QTableWidgetItem()
  item.setData(Qt.DisplayRole, row_contents[2])
  table_widget.setItem(row, 2, item)

  #for col in range(table_widget.columnCount()):
    #item = QTableWidgetItem()
    #item.setData(Qt.DisplayRole, row_contents[col])
    #table_widget.setItem(row, col, item)
  return

def getRowItems(table_widget, row):
  row_contents = table_widget.columnCount()*[0]
  for col in range(table_widget.columnCount()):
    row_contents[col] = table_widget.item(row, col)
  return row_contents

def setRowItems(table_widget, row, row_contents):
  for col in range(table_widget.columnCount()):
    table_widget.setItem(row, col, row_contents[col])
  return

#class FileListModel(QAbstractListModel):
  #numberPopulated = pyqtSignal(int)

  #def __init__(self, parent=None):
      #super(FileListModel, self).__init__(parent)

      #self.fileCount = 0    
      #self.fileList = []

  #def rowCount(self, parent=QModelIndex()):
      #return self.fileCount

  #def data(self, index, role=Qt.DisplayRole):
      #if not index.isValid():
          #return None

      #if index.row() >= len(self.fileList) or index.row() < 0:
          #return None

      #if role == Qt.DisplayRole:
          #return self.fileList[index.row()]

      #if role == Qt.BackgroundRole:
          #batch = (index.row() // 100) % 2
          #if batch == 0:
              #return QApplication.palette().base()

          #return QApplication.palette().alternateBase()

      #return None

  #def canFetchMore(self, index):
      #return self.fileCount < len(self.fileList)

  #def fetchMore(self, index):
      #remainder = len(self.fileList) - self.fileCount
      #itemsToFetch = min(100, remainder)

      #self.beginInsertRows(QModelIndex(), self.fileCount,
              #self.fileCount + itemsToFetch)

      #self.fileCount += itemsToFetch

      #self.endInsertRows()

      #self.numberPopulated.emit(itemsToFetch)

  #def setDirPath(self, path):
      #dir = QDir(path)

      #self.beginResetModel()
      #self.fileList = dir.entryList()
      #self.fileCount = 0
      #self.endResetModel()

  #def addInputFiles(self, files_to_add):
    ##print(('LOLO', files_to_add))
    ##self.beginResetModel()
    ##self.fileList = files_to_add
    ##self.fileCount = 0
    ##self.endResetModel()

    #self.beginInsertRows(QModelIndex(), len(self.fileList), len(self.fileList)+len(files_to_add)-1)
    #self.fileCount = len(self.fileList)
    ##print(self.fileList)
    #self.fileList += files_to_add
    ##print(self.fileList)
    ##self.pixmaps.insert(row, pixmap)
    ##self.locations.insert(row, location)
    #self.endInsertRows()
    
  #def removeRow():
    #return False
    
class BFDTDtoolMainWindow(QMainWindow, Ui_MainWindow):
  def __init__(self):
    super(BFDTDtoolMainWindow, self).__init__()

    # Set up the user interface from Designer.
    self.setupUi(self)

    # Connect up the buttons.
    self.pushButton_addInputFiles.clicked.connect(self.addInputFiles)
    self.pushButton_removeInputFiles.clicked.connect(self.removeInputFiles)

    self.pushButton_moveInputFileUp.clicked.connect(self.moveInputFileUp)
    self.pushButton_moveInputFileDown.clicked.connect(self.moveInputFileDown)
    self.pushButton_loadInputFiles.clicked.connect(self.loadInputFiles)
    
    self.actionSaveConfig.triggered.connect(self.SaveConfig)
    self.actionSaveConfigAs.triggered.connect(self.SaveConfigAs)
    self.actionLoadConfig.triggered.connect(self.LoadConfig)
    
    self.pushButton_AddFrequency.clicked.connect(self.AddFrequencyButtonClicked)
    self.pushButton_AddFrequencyFromFrequencyList.clicked.connect(self.AddFrequencyFromFrequencyList)
    self.pushButton_AddFrequencyFromInpFile.clicked.connect(self.AddFrequencyFromInpFile)
    self.pushButton_RemoveFrequency.clicked.connect(self.RemoveFrequency)
    self.pushButton_moveFrequencyUp.clicked.connect(self.moveFrequencyUp)
    self.pushButton_moveFrequencyDown.clicked.connect(self.moveFrequencyDown)
    self.pushButton_clearFrequencyList.clicked.connect(self.clearFrequencyList)
    
    self.pushButton_SelectOutputDirectory.clicked.connect(self.SelectOutputDirectory)
    
    self.comboBox_ObjectLocation.currentIndexChanged.connect(self.updateLocation)
    
    self.pushButton_Run.clicked.connect(self.Run)

    self.radioButton_ObjectLocation.toggled.connect(self.radioButton_ObjectLocation_toggled)
    
    self.ignoreChange = False
    self.tableWidget_Frequencies.cellChanged.connect(self.FreqTableChanged)
    self.tableWidget_Frequencies.verticalHeader().setSectionsMovable(True)
    
    #self.model_InputFiles = FileListModel(self)
    
    self.BFDTD_object = BFDTDobject()
    self.object_list = []
    
    self.ConfigFileName = None

    # default directories for the various filedialogs
    self.default_dir_InputDir = os.path.expanduser("~")
    self.default_dir_Config = os.path.expanduser("~")
    self.default_dir_OutputDir = os.path.expanduser("~")

    #self.model_InputFiles = QStringListModel(self)
    
    #self.listView_InputFiles.setModel(self.model_InputFiles)
    
    
        #item = QtWidgets.QListWidgetItem()
        #self.listWidget_InputFiles.addItem(item)
        #item = QtWidgets.QListWidgetItem()
        #self.listWidget_InputFiles.addItem(item)
        
    #item = QtWidgets.QListWidgetItem()
    #item.setText('ROFFLLOLLOOL')
    #self.listWidget_InputFiles.addItem(item)
    #self.listWidget_InputFiles.addItems(['jijuijij', '454654', 'jijfsdfsdij'])

        #__sortingEnabled = self.listWidget_InputFiles.isSortingEnabled()
        #self.listWidget_InputFiles.setSortingEnabled(False)
        #item = self.listWidget_InputFiles.item(0)
        #item.setText(_translate("MainWindow", "New Item"))
        #item = self.listWidget_InputFiles.item(1)
        #item.setText(_translate("MainWindow", "gdf"))
        #item = self.listWidget_InputFiles.item(2)
        #item.setText(_translate("MainWindow", "New gdfg"))
        #self.listWidget_InputFiles.setSortingEnabled(__sortingEnabled)

    #lol = QListWidgetItem("Sycamore", self.listView_InputFiles);
    #QListWidgetItem("Chestnut"), listWidget);
    #QListWidgetItem("Mahogany"), listWidget);
    
    #QListWidgetItem *newItem = new QListWidgetItem;
    #newItem->setText(itemText);
    #listWidget->insertItem(row, newItem);
    self.readSettings()

  def radioButton_ObjectLocation_toggled(self, checked):
    if checked:
      self.lineEdit_X.setReadOnly(True)
      self.lineEdit_Y.setReadOnly(True)
      self.lineEdit_Z.setReadOnly(True)
      self.updateLocation()
    else:
      self.lineEdit_X.setReadOnly(False)
      self.lineEdit_Y.setReadOnly(False)
      self.lineEdit_Z.setReadOnly(False)
      
    return

  def FreqTableChanged(self, row, column):
    print('Change at ({}, {})'.format(row, column))
    if not self.ignoreChange:
      self.ignoreChange = True
      if column == 0:
        freq = float(self.tableWidget_Frequencies.item(row, 0).text())
        wavelength = get_c0()/freq
        item = QTableWidgetItem()
        item.setData(Qt.DisplayRole, wavelength)
        self.tableWidget_Frequencies.setItem(row, 1, item)
      elif column == 1:
        wavelength = float(self.tableWidget_Frequencies.item(row, 1).text())
        freq = get_c0()/wavelength
        item = QTableWidgetItem()
        item.setData(Qt.DisplayRole, freq)
        self.tableWidget_Frequencies.setItem(row, 0, item)
    self.ignoreChange = False

  def addInputFiles(self):
    print('self.default_dir_InputDir = {}'.format(self.default_dir_InputDir))
    (files_to_add, selected_filter) = QtWidgets.QFileDialog.getOpenFileNames(parent=self, caption='Add BFDTD input files', filter='BFDTD input files (*.in *.geo *.inp);; All Files(*)', directory=self.default_dir_InputDir)
    if files_to_add:
      print('Setting self.default_dir_InputDir to {}'.format(files_to_add[0]))
      self.default_dir_InputDir = files_to_add[0]
      print('self.default_dir_InputDir = {}'.format(self.default_dir_InputDir))
    
    if not self.checkBox_DirectLoad.isChecked():
      self.listWidget_InputFiles.addItems(files_to_add)
    else:
      self.listWidget_InputFiles.clear()
      self.listWidget_InputFiles.addItems(files_to_add)
      self.loadInputFiles()

    #for i in files_to_add:
      #item = QtWidgets.QListWidgetItem()
      #item.setText(i)
      #self.listWidget_InputFiles.addItem(item)      

    #print((files_to_add, dirname))
    #self.model_InputFiles.setStringList(files_to_add)
    #self.model_InputFiles.addInputFiles(files_to_add)

  def removeInputFiles(self):
    #print('A')
    #self.listWidget_InputFiles.selectedItems()
    #print('B')
    for i in self.listWidget_InputFiles.selectedItems():
      self.listWidget_InputFiles.takeItem(self.listWidget_InputFiles.row(i))
    #self.listWidget_InputFiles.removeItemWidget(self.listWidget_InputFiles.currentItem())
    
    #index = self.listView_InputFiles.selectionModel().currentIndex()
    #model = self.listView_InputFiles.model()
    
    #print(index)
    #print(index.row())

    #if (model.removeRow(index.row(), index.parent())):
      #print('YIPPIKAYAY!!!')
      ##self.updateActions()

  def moveInputFileUp(self):
    current_selection = self.listWidget_InputFiles.selectedItems()
    selected_rows = []
    for item in current_selection:
      selected_rows.append(self.listWidget_InputFiles.row(item))
      
    selected_rows.sort(reverse=False)
    
    for row in selected_rows:
      item = self.listWidget_InputFiles.takeItem(row)
      self.listWidget_InputFiles.insertItem(row-1, item)
      self.listWidget_InputFiles.setCurrentItem(item, QItemSelectionModel.SelectCurrent)


    #current_selection = self.listWidget_InputFiles.selectedItems()
    #for i in current_selection:
      #current_row = self.listWidget_InputFiles.row(i)
      #item = self.listWidget_InputFiles.takeItem(current_row)
      #self.listWidget_InputFiles.insertItem(current_row-1, item)
      #self.listWidget_InputFiles.setCurrentItem(item, QItemSelectionModel.SelectCurrent)
    return
    
  def moveInputFileDown(self):
    current_selection = self.listWidget_InputFiles.selectedItems()
    selected_rows = []
    for item in current_selection:
      selected_rows.append(self.listWidget_InputFiles.row(item))
      
    selected_rows.sort(reverse=True)
    
    for row in selected_rows:
      item = self.listWidget_InputFiles.takeItem(row)
      self.listWidget_InputFiles.insertItem(row+1, item)
      self.listWidget_InputFiles.setCurrentItem(item, QItemSelectionModel.SelectCurrent)
      
      #current_row = self.listWidget_InputFiles.row(i)
      #print((current_row, i.text()))
      #item = self.listWidget_InputFiles.takeItem(current_row)
      #self.listWidget_InputFiles.insertItem(current_row+1, item)
      #self.listWidget_InputFiles.setCurrentItem(item, QItemSelectionModel.SelectCurrent)
    return  
  
  def loadInputFiles(self):
    self.BFDTD_object = BFDTDobject()
    for row in range(self.listWidget_InputFiles.count()):
      input_file = self.listWidget_InputFiles.item(row).text()
      self.BFDTD_object.readBristolFDTD(input_file)
      
    self.lineEdit_Ncells.setText('{}'.format(self.BFDTD_object.getNcells()))

    # populate the object list
    self.object_list = self.BFDTD_object.getObjects()
    
    self.comboBox_ObjectLocation.clear()
    self.comboBox_ObjectLocation.addItems([i.getName() for i in self.object_list])    
    
    return

  def updateLocation(self, index=None):
    
    if index is None:
      index = self.comboBox_ObjectLocation.currentIndex()
      
    if self.radioButton_ObjectLocation.isChecked():
      if 0 <= index and index < len(self.object_list):
        print((index,len(self.object_list)))
        obj = self.object_list[index]
        loc = obj.getLocation()
        print(loc)
        self.lineEdit_X.setText(str(loc[0]))
        self.lineEdit_Y.setText(str(loc[1]))
        self.lineEdit_Z.setText(str(loc[2]))
    
    return

  def writeSettings(self, filename=None):
    
    if filename is None:
      settings = QSettings()
    else:
      settings = QSettings(filename, QSettings.IniFormat)
    
    settings.setValue("Niterations", self.spinBox_Niterations.value())
    settings.setValue("Walltime", self.spinBox_Walltime.value())
    
    Executable_List = [self.comboBox_Executable.itemText(i) for i in range(self.comboBox_Executable.count())]
    settings.setValue("Executable_List", Executable_List)
    
    settings.setValue("Executable_Index", self.comboBox_Executable.currentIndex())

    settings.setValue("BaseName", self.lineEdit_BaseName.text())
    settings.setValue("OutputDirectory", self.lineEdit_OutputDirectory.text())

    settings.setValue("lineEdit_X", self.lineEdit_X.text())
    settings.setValue("lineEdit_Y", self.lineEdit_Y.text())
    settings.setValue("lineEdit_Z", self.lineEdit_Z.text())

    settings.setValue("DirectLoad", self.checkBox_DirectLoad.isChecked())

    settings.setValue("Verbosity", self.spinBox_Verbosity.value())
    settings.setValue("StartingSample", self.spinBox_StartingSample.value())
    settings.setValue("First", self.spinBox_First.value())
    settings.setValue("Repetition", self.spinBox_Repetition.value())
    
    settings.setValue("Operation", self.comboBox_Operation.currentIndex())
    settings.setValue("ObjectLocation", self.comboBox_ObjectLocation.currentIndex())

    settings.setValue("ArbitraryLocation", self.radioButton_ArbitraryLocation.isChecked())
    
    settings.setValue("default_dir_Config", self.default_dir_Config)
    settings.setValue("default_dir_InputDir", self.default_dir_InputDir)
    settings.setValue("default_dir_OutputDir", self.default_dir_OutputDir)
    
    #self.radioButton_ObjectLocation.isChecked()

  def readSettings(self, filename=None):

    if filename is None:
      settings = QSettings()
    else:
      settings = QSettings(filename, QSettings.IniFormat)
    
    self.spinBox_Niterations.setValue(int(settings.value("Niterations", 1)))
    self.spinBox_Walltime.setValue(int(settings.value("Walltime", 1)))

    Executable_List = settings.value("Executable_List", ['fdtd64_2003', 'fdtd64_2008', 'fdtd64_2013', 'fdtd64_2013_dispersive', 'fdtd64_withRotation'])
    self.comboBox_Executable.clear()
    self.comboBox_Executable.addItems(Executable_List)
    
    self.comboBox_Executable.setCurrentIndex(int(settings.value("Executable_Index", 2)))

    self.lineEdit_BaseName.setText(settings.value("BaseName", 'sim'))
    self.lineEdit_OutputDirectory.setText(settings.value("OutputDirectory", tempfile.gettempdir()))

    self.lineEdit_X.setText(settings.value("lineEdit_X", '0'))
    self.lineEdit_Y.setText(settings.value("lineEdit_Y", '0'))
    self.lineEdit_Z.setText(settings.value("lineEdit_Z", '0'))

    self.checkBox_DirectLoad.setChecked(settings.value("DirectLoad", False, type=bool))

    self.spinBox_Verbosity.setValue(settings.value("Verbosity", 0, type=int))

    self.spinBox_StartingSample.setValue(settings.value("StartingSample", 1, type=int))
    self.spinBox_First.setValue(settings.value("First", 1, type=int))
    self.spinBox_Repetition.setValue(settings.value("Repetition", 1, type=int))
    
    self.comboBox_Operation.setCurrentIndex(settings.value("Operation", 0, type=int))
    self.comboBox_ObjectLocation.setCurrentIndex(settings.value("ObjectLocation", 0, type=int))

    self.radioButton_ArbitraryLocation.setChecked(settings.value("ArbitraryLocation", False, type=bool))
    self.radioButton_ObjectLocation.setChecked(not(settings.value("ArbitraryLocation", False, type=bool)))
  
    self.default_dir_Config = settings.value("default_dir_Config", os.path.expanduser("~"))
    self.default_dir_InputDir = settings.value("default_dir_InputDir", os.path.expanduser("~"))
    self.default_dir_OutputDir = settings.value("default_dir_OutputDir", os.path.expanduser("~"))

  def closeEvent(self, event):
    print('Exiting 1')
    self.writeSettings()
    print('Exiting 2')
    event.accept()
    return
    
  def SaveConfig(self):
      """
      what to do when the save button is clicked
      """
      if not self.ConfigFileName: 
        self.SaveConfigAs()
      else:
        try:
          self.writeSettings(self.ConfigFileName)
        except:
          QtGui.QMessageBox.critical(self, "Critical", "Couldn't write to file {0}".format(os.path.abspath(self.ConfigFileName)))

  def SaveConfigAs(self):
      """
      what to do when the save as button is clicked
      """
      # TODO: Use custom dialog with default suffix (use setDefaultSuffix())
      (filename, directory) = QFileDialog.getSaveFileName(caption='Save configuration', directory=self.default_dir_Config)
      if filename:
        self.default_dir_Config = filename
        self.ConfigFileName = filename
        self.SaveConfig()

  def LoadConfig(self):
      """
      handle load button pressed
      """
      (filename, directory)  = QFileDialog.getOpenFileName(caption='Load configuration', directory=self.default_dir_Config)
      if filename:
        self.default_dir_Config = filename
        self.ConfigFileName = filename
        self.readSettings(self.ConfigFileName)

  def SelectOutputDirectory(self):
    options =  QFileDialog.ShowDirsOnly
    directory = QFileDialog.getExistingDirectory(self, "Select output directory", options=options, directory=self.default_dir_OutputDir)
    if directory:
      self.default_dir_OutputDir = directory
      self.lineEdit_OutputDirectory.setText(directory)
    return

  # TODO: Get sorting by numbers (not string) to work.
  # TODO: Get validators to work.
  # TODO: Get drag and drop of rows to work
  # TODO: spreadsheet/.csv import/export/drag-drop
  # TODO: Fix incorrect exiting. Sometimes the process just stays active after closing the window, sometimes, there is this error:
  # *** glibc detected *** python3: malloc(): memory corruption: 0x00000000023d3cb0 ***

  
  def AddFrequencyButtonClicked(self):
    self.AddFrequency()
  
  def AddFrequency(self, freq=None, wavelength=None, comment=''):
    
    self.tableWidget_Frequencies.setSortingEnabled(False)
    
    self.tableWidget_Frequencies.insertRow(self.tableWidget_Frequencies.rowCount())

    if freq is None:
      freq = self.tableWidget_Frequencies.rowCount()

    if wavelength is None:
      wavelength = self.tableWidget_Frequencies.rowCount()
    
    row_contents = [float(freq), float(wavelength), str(comment)]

    setRow(self.tableWidget_Frequencies, self.tableWidget_Frequencies.rowCount()-1, row_contents)
    
    #self.tableWidget_Frequencies.
    #self.tableWidget_Frequencies.setRowCount(self.tableWidget_Frequencies.rowCount()+1)
    #self.tableWidget_Frequencies.setItem(self.tableWidget_Frequencies.rowCount()-1, 0, QTableWidgetItem(str(self.tableWidget_Frequencies.rowCount()-1), type=float) )
    #self.tableWidget_Frequencies.setItem(self.tableWidget_Frequencies.rowCount()-1, 1, QTableWidgetItem(str(self.tableWidget_Frequencies.rowCount()-1), type=float) )

    #self.tableWidget_Frequencies.setItem(self.tableWidget_Frequencies.rowCount()-1, 0, QTableWidgetItem(QVariant.Double) )
    #self.tableWidget_Frequencies.setItem(self.tableWidget_Frequencies.rowCount()-1, 1, QTableWidgetItem(QVariant.Double) )

    #freq_item = QTableWidgetItem()
    #wavelength_item = QTableWidgetItem()
    #freq_item.setData(Qt.DisplayRole, freq)
    #wavelength_item.setData(Qt.DisplayRole, wavelength)
    #self.tableWidget_Frequencies.setItem(self.tableWidget_Frequencies.rowCount()-1, 0, freq_item )
    #self.tableWidget_Frequencies.setItem(self.tableWidget_Frequencies.rowCount()-1, 1, wavelength_item )

    self.tableWidget_Frequencies.setSortingEnabled(True)

    return

  def AddFrequencyFromFrequencyList(self):
    (files, selected_filter) = QtWidgets.QFileDialog.getOpenFileNames(parent=self, caption='Add frequencies from frequency list files', filter='frequency list files (*.harminv.selection.txt);; text files (*.txt);; CSV files (*.csv);; All Files(*)', directory=self.default_dir_InputDir)

    if files:
      self.default_dir_InputDir = files[0]

    for i in files:
      freq_list = getFrequencies(i)
      for f in freq_list:
        self.AddFrequency(f, get_c0()/f, 'from '+i)

    return

  def AddFrequencyFromInpFile(self):
    (files, selected_filter) = QtWidgets.QFileDialog.getOpenFileNames(parent=self, caption='Add frequencies from BFDTD input files', filter='BFDTD input files (*.in *.geo *.inp);; All Files(*)', directory=self.default_dir_InputDir)

    if files:
      self.default_dir_InputDir = files[0]
    
    obj = BFDTDobject()
    for i in files:
      obj.readBristolFDTD(i)
      
    excitation_freq_list = sorted(list(obj.getExcitationFrequencySet()))
    snap_freq_list = sorted(list(obj.getSnapshotFrequencySet()))
    
    print(excitation_freq_list)
    print(snap_freq_list)
    
    for f in excitation_freq_list:
      self.AddFrequency(f, get_c0()/f, 'from excitation')

    for f in snap_freq_list:
      self.AddFrequency(f, get_c0()/f, 'from frequency snapshot')
    
    return

  def RemoveFrequency(self):
    current_selection = self.tableWidget_Frequencies.selectedItems()
    selected_rows = set()
    for item in current_selection:
      selected_rows.add(self.tableWidget_Frequencies.row(item))
      
    selected_rows = list(selected_rows)
    selected_rows.sort(reverse=True)
    print(selected_rows)
    
    for row in selected_rows:
      self.tableWidget_Frequencies.removeRow(row)
    return

  def moveFrequencyUp(self):

    current_selection = self.tableWidget_Frequencies.selectedItems()
    selected_rows = set()
    for item in current_selection:
      selected_rows.add(self.tableWidget_Frequencies.row(item))
      
    selected_rows = list(selected_rows)
    selected_rows.sort(reverse=False)
    print(selected_rows)
    
    for row in selected_rows:
      if row > 0:
        row_contents = getRow(self.tableWidget_Frequencies, row)
        self.tableWidget_Frequencies.removeRow(row)
        self.tableWidget_Frequencies.insertRow(row-1)
        setRow(self.tableWidget_Frequencies, row-1, row_contents)

        selectRow(self.tableWidget_Frequencies, row-1)

    return

        #item = self.tableWidget_Frequencies.item(row-1, 0)
        #self.tableWidget_Frequencies.setCurrentItem(item, QItemSelectionModel.SelectCurrent)
        
        #myrange = QTableWidgetSelectionRange(row-1, 0, row-1, self.tableWidget_Frequencies.columnCount())
        #self.tableWidget_Frequencies.setRangeSelected(myrange, True)
        

    #myrange = QTableWidgetSelectionRange(0, 0, self.tableWidget_Frequencies.rowCount(), self.tableWidget_Frequencies.columnCount())
    #self.tableWidget_Frequencies.setRangeSelected(myrange, True)

    #return
    
    #row_contents = getRow(table_widget, row)
    
    #item(row,0)
    
    #insertRow(row-1)
    #removeRow(row)
    #return
    
    #self.tableWidget_Frequencies.rowMoved(0, 0, 1)
    #return

    
    #current_selection = self.tableWidget_Frequencies.selectedItems()
    #selected_rows = set()
    #for item in current_selection:
      #selected_rows.add(self.tableWidget_Frequencies.row(item))
      
    #selected_rows = list(selected_rows)
    #print(selected_rows)
    
    #selected_rows.sort(reverse=False)
    
    #for row in selected_rows:
      #item = self.tableWidget_Frequencies.takeItem(row, 0)
      
      #self.tableWidget_Frequencies.insertRow(row-1)
      
      #self.tableWidget_Frequencies.insertItem(row-1, item)
      #self.tableWidget_Frequencies.setCurrentItem(item, QItemSelectionModel.SelectCurrent)
    #return

  def moveFrequencyDown(self):
    current_selection = self.tableWidget_Frequencies.selectedItems()
    selected_rows = set()
    for item in current_selection:
      selected_rows.add(self.tableWidget_Frequencies.row(item))
      
    selected_rows = list(selected_rows)
    selected_rows.sort(reverse=True)
    print(selected_rows)
    
    for row in selected_rows:
      if row < self.tableWidget_Frequencies.rowCount()-1:
        row_contents = getRow(self.tableWidget_Frequencies, row)
        self.tableWidget_Frequencies.removeRow(row)
        self.tableWidget_Frequencies.insertRow(row+1)
        setRow(self.tableWidget_Frequencies, row+1, row_contents)

        selectRow(self.tableWidget_Frequencies, row+1)
      
    return

  def clearFrequencyList(self):
    self.tableWidget_Frequencies.setRowCount(0)
    #self.tableWidget_Frequencies.clearContents()
    #self.tableWidget_Frequencies.clearContents()    
    return    

  def Run(self):

    # general settings
    self.BFDTD_object.setWallTime(self.spinBox_Walltime.value())
    self.BFDTD_object.setIterations(self.spinBox_Niterations.value())
    self.BFDTD_object.setExecutable(self.comboBox_Executable.currentText())
    self.BFDTD_object.setFileBaseName(self.lineEdit_BaseName.text())

    # checkbox operations
    if self.checkBox_removeProbes.isChecked():
      self.BFDTD_object.clearProbes()
    if self.checkBox_removeTimeAndEpsilonSnapshots.isChecked():
      self.BFDTD_object.clearTimeSnapshots()
      self.BFDTD_object.clearEpsilonSnapshots()
    if self.checkBox_removeFrequencySnapshots.isChecked():
      self.BFDTD_object.clearFrequencySnapshots()
    if self.checkBox_removeGeometryObjects.isChecked():
      self.BFDTD_object.clearGeometry()
    if self.checkBox_clearFileList.isChecked():
      self.BFDTD_object.clearFileList()
      
      #clearGeometry()
      #clearProbes()
      #clearFileList()
      #clearTimeSnapshots()
      #clearFrequencySnapshots()
      #clearEpsilonSnapshots()
      #clearModeFilteredProbes()
      #clearAllSnapshots()

    # operation specific handling
    if self.comboBox_Operation.currentIndex() == 0:
      print('Adding central snapshots')
      
      # get location
      location = [ float(self.lineEdit_X.text()), float(self.lineEdit_Y.text()), float(self.lineEdit_Z.text()) ]
      
      # get frequency list
      freqlist = [ float(self.tableWidget_Frequencies.item(i,0).text()) for i in range(self.tableWidget_Frequencies.rowCount()) ]

      print(location)
      print(freqlist)

      self.BFDTD_object.addCentralXYZSnapshots(location, freqlist, withEpsilon=True)
    
    # write files
    try:
      self.BFDTD_object.writeTorqueJobDirectory(self.lineEdit_OutputDirectory.text(), overwrite=False)
    except UserWarning as err:
      reply = QMessageBox.question(self, "WARNING", err.args[0] + '\n\nOne or more of the files to be written already exists in the specified destination directory.\nDo you want to proceed anyway, overwriting them?', QMessageBox.Yes | QMessageBox.No)
      if reply == QMessageBox.Yes:
        self.BFDTD_object.writeTorqueJobDirectory(self.lineEdit_OutputDirectory.text(), overwrite=True)
    except:
      QMessageBox.critical(self, 'Unexpected error', '{}: {}\n\nTraceback:\n{}'.format(sys.exc_info()[0].__name__, sys.exc_info()[1], sys.exc_info()[2]) )
    
    return

def main():
  app = QtWidgets.QApplication(sys.argv)
  
  app.setOrganizationName("University of Bristol")
  app.setOrganizationDomain("www.bristol.ac.uk")
  app.setApplicationName("BFDTD tool")
    
  ex = BFDTDtoolMainWindow()
  ex.show()
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()
