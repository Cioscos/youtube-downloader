import platform
import os
import sys
import subprocess
import re

# Add vendor directory to module search path
parent_dir = os.path.abspath(os.path.dirname(__file__))
vendor_dir = os.path.join(parent_dir, 'vendor')

sys.path.append(vendor_dir)

from pytube import YouTube
from exitstatus import ExitStatus

if platform.system() != "Windows":
    import ffmpeg


def main():
    # Asking for all the video links
    while True:
        n = input("Inserisci il numero di video da scaricare da YouTube:   ")

        if n.isdigit():
            break
        else:
            print('Inserisci un numero valido')

    links = []
    print("\nInserisci i link uno per volta premendo invio per inserirlo (Premi q per uscire):")

    for i in range(int(n)):
        while True:
            url = input()
            match = re.match(r'^(https?://)?((www\.)?youtube\.com|youtu\.?be)/.+$', url)
            if match:
                links.append(url)
                break
            elif url == 'q':
                sys.exit(ExitStatus.success)
            else:
                print('Inserisci un link valido!')

    choose = input('Vuoi scaricare direttamente o scegliere il formato?\n1) Scarica direttamente (Max. 720p)\n'
                   '2) Scegli il formato\n3) Scarica solo audio\n4) Esci\nInserisci scelta: ')

    while True:
        if choose == '4':
            break
        elif choose == '1' or choose == '2' or choose == '3':
            if platform.system() == "Windows":
                subprocess.call('cls', shell=True)
            else:
                subprocess.call('clear', shell=True)
            choosing_video(choose, links)
            break
        else:
            choose = input('Hai inserito una scelta non accettata. Inserisci 1,2,3 o 4:')

    if platform.system() == 'Windows':
        os.system('pause')
    else:
        input('Premere un tasto per continuare')

    sys.exit(ExitStatus.success)


