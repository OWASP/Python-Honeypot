/**
 * Load list of modules in a select list
 */

var explorer_skip = 0;
var explorer_limit = 10;
var explorer_pages_number = 1;


function updatePagesNumber(event_type){
    $.ajax({
    type: "GET",
    url: "/api/events/count/" + event_type,
    data: {},
    success: function(result,status,xhr){
      explorer_pages_number = result["count"];
      document.getElementById("explorer_pages_number").val = parseInt((explorer_pages_number/explorer_limit) - 1);
      document.getElementById("explorer_pages_number").innerHTML =  "/" + parseInt((explorer_pages_number/explorer_limit) - 1);
    },
    error: function (jqXHR, textStatus, errorThrown) {
      document.getElementById('error_msg').innerHTML = jqXHR.responseText;
      if (errorThrown == "BAD REQUEST") {
      }
      if (errorThrown == "UNAUTHORIZED") {
      }
    }
  });

}


function load_module_options() {
  $.ajax({
    type: "GET",
    url: "/api/core/list/modules",
    data: {},
    success: function(result,status,xhr){
      var tableHtml = '<option value=\"\"> All Modules </option>';
      for (var i = 0; i < result.length; i++) {
        var module_name = result[i];
        tableHtml += "<option value=" +
          module_name + ">"
          + module_name
          + "</option>";
      }
      $('#module_names').html(tableHtml);
    },
    error: function (jqXHR, textStatus, errorThrown) {
      document.getElementById('error_msg').innerHTML = jqXHR.responseText;
      if (errorThrown == "BAD REQUEST") {
      }
      if (errorThrown == "UNAUTHORIZED") {
      }
    }
  });
}




// Delete datatable
function clear_table(){
  if ($.fn.dataTable.isDataTable("#datatable")) {
    $("#datatable").DataTable().clear().destroy();
    $("#datatable").empty();
  }
}



/**
 * Call the API to get the list of Files stored in the database.
 * @param {*} api_endpoint 
 * @param {*} column_list 
 * @param {*} column_defs 
 * @param {*} api_params 
 */
/**
 * Load data to the table based on user selected filters.
 * @param {*} event_type 
 * @param {*} module_name 
 * @param {*} start_date 
 * @param {*} end_date 
 */
function load_data(api_endpoint, api_params) {
  clear_table();
  var columns = [];
  if (api_params.module_name == "") {
    delete api_params.module_name;
  }

  api_params.limit = explorer_limit;
  api_params.skip = explorer_skip;

  event_types = {
    // todo; check the order
    "honeypot": ['date', 'ip_src', 'port_src', 'ip_dest', 'port_dest', 'protocol', 'module_name', 'machine_name', 'country_ip_src', 'country_ip_dest'],
    "network":  ['date', 'ip_src', 'port_src', 'ip_dest', 'port_dest', 'protocol', 'machine_name', 'country_ip_src', 'country_ip_dest'],
    "credential": ['date', 'ip', 'module_name', 'username', 'password', 'machine_name', 'country'],
    "data": ['date', 'ip', 'module_name', 'data', 'machine_name', 'country'],
    "file": ['date', 'module_name', 'file_path', 'status', 'machine_name', 'is_directory'],
    "pcap": ['chunkSize', 'date', 'filename', 'length', 'machine_name', 'md5', 'splitTimeout', 'uploadDate']
  }

  cols = ""
  for(col in event_types[api_params.event_type]){
    cols += "<th>" + event_types[api_params.event_type][col] + "</th>\n"
  }
  cols = "<tr>\n" + cols + "</tr>"
  document.getElementById("explorer_table_head").innerHTML = cols;

  $.ajax({
        type: "GET",
        url: api_endpoint,
        data: api_params,
        success: function(result,status,xhr){
            cols_data = ""
            for(col_data_res in result){
                cols_data += "<tr>"
                for(key in result[col_data_res]){
                    // todo: fix here
                    // if pcap and md5 then <td><a href="/api/pcap/download?md5=md5">download</a></td>
                    cols_data += "<td>"+ result[col_data_res][key] +"</td>"

                }
                cols_data += "</tr>"
            }
            document.getElementById("explorer_table_body").innerHTML = cols_data;
        },
        error: function (jqXHR, textStatus, errorThrown) {
            document.getElementById('error_msg').innerHTML = jqXHR.responseText;
            if (errorThrown == "BAD REQUEST") {
            }
            if (errorThrown == "UNAUTHORIZED") {
            }
        }
    });


}


/**
 * Function called when "search" button is clicked in the "Log explorer" display
 */
function search_database() {
  var api_endpoint = "/api/events/explore/";
  var api_params = {};
  // Get event type and module name if data explorer
  var event_type = $("select[name='event_type'] option:selected").val();
  var module_name = $("select[name='module_names'] option:selected").val();
  // Update end point
  api_endpoint += event_type;
  updatePagesNumber(event_type);
  // Set the API parameters
  api_params.event_type = event_type;
  api_params.module_name = module_name;
  // Get date range
  var start_date = $("#start_date").val();
  var end_date = $("#end_date").val();

  if (start_date == "" || end_date == "") {
    alert("Either Start Date or End date missing!");
  }
  else {
    if (start_date <= end_date) {
      // Date Range format Eg: 2020-09-10|2020-10-10
      api_params.date = start_date + '|' + end_date
      // Call API and load data to table
      load_data(
        api_endpoint,
        api_params
      );
    }
    else {
      alert("Start date is greater than End date!")
    }
  }
}


/**
 * Form update based on event type selected
 */
function change_form() {
  explorer_skip = 0;
  var events_with_module = new Array(
    "honeypot",
    "credential",
    "file",
    "data"
  )
  var event_type = $("select[name='event_type'] option:selected").val();

  if (events_with_module.indexOf(event_type) > -1) {
    document.getElementById("module_names").disabled = false;
  }
  else {
    document.getElementById("module_names").selectedIndex = 0;
    document.getElementById("module_names").disabled = true;
  }
  explorer_skip = 0;
  updatePagesNumber($("select[name='event_type'] option:selected").val());
}

/**
 * Change layout based on user selection
 */
function get_layout(layout_type) {
  document.getElementById("dashboard").hidden = (layout_type=="dashboard") ? false : true;
  document.getElementById("log-explorer").hidden = (layout_type=="log-explorer") ? false : true;
}

function explorer_next_page() {
    explorer_skip = explorer_skip + explorer_limit;


    document.getElementById("explorer_skip").val =  parseInt((explorer_skip/explorer_limit) + 1);
    document.getElementById("explorer_skip").innerHTML =   parseInt((explorer_skip/explorer_limit) + 1);
    updatePagesNumber($("select[name='event_type'] option:selected").val());
    search_database();
}

function explorer_previous_page() {
    explorer_skip = explorer_skip - explorer_limit;

    console.log(parseInt((explorer_skip/explorer_limit) + 1));

    document.getElementById("explorer_skip").val =  parseInt((explorer_skip/explorer_limit) + 1);
    document.getElementById("explorer_skip").innerHTML =  parseInt((explorer_skip/explorer_limit) + 1);
    updatePagesNumber($("select[name='event_type'] option:selected").val());
    search_database();

}

load_module_options();