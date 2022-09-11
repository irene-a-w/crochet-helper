import PySimpleGUI as sg
import json
import os

#if button is clicked -> increase amount of stitches by one -> calculate number of stitches remaining and rows -> track current # of stitches and rows
#user needs to enter number of stitches and rows (for square pattern)

#later -> manually add pattern
#later -> read pattern

#button pressed -> stitch increased, stitches left decreased

def save(save_dict):
    layout = [[sg.Text('Enter name of save file'), sg.Input('', key='-name-'), sg.Button('Save', key='-save-'), sg.Button('Update', key='-update-')],
              [sg.Text('', key='-success-')]]
    save = sg.Window('Save', layout)

    while True:
        event, values = save.read()

        if event == sg.WIN_CLOSED:
            break

        if event == '-save-':
            name = values['-name-']
            save_dict["file name"] = name

            # check if file name already exists
            f = open("save files/save_info.json")
            check = json.load(f)
            # if len(check["save data"]) != 0:
            for file in check["save data"]:
                if name == file["file name"]:
                    save['-success-'].update("You already have a file with that name.")
                    break
            store_data("save files/save_info.json", save_dict)
            save['-success-'].update("Your data has successfully been saved!")

        if event == '-update-':
            name = values['-name-']
            save_dict["file name"] = name
            f1 = open("save files/save_info.json")
            obj = json.load(f1)
            for file in obj["save data"]:
                if name == file["file name"]:
                    idx = obj["save data"].index(file)
                    obj["save data"][idx] = save_dict
                    f2 = open("save files/save_info.json", "w")
                    json.dump(obj, f2)
                    f2.close()
                    save['-success-'].update("Your data has successfully been updated!")

    save.close()

def stitch_counter():
    layout1 = [
        [sg.Text('Enter the amount of stitches per row', key='-stitches-'), sg.Input('', key='-inputs-'),
         sg.Button('Enter', key='-enters-')],
        [sg.Text('Enter the number of rows', key='-row-'), sg.Input('', key='-inputr-'),
         sg.Button('Enter', key='-enterr-')],
        [sg.Button('Click to increase number of stitches', key='-buttoni-'),
         sg.Button('Click to decrease number of stitches', key='-buttond-')],
        [sg.Text('You have done 0 total stitches.', key='-totals1-'),
         sg.Text('You have 0 stitches left in the row.', key='-totals2-')],
        [sg.Text('You have done 0 rows.', key='-totalr1-'), sg.Text('You have 0 rows left.', key='-totalr2-')],
        [sg.Button('Save', key='-save-'), sg.Button('Reset', key='-reset-')],
        [sg.Text("Name of file:"), sg.Input("", key="-fname-"), sg.Button('Load', key='-load-')]
    ]

    window = sg.Window("Stitch Counter", layout1)

    stitch_count = 0
    row_count = 0
    stitch_total = 0
    row_total = 0

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == '-load-':
            f = open("save files/save_info.json")
            obj = json.load(f)
            for file in obj["save data"]:
                if values['-fname-'] in file['file name']:
                    data = file
                    stitch_total = data["remaining stitches"]
                    row_total = data["remaining rows"]
                    remaining_stitch = f'You have {data["remaining stitches"]} stitches left in the row.'
                    window['-totals2-'].update(remaining_stitch)
                    remaining_row = f'You have {data["remaining rows"]} rows left.'
                    window['-totalr2-'].update(remaining_row)
                    stitch_inc = f'You have done {data["current stitches"]} total stitches.'
                    window['-totals1-'].update(stitch_inc)
                    stitch_dec = f'You have done {data["current rows"]} total rows.'
                    window['-totalr1-'].update(stitch_dec)

        if event == '-enters-':
            stitch_input = values['-inputs-']
            if stitch_input == '':
                error_popup()
            else:
                stitch_total = int(values['-inputs-'])
                remaining_stitch = f'You have {stitch_input} stitches left in the row.'
                window['-totals2-'].update(remaining_stitch)


        if event == '-enterr-':
            row_input = values['-inputr-']
            if row_input == '':
                error_popup()
            else:
                row_total = int(values['-inputr-'])
                remaining_row = f'You have {row_input} rows left.'
                window['-totalr2-'].update(remaining_row)


        if event == '-buttoni-':
            stitch_count += 1


            if stitch_count <= stitch_total:
                stitch_inc = f'You have done {stitch_count} total stitches.'
                stitch_dec = f'You have {stitch_total-stitch_count} stitches left in the row.'

            elif stitch_count > stitch_total:
                row_count += 1
                stitch_count = 1

                stitch_inc = f'You have done 1 total stitches.'
                stitch_dec = f'You have {stitch_total} stitches left in the row.'
                row_inc = f'You have done {row_count} rows.'
                row_dec = f'You have {row_total-row_count} rows left.'
                window['-totalr1-'].update(row_inc)
                window['-totalr2-'].update(row_dec)
                #increase row, decrease total row
                #reset stitch counter

            window['-totals1-'].update(stitch_inc)
            window['-totals2-'].update(stitch_dec)


        if event == '-buttond-':
            stitch_count -= 1
            if  0 <= stitch_count <= stitch_total:
                stitch_inc = f'You have done {stitch_count} total stitches.'
                stitch_dec = f'You have {stitch_total-stitch_count} stitches left in the row.'

            elif stitch_count == 0 and row_count != 0:
                stitch_inc = f'You have done 0 total stitches.'
                stitch_dec = f'You have {stitch_total} stitches left in the row.'

            elif stitch_count < 0 and row_count != 0:
                row_count -= 1
                stitch_count = stitch_total
                stitch_inc = f'You have done {stitch_count} total stitches.'
                stitch_dec = f'You have {stitch_total - 1} stitches left in the row.'
                row_inc = f'You have done {row_count} rows.'
                row_dec = f'You have {row_total-row_count} rows left.'
                window['-totalr1-'].update(row_inc)
                window['-totalr2-'].update(row_dec)

            window['-totals1-'].update(stitch_inc)
            window['-totals2-'].update(stitch_dec)

        if event == '-save-':
            if values['-inputs-'] == '' and values['-inputs-'] == '' and values['-inputr-'] == '':
                error_popup()
            else:
                save_dict = {}
                save_dict['current stitches'] = stitch_count
                save_dict['remaining stitches'] = stitch_total - stitch_count
                save_dict['current rows'] = row_count
                save_dict['remaining rows'] = row_total - row_count
                # # print(save_dict)
                save(save_dict)

        if event == '-reset-':
            window['-inputs-'].update('')
            window['-inputr-'].update('')
            window['-totals1-'].update('You have done 0 total stitches.')
            window['-totals2-'].update('You have 0 stitches left in the row.')
            window['-totalr1-'].update('You have done 0 rows.')
            window['-totalr2-'].update('You have 0 rows left.')


    #if save button is pressed, save current info as a dictionary then to json file
    #load json file
    #automatically input it in
    window.close()

