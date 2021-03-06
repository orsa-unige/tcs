#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Telnet
import socket, threading, json

# Coordinates
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation

# from astropy.utils import iers
# iers.conf.auto_download = False

print ( "TCS Simulator. Conenct with" )
print ( "telnet localhost 65432" )

oarpaf = EarthLocation(lat=44.5911, lon=9.2034, height=1480)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 65432))
s.listen(1)

lock = threading.Lock()

status={
        'pointing.target.ra': 1.045,
        'pointing.target.dec': 29.66,
        'pointing.track': 0,
        'object.solarsystem.object': 0,
        'object.solarsystem.moon': 1,
        'object.horizontal.alt': 45,
        'object.horizontal.az': 90,
        'object.equatorial.ra': 1.045,
        'object.equatorial.dec': 29.66,
        'gps.status' : 2,
        'gps.time' : Time.now().unix,
        'gps.latitude' : oarpaf.lat.deg,
        'gps.longitude' : oarpaf.lon.deg,
        'gps.height' : oarpaf.height.value,
        
}

welcome_message = """
OARPAF telescope simulator
s for status
h for help
q to quit
"""

def manage_command(data):

        def command_ok():
                ret="1 COMMAND OK\n"
                return ret

        def data_inline(key,val):
                ret=command_ok()
                ret+="1 DATA INLINE "+str(key).upper()+"="+str(val)+"\n"
                ret+=command_complete()
                return ret

        def command_complete():
                return "1 COMMAND COMPLETE\n"

        def fail():
                return "1 COMMAND ERROR\n"

        def unknown():
                return "1 UNKNOWN STATUS COMMAND\n"

        def convert(c1,c2,frame):
                if frame=='altaz':
                        c = SkyCoord(ra=c1*u.hourangle, dec=c2*u.degree, frame='fk5', obstime=time, location=oarpaf)
                        status['object.horizontal.alt']=c.altaz.alt.deg
                        status['object.horizontal.az']=c.altaz.az.deg
                elif frame=='radec':
                        c = SkyCoord(alt=c1*u.degree, az=c2*u.degree, frame='altaz', obstime=time, location=oarpaf)
                        status['object.equatorial.ra']=c.icrs.ra.hourangle
                        status['object.equatorial.dec']=c.icrs.dec.deg
                else: unknown();

        def setter(cmd):
                if "=" in cmd:
                        keyval=cmd.strip().split("=")
                        key=keyval[0].strip()
                        val=keyval[1].strip()
                        if not key : unknown()
                        else:
                                try: val=float(val)
                                except: unknown()

                else:
                        return unknown()

                if key in status.keys():

                        if key=="pointing.track":
                                if val==0 or val==1 or val==2:
                                        status[key]=val
                                        return command_ok();
                                else: return fail();

                        elif key=="object.solarsystem.object":
                                if val>=0 and val<=7:
                                        status[key]=val
                                        return command_ok();
                                else: return fail();

                        elif key=="object.solarsystem.moon":
                                if val==0 or val==1:
                                        status[key]=val
                                        return command_ok();
                                else: return fail();

                        elif key=="object.solarsystem.object":
                                if val>=0 and val<=7:
                                        status[key]=val
                                        return command_ok();
                                else: return fail();

                        elif key=="object.horizontal.alt":
                                az=status["object.horizontal.az"]
                                if val>=10 and val<=90:
                                        status[key]=val
                                        convert(val,az,"radec")
                                        return command_ok();
                                else: return fail();

                        elif key=="object.horizontal.az":
                                alt=status["object.horizontal.alt"]
                                if val>=0 and val<=360:
                                        status[key]=val
                                        convert(alt,val,"radec")
                                        return command_ok();
                                else: return fail();

                        elif key=="object.equatorial.ra":
                                dec=status["object.equatorial.dec"]
                                if val>=0 and val<=24:
                                        status[key]=val
                                        convert(val,dec,"altaz")
                                        return command_ok();
                                else: return fail();

                        elif key=="object.equatorial.dec":
                                ra=status["object.equatorial.ra"]
                                if val>=-30 and val<=90:
                                        status[key]=val
                                        convert(ra,val,"altaz")
                                        return command_ok();
                                else: return fail();

                        elif key=="pointing.target.ra":
                                if val>=0 and val<=24:
                                        status[key]=val
                                        return command_ok();
                                else: return fail();

                        elif key=="pointing.target.dec":
                                if val>=-30 and val<=90:
                                        status[key]=val
                                        return command_ok();
                                else: return fail();

                        else: return "not managed yet\n",

                else: return unknown();

        def getter(cmd):
                key=cmd.strip()
                if key in status.keys():
                        val=status[key]
                        return data_inline(key,val)
                else:
                        return unknown()


        # removing spaces, getting rid of "1", removing spaces and end of line.
        command=data.strip()[1:].strip().replace("\r\n","")

        setorget=command[0:3]

        time = Time.now() #(datetime.datetime.utcnow().isoformat(), format='isot')
        status["gps.time"] = time.unix                

        if setorget=="set":
                return setter(command[4:])
        elif setorget=="get":
                return getter(command[4:])
        else:
                return 'Not set nor get\n'


class daemon(threading.Thread):

    def __init__(self, sa):

            threading.Thread.__init__(self)

            self.socket = sa[0]
            self.address = sa[1]

    def run(self):

        # display welcome message
        self.socket.sendall(welcome_message.encode())

        while(True):

            # wait for keypress + enter
            data = (self.socket.recv(1024)).decode()
            #print('request---------------->'+data+'<-------------\n')

            if data:
                    # handle menu alterantives and set proper return message
                    if data[0] == '1':
                            data = manage_command(data)
                    elif data[0] == 'q':
                            break;
                    elif data[0] == 's':
                            data = json.dumps(status, indent=4, sort_keys=True)+'\n'
                    elif data[0] == 'h':
                            data = """Command examples for copy&paste (NO LEADING SPACES!):
                            1 get object.equatorial.dec
                            1 get object.horizontal.alt
                            1 set object.equatorial.dec=10
                            1 set object.horizontal.alt=20
                            \n"""

                    else:
                            data = welcome_message
            else:
                    data = welcome_message

            # send the designated message back to the client
            #print('answer---------------->'+data+'<-------------\n')
            try:
                    self.socket.sendall(data.encode());
                    
            except socket.error as e:
                    print(e)
                    break;

        # close connection
        self.socket.close()

while True:
        daemon(s.accept()).start()


# From:
# https://grocid.net/2012/06/14/a-very-simple-server-telnet-example/
