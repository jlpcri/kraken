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

var file_names = '{{version_files_names }}';

$("button[name='save_file']").on('click', function () {
    if ( !$.trim($("#textareaViewer").val()) ) {   // check file contents empty
        showErrMsg('No input of contents');
        return false;
    } else if ( !$("#id_name").val() ){   //check file name empty
        showErrMsg('No input of file name');
        return false;
    } else if ( $.inArray('\\', $("#id_name").val()) > -1 ) {
        showErrMsg('File name cannot include \'\\\'');
        return false;
    } else if ($.inArray($('#id_name').val(), file_names) > -1) {
        showErrMsg('File Name is duplicated');
        return false;
    }

    var payloads = [];
    $("#tableDefinitions tbody tr").each(function () {
        var type = $(this).find("select option:selected").val();
        var payload = $(this).find("select option:selected").attr('data-payload');
        payloads.push({"type": type, "payload": payload});
    });
    $('input[name="payloads"]').val(JSON.stringify(payloads));
    window.content_change = false;
});

//check textarea contents changed or not
window.content_change = false;
$('#textareaViewer').change(function (){
    window.content_change = true;
});

$("button[name='download_file']").on('click', function() {
    if (window.content_change) {
        showErrMsg('Contents Changed, save first');
        return false;
    }
});

// Total fail generate data no more than X times
var fail_generate = 0;

$('#buttonGenerate').click(function () {
    if (fail_generate > 19) {
        showErrMsg('Retry data generation up to 20 times');
        return false;
    }

    // initialize errMsg
    $('#errMsg').html('');
    var record_number = $('#inputRecordNumber').val();

    if (!$.isNumeric(record_number)) {
        showErrMsg('Records to Generate \'' + record_number + '\' is not a Number');
        //$('#errMsg').html('Input \'' + record_number + '\' is not a Number');
    } else if ($.inArray('.', record_number) > -1 || record_number <= 0) {
        showErrMsg('Records to Generate \'' + record_number + '\' should be positive integer. ');
    } else if (Number(record_number) > 1000) {
        showErrMsg('Records to Generate should be less than 1000.');
    } else if (field_number == 0) {
        showErrMsg('No schema field is added, Cannot generate records');
    } else {
        // check column configuration error
        var error_found = false;
        $("#tableDefinitions tbody tr").each(function() {
            var column_config = $(this).find(".data-generator-params > select").val();
            if (column_config == 'specify') {
                showErrMsg('Please select column configuration');
                error_found = true;
                return false;
            }
        });
        if (error_found) {
            return false;
        }

        generateRecords(record_number);

        var delimiter = '{{version.delimiter}}';

        // calculate record number which has value
        var found = true, record_number = 0;
        while (found) {
            if (!$('#record_0_{0}'.format(record_number)).val()) {
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
                        $('#record_{0}_{1}'.format(j, i)).val('');
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

            //showSuccessMsg('No errors found');
        }
    }
});


$('#validation_schema_to_input').click(function () {
    // initialize errMsg
    $('#errMsg').html('');

    if ($('#record_0_0').length > 0) {
        if (!$('#record_0_0').val()) {
            showErrMsg('No input from Schema');
        } else {
            //var field_number = 5;
            var delimiter = '{{version.delimiter}}';

            // calculate record number which has value
            var found = true, record_number = 0;
            while (found) {
                if (!$('#record_0_{0}'.format(record_number)).val()) {
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
            showErrMsg('Row ' + Number(i + 1) + ' exceeds total length of schema.');
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
                    var current_field_name = $('#field_type_{0}'.format(j)).closest('tr').find('td:first').text().trim();
                    showErrMsg('Row \'{0}\' Field \'{1}\' is not Number.'.format(rows[i].substring(0, 25), current_field_name));
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
                    $('#record_{0}_{1}'.format(j, i)).val(field);
                }
                position += Number(length);
            }
        }
        showSuccessMsg('No errors found');
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
            showErrMsg('Row ' + Number(i + 1) + ' exceeds field number.');
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
                    var current_field_name = $('#field_type_{0}'.format(j)).closest('tr').find('td:first').text().trim();
                    showErrMsg('Row \'{0}\' Field \'{1}\' exceeds length limitation.'.format(rows[i].substring(0, 25), current_field_name));
                    break;
                }
                // check type
                if (columns[j] && type == 'Number' && isNaN(columns[j])) {
                    field_type_error_found = true;
                    var current_field_name = $('#field_type_{0}'.format(j)).closest('tr').find('td:first').text().trim();
                    showErrMsg('\'{0}\' Field \'{1}\' is not Number.'.format(rows[i].substring(0, 25), current_field_name));
                    break;
                }
            }

            if (field_length_error_found || field_type_error_found) {
                break;
            }
        }
    }

    if (!field_number_error_found && !field_length_error_found && !field_type_error_found) {
        for (var i = 0; i < rows.length; i++) {
            var columns = rows[i].split(delimiter);
            for (var j = 0; j < field_number; j++) {
                $('#record_{0}_{1}'.format(j, i)).val(columns[j]);
            }
        }
        showSuccessMsg('No errors found');
    }
}

