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

function call_api(api_endpoint, columns_def){
  $(document).ready(function() {

    var table = $('#datatable').dataTable({
      ajax: {
            type: "GET",
            url: api_endpoint,
            contentType:'application/json; charset=utf-8',
            dataType: "json",
            dataSrc: ""
        },
      autoWidth: true,
      columns:columns_def,
      destroy: true,
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


function load_data(event_type) {
  if ( $.fn.dataTable.isDataTable( '#datatable' ) ) {
    $('#datatable').DataTable().clear().destroy();
    $('#datatable').empty();
  }
  var columns = []
  var api_endpoint = ""
     
  if(event_type == "honeypot-event"){
    columns = [
      { data: 'ip_src', defaultContent: '', title: "Src IP"},
      { data: 'port_src', defaultContent: '', title: "Src Port"},
      { data: 'ip_dest', defaultContent: '', title: "Dest IP"},
      { data: 'port_dest', defaultContent: '', title: "Dest Port"},
      { data: 'module_name', defaultContent: '', title: "Module Name"},
      { data: 'date', defaultContent: '', title: "Date"},
      { data: 'machine_name', defaultContent: '', title: "Machine Name"},
      { data: 'country_ip_src', defaultContent: '', title: "Src Country"},
      { data: 'country_ip_dest', defaultContent: '', title: "Dest Country"}];
    
    api_endpoint = "/api/events/honeypot-events";
    call_api(api_endpoint, columns);
  }
  else if( event_type == "network-event"){
    columns = [
      { data: 'ip_src', defaultContent: '', title: "Src IP"},
      { data: 'port_src', defaultContent: '', title: "Src Port"},
      { data: 'ip_dest', defaultContent: '', title: "Dest IP"},
      { data: 'port_dest', defaultContent: '', title: "Dest Port"},
      { data: 'date', defaultContent: '', title: "Date"},
      { data: 'machine_name', defaultContent: '', title: "Machine Name"},
      { data: 'country_ip_src', defaultContent: '', title: "Src Country"},
      { data: 'country_ip_dest', defaultContent: '', title: "Dest Country"}];

    api_endpoint = "/api/events/network-events";
    call_api(api_endpoint, columns);
  }
}

function search() {
    var event_type=$("select[name='event_type'] option:selected").val();
    var module_name=$("select[name='module_names'] option:selected").val();
    var start_date=$("#start_date").val();
    var end_date=$("#end_date").val();
    
    load_data(event_type);
}

function change_form(){
    var events_with_module = new Array("honeypot-event", "credential-event")
    var event_type=$("select[name='event_type'] option:selected").val();

    if(events_with_module.indexOf(event_type)>-1){
        document.getElementById("module_list").style.visibility= "visible" ;
    }
    else{
        document.getElementById("module_list").style.visibility= "hidden" ;
    }
    
}

load_module_options();

load_data();