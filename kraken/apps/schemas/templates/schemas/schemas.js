/**
 * Created by sliu on 2/13/15.
 */

// String format custom method
String.prototype.format = function(){
    var s = this,
            i = arguments.length;

    while (i--) {
        s = s.replace(new RegExp('\\{' + i + '\\}', 'gm'), arguments[i]);
    }
    return s;
};


$('#buttonGenerate').click(function(){
    var record_number = $('#inputRecordNumber').val();
    var field_number = 5;
    if (! $.isNumeric(record_number)) {
        alert('Input \'' + record_number + '\' is not a Number');
    }
    else {
        var contents_head = '<tr>';
        for (var i = 1; i < Number(record_number) + 1; i++) {
            contents_head += '<th>Record ' + i + '</th>';
        }
        contents_head += '</tr>';

        var contents_body = '';

        for (i = 1; i < field_number + 1; i++){
            var contents_body_row = '<tr>';
            for (var j = 1; j < Number(record_number) + 1; j++){
                contents_body_row += "<td><input id={0} name='' type='text' class='form-control'></td>".format('record'+i+j);
            }
            contents_body_row += '</tr>';

            contents_body += contents_body_row;
        }

        var add_records_contents = "<table id='tableData' class='table'>" +
                " <thead>" +
                contents_head +
                "</thead>" +
                "<tbody>" +
                "</tbody>" +
                contents_body +
                "</table> ";
        $('#add_records').html(add_records_contents);
    }
});