def yarn_calculator():

    def yarn_amount(stitches, type):
        """

        :param stitches: number of stitches in total pattern
        :param type: type of yarn used
        :return: # of yards of yarn needed
        """
        yarn_dict = {"Fingering": 1, "DK": 1.5, "Worsted": 1.8, "Bulky": 2.5, "Super Bulky": 7.5}
        return (stitches * yarn_dict[type]) / 36

    #interface
    layout = [
        [sg.Text('Enter number of stitches'), sg.Input(key="-input-")],
        [sg.Text('Select type of yarn'), sg.Spin(["Fingering", "DK", "Worsted", "Bulky", "Super Bulky"], size = (10,1), key='-type-')],
        [sg.Button('Calculate', key='-enter-'), sg.Text('', key='-output-')],
        [sg.Button('Reset', key='-reset-')]
    ]

    window = sg.Window("Yarn Calculator", layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == '-enter-':
            input_values = values['-input-']
            if input_values.isnumeric():
                if values['-type-'] == 'Fingering':
                    yards = round(yarn_amount(int(input_values), 'Fingering'), 1)
                    output = f'You will need {yards} yards.'
                elif values['-type-'] == 'DK':
                    yards = round(yarn_amount(int(input_values), 'DK'), 1)
                    output = f'You will need {yards} yards.'
                elif values['-type-'] == 'Worsted':
                    yards = round(yarn_amount(int(input_values), 'Worsted'), 1)
                    output = f'You will need {yards} yards.'
                elif values['-type-'] == 'Bulky':
                    yards = round(yarn_amount(int(input_values), 'Bulky'), 1)
                    output = f'You will need {yards} yards.'
                elif values['-type-'] == 'Super Bulky':
                    yards = round(yarn_amount(int(input_values), 'Super Bulky'), 1)
                    output = f'You will need {yards} yards.'
                window["-output-"].update(output)
            else:
                window["-output-"].update('Please enter the number of stitches.')

        if event == '-reset-':
            window["-output-"].update('')

    window.close()

def error_popup():
    error_layout = [[sg.Text('You have entered no values!')]]
    error = sg.Window('Error', error_layout)

    while True:
        event, values = error.read()

        if event == sg.WIN_CLOSED:
            break

    error.close()

def store_data(fpath, ob):
        f = open(fpath)
        add = json.load(f)
        add["save data"].append(ob)
        updated = open(fpath, 'w')
        json.dump(add, updated)
        updated.close()

layout = [[sg.Button('Yarn Calculator', key='-calculator-'), sg.Button('Stitch Counter', key='-counter-')]]
opening = sg.Window('Crochet Helper', layout)

while True:
    event, values = opening.read()

    if event == sg.WIN_CLOSED:
        break

    if event == '-counter-':
        stitch_counter()

    if event =='-calculator-':
        yarn_calculator()

opening.close()

