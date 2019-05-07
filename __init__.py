# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DebugVS
                                 A QGIS plugin
 Plugin to connect Visual Studio Remote Debugger
                             -------------------
        begin                : 2018-10-16
        copyright            : (C) 2018 by Luiz Motta
        email                : motta.luiz@gmail.com

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""

__author__ = 'Luiz Motta'
__date__ = '2018-10-16'
__copyright__ = '(C) 2018, Luiz Motta'
__revision__ = '$Format:%H$'


import os

from qgis.PyQt.QtCore import QObject, pyqtSlot
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

def classFactory(iface):
  return DebugVSPlugin( iface )

class DebugVSPlugin( QObject ):

  def __init__(self, iface):
    super().__init__()
    self.ptvsd = None
    try:
      import ptvsd
      self.ptvsd = ptvsd
    except:
      pass
    self.iface, self.action, self.hasInit = iface, None, False
    self.msgBar = iface.messageBar()
    self.pluginName = 'DebugVS'
    self.nameAction = 'Enable Debug for Visual Studio'
    self.action = None

  def initGui(self):
    icon = QIcon( os.path.join( os.path.dirname(__file__), 'code.svg' ) )
    self.action = QAction( icon, self.nameAction, self.iface.mainWindow())
    self.action.triggered.connect( self.run )
    self.iface.addToolBarIcon(self.action)
    self.iface.addPluginToMenu( f"&{self.nameAction}" , self.action)

  def unload(self):
    self.iface.removePluginMenu( f"&{self.nameAction}", self.action)
    self.iface.removeToolBarIcon( self.action )

  @pyqtSlot(bool)
  def run(self, checked):
    self.msgBar.popWidget()
    if self.ptvsd is None:
      self.msgBar.pushCritical( self.pluginName, "Need install ptvsd: pip3 install ptvsd")
      return
    if self.ptvsd.is_attached():
      self.msgBar.pushWarning( self.pluginName, "Remote Debug for Visual Studio is active")
      return
    self.msgBar.pushInfo( self.pluginName, "Run the Debug in Visual Studio(Python:Attach)")
    self.ptvsd.enable_attach( address = ('localhost', 5678) )
    #self.ptvsd.wait_for_attach()
    
