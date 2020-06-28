function load_module_options(){
	$.ajax({
        type: "GET",
        url: "/api/events/module-names",
		data: {},
    }).done(function (res) {
		var tableHtml='<option value=\"\"> All Modules </option>';
		for (var i = 0; i < res.module_names.length; i++) {
            var module_name = res.module_names[i];
			tableHtml += "<option value="+
				module_name+">"
				+module_name
			+ "</option>";
        }
		$('#module_names').html(tableHtml);
    }).fail(function (jqXHR, textStatus, errorThrown) {
        document.getElementById('error_msg').innerHTML = jqXHR.responseText;
        if (errorThrown == "BAD REQUEST") {
        }
        if (errorThrown == "UNAUTHORIZED") {
        }
    });
}

function populate_table(result){
    console.log(Object.keys(result[0]));
    var headers = Object.keys(result[0]);
    var table = document.getElementById("event_data_table");
    if(table.rows.length>0){
        table.innerHTML = "";
    }

    var header = table.createTHead();
    var header_row = header.insertRow(-1);

    var header_cell = header_row.insertCell(-1);
    header_cell.innerHTML = "<b><center>#</center></b>";
    
    for (var i = 0; i < headers.length; i++) {
        var header_cell = header_row.insertCell(-1);
        header_cell.innerHTML = "<b><center>"+ headers[i] +"</center></b>";
        console.log(result[0][headers[i]]);
    }

    // var table_body_html = "";
    for(var j = 0; j < result.length; j++) {
        var table_row = table.insertRow(-1);
        var record = result[j];
        console.log(record);

        var body_cell = table_row.insertCell(-1);
        body_cell.innerHTML = "<center>"+ (j+1) +"</center>";
        
        for (var i = 0; i < headers.length; i++) {
            var body_cell = table_row.insertCell(-1);
            body_cell.innerHTML = "<center>" +record[headers[i]]+"</center>";
        }
    }   
       
}


function load_data(event_type) {
    if(event_type == "honeypot-event"){
        // request honeypot events
        $.ajax({
            type: "GET",
            url: "/api/events/honeypot-events",
        }).done(function (res) {
            populate_table(res);
            // console.log(res);
        }).fail(function (jqXHR, textStatus, errorThrown) {
            document.getElementById('error_msg').innerHTML = jqXHR.responseText;
            if (errorThrown == "BAD REQUEST") {
            }
            if (errorThrown == "UNAUTHORIZED") {
            }
        });
    }
    else if( event_type == "network-event"){
        // request honeypot events
        $.ajax({
            type: "GET",
            url: "/api/events/network-events",
        }).done(function (res) {
            populate_table(res);
            for(let key of Object.keys(res[0])){
                console.log(key)
            }
        }).fail(function (jqXHR, textStatus, errorThrown) {
            document.getElementById('error_msg').innerHTML = jqXHR.responseText;
            if (errorThrown == "BAD REQUEST") {
            }
            if (errorThrown == "UNAUTHORIZED") {
            }
        });
    }
}

function search() {
    var event_type=$("select[name='event_type'] option:selected").val();
    var module_name=$("select[name='module_names'] option:selected").val();
    var start_date=$("#start_date").val();
    var end_date=$("#end_date").val();
    
    load_data(event_type);
}

load_module_options();

load_data();