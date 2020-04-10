#!/usr/bin/python

# Telnet
import socket, threading, json

# Coordinates
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, ICRS
import datetime

oarpaf = EarthLocation(lat=44.5911*u.deg, lon=9.2035*u.deg, height=1487*u.m)

def command_ok():
    ret="1 COMMAND OK\n"
    return ret

def fail():
    return "1 COMMAND ERROR\n"

def status(key):
    val=10
    
    def targetra():
        if val>=0 and val<=24:
            options[key]=val
            return command_ok();
        else: return fail();
        
    def targetdec():
        if val>=-30 and val<=90:
            options[key]=val
            return command_ok();
        else: return fail();

    def track():
        if val==0 or val==1 or val==2:
            options[key]=val
            return command_ok();
        else: return fail();

    def setalt():
        az=options["object.horizontal.az"][0]
        if val>=10 and val<=90:
            options[key]=val
            convert(val,az,"radec")
            return command_ok();
        else: return fail();

    def setaz():
        alt=options["object.horizontal.alt"][0]
        if val>=0 and val<=360:
            options[key]=val
            convert(alt,val,"radec")
            return command_ok();
        else: return fail();

    def setra():
        dec=options["object.equatorial.dec"][0]
        if val>=0 and val<=24:
            options[key]=val
            convert(val,dec,"altaz")
            return command_ok();
        else: return fail();

    def setdec():
        ra=options["object.equatorial.ra"][0]
        if val>=-30 and val<=90:
            options[key]=val
            convert(ra,val,"altaz")
            return command_ok();
        else: return fail();    
                
    # Map the inputs to the function blocks.
    options={
        'pointing.target.ra'       : [1.045,  targetra ],
        'pointing.target.dec'      : [29.66,  targetdec],
        'pointing.track'           : [0,      track    ],
        'object.horizontal.alt'    : [45,     setalt   ],
        'object.horizontal.az'     : [90,     setaz    ],
        'object.equatorial.ra'     : [1.045,  setra    ],
        'object.equatorial.dec'    : [29.66,  setdec   ],
    }
        
    print("Calling the option: "+key+"...")
    result = options[key][1]() # Call the status function (element 1 of the array).

status('object.equatorial.dec')

