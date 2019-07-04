import socket, threading

import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, ICRS
import datetime

oarpaf = EarthLocation(lat=44.591307*u.deg, lon=9.203467*u.deg, height=1460*u.m)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 65432))
s.listen(1)

lock = threading.Lock()

welcome_message = 'Welcome to MUD\n1. Go west\n2. Open a window\n3. Quit\n'

status={
        'pointing.track': 0,
        'object.solarsystem.object': 0,
        'object.solarsystem.moon': 1,
        'object.horizontal.alt': 45,
        'object.horizontal.az': 90,
        'object.equatorial.ra': 8.002,
        'object.equatorial.dec': 21.23,
}

def manage_command(data):
        
        def success():
                return "command ok\n"

        def fail():
                return "value out of range\n"

        def unknown():
                return "unknown status command\n"

        def answer(a):
                return str(a)+"\n"

        def convert(c1,c2,frame):
                t = Time(datetime.datetime.now().isoformat(), format='isot', scale='utc') - 2*u.hour

                if frame=='radec':
                        c = SkyCoord(ra=c1*u.degree, dec=c2*u.degree, frame='icrs', obstime=t, location=oarpaf)
                        status['object.horizontal.alt']=c.altaz.alt.deg
                        status['object.horizontal.az']=c.altaz.az.deg
                elif frame=='altaz':
                        c = SkyCoord(alt=c1*u.degree, az=c2*u.degree, frame='altaz', obstime=t, location=oarpaf)                        
                        status['object.equatorial.ra']=c.icrs.ra.deg
                        status['object.equatorial.dec']=c.icrs.dec.deg
                else: unknown();

                
        def setter(cmd):
                if not "=" in cmd:
                        return unknown()
                else:
                        keyval=cmd.strip().split("=")
                        key=keyval[0].strip()
                        val=int(keyval[1])

                if key in status.keys():

                        if key=="pointing.track":
                                if val==0 or val==1 or val==2:
                                        status[key]=val
                                        return success();
                                else: return fail();

                        if key=="object.solarsystem.object":
                                if val>=0 and val<=7:
                                        status[key]=val
                                        return success();
                                else: return fail();

                        if key=="object.solarsystem.moon":
                                if val==0 or val==1:
                                        status[key]=val
                                        return success();
                                else: return fail();

                        if key=="object.solarsystem.object":
                                if val>=0 and val<=7:
                                        status[key]=val
                                        return success();
                                else: return fail();

                        if key=="object.horizontal.alt":
                                if val>=10 and val<=90:
                                        status[key]=val
                                        return success();
                                else: return fail();

                        if key=="object.horizontal.az":
                                if val>=0 and val<=360:
                                        status[key]=val
                                        return success();
                                else: return fail();

                        if key=="object.equatorial.ra":
                                if val>=0 and val<=24:
                                        status[key]=val
                                        return success();
                                else: return fail();

                        if key=="object.horizontal.dec":
                                if val>=-30 and val<=90:
                                        status[key]=val
                                        return success();
                                else: return fail();

                else: return unknown();

        def getter(cmd):
                key=cmd.strip()
                if key in status.keys(): return answer(status[key])
                else: return unknown()


        # removing spaces, getting rid of "1", removing spaces and end of line.
        command=data.strip()[1:].strip().replace("\r\n","")

        setorget=command[0:3]

        if setorget=="set":
                return setter(command[4:])
        elif setorget=="get":
                return getter(command[4:])
        else:
                return 'Not set nor get'


class daemon(threading.Thread):

    def __init__(self, (socket,address)):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address

    def run(self):

        # display welcome message
        self.socket.send(welcome_message)

        while(True):

            # wait for keypress + enter
            data = self.socket.recv(1024)

            # handle menu alterantives and set proper return message
            if data[0] == '1':
                data = manage_command(data)
            elif data[0] == '2':
                data = 'I feel a chilly wind\n'
            elif data[0] == '3':
                break;
            else:
                data = welcome_message

            # send the designated message back to the client
            self.socket.send(data);

        # close connection
        self.socket.close()

while True:
    daemon(s.accept()).start()


# From:
# https://grocid.net/2012/06/14/a-very-simple-server-telnet-example/
