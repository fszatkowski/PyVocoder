from dataclasses import dataclass
from gui import *
from callbacks import process
from callbacks import play_in_audio
from callbacks import play_out_audio


@dataclass
class Parameters:
    num_of_filters:     int = 0
    input_path:         str = ''
    output_path:        str = ''
    compression_level:  float = 0


dispatch_dictionary = {'Process':           process,
                       'play_in_audio':     play_in_audio,
                       'play_out_audio':    play_out_audio,
}

params = Parameters()
window = sg.Window('Vocoder model', layout, no_titlebar=False)
while True:
    event, values = window.read(timeout=0)
    if event in (None, 'Exit'):
        break

    number_of_filters = int(values['number_of_filters'])

    window['num_text'].update(number_of_filters)
    if event in dispatch_dictionary:
        params = Parameters(num_of_filters=number_of_filters,
                            input_path=values['in_path'],
                            output_path=values['out_path'])
        fun_to_call = dispatch_dictionary[event]
        fun_to_call(params)
    if event == 'Process':
        window['compression_level'].update(f'Compression level: {int(params.compression_level)}%')
        window['canvas_in_stft'].update(filename='../img/input_spectrum.png')
        window['canvas_in_signal'].update(filename='../img/input_signal.png')
        window['canvas_out_stft'].update(filename='../img/output_spectrum.png')
        window['canvas_out_signal'].update(filename='../img/output_signal.png')

window.close()
