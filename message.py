from os import path
from xml.sax.saxutils import escape


basepath = path.dirname(__file__)
filename = "message.ui"
filepath = path.abspath(path.join(basepath, filename))

template = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Dialog</class>
 <widget class="QDialog" name="Dialog">
  <property name="windowTitle">
   <string>EasyAlign</string>
  </property>
  <layout class="QVBoxLayout" name="verticalLayout">
   <property name="spacing">
    <number>16</number>
   </property>
   <property name="leftMargin">
    <number>16</number>
   </property>
   <property name="topMargin">
    <number>16</number>
   </property>
   <property name="rightMargin">
    <number>16</number>
   </property>
   <property name="bottomMargin">
    <number>16</number>
   </property>
   <item>
    <widget class="QLabel" name="message">
     <property name="text">
      <string>{text}</string>
     </property>
     <property name="wordWrap">
      <bool>true</bool>
     </property>
    </widget>
   </item>
   <item>
    <widget class="QDialogButtonBox" name="buttonBox">
     <property name="orientation">
      <enum>Qt::Horizontal</enum>
     </property>
     <property name="standardButtons">
      <set>QDialogButtonBox::Ok</set>
     </property>
    </widget>
   </item>
  </layout>
 </widget>
 <resources/>
 <connections>
  <connection>
   <sender>buttonBox</sender>
   <signal>accepted()</signal>
   <receiver>Dialog</receiver>
   <slot>accept()</slot>
  </connection>
  <connection>
   <sender>buttonBox</sender>
   <signal>rejected()</signal>
   <receiver>Dialog</receiver>
   <slot>reject()</slot>
  </connection>
 </connections>
</ui>
"""


def warning(window, text):
    f = open(filepath, "w")

    f.write(template.format(text=escape(text)))
    f.close()

    dialog = window.create_dialog(filename)

    if dialog:
        dialog.exec()