function parse_schema(record_number, delimiter) {
    var schema_string = '',
        undefined_error_found = false,
        field_length_error_found = false,
        field_type_error_found = false,
        inner_loop_error_found = false;

    // Check length and type of per field
    for (var i = 0; i < record_number; i++) {
        for (var j = 0; j < field_number; j++) {
            var type = $('#field_type_' + j).val();
            var length = $('#field_length_' + j).val();

            // check undefined
            if ($('#record_{0}_{1}'.format(j, i)).val() == 'undefined') {
                undefined_error_found = true;
                inner_loop_error_found = true;
                showErrMsg('Number of generated records increased for Manual Input');
                break;
            }

            // check length
            if ($('#record_{0}_{1}'.format(j, i)).val().length > length) {
                field_length_error_found = true;
                inner_loop_error_found = true;
                //showErrMsg('Length of Record ' + Number(i + 1) + ' Field ' + Number(j + 1) + ' exceeds limitation.');
                var current_field_name = $('#field_type_{0}'.format(j)).closest('tr').find('td:first').text().trim();
                showErrMsg('Generated data length error of field: {0}'.format(current_field_name));
                break;
            }

            // check type
            if (type == 'Number' && isNaN($('#record_{0}_{1}'.format(j, i)).val())) {
                field_type_error_found = true;
                inner_loop_error_found = true;
                //showErrMsg('Contents of Record ' + Number(i + 1) + ' Field ' + Number(j + 1) + ' is not Number.');
                showErrMsg('Generated data type  error');
                break;
            }
        }

        if (inner_loop_error_found) {
            break;
        }

    }

    if (!undefined_error_found && !field_length_error_found && !field_type_error_found) {
        for (var i = 0; i < record_number; i++) {
            for (var j = 0; j < field_number; j++) {
                var length = $('#field_length_' + j).val(),
                    content = $('#record_{0}_{1}'.format(j, i)).val();

                while (delimiter == '' && content.length < length) {
                    content += ' ';
                }
                schema_string += content;
                if ($('#record_{0}_{1}'.format(j, i)).val() && j < field_number - 1) {
                    schema_string += delimiter;
                }
            }

            schema_string += '\n';
        }

        //reset total fail generate times
        fail_generate = 0;

    } else {
        // fail generate times add 1
        fail_generate += 1;
    }

    $('#textareaViewer').val(schema_string);
}

function showErrMsg(message) {
    $('#errMsg').css({
        //'font-family': 'Comic Sans MS',
        'font-size': 15,
        'color': 'blue'
    });
    $('#errMsg').html('Error: ' + message);
}

function showSuccessMsg(message) {
    $('#errMsg').css({
        //'font-family': 'Comic Sans MS',
        'font-size': 15,
        'color': 'green'
    });
    $('#errMsg').html('Successful: ' + message);
}

