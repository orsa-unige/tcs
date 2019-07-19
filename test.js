var tel = require('./index')

var cmd='1 get object.horizontal.alt'

//tel.connect()

var p=tel.poll_status(cmd,2000)


//tel.send_command('1 get object.horizontal.alt')
//tel.send_command('1 set object.horizontal.alt=10')
//tel.send_command('s')
