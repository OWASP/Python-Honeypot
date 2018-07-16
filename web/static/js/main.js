// this file will be used as general JS file

// colors used in charts
window.chartColors = {
    red: "rgb(255, 99, 132)",
    orange: "rgb(255, 159, 64)",
    yellow: "rgb(255, 205, 86)",
    green: "rgb(75, 192, 192)",
    blue: "rgb(54, 162, 235)",
    purple: "rgb(153, 102, 255)",
    grey: "rgb(201, 203, 207)"
};

// check number of total events if updated then renew the graph
var old_number_of_total_events;
var new_number_of_total_events;


function past_week_events_graph() {

    // get number of all events
    $.ajax({
        type: "GET",
        url: "/api/events/count_all_events",
    }).done(function (res) {
        new_number_of_total_events = res["count_all_events"];
        document.getElementById('count_all_events').innerHTML = res["count_all_events"];
    }).fail(function (jqXHR, textStatus, errorThrown) {
        document.getElementById('error_msg').innerHTML = jqXHR.responseText;
        if (errorThrown == "BAD REQUEST") {
        }
        if (errorThrown == "UNAUTHORIZED") {
        }
    });

    // wait 3 seconds to get responded for the request
    setTimeout(function () {
        // if events number updated or its first time to load the graph
        if (old_number_of_total_events != new_number_of_total_events) {
            // set old events num as new to prevent repeating requests
            old_number_of_total_events = new_number_of_total_events;
            // request honeypot related events number
            $.ajax({
                type: "GET",
                url: "/api/events/count_ohp_events",
            }).done(function (res) {
                document.getElementById('count_ohp_events').innerHTML = res["count_ohp_events"];
            }).fail(function (jqXHR, textStatus, errorThrown) {
                document.getElementById('error_msg').innerHTML = jqXHR.responseText;
                if (errorThrown == "BAD REQUEST") {
                }
                if (errorThrown == "UNAUTHORIZED") {
                }
            });
            // request network related events number
            $.ajax({
                type: "GET",
                url: "/api/events/count_network_events",
            }).done(function (res) {
                document.getElementById('count_network_events').innerHTML = res["count_network_events"];
            }).fail(function (jqXHR, textStatus, errorThrown) {
                document.getElementById('error_msg').innerHTML = jqXHR.responseText;
                if (errorThrown == "BAD REQUEST") {
                }
                if (errorThrown == "UNAUTHORIZED") {
                }
            });

            // load last week graph based by date

            // generate past week ago dates (e.g. 2018-07-16)
            var dates_network_events_json = {};
            var dates_honeypot_events_json = {};
            var dates_all_events_json = {};
            var week_dates_array = [];

            for (var days = 6; days >= 0; days--) {
                var date = new Date();
                var last = new Date(date.getTime() - (days * 24 * 60 * 60 * 1000));
                week_dates_array.push(last.getFullYear() + (((last.getMonth() + 1) <= 9) ?
                    ("-0" + (last.getMonth() + 1)) : "-" + (last.getMonth() + 1)) + ((last.getDate() <= 9) ?
                    ("-0" + last.getDate()) : "-" + last.getDate()));
            }

            // request all events number by date for past week
            for (var counter = 0; counter < week_dates_array.length; counter++) {

                $.ajax({
                    type: "GET",
                    url: "/api/events/count_all_events_by_date?date=" + week_dates_array[counter],
                }).done(function (res) {
                    dates_all_events_json[res["date"]] = res["count_all_events_by_date"];
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
                    url: "/api/events/count_network_events_by_date?date=" + week_dates_array[counter],
                }).done(function (res) {
                    dates_network_events_json[res["date"]] = res["count_network_events_by_date"];
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
                    url: "/api/events/count_honeypot_events_by_date?date=" + week_dates_array[counter],
                }).done(function (res) {
                    dates_honeypot_events_json[res["date"]] = res["count_honeypot_events_by_date"];
                }).fail(function (jqXHR, textStatus, errorThrown) {
                    document.getElementById('error_msg').innerHTML = jqXHR.responseText;
                    if (errorThrown == "BAD REQUEST") {
                    }
                    if (errorThrown == "UNAUTHORIZED") {
                    }
                });
            }

            // wait 5 seconds to get responded for all requests
            setTimeout(function () {
                // impalement the past week events graph

                // create the graph config
                var config = {
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
                var ctx = document.getElementById('past_week_events_graph').getContext('2d');
                window.myLine = new Chart(ctx, config);


            }, 5000);
        }
    }, 3000);
}

function keep_update() {
    setTimeout(function () {
        past_week_events_graph();
        keep_update();
    }, 30000);
}

// run graph for the first time
past_week_events_graph();

// 30 seconds delay loop
keep_update();