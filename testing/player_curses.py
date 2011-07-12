import curses
import grooveshark
import locale
import tempfile
import subprocess
import sys

# Handle Error Output
#def except_output_handler(except_type, except_value, traceback):
#    if except_type == KeyboardInterrupt:
#        print('Closing application ...')
#    else:
#        print(traceback)
#	curses.nocbreak()
#	stdscr.keypad(0)
#	curses.echo()
#	curses.endwin()
#sys.excepthook = except_output_handler


#Encoding
locale.setlocale(locale.LC_ALL, '')
charcoding = locale.getpreferredencoding()

#Start curses window
mainscreen = curses.initscr()
maxheight, maxwith = mainscreen.getmaxyx()
headscr= curses.newwin(5,maxwith-20,0,20)
stdscr = curses.newwin(maxheight-5,maxwith-20,5,20)
tbar   = curses.newwin(maxheight,20,0,0)
curses.start_color()
curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
tbar.bkgd(curses.color_pair(1))
headscr.bkgd(curses.color_pair(1))
stdscr.bkgd(curses.color_pair(2))
tbar.addstr(1,5,"left")
headscr.addstr(1,5,"test")
headscr.addstr(2,maxwith/2,"Grooveshark-Curses-Player",curses.A_BOLD)
curses.echo()
curses.cbreak()
stdscr.keypad(1)

#Call grooveshark API
stdscr.addstr (0,0,"Loading...")
stdscr.refresh()
client = grooveshark.Client()
client.init()
run = True

#Def radiodict
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

#Def main menu
def menu():
	stdscr.clear()
        stdscr.addstr(0,0, "Play radio or search for song?")
        stdscr.addstr(1,0, "1 Search")
        stdscr.addstr(2,0, "2 Radio" )
	stdscr.addstr(3,0, "Your choose:")
	stdscr.refresh()
        choose = stdscr.getstr(3,13,1)
        return choose


while run==True:
	
	if menu() == "1":
		stdscr.clear()
	        stdscr.addstr(0,0, "Search for:")
	        query = stdscr.getstr(0,12,100)
		stdscr.refresh()
	        stdscr.addstr(1,0, "Top 10 results:")
		count = 2
                for i, song in enumerate(client.search(query)):
            		stdscr.addstr(count,0, (str(song.id)+" "+song.name+" "+song.artist.name+" "+song.album.name).encode(charcoding, errors='ignore'))
            		count+=1
        	stdscr.addstr(count,0,"Press return")
		a = stdscr.getstr(count,0,1)
		stdscr.refresh()

	else:
	        null = open('/dev/null', 'wb')
		stdscr.clear()
		rcount=0
                for radio in radiodict.keys():
                        stdscr.addstr(rcount,0, radio)
			rcount+=1
		stdscr.addstr(rcount,0, "Radio:")
		stdscr.refresh()
                radiochoose = stdscr.getstr(rcount, 7,40)
		stdscr.clear()
                stdscr.addstr(0,1, "Press space to pause. Press Ctlr+C to switch to next Song. Double Ctlr+C to switch it off")
                radio = client.radio(radiodict.get(radiochoose))
                for i in range(0, 1000):
                    song = radio.song
                    stdscr.addstr(1,0, (song.name+" "+song.artist.name+" "+song.album.name).encode(charcoding, errors='ignore'))
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

#Terminate window
curses.nocbreak()
stdscr.keypad(0)
curses.echo()
curses.endwin()




