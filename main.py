#from icrawler.builtin import GoogleImageCrawler
from bing_image_downloader import downloader
#from google_images_search import GoogleImagesSearch
import os
import shutil
import PySimpleGUI as sg
import threading

SAVE_FOLDER = 'images'

def download_images(id, query, number):
    outdir = SAVE_FOLDER + '/' + query
    if os.path.exists(outdir):
        shutil.rmtree(outdir)
    
    downloader.download(query=query, 
                        limit=int(number), 
                        output_dir=SAVE_FOLDER, 
                        adult_filter_off=True, 
                        force_replace=False, 
                        timeout=120, 
                        verbose=False)

    threadsList[id] = query + " : Search finished!"
    window['-THREADS-LIST-'].update(threadsList)
    
numberThreads = 0
threadsList = list()

# setting up the pysimplegui screen

fontUsed = ('Ubuntu', 12)
sg.theme('DarkTeal4')

left_part = [[sg.Text("What's the query you want to search?", font=fontUsed)],
          [sg.Input(key='-INPUT-QUERY-', font=fontUsed)],
          [sg.Text("How many images?", font=fontUsed)],
          [sg.Input(key='-INPUT-NUMBER-', font=fontUsed)],
          [sg.Text(key='-ERROR-', font=fontUsed)],
          [sg.Text()],
          [sg.Button('Search!', font=fontUsed)]]

right_part=[[sg.Listbox(values=threadsList, size=(40, 20), key="-THREADS-LIST-", font=fontUsed)]]

layout = [
    [
        sg.Column(left_part),
        sg.VSeperator(),
        sg.Column(right_part),
    ]
]

window = sg.Window('Web Scraping', layout)


while True:
    event, values = window.read()
    
    if event == sg.WINDOW_CLOSED:
        break

    if event == 'Search!':
        query = values['-INPUT-QUERY-']
        number = values['-INPUT-NUMBER-']

        # error handling
        if not query:
            window['-ERROR-'].update("Please provide search query!", text_color='yellow', font=fontUsed)
            continue

        if not number or not number.isdigit():
            window['-ERROR-'].update("Please provide valid number!", text_color='yellow', font=fontUsed)
            continue
        with open("log.txt", "w") as log:
            try:
                x = threading.Thread(target=download_images, args=(numberThreads, query, number))
                x.start()
            except Exception as e:
                # tkinter and threads have a lot of problems working together :(
                log.write(e)

        # update threads list
        threadsList.append(query + " : Searching...")
        window['-THREADS-LIST-'].update(threadsList)

        # clear input texts
        window['-ERROR-'].update("")
        window['-INPUT-QUERY-'].update("")
        window['-INPUT-NUMBER-'].update("")
        window['-INPUT-QUERY-'].set_focus()

        numberThreads += 1


window.close()




