import os
import shutil
from abc import abstractmethod, ABC
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

from pygame import mixer

playlist = os.listdir('Playlist')
currIndex = 0
state = False

"""
class ProgressBar:
    def __init__(self, window):
        super().__init__(window)
        s = Style()
        s.theme_use("default")
        s.configure("TProgressbar", thickness=5)
        self.progressBar = Progressbar(window, orient=HORIZONTAL, length=150, mode='determinate', style="TProgressbar")
        self.progressBar.pack()
        self.progressBar.place(x=175, y=10)

    def drawProgress(self):
        file = MP3('Playlist/' + playlist[currIndex])
        lenght = int(file.info.length)
        i = 0
        while mixer.music.get_busy():
            self.progressBar.configure(value=i)
            self.progressBar.update()
            sleep(1)
            i += 1
"""


class Btn(ABC):
    def __init__(self, window):
        super().__init__()
        self.win = window
        self.btn = Button(self.win, command=self.command)

    @abstractmethod
    def command(self):
        pass


class PlayButton(Btn):
    def __init__(self, window):
        super().__init__(window)
        self.btn.configure(text='Play', width=7, height=3)
        self.btn.place(x=230, y=285)

    def command(self):
        self.drawSongName(self.win)
        mixer.music.load('Playlist/' + playlist[currIndex])
        global state
        state = True
        mixer.music.play()

    def drawSongName(self, window):
        song_name = playlist[currIndex]
        label = Label(window, text=song_name)
        label.place(x=10, y=10)


class PauseButton(Btn):
    def __init__(self, window):
        super().__init__(window)
        self.btn.configure(text='Pause', width=7, height=3)
        self.btn.place(x=230, y=350)

    def command(self):
        global state
        if state:
            state = False
            mixer.music.pause()
        else:
            state = True
            mixer.music.unpause()


class NextButton(PlayButton):
    def __init__(self, window):
        super().__init__(window)
        self.btn.configure(text='->', width=5, height=3)
        self.btn.place(x=340, y=320)

    def command(self):
        global currIndex
        if len(playlist) - 1 <= currIndex:
            return
        currIndex += 1
        PlayButton.command(self)


class PrevButton(PlayButton):
    def __init__(self, window):
        super().__init__(window)
        self.btn.configure(text='<-', width=5, height=3)
        self.btn.place(x=130, y=320)

    def command(self):
        global currIndex
        if currIndex <= 0:
            return
        currIndex -= 1
        PlayButton.command(self)


class RepeatButton(Btn):
    def __init__(self, window):
        super().__init__(window)
        self.btn.configure(text='Repeat', width=10, height=1)
        self.btn.place(x=10, y=400)
        self.repeat_state = False

    def command(self):
        mixer.music.load('Playlist/' + playlist[currIndex])
        if not self.repeat_state:
            mixer.music.play(-1)
            self.repeat_state = True
            self.btn.configure(bg='gray')
        else:
            mixer.music.play()
            self.repeat_state = False
            self.btn.configure(bg='white')


class ScaleBtn(ABC):
    def __init__(self, window):
        super().__init__()
        self.win = window
        self.scaleBtn = Scale(self.win, command=self.command)

    @abstractmethod
    def command(self, value):
        pass


class VolumeScale(ScaleBtn):
    def __init__(self, window):
        super().__init__(window)
        self.scaleBtn.configure(from_=0, to=1, width=2, resolution=0.1, orient=HORIZONTAL,
                           command=self.command)
        self.scaleBtn.place(x=450, y=400)
        self.scaleBtn.set(0.5)
        self.win.bind()

    def command(self, value):
        mixer.music.set_volume(float(value))


class Cascade(ABC):
    def __init__(self, name, menuBar, window):
        super().__init__()
        self.win = window
        self.subMenu = Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label=name, menu=self.subMenu)

    @abstractmethod
    def firstCommand(self):
        pass

    @abstractmethod
    def secondCommand(self):
        pass

    @abstractmethod
    def thirdCommand(self):
        pass


