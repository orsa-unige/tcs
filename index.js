"use strict";


var telnet = require("telnet-client")
var connection = new telnet()

var params = {
    host: "localhost",
    port: 65432,
    shellPrompt: "/ # ",
    timeout: 1500,
    // removeEcho: 4
}

connection.connect(params)
    .then(function(prompt) {
        connection.exec(cmd)
            .then(function(res) {
                console.log('promises result:', res)
            })
    }, function(error) {
        console.log('promises reject:', error)
    })
    .catch(function(error) {
        console.log('catched error:', error)
    })
