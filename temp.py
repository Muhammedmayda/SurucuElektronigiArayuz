# hello_psg.py

import PySimpleGUI as sg
import serial
import time
import array

port_name = "Test"
def serial_ports():


    ports = ['COM%s' % (i + 1) for i in range(256)]

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

ports = serial_ports()
layout_column   = [[sg.Text('Lütfen COM-Port Seçiniz(Baud:9600,8N1) : ')],
          [sg.Combo(ports,'Default-COM0',enable_events=True, key='combo',size=(30,0))],
          [sg.Text('Transducer Sayisi: '),sg.Input(default_text = '4',key = '-N-',size=(10,10))],
          [sg.Button('OK'), sg.Button('Cancelled')]]

layout = [[sg.Column(layout_column, element_justification='center')]]
window = sg.Window('MCU Com-Port',layout,finalize=True)

while True:
    event,values = window.read()
    if event is None or event == 'Cancelled':
        break
    if(event=='OK'):
        combo = values['combo']  # use the combo key
        if(combo == "Default-COM0"):
            port_name = "COM0"
        else:
            port_name = combo
        print(port_name)
        break

print ('Port Window Closing....')
window.close()



uart_port = serial.Serial(port=port_name, baudrate=9600, timeout=.1)
def write_read(x):
    uart_port.write(bytes(x, 'utf-8'))
    return 0
layout_column = [[sg.Text('            Transducer - 1'), sg.Text('                                   MCU-'+port_name)],
                 [sg.Text('Frequency(kHz): '),sg.Input(default_text = '1000',key = 'F1',size=(10,10))],
                 [sg.Text('Phase:               '),sg.Input(default_text = '0',key = 'P1',size=(10,10))],
                 [sg.Text('            Transducer - 2')],
                 [sg.Text('Frequency(kHz): '),sg.Input(default_text = '1000',key = 'F2',size=(10,10))],
                 [sg.Text('Phase:               '),sg.Input(default_text = '0',key = 'P2',size=(10,10))],
                 [sg.Text('            Transducer - 3'),sg.Text('                               TIME(s):')],
                 [sg.Text('Frequency(kHz): '),sg.Input(default_text = '1000',key = 'F3',size=(10,10)),sg.Text('        Period:'),sg.Input(default_text = '30',key = 'TM',size=(10,10))],
                 [sg.Text('Phase:               '),sg.Input(default_text = '0',key = 'P3',size=(10,10)),sg.Text('      OnTime:'),sg.Input(default_text = '15',key = 'DT',size=(10,10))],
                 [sg.Text('            Transducer - 4')],
                 [sg.Text('Frequency(kHz): '),sg.Input(default_text = '1000',key = 'F4',size=(10,10))],
                 [sg.Text('Phase:               '),sg.Input(default_text = '0',key = 'P4',size=(10,10))],
                 [sg.Text('Received Data : '), sg.Text(key = '-OUT-')],
                 [sg.Button('OK'), sg.Button('Cancelled')]]

layout = [[sg.Column(layout_column)]]
# Create the window
window = sg.Window('Sürücü Devre Arayüzü',layout,size=(400,400))
# Create an event loop
mylist = []

while True:
    try:
        event,values = window.read()
        if event is None or event == 'Cancelled':
            break
        elif event == 'OK':
            mylist.extend('PC')
            count_total = 0
            for x in range(4):
                mylist.append('N')
                count_total +=1
                mylist.append(x+1)
                count_total +=1
                mylist.append('f')
                count_total +=1
                mylist.append(values['F'+str(x+1)])
                count_total += len(values['F'+str(x+1)])
                mylist.append('p')
                count_total +=1
                mylist.append(values['P'+str(x+1)])
                count_total += len(values['P'+str(x+1)])
            mylist.append('TM')
            mylist.append(values['TM'])
            mylist.append('DT')
            mylist.append(values['DT'])
            mylist.append('FF')
            count_total +=2
            print('MyTotal : ' + str(count_total))
            print('Mylist Size : ' + str(len(str(mylist))))
            counter = 0
            for x in mylist:
                print('Sending(%d) : ' %counter + str(x))
                write_read(str(x))
                counter += 1
            mylist.clear()
            print('-----------------------\n')
            serialReadData = uart_port.readline()
            print(serialReadData.decode('Ascii'))
            window['-OUT-'].update(serialReadData.decode('Ascii'))
    except Exception as e: 
        print(e)
        break
    
print ('Window Closing.. and UART port Closing...')
window.close()
uart_port.close()