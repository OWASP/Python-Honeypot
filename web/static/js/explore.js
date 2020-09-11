/**
 * Load list of modules in a select list
 */
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


// Get the file name of the export file
function get_export_fileName(file_type) {
  var d = new Date();
  var n = d.getTime();
  return 'Honeypot-data-' + file_type + '-' + n;
}


// Delete datatable
function clear_table(){
  if ($.fn.dataTable.isDataTable("#datatable")) {
    $("#datatable").DataTable().clear().destroy();
    $("#datatable").empty();
  }
}


/**
 * Taken from https://storiknow.com/download-file-with-jquery-and-web-api-2-0-ihttpactionresult/
 * @param {*} xhr 
 * @param {*} blob 
 */
function download(xhr, blob) {
  var downloadLink = document.createElement('a');
  
  var url = window.URL || window.webkitURL;
  var downloadUrl = url.createObjectURL(blob);
  var fileName = '';
 
  // get the file name from the content disposition
  var disposition = xhr.getResponseHeader('Content-Disposition');
  if (disposition && disposition.indexOf('attachment') !== -1) {
      var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
      var matches = filenameRegex.exec(disposition);
      if (matches != null && matches[1]) {
          fileName = matches[1].replace(/['"]/g, '');
      }
  }
  // Blob download logic taken from: https://stackoverflow.com/questions/16086162/handle-file-download-from-ajax-post
  if (typeof window.navigator.msSaveBlob !== 'undefined') {
    // IE workaround for "HTML7007" and "Access Denied" error.
    window.navigator.msSaveBlob(blob, fileName);
  } else {
      if (fileName) {
          if (typeof downloadLink.download === 'undefined') {
              window.location = downloadUrl;
          } else {
              downloadLink.href = downloadUrl;
              downloadLink.download = fileName;
              document.body.appendChild(downloadLink);
              downloadLink.click();
          }
      } else {
          window.location = downloadUrl;
      }

      setTimeout(function () {
            url.revokeObjectURL(downloadUrl);
        },
        100
      );
  }
}

//
// Pipelining function for DataTables. To be used to the `ajax` option of DataTables
// Pipelining data to reduce Ajax calls for paging:
// https://datatables.net/examples/server_side/pipeline.html
//
$.fn.dataTable.pipeline = function ( opts ) {
  // Configuration options
  var conf = $.extend( {
      contentType: null,
      pages: 5,     // number of pages to cache
      url: '',      // script url
      data: null,   // function or object with parameters to send to the server
                    // matching how `ajax.data` works in DataTables
      dataSrc: null,
      method: 'GET' // Ajax HTTP method
  }, opts );
  // Private variables for storing the cache
  var cacheLower = -1;
  var cacheUpper = null;
  var cacheLastRequest = null;
  var cacheLastJson = null;

  return function ( request, drawCallback, settings ) {
      var ajax          = false;
      var requestStart  = request.start;
      var drawStart     = request.start;
      var requestLength = request.length;
      var requestEnd    = requestStart + requestLength;
       
      if ( settings.clearCache ) {
          // API requested that the cache be cleared
          ajax = true;
          settings.clearCache = false;
      }
      else if ( cacheLower < 0 || requestStart < cacheLower || requestEnd > cacheUpper ) {
          // outside cached data - need to make a request
          ajax = true;
      }
      else if ( JSON.stringify( request.order )   !== JSON.stringify( cacheLastRequest.order ) ||
                JSON.stringify( request.columns ) !== JSON.stringify( cacheLastRequest.columns ) ||
                JSON.stringify( request.search )  !== JSON.stringify( cacheLastRequest.search )
      ) {
          // properties changed (ordering, columns, searching)
          ajax = true;
      }
       
      // Store the request for checking next time around
      cacheLastRequest = $.extend( true, {}, request );

      if ( ajax ) {
          // Need data from the server
          if ( requestStart < cacheLower ) {
              requestStart = requestStart - (requestLength*(conf.pages-1));

              if ( requestStart < 0 ) {
                  requestStart = 0;
              }
          }
           
          cacheLower = requestStart;
          cacheUpper = requestStart + (requestLength * conf.pages);

          request.start = requestStart;
          request.length = requestLength*conf.pages;
          conf.data.skip = requestStart;
          conf.data.limit = request.length;
          if($("#datatable_filter > label > input")[0].value){
            conf.data.filter = $("#datatable_filter > label > input")[0].value;
          }

          // Provide the same `data` options as DataTables.
          if ( typeof conf.data === 'function' ) {
              // As a function it is executed with the data object as an arg
              // for manipulation. If an object is returned, it is used as the
              // data object to submit
              var d = conf.data( request );
              if ( d ) {
                  $.extend( request, d );
              }
          }
          else if ( $.isPlainObject( conf.data ) ) {
              // As an object, the data given extends the default
              $.extend( request, conf.data );
          }
          return $.ajax( {
              "type":     conf.method,
              "url":      conf.url,
              "contentType": conf.contentType,
              "data":     conf.data,
              "dataType": "json",
              "cache":    false,
              "dataFilter": function(data){
                var json = jQuery.parseJSON( data );
                json.recordsTotal = json.total;
                json.recordsFiltered = json.total;
                tmpj = json
                if(conf.url.split("/")[4] == "data"){
                    for(index in tmpj['data']){
                        tmpj['data'][index]['data'] = JSON.stringify(json['data'][index]['data'])
                    }
                }
                json = tmpj
                return JSON.stringify( json );
              },
              "success":  function ( json ) {
                  cacheLastJson = $.extend(true, {}, json);

                  if ( cacheLower != drawStart ) {
                      json.data.splice( 0, drawStart-cacheLower );
                  }
                  if ( requestLength >= -1 ) {
                      json.data.splice( requestLength, json.data.length );
                  }
                   
                  drawCallback( json );
              }
          } );
      }
      else {
          json = $.extend( true, {}, cacheLastJson );
          json.draw = request.draw; // Update the echo for each response
          json.data.splice( 0, requestStart-cacheLower );
          json.data.splice( requestLength, json.data.length );

          drawCallback(json);
      }
  }
};

// Register an API method that will empty the pipelined data, forcing an Ajax
// fetch on the next draw (i.e. `table.clearPipeline().draw()`)
$.fn.dataTable.Api.register( 'clearPipeline()', function () {
  return this.iterator( 'table', function ( settings ) {
      settings.clearCache = true;
  } );
} );

/**
 * Call the API to get event data from the database
 * @param {*} api_endpoint : API endpoint URL
 * @param {*} column_list : List of Columns for the selected event type
 * @param {*} api_params  : GET parameters for the API call
 */
function get_event_data(api_endpoint, column_list, api_params) {
  
  $(document).ready(function () {
    var table = $("#datatable").DataTable({
      ajax: $.fn.dataTable.pipeline({
        pages: 10,
        type: "GET",
        url: api_endpoint,
        contentType: 'application/json; charset=utf-8',
        data: api_params,
        dataType: "json",
        dataSrc: "data"
      }),
      autoWidth: true,
      dom: "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>" +
        "<'row'<'col-sm-12'tr>>" +
        "<'row'<'col-sm-12 col-md-2'B><'col-sm-12 col-md-4'i><'col-sm-12 col-md-6'p>>",
      buttons: [
        {
          extend: 'csv',
          filename: function () { return get_export_fileName('csv'); },
          className: "btn btn-info btn-sm"
        },
        {
          extend: 'excel',
          filename: function () { return get_export_fileName('excel'); },
          className: "btn btn-info btn-sm"
        }
      ],
      columns: column_list,
      destroy: true,
      order: [[0, 'desc']],
      sort: true,
      info: true,
      paging: true,
      serverSide: true,
      processing: true,
      language:{
          loadingRecords: '&nbsp;',
          processing: '<div class="spinner">Loading...</div>'
      },
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
          '<option value="100">100</option>' +
          '<option value="500">500</option>' +
          '</select></div>'
      },
      searching: true,
      responsive: true
    });
  });
}


/**
 * Call the API to get the list of Files stored in the database.
 * @param {*} api_endpoint 
 * @param {*} column_list 
 * @param {*} column_defs 
 * @param {*} api_params 
 */
function get_pcap_file_data(api_endpoint, column_list, api_params) {

  $(document).ready(function () {
    var table = $("#datatable").DataTable({
      ajax: $.fn.dataTable.pipeline({
        pages: 5,
        type: "GET",
        url: api_endpoint,
        contentType: 'application/json; charset=utf-8',
        data: api_params,
        dataType: "json",
        dataSrc: ""
      }),
      autoWidth: true,
      dom: "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>" +
        "<'row'<'col-sm-12'tr>>" +
        "<'row'<'col-sm-12 col-md-2'B><'col-sm-12 col-md-4'i><'col-sm-12 col-md-6'p>>",
      buttons:[
        {
          extend: 'selectedSingle',
          text: "Download",
          className: "btn btn-info btn-sm",
          action: function(event, data, node, config){
            var selected_row_data =  table.rows({ selected: true }).data();
              download_api_params = {
                "md5": selected_row_data[0]["md5"]
              }
        
              // Call the download-file API endpoint with the file ID
              $.ajax({
                type: "GET",
                url: "/api/pcap/download",
                data: download_api_params,
                xhrFields:{
                  responseType: "arraybuffer"
                },
                success: function(result,status,xhr){
                  var blob = new Blob([result],
                    {
                      type: xhr.getResponseHeader('Content-Type')
                    });
                  download(xhr, blob);
                },
                error: function (jqXHR, textStatus, errorThrown) {
                  if (errorThrown == "BAD REQUEST") {
                    alert(jqXHR.responseText)
                  }
                  if (errorThrown == "UNAUTHORIZED") {
                    alert(jqXHR.responseText)
                  }
                }
              });
          }
        }
      ],
      columns: column_list,
      columnDefs: [
        {
          targets: [0],
          searchable: false,
          orderable: false,
          className : 'select-checkbox',
          checkboxes: {
            selectRow: true,
            stateSave: false
          }
       },
      ],
      retrieve : true,
      select: {
        style: 'single'
      },
      destroy: true,
      order: [[1, 'desc']],
      sort: true,
      info: true,
      paging: true,
      serverSide: true,
      processing: true,
      language:{
          loadingRecords: '&nbsp;',
          processing: '<div class="spinner">Loading...</div>'
      },
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
          '<option value="100">100</option>' +
          '<option value="500">500</option>' +
          '</select></div>'
      },
      searching: true,
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
function load_data(api_endpoint, api_params) {
  clear_table();
  var columns = [];
  if (api_params.module_name == "") {
    delete api_params.module_name;
  }

  // Define table columns based on selected event type
  if (api_params.event_type == "honeypot") {
    columns = [
      { data: 'date', defaultContent: '', title: "Date" },
      { data: 'ip_src', defaultContent: '', title: "Src IP" },
      { data: 'port_src', defaultContent: '', title: "Src Port" },
      { data: 'ip_dest', defaultContent: '', title: "Dest IP" },
      { data: 'port_dest', defaultContent: '', title: "Dest Port" },
      { data: 'module_name', defaultContent: '', title: "Module Name" },
      { data: 'machine_name', defaultContent: '', title: "Machine Name" },
      { data: 'country_ip_src', defaultContent: '', title: "Src Country" },
      { data: 'country_ip_dest', defaultContent: '', title: "Dest Country" }];
      get_event_data(api_endpoint, columns, api_params);
  }
  else if (api_params.event_type == "network") {
    columns = [
      { data: 'date', defaultContent: '', title: "Date" },
      { data: 'ip_src', defaultContent: '', title: "Src IP" },
      { data: 'port_src', defaultContent: '', title: "Src Port" },
      { data: 'ip_dest', defaultContent: '', title: "Dest IP" },
      { data: 'port_dest', defaultContent: '', title: "Dest Port" },
      { data: 'protocol', defaultContent: '', title: "Protocol" },
      { data: 'machine_name', defaultContent: '', title: "Machine Name" },
      { data: 'country_ip_src', defaultContent: '', title: "Src Country" },
      { data: 'country_ip_dest', defaultContent: '', title: "Dest Country" }];
      get_event_data(api_endpoint, columns, api_params);
  }
  else if (api_params.event_type == "credential") {
    columns = [
      { data: 'date', defaultContent: '', title: "Date" },
      { data: 'ip', defaultContent: '', title: "IP" },
      { data: 'module_name', defaultContent: '', title: "Module Name" },
      { data: 'username', defaultContent: '', title: "Username" },
      { data: 'password', defaultContent: '', title: "Password" },
      { data: 'machine_name', defaultContent: '', title: "Machine Name" },
      { data: 'country', defaultContent: '', title: "Country" }];
      get_event_data(api_endpoint, columns, api_params);
  }
  else if (api_params.event_type == "data") {
    columns = [
      { data: 'date', defaultContent: '', title: "Date" },
      { data: 'ip', defaultContent: '', title: "IP" },
      { data: 'module_name', defaultContent: '', title: "Module Name" },
      { data: 'data', defaultContent: '', title: "Data" },
      { data: 'machine_name', defaultContent: '', title: "Machine Name" },
      { data: 'country', defaultContent: '', title: "Country" }];
      get_event_data(api_endpoint, columns, api_params);
  }
  else if (api_params.event_type == "file") {
    columns = [
      { data: 'date', defaultContent: '', title: "Date" },
      { data: 'module_name', defaultContent: '', title: "Module Name" },
      { data: 'file_path', defaultContent: '', title: "File Path" },
      { data: 'status', defaultContent: '', title: "Status" },
      { data: 'machine_name', defaultContent: '', title: "Machine Name" },
      { data: 'is_directory', defaultContent: '', title: "Is Directory" }];
      get_event_data(api_endpoint, columns, api_params);
  }

  else if (api_params.event_type == "pcap") {
    columns = [
        { data: null, defaultContent: ''},
        { data: 'date', defaultContent: '', title: "Generation Time"},
        { data: 'splitTimeout', defaultContent: '', title: "Split Timeout"},
        { data: 'filename', defaultContent: '', title: "Filename"},
        { data: 'length', defaultContent: '', title: "File Size"},
        { data: 'md5', defaultContent: '', title: "MD5"}
    ];
    get_pcap_file_data(api_endpoint, columns, api_params);

  }

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
}

/**
 * Change layout based on user selection
 */
function get_layout(layout_type) {
  document.getElementById("dashboard").hidden = (layout_type=="dashboard") ? false : true;
  document.getElementById("log-explorer").hidden = (layout_type=="log-explorer") ? false : true;
  document.getElementById("log-explorer-table").hidden = (layout_type=="log-explorer") ? false : true;
}

load_module_options();