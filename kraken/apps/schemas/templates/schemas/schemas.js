/**
 * Created by sliu on 2/13/15.
 */

// String format custom method
String.prototype.format = function () {
    var s = this,
        i = arguments.length;

    while (i--) {
        s = s.replace(new RegExp('\\{' + i + '\\}', 'gm'), arguments[i]);
    }
    return s;
};

// get number of fields
var field_number = Number('{{field_number}}');


$('#buttonGenerate').click(function () {
    // initialize errMsg
    $('#errMsg').html('');
    var record_number = $('#inputRecordNumber').val();

    if (!$.isNumeric(record_number)) {
        showErrMsg('Input \'' + record_number + '\' is not a Number');
        //$('#errMsg').html('Input \'' + record_number + '\' is not a Number');
    }
    else if (field_number == 0) {
        showErrMsg('No schema field is added, Cannot generate records');
    }
    else {
        generateRecords(record_number);
    }
});


$('#validation_input_to_schema').click(function () {
    // initialize errMsg
    $('#errMsg').html('');

    var input = $('#textareaViewer').val();

    if (!input) {
        showErrMsg('No input from Input');
    } else {
        var delimiter = '{{version.delimiter}}';
        var rows = input.split('\n');

        // remove empty line at end
        while (!rows[Number(rows.length) - 1]) {
            rows.splice(-1, 1);
        }

        if (field_number == 0) {
            showErrMsg('No schema field is added, Cannot generate records');
        }
        else {
            // calculate record number which exists
            var found = true, record_number = 0;
            while (found) {
                if ($('#record0{0}'.format(record_number)).length <= 0) {
                    found = false;
                } else {
                    record_number++;
                }
            }

            if (rows.length > record_number) {
                // generate records first
                generateRecords(rows.length);
            } else {
                // clear all fields of records
                for (var i = 0; i < record_number; i++) {
                    for (var j = 0; j < field_number; j++) {
                        $('#record{0}{1}'.format(j, i)).val('');
                    }
                }
            }

            if (delimiter == 'Fixed') {
                parse_input_fixed(rows);
            } else if (delimiter == 'Pipe') {
                parse_input(rows, '|');
            } else if (delimiter == 'Comma') {
                parse_input(rows, ',');
            }
        }
    }
});


$('#validation_schema_to_input').click(function () {
    // initialize errMsg
    $('#errMsg').html('');

    if ($('#record00').length > 0) {
        if (!$('#record00').val()) {
            showErrMsg('No input from Schema');
        } else {
            //var field_number = 5;
            var delimiter = '{{version.delimiter}}';

            // calculate record number which has value
            var found = true, record_number = 0;
            while (found) {
                if (!$('#record0{0}'.format(record_number)).val()) {
                    found = false;
                } else {
                    record_number++;
                }
            }

            if (delimiter == 'Fixed') {
                parse_schema(record_number, '');
            } else if (delimiter == 'Pipe') {
                parse_schema(record_number, '|');

            } else if (delimiter == 'Comma') {
                parse_schema(record_number, ',');
            }
        }
    } else {
        showErrMsg('You need generate record first.');
    }
});

