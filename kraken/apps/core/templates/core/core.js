// Session Timeout Redirect to Login
var session_expired,
    session_lastActivity,
    session_now,
    down,
    session_check_interval = 30* 60 * 1000;


function InitSessionTimer(){
    session_expired = 8 * 60 * 60 * 1000;  //Actual timeout 8 hours in milliseconds
    session_lastActivity = new Date().getTime();
    CheckSessionStatus();
}

InitSessionTimer();

function CheckSessionStatus(){
    // Check for session warning
    session_now = new Date().getTime();
    if (session_now > session_lastActivity + session_expired) {
        window.location.href = '/kraken/signout/';
    } else {
        down = setTimeout('CheckSessionStatus();', session_check_interval);
    }
}



// Client
$("#modal_create_client_form").submit(function(event) {
    event.preventDefault();
    var url = "{% url 'core:create_client' %}";
    var posting = $.post( url, $("#modal_create_client_form").serialize() );
    posting.done(function( data ) {
        var data_obj = eval("(" + data + ")");
        if (data_obj.success === true)
        {
            location.reload(true);
        }
        else
        {
            $("#modal_create_client_error").html(data_obj.error);
        }
    });
});
