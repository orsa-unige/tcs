var telnet = require('telnet-client');

var params = {
    host: 'localhost',
    port: 65432,
    negotiationMandatory: false,
    sendTimeout: 100
};

exports = module.exports = {

    connect: function(){
        var connection = new telnet();

        connection.connect(params).then(function() {
            console.log("connected");
        });

    }, /// connect

    send_command: function(cmd) {
        var connection = new telnet();

        connection.connect(params).then(function() {
            connection.send(cmd).then(function(res) {
                console.log(res);
                connection.end().then(function(){
                    connection.destroy()
                });
            });
        });

    }, /// send_command

    poll_status: function(cmd,time=1000) {
        var connection = new telnet();

        connection.connect(params).then(function() {
            setInterval(function(){
                connection.send(cmd).then(function(res) {
                    console.log(res);
                });
            },time)
        });

    } /// poll_status

}; /// exports


/// From: https://www.npmjs.com/package/telnet-client
/// From: https://github.com/mkozjak/node-telnet-client/issues/117