function parse_input_fixed(rows) {
    var field_length_error_found = false,
        field_type_error_found = false;

    var total_length = $('#fields_total_length').val();
    for (var i = 0; i < rows.length; i++) {
        if (rows[i].length > total_length) {
            field_length_error_found = true;
            showErrMsg('Row ' + Number(i + 1) + ' exceed total length of fields.');
            break;
        }
    }

    if (!field_length_error_found) {
        for (var i = 0; i < rows.length; i++) {
            var field, position = 0;
            for (var j = 0; j < field_number; j++) {
                var type = $('#field_type_' + j).val();
                var length = $('#field_length_' + j).val();

                // check type
                field = rows[i].substr(position, length);
                if (field && type == 'Number' && isNaN(field)) {
                    field_type_error_found = true;
                    showErrMsg('Row ' + Number(i + 1) + ' Field ' + Number(j + 1) + ' is not Number.');
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

        // if this line of inputs is empty
        if (columns == '') continue;

        //remove empty at end of each row
        while (!columns[Number(columns.length) - 1]) {
            columns.splice(-1, 1);
        }

        if (columns.length > field_number) {
            field_number_error_found = true;
            showErrMsg('Row ' + Number(i + 1) + ' exceed field number.');
            break;
        }
    }

    // Check length and type of per field
    if (!field_number_error_found) {
        for (var i = 0; i < rows.length; i++) {
            var columns = rows[i].split(delimiter);
            for (var j = 0; j < field_number; j++) {
                var type = $('#field_type_' + j).val();
                var length = $('#field_length_' + j).val();
                // check length
                if (columns[j] && columns[j].length > length) {
                    field_length_error_found = true;
                    showErrMsg('Length of row ' + Number(i + 1) + ' Field ' + Number(j + 1) + ' is exceed limitation.');
                    break;
                }
                // check type
                if (columns[j] && type == 'Number' && isNaN(columns[j])) {
                    field_type_error_found = true;
                    showErrMsg('Contents of row ' + Number(i + 1) + ' Field ' + Number(j + 1) + ' is not Number.');
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
            var type = $('#field_type_' + j).val();
            var length = $('#field_length_' + j).val();

            // check length
            if ($('#record{0}{1}'.format(j, i)).val().length > length) {
                field_length_error_found = true;
                showErrMsg('Length of Record ' + Number(i + 1) + ' Field ' + Number(j + 1) + ' is exceed limitation.');
                break;
            }

            // check type
            if (type == 'Number' && isNaN($('#record{0}{1}'.format(j, i)).val())) {
                field_type_error_found = true;
                showErrMsg('Contents of Record ' + Number(i + 1) + ' Field ' + Number(j + 1) + ' is not Number.');
                break;
            }
        }
    }

    if (!field_length_error_found && !field_type_error_found) {
        for (var i = 0; i < record_number; i++) {
            for (var j = 0; j < field_number; j++) {
                var length = $('#field_length_' + j).val(),
                    content = $('#record{0}{1}'.format(j, i)).val();

                while (delimiter == '' && content.length < length) {
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

function showErrMsg(message) {
    $('#errMsg').css({
        'font-family': 'Comic Sans MS',
        'font-size': 15,
        'color': 'blue'
    });
    $('#errMsg').html('Error: ' + message);
}

function generateRecords(record_number) {
    var contents_head = '<tr>';
    for (var i = 1; i < Number(record_number) + 1; i++) {
        contents_head += '<th>Record ' + i + '</th>';
    }
    contents_head += '</tr>';

    var data = [];
    $("#tableDefinitions tbody tr").each(function () {
        var type = $(this).find("select option:selected").val();
        var payload = $(this).find("select option:selected").attr('data-payload');
        var d = []
        if (type == "Random text") {
            var min = record_number;
            var max = record_number;
            var s = "result|{0}-{1}".format(min, max);

            var textTemplate = {};
            textTemplate[s] = [
                { "text": "@LOREM" }
            ];

            try {
                $.mockJSON(/mockme\.json/, textTemplate);

                $.getJSON('mockme.json', function(json) {
                    console.log(json);
                    for (var i = 0; i < json['result'].length; i++) {
                        d.push(json['result'][i]['text']);
                    }
                });
            } catch(e) {
                alert('Invalid JSON');
            }
        } else if (type == "Number") {
            var s = "result|{0}-{1}".format(record_number, record_number);
            var min = 1000; // from modal
            var max = 9999; // from modal
            var n = "number|{0}-{1}".format(min, max);
            var o = {};
            o[n] = 0;

            var textTemplate = {};
            textTemplate[s] = [
                o
            ];

            try {
                $.mockJSON(/mockme\.json/, textTemplate);

                $.getJSON('mockme.json', function(json) {
                    for (var i = 0; i < json['result'].length; i++) {
                        d.push(json['result'][i]['number']);
                    }
                });
            } catch(e) {
                alert('Invalid JSON');
            }
        } else if (type == "User defined list") {
            for (var i = 0; i < record_number; i++) {
                d.push("list");
            }
        } else if (type == "First name") {
            for (var i = 0; i < record_number; i++) {
                d.push("first name");
            }
        } else if (type == "Last name") {
            for (var i = 0; i < record_number; i++) {
                d.push("last name");
            }
        } else if (type == "Address") {
            for (var i = 0; i < record_number; i++) {
                d.push("address");
            }
        } else if (type == "Zip code") {
            for (var i = 0; i < record_number; i++) {
                d.push("zip code");
            }
        }
        data.push(d);
    })

    var contents_body = '';
    for (i = 0; i < field_number; i++) {
        var contents_body_row = '<tr>';
        for (var j = 0; j < Number(record_number); j++) {
            contents_body_row += "<td><input id={0} name='' type='text' class='form-control' value={1}></td>".format('record' + i + j, data[i][j]);
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