// this file will be used as general JS file

// colors used in charts
window.chartColors = {
    red: "rgb(255, 0, 0)",
    pink: "rgb(255, 0, 191)",
    orange: "rgb(255, 159, 64)",
    yellow: "rgb(255, 205, 86)",
    green: "rgb(75, 192, 192)",
    green_yellow: "rgb(191, 255, 0)",
    blue: "rgb(54, 162, 235)",
    purple: "rgb(153, 102, 255)",
    grey: "rgb(201, 203, 207)",
    cyan: "rgb(0, 255, 255"
};

var colors_array = ["rgb(255, 0, 0)", "rgb(255, 0, 191)", "rgb(255, 159, 64)", "rgb(255, 205, 86)", "rgb(75, 192, 192)",
    "rgb(191, 255, 0)", "rgb(54, 162, 235)", "rgb(153, 102, 255)", "rgb(201, 203, 207)", "rgb(0, 255, 255"]

var color = Chart.helpers.color;
var chartColors = window.chartColors;

// check number of total events if updated then renew the graph
var old_number_of_total_events;
var new_number_of_total_events;

var top_values = new Object();

/**
 * Function to get total event counts and set the Element value
 * @param {*} event_type 
 * @param {*} element_id 
 */
function get_event_count(event_type, html_element_id){
    $.ajax({
        type: "GET",
        url: "/api/events/count/" + event_type,
        success: function(result,status,xhr){
            new_number_of_total_events = (event_type=="all") ? result["count"] : new_number_of_total_events;
            document.getElementById(html_element_id).innerHTML = result["count"];
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
 * Create object structure for the givent event type and element, if it doesn't already exist
 * @param {*} event_type 
 * @param {*} element 
 */
function create_object_structure(event_type, element){
    !(event_type in top_values) ? top_values[event_type] = new Object() : true;
    !(element in top_values[event_type]) ? top_values[event_type][element] = new Object() : true;
    !("keys" in top_values[event_type][element]) ? top_values[event_type][element].keys = [] : true;
    !("values" in top_values[event_type][element]) ? top_values[event_type][element].values = [] : true;
    !("colors" in top_values[event_type][element]) ? top_values[event_type][element].colors = [] : true;
}

function get_top_ten_element_in_event(event_type, element, html_element_id){
    $.ajax({
        type: "GET",
        url: "/api/events/count/groupby/"+event_type+"/"+element,
        success: function(res,status,xhr){
            create_object_structure(event_type, element);
            for (var i = 0; i < res.length; i++) {
                top_values[event_type][element].keys.push(
                    res[i][Object.keys(res[i])[1]]
                );
                top_values[event_type][element].values.push(res[i][Object.keys(res[i])[0]]);
                top_values[event_type][element].colors.push(color(colors_array[i]).alpha(0.5).rgbString());
            }
            var top_ten_graph_config = {
                data: {
                    datasets: [{
                        data: top_values[event_type][element].values,
                        backgroundColor: top_values[event_type][element].colors,
                        label: 'Top Ten '+element+'s - '+event_type
                    }],
                    labels: top_values[event_type][element].keys
                },
                options: {
                    responsive: true,
                    legend: {
                        position: 'right',
                    },
                    title: {
                        display: true,
                        text: 'Top Ten '+element+'s - '+event_type
                    },
                    scale: {
                        ticks: {
                            beginAtZero: true
                        },
                        reverse: false
                    },
                    animation: {
                        animateRotate: false,
                        animateScale: true
                    }
                }
            };

            var ctx = document.getElementById(html_element_id);
            window.myPolarArea = Chart.PolarArea(ctx, top_ten_graph_config);

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

function load_graphs() {
    // generate past week ago dates (e.g. 2018-07-16)
    var dates_network_events_json = {};
    var dates_honeypot_events_json = {};
    var dates_all_events_json = {};


    // get number of all events
    total_number_of_events =  get_event_count("all", "count_all_events");

    // wait 3 seconds to get responded for the request
    setTimeout(function () {
        // if events number updated or its first time to load the graph
        if (old_number_of_total_events != new_number_of_total_events) {
            var week_dates_array = [];
            // generate days (7 days ago until now)
            for (var days = 6; days >= 0; days--) {
                var date = new Date();
                var last = new Date(date.getTime() - (days * 24 * 60 * 60 * 1000));
                week_dates_array.push(last.getFullYear() + (((last.getMonth() + 1) <= 9) ?
                    ("-0" + (last.getMonth() + 1)) : "-" + (last.getMonth() + 1)) + ((last.getDate() <= 9) ?
                    ("-0" + last.getDate()) : "-" + last.getDate()));
            }
            // set old events num as new to prevent repeating requests
            old_number_of_total_events = new_number_of_total_events;
            // request honeypot related events number
            get_event_count("honeypot", "count_honeypot_events");
            // request network related events number
            get_event_count("network", "count_network_events");
            // request top ten ips in honeypot events
            get_top_ten_element_in_event("honeypot", "ip", "top_ten_ips_in_honeypot_events_graph");
            // request top ten ips in network events
            get_top_ten_element_in_event("network", "ip", "top_ten_ips_in_network_events_graph");
            // request top ten ports in honeypot events
            get_top_ten_element_in_event("honeypot", "port", "top_ten_ports_in_honeypot_events_graph");
            // request top ten ports in network events
            get_top_ten_element_in_event("network", "port", "top_ten_ports_in_network_events_graph");
            // 7 days ago config
            // request all events number by date for past week
            for (var counter = 0; counter < week_dates_array.length; counter++) {

                $.ajax({
                    type: "GET",
                    url: "/api/events/count/all?date=" + week_dates_array[counter],
                }).done(function (res) {
                    dates_all_events_json[res["date"].toString().split(" ")[0]] = res["count"];

                    var past_week_events_graph_config = {
                        type: 'line',
                        data: {
                            labels: week_dates_array,
                            datasets: [{
                                label: 'All Events',
                                backgroundColor: window.chartColors.red,
                                borderColor: window.chartColors.red,
                                data: [
                                    dates_all_events_json[week_dates_array[0]],
                                    dates_all_events_json[week_dates_array[1]],
                                    dates_all_events_json[week_dates_array[2]],
                                    dates_all_events_json[week_dates_array[3]],
                                    dates_all_events_json[week_dates_array[4]],
                                    dates_all_events_json[week_dates_array[5]],
                                    dates_all_events_json[week_dates_array[6]]
                                ],
                                fill: false,
                            }, {
                                label: 'Honeypot Events',
                                fill: false,
                                backgroundColor: window.chartColors.blue,
                                borderColor: window.chartColors.blue,
                                data: [
                                    dates_honeypot_events_json[week_dates_array[0]],
                                    dates_honeypot_events_json[week_dates_array[1]],
                                    dates_honeypot_events_json[week_dates_array[2]],
                                    dates_honeypot_events_json[week_dates_array[3]],
                                    dates_honeypot_events_json[week_dates_array[4]],
                                    dates_honeypot_events_json[week_dates_array[5]],
                                    dates_honeypot_events_json[week_dates_array[6]]
                                ],
                            }, {
                                label: 'Network Events',
                                fill: false,
                                backgroundColor: window.chartColors.yellow,
                                borderColor: window.chartColors.yellow,
                                data: [
                                    dates_network_events_json[week_dates_array[0]],
                                    dates_network_events_json[week_dates_array[1]],
                                    dates_network_events_json[week_dates_array[2]],
                                    dates_network_events_json[week_dates_array[3]],
                                    dates_network_events_json[week_dates_array[4]],
                                    dates_network_events_json[week_dates_array[5]],
                                    dates_network_events_json[week_dates_array[6]]
                                ],
                            }]
                        },
                        options: {
                            responsive: true,
                            title: {
                                display: true,
                                text: 'OHP Events'
                            },
                            tooltips: {
                                mode: 'index',
                                intersect: false,
                            },
                            hover: {
                                mode: 'nearest',
                                intersect: true
                            },
                            scales: {
                                xAxes: [{
                                    display: true,
                                    scaleLabel: {
                                        display: true,
                                        labelString: 'Past Week Events Graph (update 30 seconds)'
                                    }
                                }],
                                yAxes: [{
                                    display: true,
                                    scaleLabel: {
                                        display: true,
                                        labelString: 'Events Number'
                                    }
                                }]
                            }
                        }
                    };

                    // hide blink message
                    document.getElementById("blink_loading_graph").hidden = true;

                    // place the graph in canvas
                    var past_week_events_graph_config_ctx = document.getElementById('past_week_events_graph').getContext('2d');
                    window.myLine = new Chart(past_week_events_graph_config_ctx, past_week_events_graph_config);

                }).fail(function (jqXHR, textStatus, errorThrown) {
                    document.getElementById('error_msg').innerHTML = jqXHR.responseText;
                    if (errorThrown == "BAD REQUEST") {
                    }
                    if (errorThrown == "UNAUTHORIZED") {
                    }
                });
            }

            // request network events number by date for past week
            for (var counter = 0; counter < week_dates_array.length; counter++) {
                $.ajax({
                    type: "GET",
                    url: "/api/events/count/network?date=" + week_dates_array[counter],
                }).done(function (res) {
                    dates_network_events_json[res["date"].toString().split(" ")[0]] = res["count"];
                    var past_week_events_graph_config = {
                        type: 'line',
                        data: {
                            labels: week_dates_array,
                            datasets: [{
                                label: 'All Events',
                                backgroundColor: window.chartColors.red,
                                borderColor: window.chartColors.red,
                                data: [
                                    dates_all_events_json[week_dates_array[0]],
                                    dates_all_events_json[week_dates_array[1]],
                                    dates_all_events_json[week_dates_array[2]],
                                    dates_all_events_json[week_dates_array[3]],
                                    dates_all_events_json[week_dates_array[4]],
                                    dates_all_events_json[week_dates_array[5]],
                                    dates_all_events_json[week_dates_array[6]]
                                ],
                                fill: false,
                            }, {
                                label: 'Honeypot Events',
                                fill: false,
                                backgroundColor: window.chartColors.blue,
                                borderColor: window.chartColors.blue,
                                data: [
                                    dates_honeypot_events_json[week_dates_array[0]],
                                    dates_honeypot_events_json[week_dates_array[1]],
                                    dates_honeypot_events_json[week_dates_array[2]],
                                    dates_honeypot_events_json[week_dates_array[3]],
                                    dates_honeypot_events_json[week_dates_array[4]],
                                    dates_honeypot_events_json[week_dates_array[5]],
                                    dates_honeypot_events_json[week_dates_array[6]]
                                ],
                            }, {
                                label: 'Network Events',
                                fill: false,
                                backgroundColor: window.chartColors.yellow,
                                borderColor: window.chartColors.yellow,
                                data: [
                                    dates_network_events_json[week_dates_array[0]],
                                    dates_network_events_json[week_dates_array[1]],
                                    dates_network_events_json[week_dates_array[2]],
                                    dates_network_events_json[week_dates_array[3]],
                                    dates_network_events_json[week_dates_array[4]],
                                    dates_network_events_json[week_dates_array[5]],
                                    dates_network_events_json[week_dates_array[6]]
                                ],
                            }]
                        },
                        options: {
                            responsive: true,
                            title: {
                                display: true,
                                text: 'OHP Events'
                            },
                            tooltips: {
                                mode: 'index',
                                intersect: false,
                            },
                            hover: {
                                mode: 'nearest',
                                intersect: true
                            },
                            scales: {
                                xAxes: [{
                                    display: true,
                                    scaleLabel: {
                                        display: true,
                                        labelString: 'Past Week Events Graph (update 30 seconds)'
                                    }
                                }],
                                yAxes: [{
                                    display: true,
                                    scaleLabel: {
                                        display: true,
                                        labelString: 'Events Number'
                                    }
                                }]
                            }
                        }
                    };

                    // hide blink message
                    document.getElementById("blink_loading_graph").hidden = true;

                    // place the graph in canvas
                    var past_week_events_graph_config_ctx = document.getElementById('past_week_events_graph').getContext('2d');
                    window.myLine = new Chart(past_week_events_graph_config_ctx, past_week_events_graph_config);
                }).fail(function (jqXHR, textStatus, errorThrown) {
                    document.getElementById('error_msg').innerHTML = jqXHR.responseText;
                    if (errorThrown == "BAD REQUEST") {
                    }
                    if (errorThrown == "UNAUTHORIZED") {
                    }
                });
            }

            // request honeypot events number by date for past week
            for (var counter = 0; counter < week_dates_array.length; counter++) {

                $.ajax({
                    type: "GET",
                    url: "/api/events/count/honeypot?date=" + week_dates_array[counter],
                }).done(function (res) {
                    dates_honeypot_events_json[res["date"].toString().split(" ")[0]] = res["count"];
                    var past_week_events_graph_config = {
                        type: 'line',
                        data: {
                            labels: week_dates_array,
                            datasets: [{
                                label: 'All Events',
                                backgroundColor: window.chartColors.red,
                                borderColor: window.chartColors.red,
                                data: [
                                    dates_all_events_json[week_dates_array[0]],
                                    dates_all_events_json[week_dates_array[1]],
                                    dates_all_events_json[week_dates_array[2]],
                                    dates_all_events_json[week_dates_array[3]],
                                    dates_all_events_json[week_dates_array[4]],
                                    dates_all_events_json[week_dates_array[5]],
                                    dates_all_events_json[week_dates_array[6]]
                                ],
                                fill: false,
                            }, {
                                label: 'Honeypot Events',
                                fill: false,
                                backgroundColor: window.chartColors.blue,
                                borderColor: window.chartColors.blue,
                                data: [
                                    dates_honeypot_events_json[week_dates_array[0]],
                                    dates_honeypot_events_json[week_dates_array[1]],
                                    dates_honeypot_events_json[week_dates_array[2]],
                                    dates_honeypot_events_json[week_dates_array[3]],
                                    dates_honeypot_events_json[week_dates_array[4]],
                                    dates_honeypot_events_json[week_dates_array[5]],
                                    dates_honeypot_events_json[week_dates_array[6]]
                                ],
                            }, {
                                label: 'Network Events',
                                fill: false,
                                backgroundColor: window.chartColors.yellow,
                                borderColor: window.chartColors.yellow,
                                data: [
                                    dates_network_events_json[week_dates_array[0]],
                                    dates_network_events_json[week_dates_array[1]],
                                    dates_network_events_json[week_dates_array[2]],
                                    dates_network_events_json[week_dates_array[3]],
                                    dates_network_events_json[week_dates_array[4]],
                                    dates_network_events_json[week_dates_array[5]],
                                    dates_network_events_json[week_dates_array[6]]
                                ],
                            }]
                        },
                        options: {
                            responsive: true,
                            title: {
                                display: true,
                                text: 'OHP Events'
                            },
                            tooltips: {
                                mode: 'index',
                                intersect: false,
                            },
                            hover: {
                                mode: 'nearest',
                                intersect: true
                            },
                            scales: {
                                xAxes: [{
                                    display: true,
                                    scaleLabel: {
                                        display: true,
                                        labelString: 'Past Week Events Graph (update 30 seconds)'
                                    }
                                }],
                                yAxes: [{
                                    display: true,
                                    scaleLabel: {
                                        display: true,
                                        labelString: 'Events Number'
                                    }
                                }]
                            }
                        }
                    };

                    // hide blink message
                    document.getElementById("blink_loading_graph").hidden = true;

                    // place the graph in canvas
                    var past_week_events_graph_config_ctx = document.getElementById('past_week_events_graph').getContext('2d');
                    window.myLine = new Chart(past_week_events_graph_config_ctx, past_week_events_graph_config);
                }).fail(function (jqXHR, textStatus, errorThrown) {
                    document.getElementById('error_msg').innerHTML = jqXHR.responseText;
                    if (errorThrown == "BAD REQUEST") {
                    }
                    if (errorThrown == "UNAUTHORIZED") {
                    }
                });
            }


        }
    }, 3000);
}

function keep_update() {
    setTimeout(function () {
        load_graphs();
        keep_update();
    }, 30000);
}

// load first time
load_graphs();

// 30 seconds delay loop
keep_update();
