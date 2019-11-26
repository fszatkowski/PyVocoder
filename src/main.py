from interface.callbacks import Parameters, play_in_audio, play_out_audio, process
from interface.gui import *

dispatch_dictionary = {
    "Process": process,
    "play_in_audio": play_in_audio,
    "play_out_audio": play_out_audio,
}


if __name__ == "__main__":
    params = Parameters()
    window = sg.Window("Vocoder model", layout, no_titlebar=False)
    while True:
        event, values = window.read(timeout=0)
        if event in (None, "Exit"):
            break

        num_filters = int(values["number_of_filters"])

        window["num_text"].update(num_filters)
        if event in dispatch_dictionary:
            params = Parameters(
                num_filters=num_filters,
                input_path=values["in_path"],
                output_path=values["out_path"],
            )
            fun_to_call = dispatch_dictionary[event]
            fun_to_call(params)
        if event == "Process":
            window["compression_level"].update(
                f"Compression level: {params.compression_level}%"
            )
            window["canvas_in_stft"].update(filename=constants.INPUT_SPECTRUM)
            window["canvas_in_signal"].update(filename=constants.INPUT_SIGNAL)
            window["canvas_out_stft"].update(filename=constants.OUTPUT_SPECTRUM)
            window["canvas_out_signal"].update(filename=constants.OUTPUT_SIGNAL)

    window.close()
