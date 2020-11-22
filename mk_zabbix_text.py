#!python3
# mk_purple_text.py - create text file to load all former values in to zabbix

'''
    !!WARNING!! zabbix will accept a limited number of data points at one time!
    This will still overload diskI/O on the server!

    ensure zabbix items are preconfigured before sending to server
'''

from dataloggers import PurpleAir, Kestrel, CampbellSci, write_txt
import os
import sys

if __name__ == '__main__':

    # p = PurpleAir(36031)
    # purple_file = 'old_data/old_purple.csv'
    # purple_data = p.format_csv(purple_file)

    # k = Kestrel('redKestrel')
    # kestrel_file = 'old_data/kestrel_drop_old.csv'
    # kestrel_data = k.format_csv(kestrel_file)
    
    c = CampbellSci('rosenthal')
    c_file = 'old_data/CR1000XSeries_Rain_guage.dat'
    campbell_data = c.format_csv(c_file)

    # write_txt(purple_data)
    # write_txt(kestrel_data)
    write_txt(campbell_data)
