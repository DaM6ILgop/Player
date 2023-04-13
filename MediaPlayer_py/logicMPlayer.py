import sys
#FOR_SLIDER
from PyQt5.QtCore import QUrl  #
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog

#add Ui_Dialog.py
from MPlayer import Ui_Dialog

#add admin ui
from LogToAdmin import *
from AdminForm import *

# class File:
#     def __init__(self, main_window):
#         self.main_window = main_window
#         self.media_player = main_window.media_player
#
#     def open_file(self):
#         filename, _ = QFileDialog.getOpenFileName(self.main_window, "Open Video")
#
#         if filename:
#             self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
#             self.main_window.OpenButton.setEnabled(True)
from abc import ABC, abstractmethod

class AbstractFile(ABC):
    @abstractmethod
    def open_file(self):
        pass


class File(AbstractFile):
    def __init__(self, main_window):
        self.main_window = main_window
        self.media_player = main_window.media_player

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self.main_window, "Open Video")

        if filename:
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.main_window.OpenButton.setEnabled(True)



class SliderPosition:
    def __init__(self, main_window):
        self.main_window = main_window
        self.media_player = main_window.media_player

        # reference to the slider widget
        self.slider = main_window.VideoSlider

        # set slider orientation and connect signals
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.sliderMoved.connect(self.change_video_position)
        self.slider.sliderPressed.connect(self.set_video_position)

        # connect media player signals
        self.media_player.durationChanged.connect(self.set_duration)
        self.media_player.positionChanged.connect(self.set_position)

    def set_position(self, position):
        self.slider.setValue(position)

    def set_duration(self, duration):
        self.slider.setRange(0, duration)

    def set_video_position(self):
        position = self.slider.value()
        self.media_player.setPosition(position)

    def change_video_position(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
            self.set_video_position()
            self.media_player.play()
        else:
            self.set_video_position()



class PlayPause:
    def __init__(self, main_window):
        self.main_window = main_window
        self.media_player = main_window.media_player

    def play_video(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()



#func for open logIn form
def LogIn():
    try:
        global LogToAdmin
        LogToAdmin = QtWidgets.QDialog()
        ui = Ui_AdminForm()  #если ломается при сохранении, то поменять в ui название AdminForm на Ui_AdminForm
        ui.setupUi(LogToAdmin)
        window.hide()
        LogToAdmin.show()


        #Экземпляр класса AdminForm
        admForm = AdminForm()
        def checkPassLog():
            try:
                if ui.TexBox_LogIN.text() == '123' and ui.TextBox_Password.text() == '123':
                    admForm.openAdminForm()
            except Exception as e:
                print(e)

        ui.Button_Log_In.clicked.connect(checkPassLog)

        try:
            def returnBttn():
                LogToAdmin.close()
                window.show()
        except Exception as e:
            print(e)

        #return of main window button
        ui.pushButton.clicked.connect(returnBttn)
    except Exception as e:
        print(e)


class AdminForm():
    def openAdminForm(self):
        try:
            global SetColorPanel
            SetColorPanel = QtWidgets.QDialog()
            ui = Ui_SetColorPanel()
            ui.setupUi(SetColorPanel)
            LogToAdmin.close()
            SetColorPanel.show()

            def standart_thema(self):
                # Установка светлой темы для Screen_translator
                palette = QPalette()
                palette.setColor(QPalette.Window, QColor('green'))
                palette.setColor(QPalette.WindowText, QColor('purple'))
                palette.setColor(QPalette.ButtonText, QColor('purple'))
                window.setPalette(palette)

                # window.setStyleSheet(f"background-color: green; color: black;") Полное изменения цвета всех элементов

                # Установка светлой темы для текстовых окон и кнопок
                # window.setStyleSheet(f"background-color: purple; color: black;")
        except Exception as e:
            print(e)


        try:
            def showMainWindow():
                SetColorPanel.close()
                window.show()
        except Exception as e:
            print(e)
        #Вызов метода для изменения темы по нажатии на кнопку
        ui.SaveColor.clicked.connect(standart_thema)

        #Метод, который вызывает главную форму с измененным цветом
        ui.SaveColor.clicked.connect(showMainWindow)

class VolumeSliderHandler:
    def __init__(self, media_player, slider):
        self.media_player = media_player
        self.slider = slider
        self.slider.valueChanged.connect(self.set_volume)

    try:
        def set_volume(self, value):
            volume = value / 100
            self.media_player.setVolume(int(volume * 100))
    except Exception as e:
        print(e)



class MyWindow(QMainWindow, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.media_player = QMediaPlayer(self, QMediaPlayer.VideoSurface)
        self.video_widget = QVideoWidget(self)
        self.media_player.setVideoOutput(self.video_widget)

        #create rectanglo for video
        self.video_widget.setGeometry(0, 0, 1125, 525)

        #  File
        self.file = File(self)
        self.OpenButton.clicked.connect(self.file.open_file)

        # PlayPause
        self.play_pause = PlayPause(self)
        self.PlayPauseButton.clicked.connect(self.play_pause.play_video)

        #SliderPosition
        self.slider_position = SliderPosition(self)

        self.Button_LogInAdmin.clicked.connect(LogIn)

        # VolumeSlider
        self.slider_handler = VolumeSliderHandler(self.media_player, self.VolumeSlider2)
        # self.volume_slider = VolumeSlider(self)
        # self.horizontalLayout.addWidget(self.volume_slider)




app = QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec_())