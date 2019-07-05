var telnet = require('telnet-client');

var params = {
    host: 'localhost',
    port: 65432,
    negotiationMandatory: false,
    sendTimeout: 100
};

exports = module.exports = {
    
    send_command: function(cmd) {
        var connection = new telnet();

        connection.connect(params).then(function() {

            // first time
            connection.send(cmd).then(function(res) {
                console.log(res);
            });

            // second time
            connection.send(cmd).then(function(res) {
                console.log(res);
            });


        });

    } /// send_command
                
}; /// exports


/// From: https://www.npmjs.com/package/telnet-client
/// From: https://github.com/mkozjak/node-telnet-client/issues/117
