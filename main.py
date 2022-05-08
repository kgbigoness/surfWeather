# Triggers the entire project

import weather
import buoy
import PySimpleGUI as sg


def main():
    #set the theme for the screen/window
    sg.theme('DefaultNoMoreNagging')

    # hard code locations we want for buoy data
    buoys_per_locations = {'Wrightsville Beach':'41110', 
                            'Nags Head':'44095',
                            'St. Augustine':'41117',
                            'Oceanside':'46224',
                            'Santa Barbara':'46053',
                            'North Shore':'51201'}

    #define layout
    layout=[[sg.Text('Choose Location', font=('Times New Roman', 28, 'underline'), justification='left'),
                    sg.Combo(list(buoys_per_locations.keys()), font=('Times New Roman', 28), default_value='', key='-IN-')],
            [sg.Text('Air Temperature:', font=('Times New Roman', 24)), sg.Text(key='-OUT1-', font=('Times New Roman', 24))],
            [sg.Text('Temperature min / max:', font=('Times New Roman', 24)), sg.Text(key='-OUT2-', font=('Times New Roman', 24))],
            [sg.Text('Conditions:', font=('Times New Roman', 24)), sg.Text(key='-OUT3-', font=('Times New Roman', 24))],
            [sg.Text('Wind (speed / direction):', font=('Times New Roman', 24)), sg.Text(key='-OUT4-', font=('Times New Roman', 24))],
            [sg.Text('Tide:', font=('Times New Roman', 24)), sg.Text(key='-OUT5-', font=('Times New Roman', 24))],
            [sg.Button('ENTER', font=('Times New Roman',24)), sg.Button('EXIT', font=('Times New Roman', 24))]]

    # create window
    window = sg.Window('Current Buoy & Weather Status', layout)

    # event loop
    while True:
        event, values = window.read()
        if event is None or event == 'EXIT': # if event is closed
            break
        location = values['-IN-']


        # add values to gui
        # weather conidtions
        air_temp = weather.get_weather(location)['main']['temp']
        temp_min = str(weather.get_weather(location)['main']['temp_min'])
        temp_max = str(weather.get_weather(location)['main']['temp_max'])
        conditions = weather.get_weather(location)['weather'][0]['description']
        wind_speed = str(weather.get_weather(location)['wind']['speed'])
        wind_deg = str(weather.get_weather(location)['wind']['deg'])

        # tide conditions
        lat_lon = weather.get_weather(location)['coord']
        lon = lat_lon['lon']
        lat = lat_lon['lat']
        tides = weather.get_tide(lon, lat)


        window['-OUT1-'].update(air_temp)
        window['-OUT2-'].update(temp_min + ' / ' + temp_max)
        window['-OUT3-'].update(conditions)
        window['-OUT4-'].update(wind_speed + ' mph at ' + wind_deg + ' degrees')
        window['-OUT5-'].update(tides)

        # for buoy fn
        buoy_number = buoys_per_locations[location]
        df = buoy.raw_df(buoy_number, '.spec')
        df = buoy.clean_df(df)

        buoy.plot(df)
        
        
    window.close()

    
if __name__ == "__main__":
    main()
