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

// get number of fields
var field_number = Number('{{field_number}}');

$('#buttonGenerate').click(function(){
    var record_number = $('#inputRecordNumber').val();
    if (! $.isNumeric(record_number)) {
        alert('Input \'' + record_number + '\' is not a Number');
    }
    else if (field_number == 0){
        alert('No schema field is added, Cannot generate records');
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


$('#validation_input_to_schema').click(function(){

    var input = $('#textareaViewer').val();
    if (! input) {
        alert('No input from Input');
    } else if (! $('#record11').length > 0){
        alert('You need generate record first.');
    } else {
        var delimiter = '{{version.delimiter}}';
        var rows = input.split('\n');

        if (delimiter == 'Fixed') {
            parse_input_fixed(rows);
        } else if (delimiter == 'Pipe') {
            parse_input(rows, '|');
        } else if (delimiter == 'Comma') {
            parse_input(rows, ',');
        }
    }
});


$('#validation_schema_to_input').click(function(){
    if ($('#record00').length > 0){
        if (!$('#record00').val()){
            alert('No input from Schema');
        } else {
            //var field_number = 5;
            var delimiter = '{{version.delimiter}}';

            // calculate record number
            var found = true, record_number = 0;
            while (found) {
                if (! $('#record0{0}'.format(record_number)).val()) {
                    found = false;
                } else {
                    record_number++;
                }
            }

            if (delimiter == 'Fixed'){
                parse_schema(record_number,'');
            } else if (delimiter == 'Pipe') {
                parse_schema(record_number, '|');

            } else if (delimiter == 'Comma'){
                parse_schema(record_number, ',');
            }
        }
    } else {
        alert('You need generate record first.');
    }
});

function parse_input_fixed(rows) {
    var field_length_error_found = false,
        field_type_error_found = false;

    var total_length = $('#fields_total_length').val();
    for (var i = 0; i < rows.length; i++) {
        if (rows[i].length > total_length) {
            field_length_error_found = true;
            alert('Row ' + Number(i + 1) + ' exceed total length of fields.');
            break;
        }
    }

    if (! field_length_error_found) {
        for (var i = 0; i < rows.length; i++) {
            var field, position = 0;
            for (var j = 0; j < field_number; j++) {
                var type = $('#field_type_' + j).val();
                var length = $('#field_length_' + j).val();

                // check type
                field = rows[i].substr(position, length);
                if (field && type == 'Number' && isNaN(field)) {
                    field_type_error_found = true;
                    alert('Row ' + Number(i + 1) + ' Field ' +Number(j + 1) + ' is not Number.');
                    break;
                }
                position += Number(length);
            }
        }
    }

    if (!field_length_error_found && !field_type_error_found) {
        for (var i = 0; i < rows.length; i++) {
            var field, position = 0;
            for (var j = 0; j < field_number; j++) {
                var type = $('#field_type_' + j).val();
                var length = $('#field_length_' + j).val();

                // check type
                field = rows[i].substr(position, length);
                if (field) {
                    $('#record{0}{1}'.format(j, i)).val(field);
                }
                position += Number(length);
            }
        }
    }
}

function parse_input(rows, delimiter) {
    var field_number_error_found = false,
        field_length_error_found = false,
        field_type_error_found = false;

    // Check the number of fields per record
    for (var i = 0; i < rows.length; i++) {
        var columns = rows[i].split(delimiter);
        if (columns.length > field_number) {
            field_number_error_found = true;
            alert('Row ' + Number(i+1) + ' exceed field number.');
            break;
        }
    }

    // Check length and type of per field
    if (! field_number_error_found) {
        for (var i = 0; i < rows.length; i++) {
            var columns = rows[i].split(delimiter);
            for (var j = 0; j < field_number; j++) {
                var type = $('#field_type_'+j).val();
                var length = $('#field_length_' + j).val();
                // check length
                if ( columns[j] && columns[j].length > length) {
                    field_length_error_found = true;
                    alert('Length of row '+Number(i+1) + ' Field ' + Number(j+1) + ' is exceed limitation.');
                    break;
                }
                // check type
                if (columns[j] && type == 'Number' && isNaN(columns[j])) {
                    field_type_error_found = true;
                    alert('Contents of row '+Number(i+1) + ' Field ' + Number(j+1) + ' is not Number.');
                    break;
                }
            }
        }
    }

    if (!field_number_error_found && !field_length_error_found && !field_type_error_found) {
        for (var i = 0; i < rows.length; i++) {
            var columns = rows[i].split(delimiter);
            for (var j = 0; j < field_number; j++) {
                $('#record{0}{1}'.format(j, i)).val(columns[j]);
            }
        }
    }
}

function parse_schema(record_number, delimiter) {
    var schema_string = '',
        field_length_error_found = false,
        field_type_error_found = false;

    // Check length and type of per field
    for (var i = 0; i < record_number; i++) {
        for (var j = 0; j < field_number; j++) {
            var type = $('#field_type_'+j).val();
            var length = $('#field_length_' + j).val();

            // check length
            if ( $('#record{0}{1}'.format(j, i)).val().length > length) {
                field_length_error_found = true;
                alert('Length of Column '+Number(i+1) + ' Field ' + Number(j+1) + ' is exceed limitation.');
                break;
            }

            // check type
            if (type == 'Number' && isNaN($('#record{0}{1}'.format(j, i)).val())){
                field_type_error_found = true;
                alert('Contents of row '+Number(i+1) + ' Field ' + Number(j+1) + ' is not Number.');
                break;
            }
        }
    }

    if (!field_length_error_found && !field_type_error_found) {
        for (var i = 0; i < record_number; i++) {
            for (var j = 0; j < field_number; j++) {
                var length = $('#field_length_' + j).val(),
                    content = $('#record{0}{1}'.format(j, i)).val();
                while ( content.length < length) {
                    content += ' ';
                }
                schema_string += content;
                if ($('#record{0}{1}'.format(j, i)).val() && j < field_number - 1) {
                    schema_string += delimiter;
                }
            }

            schema_string += '\n';
        }
    }

    $('#textareaViewer').val(schema_string);
}