def download(yt, separate_tracks=False, tag=None, audio_only=False):
    # It creates the file name
    file_name = yt.title + '.mp4'

    # Check if there are some not enable characters and replaces it
    if file_name.find("\"") != -1:
        file_name = file_name.replace('"', '``')

    if file_name.find("\\") != -1:
        file_name = file_name.replace('\\', '-')

    if file_name.find('/') != -1:
        file_name = file_name.replace('/', '-')

    if file_name.find(':') != -1:
        file_name = file_name.replace(':', ' ')

    # If user choose to select the quality
    if separate_tracks:
        # It will be false if something went wrong
        alright = True

        print('\nDownload in corso...', end='')
        # Download just the video
        try:
            ys = yt.streams.get_by_itag(tag)
        except Exception as e:
            print(str(e))
            alright = False
        else:
            try:
                ys.download(filename='video_file')
            except Exception as e:
                print(str(e))
                alright = False

        # Download just the audio
        try:
            ys = yt.streams.get_audio_only()
        except Exception as e:
            print(str(e))
            alright = False
        else:
            try:
                ys.download(filename='audio_file')
            except Exception as e:
                print(str(e))
                alright = False

        # Check if something went wrong
        if alright:
            print('finito!')
        else:
            print("\nC'è un problema con il download di questo video.")
            return

        print("\nMuxing in corso...", end='')

        # Cross-platform ffmpeg

        # Create list of file and dir in root
        os.chdir('./')
        listdir = os.listdir(os.getcwd())

        # It will be true when the iterator will find a point inside the searched name
        point_found = False
        # Type of the extension
        extension = ''

        for i in listdir:
            # if the current file is video_file
            if i.find('video_file') != -1:
                # Check each character of the name up to the .
                for j in range(len(i)):
                    if i[j] == '.':
                        # if the point is reached, point_found is true and adds the point to estension
                        point_found = True
                        extension += i[j]
                    elif point_found:
                        extension += i[j]

        # Name of video file source
        input_name = 'video_file' + extension

        # Calls to FFmpeg
        if platform.system() == 'Windows':
            if platform.architecture()[0] == '64bit':
                command = "ffmpeg_x64 -i {video} -i {audio} -loglevel warning -c:v copy -c:a aac {output}". \
                    format(video='../' + input_name, audio='../audio_file.mp4', output="\"../" + file_name + "\"")
            else:
                command = "ffmpeg_x86 -i {video} -i {audio} -loglevel warning -c:v copy -c:a aac {output}". \
                    format(video='../' + input_name, audio='../audio_file.mp4', output="\"../" + file_name + "\"")

            try:
                subprocess.call(command, shell=True, cwd='./ffmpeg/')
            except Exception as e:
                print(str(e))
                alright = False
        else:
            video_stream = ffmpeg.input('./' + input_name)
            audio_stream = ffmpeg.input('./audio_file.mp4')

            try:
                ffmpeg.output(audio_stream, video_stream, file_name).run(quiet=True)
            except ffmpeg.Error as e:
                print(e.stderr.decode(), file=sys.stderr)
                alright = False

        # Check if something went wrong
        if alright:
            print('finito!')
        else:
            print("\nC'è un problema con il muxing del video")

        os.remove('./' + 'video_file' + extension)
        os.remove('./audio_file.mp4')
    else:
        alright = True

        print('\nDownload in corso...', end='')

        # If user want to download just the audio
        if audio_only:
            try:
                ys = yt.streams.get_audio_only()
            except Exception as e:
                print(str(e))
                alright = False
            else:
                try:
                    ys.download()
                except Exception as e:
                    print(str(e))
                    alright = False

            # Check if something went wrong
            if alright:
                print('finito!')
            else:
                print("\nC'è un problema con il download di questo video.")
                return

            # Create list of file and dir in root
            os.chdir('./')
            listdir = os.listdir(os.getcwd())

            for i in listdir:
                if i.find('.mp4') != -1:
                    os.rename(i, file_name)

            print("\nMuxing in corso...", end='')

            # Calls to FFmpeg
            if platform.system() == 'Windows':
                if platform.architecture()[0] == '64bit':
                    command = "ffmpeg_x64 -i {video} -f mp3 -ab 192000 -vn {audio} -loglevel warning". \
                        format(video="\"../" + file_name + "\"", audio="\"../" + file_name.replace('mp4', 'mp3') + "\"")
                else:
                    command = "ffmpeg_x86 -i {video} -f mp3 -ab 192000 -vn {audio} -loglevel warning". \
                        format(video="\"../" + file_name + "\"", audio="\"../" + file_name.replace('mp4', 'mp3') + "\"")

                try:
                    subprocess.call(command, shell=True, cwd='./ffmpeg/')
                except Exception as e:
                    print(str(e))
                    alright = False
            else:
                try:
                    (
                        ffmpeg
                        .input('./' + file_name)
                        .output('./' + file_name.replace('mp4', 'mp3'))
                        .global_args('-loglevel', 'error')
                        .global_args('-f', 'mp3')
                        .global_args('-ab', '192000')
                        .run()
                    )
                except ffmpeg.Error as e:
                    print(e.stderr.decode(), file=sys.stderr)
                    alright = False

            # Check if something went wrong
            if alright:
                print('finito!')
            else:
                print("\nProblema con la conversione del file")
            os.remove(file_name)
        else:
            # If user wants to download in 720p
            try:
                ys = yt.streams.get_highest_resolution()
            except Exception as e:
                print(str(e))
                alright = False
            else:
                try:
                    ys.download()
                except Exception as e:
                    print(str(e))
                    alright = False

            # Check is something went wrong
            if alright:
                print('finito!')
            else:
                print("\nProblema con il download del file")


def print_error(error):
    print(error)
    if platform.system() == 'Windows':
        os.system('pause')
    else:
        input('Premere un tasto per continuare')
    sys.exit(ExitStatus.failure)


def choosing_video(choose, links):
    # Showing all details for videos and downloading them one by one
    for i in range(0, len(links)):
        link = links[i]

        # Taking info about video
        try:
            yt = YouTube(link)
        except Exception as e:
            print_error(str(e))
        else:
            print("\nDettagli del video ", i + 1, "\n")
            print("Titolo del video:          ", yt.title)
            print("Numero di visualizzazioni: ", yt.views)
            print("Lunghezza del video:       ", yt.length, "secondi")

            print("\nDownloading video number ", i + 1)

            if choose == '1':
                # Download directly without muxing from youtube in 720p
                download(yt)
            elif choose == '2':
                # Filters results for type video, mp4.
                stream = yt.streams.filter(type='video', progressive=False)
                stream_dict = stream.itag_index

                print("\nTutte le opzioni disponibili per il download:\n")
                index = 1
                for key, value in stream_dict.items():
                    print(index, ')', value)
                    index += 1

                tag = int(input("\nInserisci l'itag del tuo stream preferito da scaricare:   "))
                download(yt, True, tag=tag)
            else:
                download(yt, audio_only=True)


if __name__ == '__main__':
    main()
