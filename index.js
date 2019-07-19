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
        
        connection.connect(params).then(function() {
            console.log("connected");
        });

    }, /// connect

    send: function(cmd) {
        var connection = this.connection;
            connection.send(cmd).then(function(res) {
                console.log(res);
            });
    }, /// send

    disconnect: function() {
        var connection = this.connection;
                connection.end().then(function(){
                    connection.destroy()
                });
    }, /// disconnect

    send_once: function(cmd) {
        var connection = new telnet();
        connection.connect(params).then(function() {
            connection.send(cmd).then(function(res) {
                console.log(res);
                connection.end().then(function(){
                    connection.destroy()
                });
            });
        });
    }, /// send_once

    start_poll: function(cmd,time=1000) {
        var connection = new telnet();
        connection.connect(params).then(function() {
            clearInterval(this.interval)
            this.interval = setInterval(function(){
                connection.send(cmd).then(function(res) {
                    console.log(res);
                });
            },time)
        });
        
    }, /// start_poll
    
    stop_poll: function() {
        clearInterval(this.interval)
        console.log("ciao")
    }, /// stop_poll
    
}; /// exports


/// From: https://www.npmjs.com/package/telnet-client
/// From: https://github.com/mkozjak/node-telnet-client/issues/117
