#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import tempfile
import subprocess
import sys

from gsapi import grooveshark


# Handle Error Output
def except_output_handler(except_type, except_value, traceback):
    if except_type == KeyboardInterrupt:
        print('Closing application ...')
    else:
        print(traceback)

sys.excepthook = except_output_handler

os.system('clear')
print "Loading..."
client = grooveshark.Client()
client.init()
run = True


radiodict = {'Alternative':     grooveshark.RADIO_ALTERNATIVE,
             'Rap':             grooveshark.RADIO_RAP,
             'R_AND_B':         grooveshark.RADIO_R_AND_B,
             'Rock':            grooveshark.RADIO_ROCK,
             'Pop':             grooveshark.RADIO_POP,
             'Hip Hop':         grooveshark.RADIO_HIP_HOP,
             'Jazz':            grooveshark.RADIO_JAZZ,
             'Metal':           grooveshark.RADIO_METAL,
             'Electronica':     grooveshark.RADIO_ELECTRONICA,
             'Trance':          grooveshark.RADIO_TRANCE,
             'Ambient':         grooveshark.RADIO_AMBIENT,
             'Country':         grooveshark.RADIO_COUNTRY,
             'Bluegrass':       grooveshark.RADIO_BLUEGRASS,
             'Oldies':          grooveshark.RADIO_OLDIES,
             'Punk':            grooveshark.RADIO_PUNK,
             'Folk':            grooveshark.RADIO_FOLK,
             'Indie':           grooveshark.RADIO_INDIE,
             'Raggae':          grooveshark.RADIO_REGGAE,
             'Experimental':    grooveshark.RADIO_EXPERIMENTAL,
             'Latin':           grooveshark.RADIO_LATIN,
             'Classic':         grooveshark.RADIO_CLASSICAL,
             'Blues':           grooveshark.RADIO_BLUES,
             'Classic Rock':    grooveshark.RADIO_CLASSIC_ROCK}

def menu():
    print "Play radio or search for song?"
    print "1 Search"
    print "2 Radio"
    choose = raw_input("Your choose: ")
    return choose

while run == True:
    if menu() == "1":

        os.system('clear')
        query = raw_input("Search for Song: ")

        print "Top 10 results:"
        for i, song in enumerate(client.search(query)):
            if i < 10:
                    print '%i (%s): %s - %s - %s' % (i + 1, song.id, song.name, song.artist.name, song.album.name)
            else:
                break
        print ""

    else:
        null = open('/dev/null', 'wb')
        os.system('clear')

        for radio in radiodict.keys():
            print radio
        print ""
        radiochoose = raw_input("Radio: ")
        os.system('clear')
        print "Press space to pause. Press Ctlr+C to switch to next Song. Double Ctlr+C to switch it off"
        radio = client.radio(radiodict.get(radiochoose))

        for i in range(0, 1000):
            song = radio.song
            print '%i: %s - %s - %s' % (i + 1, song.name, song.artist.name, song.album.name)
            stream = song.stream
            output = tempfile.NamedTemporaryFile(suffix='.mp3', prefix='grooveshark_')
            process = None
            try:
                output.write(stream.data.read(524288))
                process = subprocess.Popen(['/usr/bin/mplayer', output.name], stdout=null, stderr=null)
                data = stream.data.read(2048)
                while data:
                    output.write(data)
                    data = stream.data.read(2048)
                process.wait()
            except KeyboardInterrupt:
                if process:
                    process.terminate()
            output.close()
        null.close()

