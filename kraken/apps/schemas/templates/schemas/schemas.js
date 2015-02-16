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

        for (i = 0; i < field_number; i++){
            var contents_body_row = '<tr>';
            for (var j = 0; j < Number(record_number); j++){
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


$('#validation_schema_to_input').click(function(){
    var field_number = 5;

    var input = $('#textareaViewer').val();
    if (! input) {
        alert('No input from Input');
    } else if (! $('#record11').length > 0){
        alert('You need generate record first.');
    } else {
        var delimiter = '{{version.delimiter}}';
        var rows = input.split('\n');

        if (delimiter == 'Pipe') {
            for (var i = 0; i < rows.length; i++) {
                var columns = rows[i].split('|');
                for (var j = 0; j < field_number; j++) {
                    $('#record{0}{1}'.format(j, i)).val(columns[j]);
                }
            }
        } else if (delimiter == 'Fixed') {
            $('#record11').val(input) ;
        } else if (delimiter == 'Comma') {
            for (var i = 0; i < rows.length; i++) {
                var columns = rows[i].split(',');
                for (var j = 0; j < field_number; j++) {
                    $('#record{0}{1}'.format(j, i)).val(columns[j]);
                }
            }
        }
    }
});


$('#validation_input_to_schema').click(function(){
    if ($('#record11').length > 0){
        if (!$('#record11').val()){
            alert('No input from Schema');
        } else {
            alert($('#record11').val());
        }
    } else {
        alert('You need generate record first.');
    }
});