# this file contains GUI elements' definitions

import PySimpleGUI as sg

# input column fields
column_in = [
    [sg.Text('input file', size=(8, 1)), sg.Input(default_text='../data/1.wav', key='in_path'), sg.FileBrowse()],
    [sg.Button('play input audio', key='play_in_audio')],
    [sg.Image(filename='../img/test.png', key='canvas_in_stft')],
    [sg.Image(filename='../img/test.png', key='canvas_in_signal')]
]

# output column fields
column_out = [
    [sg.Text('output file', size=(8, 1)), sg.Input(default_text='../data/out.wav', key='out_path'), sg.FileBrowse()],
    [sg.Button('play output audio', key='play_out_audio')],
    [sg.Image(filename='../img/test.png', key='canvas_out_stft')],
    [sg.Image(filename='../img/test.png', key='canvas_out_signal')]
]

# GUI's layout
layout = [
    [sg.Column(column_in, background_color='#F7F3EC'),
     sg.Column(column_out, background_color='#F7F3EC')],
    [sg.Text('Number of filters: '),
     sg.Slider((10, 100), key='number_of_filters', orientation='h', disable_number_display=True, enable_events=True),
     sg.Text('100', key='num_text')],
    [sg.Text('Compression level: 0    ', key='compression_level')],
    [sg.Button('Process')]
]
