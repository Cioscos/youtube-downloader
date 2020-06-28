from pytube import YouTube
import sys
import platform
import os
import subprocess

if platform.system() != "Windows":
    import ffmpeg


def main():
    # Asking for all the video links
    n = int(input("Inserisci il numero di video da scaricare da YouTube:   "))
    links = []
    print("\nInserisci i link uno per volta premendo invio per inserirlo:")

    for i in range(0, n):
        temp = input()
        links.append(temp)

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


def download(yt, separate_tracks=False, tag=None, audio_only=False):
    file_name = yt.title + '.mp4'

    if file_name.find("\"") != -1:
        file_name = file_name.replace('"', '``')

    if separate_tracks:
        print('\nDownload in corso...', end='')
        ys = yt.streams.get_by_itag(tag)
        ys.download(filename='video_file')
        ys = yt.streams.get_audio_only()
        ys.download(filename='audio_file')
        print('finito!')

        print("\nMuxing in corso...", end='')

        # Cross-platform ffmpeg
        if platform.system() == 'Windows':
            if platform.architecture()[0] == '64bit':
                command = "ffmpeg_x64 -i {video} -i {audio} -loglevel warning -c:v copy -c:a aac {output}". \
                    format(video='../video_file.mp4', audio='../audio_file.mp4', output="\"../" + file_name + "\"")
            else:
                command = "ffmpeg_x86 -i {video} -i {audio} -loglevel warning -c:v copy -c:a aac {output}". \
                    format(video='../video_file.mp4', audio='../audio_file.mp4', output="\"../" + file_name + "\"")
            subprocess.call(command, shell=True, cwd='./ffmpeg/')
        else:
            video_stream = ffmpeg.input('./video_file.mp4')
            audio_stream = ffmpeg.input('./audio_file.mp4')
            ffmpeg.output(audio_stream, video_stream, file_name).run(quiet=True)

        print('finito!')
        os.remove('./video_file.mp4')
        os.remove('./audio_file.mp4')
    else:
        print('\nDownload in corso...', end='')
        if audio_only:
            ys = yt.streams.get_audio_only()
            ys.download()
            print('finito!')
            os.chdir('./')
            listdir = os.listdir(os.getcwd())
            for i in listdir:
                if i.find('.mp4') != -1:
                    os.rename(i, file_name)

            print("\nMuxing in corso...", end='')

            if platform.system() == 'Windows':
                if platform.architecture()[0] == '64bit':
                    command = "ffmpeg_x64 -i {video} -f mp3 -ab 192000 -vn {audio} -loglevel warning". \
                        format(video="\"../" + file_name + "\"", audio="\"../" + file_name.replace('mp4', 'mp3') + "\"")
                else:
                    command = "ffmpeg_x86 -i {video} -f mp3 -ab 192000 -vn {audio} -loglevel warning". \
                        format(video="\"../" + file_name + "\"", audio="\"../" + file_name.replace('mp4', 'mp3') + "\"")
                subprocess.call(command, shell=True, cwd='./ffmpeg/')
            else:
                (
                    ffmpeg
                        .input('./' + file_name)
                        .output('./' + file_name.replace('mp4', 'mp3'))
                        .global_args('-loglevel', 'error')
                        .global_args('-f', 'mp3')
                        .global_args('-ab', '192000')
                        .run()
                )
            print('finito!')
            os.remove(file_name)
        else:
            ys = yt.streams.get_highest_resolution()
            ys.download()
            print('finito!')


def choosing_video(choose, links):
    # Showing all details for videos and downloading them one by one
    for i in range(0, len(links)):
        link = links[i]
        yt = YouTube(link)

        print("\nDettagli del video ", i + 1, "\n")
        print("Titolo del video:          ", yt.title)
        print("Numero di visualizzazioni: ", yt.views)
        print("Lunghezza del video:       ", yt.length, "seconds")

        print("\nDownloading video number ", i + 1)

        if choose == '1':
            download(yt)
        elif choose == '2':
            stream = str(yt.streams.filter(subtype='mp4', progressive=False))
            stream = stream[1:]
            stream = stream[:-1]
            stream_list = stream.split(", ")
            print("\nTutte le opzioni disponibili per il download:\n")
            index = 1
            for stream in stream_list:
                print(index, ')', stream)
                index += 1

            tag = int(input("\nInserisci l'itag del tuo stream preferito da scaricare:   "))
            download(yt, True, tag=tag)
        else:
            download(yt, audio_only=True)
    print("\nDownload completato!!")


if __name__ == '__main__':
    main()
