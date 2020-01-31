var telnet = require('telnet-client');

var params = {
    host: 'localhost',
    port: 65432,
    negotiationMandatory: false,
    sendTimeout: 100
}

exports = module.exports = {

    connection : new telnet(),
    interval:'',

    connect: function(){
        var connection = this.connection;
        connection.connect(params)
            .then((res) => {
                console.log('result: ', res);
            })
            .catch((err) =>
                   console.log('error: ', err));
    }, /// connect

    send: function(cmd) {
        var connection = this.connection;
        connection.send(cmd)
            .then((res) =>
                  console.log(res))
            .catch((err) =>
                   console.log('error: ', err));
    }, /// send

    disconnect: function() {
        var connection = this.connection;
        connection.end()
            .then((res) =>
                  connection.destroy())
            .catch((err) =>
                   console.log('error: ', err));
    }, /// disconnect

    start_poll: function(cmd,time=1000) {
        var connection = this.connection;
        this.interval = setInterval(function(){
            connection.send(cmd)
            .then((res) =>
                  console.log(res))
            .catch((err) =>
                   console.log('error: ', err));
        },time);
    }, /// start_poll
    
    stop_poll: function() {
        clearInterval(this.interval);
    }, /// stop_poll

    send_once: function(cmd) {
        //var connection = this.connection;
        var connection = new telnet();
        connection.connect(params)
            .then(() =>
                  connection.send(cmd)
                  .then((res) => {
                      console.log(res);
                      connection.end()
                          .then((res) =>
                                connection.destroy())
                          .catch((err) =>
                                 console.log('error: ', err));
                  })
                  .catch((err) =>
                         console.log('error: ', err)))
            .catch((err) => console.log('error: ', err));
    }, /// send_once

}; /// exports


/// From: https://www.npmjs.com/package/telnet-client
/// From: https://github.com/mkozjak/node-telnet-client/issues/117