class FileCascade(Cascade):
    def __init__(self, name, menuBar, window):
        super().__init__(name, menuBar, window)
        self.music_file = ''
        self.subMenu.add_command(label='Open', command=self.secondCommand)
        self.subMenu.add_command(label='Add to Playlist', command=self.firstCommand)
        self.subMenu.add_command(label='Show Playlist', command=self.thirdCommand)

    def firstCommand(self):
        file = filedialog.askopenfilename(title='Music', filetypes=[('MP3 files', '.mp3')])
        if not file:
            return
        shutil.copy(file, 'Playlist')

    def secondCommand(self):
        self.music_file = filedialog.askopenfilename()

    def thirdCommand(self):
        newWindow = Tk()
        str = ''
        for i in playlist:
            str += i + '\n'
        l1 = Label(newWindow, text=str)
        l1.pack()


class ExitCascade(Cascade):
    def __init__(self, name, menuBar, window):
        super().__init__(name, menuBar, window)
        self.subMenu.add_command(label='Hide', command=self.firstCommand)
        self.subMenu.add_command(label='Show', command=self.secondCommand)
        self.subMenu.add_command(label='Exit', command=self.thirdCommand)

    def firstCommand(self):
        self.win.iconify()

    def secondCommand(self):
        self.win.deiconify()

    def thirdCommand(self):
        self.win.destroy()


class SettingsCascade(Cascade):
    def __init__(self, name, menuBar, window):
        super().__init__(name, menuBar, window)
        self.subMenu.add_command(label='Background', command=self.firstCommand)

    def firstCommand(self):
        file = filedialog.askopenfilename(title='', filetypes=[('PNG files', '.png')])
        if not file:
            return
        self.win.image = PhotoImage(file=file)
        background_label = Label(self.win, image=self.win.image)
        background_label.pack()

    def secondCommand(self):
        pass

    def thirdCommand(self):
        pass


class HelpCascade(Cascade):
    def __init__(self, name, menuBar, window):
        super().__init__(name, menuBar, window)
        self.subMenu.add_command(label='Info', command=self.firstCommand)

    def firstCommand(self):
        messagebox.showinfo('Info', 'This is Simple Music Player')

    def secondCommand(self):
        pass

    def thirdCommand(self):
        pass


class Controls:
    def __init__(self, window):
        super().__init__()
        self.play = PlayButton(window)
        self.pause = PauseButton(window)
        self.previous = PrevButton(window)
        self.next = NextButton(window)
        self.repeat = RepeatButton(window)
        self.scale = VolumeScale(window)


class MenuBar:
    def __init__(self, window):
        menuBar = Menu(window)
        fileMenu = FileCascade('File', menuBar, window)
        settingsMenu = SettingsCascade('Settings', menuBar, window)
        exitMenu = ExitCascade('Window', menuBar, window)
        helpMenu = HelpCascade('Help', menuBar, window)
        window.config(menu=menuBar)


class MainWindow:
    def __init__(self, window):
        super().__init__()
        self.windowSetup(window)
        self.menuBar = MenuBar(window)
        self.controls = Controls(window)

    def windowSetup(self, window):
        window.geometry('560x460')
        window.title('Music Player')
        window.resizable(width=False, height=False)
        #window.iconbitmap('Images/music_icon.ico')
        window.image = PhotoImage(file='Images/bg1.gif')
        background_label = Label(window, image=window.image)
        background_label.pack()


class MainApp:
    def __init__(self, window):
        super().__init__()
        self.createMusicDir()
        mixer.init()
        win = MainWindow(window)

    def createMusicDir(self):
        if not os.path.exists('Playlist'):
            os.mkdir("Playlist")


if __name__ == "__main__":
    root = Tk()
    app = MainApp(root)
    root.mainloop()
