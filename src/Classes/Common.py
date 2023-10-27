import os, re, sys
from PIL import Image, ImageFont
from PyQt5 import QtWidgets, QtGui, QtCore
from Classes.ExtractBackend import CharacterExtractor
from Classes.ColorDialog import ColorPickerDialog
from Classes.SettingsDialog import SettingsWindow