# this file contains GUI elements' definitions

import PySimpleGUI as sg

image_width = 320
image_height = 240

column_in = [
    [sg.Text('input file', size=(8, 1)), sg.Input(), sg.FileBrowse()],
    [sg.Button('play input audio', key='play_in_audio')],
    [sg.Canvas(size=(image_width, image_height), key='canvas_in_stft')],
    [sg.Canvas(size=(image_width, image_height), key='canvas_in_signal')]
]

column_out = [
    [sg.Text('output file', size=(8, 1)), sg.Input(), sg.FileBrowse()],
    [sg.Button('play output audio', key='play_out_audio')],
    [sg.Canvas(size=(image_width, image_height), key='canvas_out_stft')],
    [sg.Canvas(size=(image_width, image_height), key='canvas_out_signal')]
]

layout = [
    [sg.Text('Vocoder model')],
    [sg.Column(column_in, background_color='#F7F3EC'),
     sg.Column(column_out, background_color='#F7F3EC')],
    [sg.Text('Number of filters: '),
     sg.Slider((30, 1000), key='number_of_filters', orientation='h', disable_number_display=True, enable_events=True),
     sg.Text('1000', key='num_text')],
    [sg.Text('Compression level: ', key='compression_level')],
    [sg.Text(' ')],
    [sg.Button('Process')],
    [sg.Text(' ')],
    [sg.Exit()]
]
