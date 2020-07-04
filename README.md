# YouTube downloader

This software written entirely in Python allows you to download videos from YouTube quickly and easily. Just enter the number of videos to download and their links, then he will automatically download them or you can choose the quality or even download only the audio of the video.

## Installer
[Download installer from Google Drive](https://drive.google.com/file/d/1F-e4JPwW7_d6k4B7RWI_Hv-af27aoL_A/view?usp=sharing)

***

If you want you can compile it in a executable file but you have to install Python on your PC. To do it you have to:
* Go on [Python site](https://www.python.org/downloads/) and download last version.
* Install Python
* Open CMD and write
```
pip install pytube3
```
and than
```
pip install pyinstaller
```
* Download or clone my repository. To clone just use Git command:
```
git clone https://github.com/Cioscos/youtube-downloader.git
```
* From CMD reach root of project, where there is main.py file, and write on it:
```
> pyinstaller --onefile main.py --name youtube-downloader
```
* Now some new folders will be created inside the project. Go inside dist folder and copy or cut youtube-downloader.exe file and paste it inside root directory (where there is main.py file).
* Now you can start the program directly from the executable file or from CMD writing youtube-downloader.

If you get an error message, you may need to install [Visual C++ Redistributable](https://support.microsoft.com/en-ca/help/2977003/the-latest-supported-visual-c-downloads).

## How to run
### On windows
To run YouTube-Downloader without create an executable file, you just need to install Python 3.X (link below)
Then you can double-click on main.py file in the root directory! Take care that you don't have to move the position of main.py or of the other folder.

### On Linux
If you are on Linux you have to install Python from your package manager with FFmpeg too. Next it's the same of Windows.

#### Example on Ubuntu system
```
> sudo apt install ffmpeg
```
Than you have just to write on terminal:
```
> python3 main.py
```
