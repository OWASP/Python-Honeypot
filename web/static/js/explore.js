/**
 * Load list of modules in a select list
 */
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


// Get the file name of the export file
function get_export_fileName(file_type){
  var d = new Date();
  var n = d.getTime();
  if(file_type == 'csv')
    return './Honeypot-data-csv-' + n + ".csv";
  else if(file_type == 'excel')
    return './Honeypot-data-excel-' + n + ".xlsx";
}


/**
 * Call the API to get event data from the database
 * @param {*} api_endpoint : API endpoint URL
 * @param {*} columns_def : Column definition for the selected event type
 * @param {*} api_params  : GET parameters for the API call
 */
function call_api(api_endpoint, columns_def, api_params){
  $(document).ready(function() {

    var table = $('#datatable').dataTable({
      ajax: {
            type: "GET",
            url: api_endpoint,
            contentType:'application/json; charset=utf-8',
            data: api_params,
            dataType: "json",
            dataSrc: ""
        },
      autoWidth: true,
      dom: "<'row'<'col-sm-12 col-md-6'B><'col-sm-12 col-md-6'f>>" +
      "<'row'<'col-sm-12'tr>>" +
      "<'row'<'col-sm-12 col-md-5'li><'col-sm-12 col-md-7'p>>",
      buttons: [
        {
          extend: 'csv',
          filename: function () { return get_export_fileName('csv');},
          className: "export-button btn-success"
        },
        {
          extend: 'excel',
          filename: function () { return get_export_fileName('excel');},
          className: "export-button btn-success"
        }
      ],
      columns:columns_def,
      destroy: true,
      order: [0, 'desc'],
      sort: true,
      info: true,
      paging: true,
      oLanguage: {
        sStripClasses: "",
        sSearch: "",
        sSearchPlaceholder: "Search filter...",
        sInfo: "_START_ -_END_ of _TOTAL_",
        sLengthMenu: '<span>Rows per page:</span><select class="browser-default">' +
          '<option value="10">10</option>' +
          '<option value="20">20</option>' +
          '<option value="30">30</option>' +
          '<option value="40">40</option>' +
          '<option value="50">50</option>' +
          '<option value="-1">All</option>' +
          '</select></div>'
      },
      searching:true,
      responsive: true
    });
  });
}


/**
 * Load data to the table based on user selected filters.
 * @param {*} event_type 
 * @param {*} module_name 
 * @param {*} start_date 
 * @param {*} end_date 
 */
function load_data(event_type, module_name, start_date, end_date) {
  if ( $.fn.dataTable.isDataTable( '#datatable' ) ) {
    $('#datatable').DataTable().clear().destroy();
    $('#datatable').empty();
  }
  var columns = [];
  var api_endpoint = "/api/events/get-events-data";
  var limit = 1000;

  // Define table columns based on selected event type
  if(event_type == "honeypot-event"){
    columns = [
      { data: 'date', defaultContent: '', title: "Date"},
      { data: 'ip_src', defaultContent: '', title: "Src IP"},
      { data: 'port_src', defaultContent: '', title: "Src Port"},
      { data: 'ip_dest', defaultContent: '', title: "Dest IP"},
      { data: 'port_dest', defaultContent: '', title: "Dest Port"},
      { data: 'module_name', defaultContent: '', title: "Module Name"},
      { data: 'machine_name', defaultContent: '', title: "Machine Name"},
      { data: 'country_ip_src', defaultContent: '', title: "Src Country"},
      { data: 'country_ip_dest', defaultContent: '', title: "Dest Country"}];
  }
  else if( event_type == "network-event"){
    columns = [
      { data: 'date', defaultContent: '', title: "Date"},
      { data: 'ip_src', defaultContent: '', title: "Src IP"},
      { data: 'port_src', defaultContent: '', title: "Src Port"},
      { data: 'ip_dest', defaultContent: '', title: "Dest IP"},
      { data: 'port_dest', defaultContent: '', title: "Dest Port"},
      { data: 'machine_name', defaultContent: '', title: "Machine Name"},
      { data: 'country_ip_src', defaultContent: '', title: "Src Country"},
      { data: 'country_ip_dest', defaultContent: '', title: "Dest Country"}];
  }
  else if( event_type == "credential-event"){
    columns = [
      { data: 'date', defaultContent: '', title: "Date"},
      { data: 'ip', defaultContent: '', title: "IP"},
      { data: 'module_name', defaultContent: '', title: "Module Name"},
      { data: 'username', defaultContent: '', title: "Username"},
      { data: 'password', defaultContent: '', title: "Password"},
      { data: 'machine_name', defaultContent: '', title: "Machine Name"},
      { data: 'country', defaultContent: '', title: "Country"}];
  }
  else if( event_type == "ics-honeypot-event"){
    columns = [
      { data: 'date', defaultContent: '', title: "Date"},
      { data: 'ip', defaultContent: '', title: "IP"},
      { data: 'module_name', defaultContent: '', title: "Module Name"},
      { data: 'data', defaultContent: '', title: "Data"},
      { data: 'machine_name', defaultContent: '', title: "Machine Name"},
      { data: 'country', defaultContent: '', title: "Country"}];
  }

  // Set API call parameters
  api_params = {event_type: event_type, start_date: start_date, end_date: end_date, limit:limit}

  if(module_name != ""){
    api_params.module_name = module_name;
  }
  
  call_api(api_endpoint, columns, api_params);
}


/**
 * Function called when "submit" button is clicked.
 */
function search() {
    var event_type=$("select[name='event_type'] option:selected").val();
    var module_name=$("select[name='module_names'] option:selected").val();
    var start_date=$("#start_date").val();
    var end_date=$("#end_date").val();

    if(start_date == "" || end_date == ""){
      alert("Either Start Date or End date missing!")
    }
    else{
      if(start_date <= end_date){
        load_data(event_type, module_name, start_date, end_date);
      }
      else{
        alert("Start date is greater than End date!")
      }
    }
}


/**
 * Form update based on event type selected
 */
function change_form(){
    var events_with_module = new Array("honeypot-event", "credential-event")
    var event_type=$("select[name='event_type'] option:selected").val();

    if(events_with_module.indexOf(event_type)>-1){
      document.getElementById("module_names").disabled = false;
    }
    else{
      document.getElementById("module_names").selectedIndex = 0;
      document.getElementById("module_names").disabled = true;
    }
    
}

load_module_options();