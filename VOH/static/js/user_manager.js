/**
 * Created by Aadhya on 4/20/16.
 */
var socket;
//$(document).ready(function() {
//    socket = io.connect('http://' + document.domain + ':' + location.port + '/queue'); // Connect to socket.io server
//    socket.on('connect', function () {
//            socket.emit('loginTA', {});
//        }
//    )});

function manage_log_status(status){
    socket = io.connect('http://' + document.domain + ':' + location.port + '/queue'); // Connect to socket.io server
    if (status == "Login"){
        console.log("Logging In");
        window.location.href = 'http://' + document.domain + ':' + location.port +"/Login/";
    }
    else{
        console.log("Logging Out");
        $.ajax({
            url:"/Logout/",
            method:"post",
            success:function(data){
                socket.emit('loginTA', {});
                if( window.location.href.includes('/TA/')){

                    socket.emit('logout_alert',{"name":data["name"]});
                }

                window.location.href = "http://localhost:5000/"
            }
        });

    }
}