function generateRecords(record_number) {
    $('#errMsg').html('');
    var contents_head = '<tr>';
    for (var i = 1; i < Number(record_number) + 1; i++) {
        contents_head += '<th>Record ' + i + '</th>';
    }
    contents_head += '</tr>';

    var data = [];
    $("#tableDefinitions tbody tr").each(function () {
        // Field Type
        var field_type = $(this).find("input[name^='field_type_']").val();
        // Field Length
        var field_length = $(this).find("input[name^='field_length_']").val();
        // Data Generator Type
        var type = $(this).find(".data-generator-select option:selected").val();
        // Generator Options
        var generate = $(this).find(".data-generator-params option:selected").val();
        // Generator Option Parameters
        var payload = $(this).find(".data-generator-params > select option:selected").attr('data-payload');
        var d = [];
        if (type == "Text") {
            generate = generate.substring(5);
            //var generate = "manual";
            var fill = "";
            try {
                var p = $.parseJSON(payload);
                for (var i = 0; i < p.length; i++) {
                    if (p[i]['name'] == "inputFill") {
                        fill = p[i]['value'];
                    }
                }
            } catch (e) {
                if (generate != 'random') {
                    var rowindex = $(this).closest('tr').index() + 1;
                    showErrMsg('Row {0} Column Configuration invalid'.format(rowindex));
                    return false;
                }
            }

            if (generate == "manual") {
                // generate empty fields
                for (var i = 0; i < record_number; i++) {
                    d.push(p[i]);
                }
            } else if (generate == "fill") {
                // use value from fill to generate fields
                for (var i = 0; i < record_number; i++) {
                    d.push(fill);
                }
            } else if (generate == "random") {
                // use mockjson to get random text for generating fields
                var s = "result|{0}-{1}".format(record_number, record_number);

                var textTemplate = {};
                textTemplate[s] = [
                    { "text": "@LOREM" }
                ];

                try {
                    $.mockJSON(/mockme\.json/, textTemplate);

                    $.getJSON('mockme.json', function(json) {
                        for (var i = 0; i < json['result'].length; i++) {
                            d.push(json['result'][i]['text'].substring(0, field_length));
                        }
                    });
                } catch(e) {
                    alert('Invalid JSON');
                }
            }
        } else if (type == "Number") {
            generate = generate.substring(7);
            var min = 0;
            var max = 9;
            //var generate = "manual";
            var fill = "";
            var increment = 0;
            try {
                var p = $.parseJSON(payload);
                for (var i = 0; i < p.length; i++) {
                    if (p[i]['name'] == "min") {
                        min = p[i]['value'];
                    } else if (p[i]['name'] == "max") {
                        max = p[i]['value'];
                    } else if (p[i]['name'] == "inputFill") {
                        fill = p[i]['value'];
                    } else if (p[i]['name'] == "inputIncrement") {
                        increment = p[i]['value'];
                    }
                }
            } catch (e) {
                var rowindex = $(this).closest('tr').index() + 1;
                showErrMsg('Row {0} Column Configuration invalid'.format(rowindex));
                return false;
            }

            if (generate == "manual") {
                // generate empty fields
                for (var i = 0; i < record_number; i++) {
                    d.push(p[i]);
                }
            } else if (generate == "fill") {
                // use value from fill to generate fields
                for (var i = 0; i < record_number; i++) {
                    d.push(fill);
                }
            } else if (generate == "increment") {
                // use value from increment as base value to begin generating fields
                var inc = increment;
                for (var i = 0; i < record_number; i++) {
                    d.push(inc);
                    inc++;
                }
            } else if (generate == "random") {
                // use mockjson to get random numbers for generating fields
                var s = "result|{0}-{1}".format(record_number, record_number);
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
            }
        } else if (type == "Custom List") {
            generate = generate.substr(7);
            //var generate = "inorder";
            var list = [];
            try {
                var p = $.parseJSON(payload);
                for (var i = 0; i < p.length; i++) {
                    if (p[i]['name'] == "list") {
                        list = p[i]['value'].split('\n');
                    }
                }
            } catch (e) {
                var rowindex = $(this).closest('tr').index() + 1;
                showErrMsg('Row {0} Column Configuration invalid'.format(rowindex));
                return false;
            }

            if (generate == "inorder") {
                // use order of values from list to begin generating fields
                var len = list.length;
                var inc = 0;
                if (len > 0) {
                    for (var i = 0; i < record_number; i++) {
                        if (inc >= len) {
                            inc = 0;
                        }
                        d.push(list[inc]);
                        inc++;
                    }
                }
            } else if (generate == "random") {
                // use mockjson to randomize list items for generating fields
                var s = "result|{0}-{1}".format(record_number, record_number);
                $.mockJSON.data.CUSTOM_LIST = list;

                var textTemplate = {};
                textTemplate[s] = [
                    { "item": "@CUSTOM_LIST" }
                ];

                try {
                    $.mockJSON(/mockme\.json/, textTemplate);

                    $.getJSON('mockme.json', function(json) {
                        for (var i = 0; i < json['result'].length; i++) {
                            d.push(json['result'][i]['item'].substring(0, field_length));
                        }
                    });
                } catch(e) {
                    alert('Invalid JSON');
                }
            }
        } else if (type == "First Name") {
            // use mockjson to get random first names for generating fields
            var s = "result|{0}-{1}".format(record_number, record_number);

            var textTemplate = {};
            textTemplate[s] = [
                { "name": "@MALE_FIRST_NAME" }
            ];

            try {
                $.mockJSON(/mockme\.json/, textTemplate);

                $.getJSON('mockme.json', function(json) {
                    for (var i = 0; i < json['result'].length; i++) {
                        d.push(json['result'][i]['name'].substring(0, field_length));
                    }
                });
            } catch(e) {
                alert('Invalid JSON');
            }
        } else if (type == "Last Name") {
            // use mockjson to get random last names for generating fields
            var s = "result|{0}-{1}".format(record_number, record_number);

            var textTemplate = {};
            textTemplate[s] = [
                { "name": "@LAST_NAME" }
            ];

            try {
                $.mockJSON(/mockme\.json/, textTemplate);

                $.getJSON('mockme.json', function(json) {
                    for (var i = 0; i < json['result'].length; i++) {
                        d.push(json['result'][i]['name'].substring(0, field_length));
                    }
                });
            } catch(e) {
                alert('Invalid JSON');
            }
        } else if (type == "Address") {
            // Adding the @US_STATE keywork
            $.mockJSON.data.US_STATE = [
                'AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA',
                'HI','ID','IL','IN','IA','KS','KY','LA','ME','MD',
                'MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ',
                'NM','NY','NC','ND','OH','OK','OR','PA','RI','SC',
                'SD','TN','TX','UT','VT','VA','WA','WV','WI','WY'
            ];
            // use mockjson to get random addresses for generating fields
            var s = "result|{0}-{1}".format(record_number, record_number);

            var textTemplate = {};
            textTemplate[s] = [
                { "address": "@NUMBER@NUMBER@NUMBER @LOREM @US_STATE" }
            ];

            try {
                $.mockJSON(/mockme\.json/, textTemplate);

                $.getJSON('mockme.json', function(json) {
                    for (var i = 0; i < json['result'].length; i++) {
                        d.push(json['result'][i]['address'].substring(0, field_length));
                    }
                });
            } catch(e) {
                alert('Invalid JSON');
            }
        } else if (type == "ZIP Code") {
            generate = generate.substr(8);
            var min, max, n, o = {}, textTemplate = {};
            var s = "result|{0}-{1}".format(record_number, record_number);
            if (generate == '5digits') {
                min = 10000;
                max = 99951;

                n = "zipcode|{0}-{1}".format(min, max);
                o[n] = 0;
                textTemplate[s] = [
                    o
                ];
            } else if (generate == '9digits') {
                min = 100000000;
                max = 999519999;

                n = "zipcode|{0}-{1}".format(min, max);
                o[n] = 0;
                textTemplate[s] = [
                    o
                ];
            } else if (generate == '9digitshyphen') {
                //n = "zipcode|{0}-{1}".format(second_min, second_max);
                textTemplate[s] = [{
                    "zipcode": "@NUMBER@NUMBER@NUMBER@NUMBER@NUMBER-@NUMBER@NUMBER@NUMBER@NUMBER"
                }];
            }

            try {
                $.mockJSON(/mockme\.json/, textTemplate);

                $.getJSON('mockme.json', function(json) {
                    for (var i = 0; i < json['result'].length; i++) {
                        d.push(json['result'][i]['zipcode']);
                    }
                });
            } catch(e) {
                alert('Invalid JSON');
            }
        }
        data.push(d);
    });

    if (data.length == field_number) {
        var contents_body = '';
        for (i = 0; i < field_number; i++) {
            var contents_body_row = '<tr>';
            for (var j = 0; j < Number(record_number); j++) {
                contents_body_row += "<td><input id={0} name='' type='text' class='form-control' value='{1}'></td>".format('record_' + i + '_' + j, data[i][j]);
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
}

function generate_empty_records_modal(record_number, location) {
    var cell_id = '';
    if (location == '#text-manual-input') {
        cell_id = 'text';
    } else if (location == '#number-manual-input') {
        cell_id = 'number';
    }


    var contents_head = '<tr>';
    for (var i = 1; i < Number(record_number) + 1; i++) {
        contents_head += '<th>Record ' + i + '</th>';
    }
    contents_head += '</tr>';

    var contents_body = '';
    for (var i = 0; i < Number(record_number); i++) {
        contents_body += "<td><input id={0} name='' type='text' class='form-control' ></td>".format(cell_id + i );
    }
    var contents = "<table id='tableData' class='table'>" +
        " <thead>" +
        contents_head +
        "</thead>" +
        "<tbody>" +
        contents_body +
        "</tbody>" +
        "</table> ";
    $(location).html(contents);
}

function showModalErrMsg(location, message) {
    $(location).css({
        'font-size': 15,
        'color': 'blue'
    });
    $(location).html('Error: ' + message);
}
