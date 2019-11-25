from gui import *
from callbacks import process
from callbacks import play_audio


dispatch_dictionary = {'Process':process,
                       'play input audio':play_audio(type='in'),
                       'play output audio':play_audio(type='out')
                       }

window = sg.Window('Vocoder model', layout, no_titlebar=True)
while True:
    event, values = window.read(timeout=0)
    if event in (None, 'Exit'):
        break

    if event in dispatch_dictionary:
        fun_to_call = dispatch_dictionary[event]
        fun_to_call()

    window['num_text'].update(int(values['number_of_filters']))

window.close()
