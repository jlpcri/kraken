/**
 * Created by sliu on 2/4/15.
 */

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
