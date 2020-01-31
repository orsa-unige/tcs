


// /// Copy paste in node console:

var tel = require('./index')

var cmd='1 get object.horizontal.alt'

tel.connect()

tel.send('1 set object.equatorial.dec=10')

tel.send(cmd)

tel.send('1 set object.equatorial.dec=60')

tel.send(cmd)

tel.start_poll(cmd,2000)

tel.stop_poll()

tel.disconnect()

// /// Copy and paste in node console OR run as script

var tel = require('./index')

var cmd='1 get object.horizontal.alt'

tel.send_once('1 get object.horizontal.alt')

tel.send_once('1 set object.equatorial.dec=10')


