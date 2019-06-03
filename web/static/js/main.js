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

function load_graphs() {
    var top_ten_ips_in_honeypot_events_graph_data_keys = [];
    var top_ten_ips_in_honeypot_events_graph_data_values = [];
    var top_ten_ips_in_honeypot_events_graph_data_colors = [];
    var top_ten_ips_in_network_events_graph_data_keys = [];
    var top_ten_ips_in_network_events_graph_data_values = [];
    var top_ten_ips_in_network_events_graph_data_colors = [];
    var top_ten_ports_in_honeypot_events_graph_data_keys = [];
    var top_ten_ports_in_honeypot_events_graph_data_values = [];
    var top_ten_ports_in_honeypot_events_graph_data_colors = [];
    var top_ten_ports_in_network_events_graph_data_keys = [];
    var top_ten_ports_in_network_events_graph_data_values = [];
    var top_ten_ports_in_network_events_graph_data_colors = [];
    // generate past week ago dates (e.g. 2018-07-16)
    var dates_network_events_json = {};
    var dates_honeypot_events_json = {};
    var dates_all_events_json = {};


    // get number of all events
    $.ajax({
        type: "GET",
        url: "/api/events/count-all-events",
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
            $.ajax({
                type: "GET",
                url: "/api/events/count-honeypot-events",
            }).done(function (res) {
                document.getElementById('count_honeypot_events').innerHTML = res["count_honeypot_events"];
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
                url: "/api/events/count-network-events",
            }).done(function (res) {
                document.getElementById('count_network_events').innerHTML = res["count_network_events"];
            }).fail(function (jqXHR, textStatus, errorThrown) {
                document.getElementById('error_msg').innerHTML = jqXHR.responseText;
                if (errorThrown == "BAD REQUEST") {
                }
                if (errorThrown == "UNAUTHORIZED") {
                }
            });

            // request top ten ips in honeypot events
            $.ajax({
                type: "GET",
                url: "/api/events/honeypot-events-ips",
            }).done(function (res) {
                for (var i = 0; i < res.length; i++) {
                    top_ten_ips_in_honeypot_events_graph_data_keys.push(
                        res[i]["_id"]["ip"] + " (" + res[i]["_id"]["country"] + ")"
                    );
                    top_ten_ips_in_honeypot_events_graph_data_values.push(res[i]["count"]);
                    top_ten_ips_in_honeypot_events_graph_data_colors.push(color(colors_array[i]).alpha(0.5).rgbString());
                }

                var top_ten_ips_in_honeypot_events_graph_config = {
                    data: {
                        datasets: [{
                            data: top_ten_ips_in_honeypot_events_graph_data_values,
                            backgroundColor: top_ten_ips_in_honeypot_events_graph_data_colors,
                            label: 'Top Ten IPs - Honeypot'
                        }],
                        labels: top_ten_ips_in_honeypot_events_graph_data_keys
                    },
                    options: {
                        responsive: true,
                        legend: {
                            position: 'right',
                        },
                        title: {
                            display: true,
                            text: 'Top Ten IPs - Honeypot'
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

                var ctx = document.getElementById('top_ten_ips_in_honeypot_events_graph');
                window.myPolarArea = Chart.PolarArea(ctx, top_ten_ips_in_honeypot_events_graph_config);

            }).fail(function (jqXHR, textStatus, errorThrown) {
                document.getElementById('error_msg').innerHTML = jqXHR.responseText;
                if (errorThrown == "BAD REQUEST") {
                }
                if (errorThrown == "UNAUTHORIZED") {
                }
            });


            // request top ten ips in network events
            $.ajax({
                type: "GET",
                url: "/api/events/network-events-ips",
            }).done(function (res) {
                for (var i = 0; i < res.length; i++) {
                    top_ten_ips_in_network_events_graph_data_keys.push(
                        res[i]["_id"]["ip"] + " (" + res[i]["_id"]["country"] + ")"
                       );
                    top_ten_ips_in_network_events_graph_data_values.push(res[i]["count"]);
                    top_ten_ips_in_network_events_graph_data_colors.push(color(colors_array[i]).alpha(0.5).rgbString());
                }

                var top_ten_ips_in_network_events_graph_config = {
                    data: {
                        datasets: [{
                            data: top_ten_ips_in_network_events_graph_data_values,
                            backgroundColor: top_ten_ips_in_network_events_graph_data_colors,
                            label: 'Top Ten IPs - Network'
                        }],
                        labels: top_ten_ips_in_network_events_graph_data_keys
                    },
                    options: {
                        responsive: true,
                        legend: {
                            position: 'right',
                        },
                        title: {
                            display: true,
                            text: 'Top Ten IPs - Network'
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

                var ctx = document.getElementById('top_ten_ips_in_network_events_graph');
                window.myPolarArea = Chart.PolarArea(ctx, top_ten_ips_in_network_events_graph_config);

            }).fail(function (jqXHR, textStatus, errorThrown) {
                document.getElementById('error_msg').innerHTML = jqXHR.responseText;
                if (errorThrown == "BAD REQUEST") {
                }
                if (errorThrown == "UNAUTHORIZED") {
                }
            });


            // request top ten ports in honeypot events
            $.ajax({
                type: "GET",
                url: "/api/events/honeypot-events-ports",
            }).done(function (res) {
                for (var i = 0; i < res.length; i++) {
                    top_ten_ports_in_honeypot_events_graph_data_keys.push(res[i]["_id"]);
                    top_ten_ports_in_honeypot_events_graph_data_values.push(res[i]["count"]);
                    top_ten_ports_in_honeypot_events_graph_data_colors.push(color(colors_array[i]).alpha(0.5).rgbString());
                }

                var top_ten_ports_in_honeypot_events_graph_config = {
                    data: {
                        datasets: [{
                            data: top_ten_ports_in_honeypot_events_graph_data_values,
                            backgroundColor: top_ten_ports_in_honeypot_events_graph_data_colors,
                            label: 'Top Ten Ports - Honeypot'
                        }],
                        labels: top_ten_ports_in_honeypot_events_graph_data_keys
                    },
                    options: {
                        responsive: true,
                        legend: {
                            position: 'right',
                        },
                        title: {
                            display: true,
                            text: 'Top Ten Ports - Honeypot'
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

                var ctx = document.getElementById('top_ten_ports_in_honeypot_events_graph');
                window.myPolarArea = Chart.PolarArea(ctx, top_ten_ports_in_honeypot_events_graph_config);

            }).fail(function (jqXHR, textStatus, errorThrown) {
                document.getElementById('error_msg').innerHTML = jqXHR.responseText;
                if (errorThrown == "BAD REQUEST") {
                }
                if (errorThrown == "UNAUTHORIZED") {
                }
            });


            // request top ten ports in network events
            $.ajax({
                type: "GET",
                url: "/api/events/network-events-ports",
            }).done(function (res) {
                for (var i = 0; i < res.length; i++) {
                    top_ten_ports_in_network_events_graph_data_keys.push(res[i]["_id"]);
                    top_ten_ports_in_network_events_graph_data_values.push(res[i]["count"]);
                    top_ten_ports_in_network_events_graph_data_colors.push(color(colors_array[i]).alpha(0.5).rgbString());
                }

                var top_ten_ports_in_network_events_graph_config = {
                    data: {
                        datasets: [{
                            data: top_ten_ports_in_network_events_graph_data_values,
                            backgroundColor: top_ten_ports_in_network_events_graph_data_colors,
                            label: 'Top Ten Network - Honeypot'
                        }],
                        labels: top_ten_ports_in_network_events_graph_data_keys
                    },
                    options: {
                        responsive: true,
                        legend: {
                            position: 'right',
                        },
                        title: {
                            display: true,
                            text: 'Top Ten Ports - Network'
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

                var ctx = document.getElementById('top_ten_ports_in_network_events_graph');
                window.myPolarArea = Chart.PolarArea(ctx, top_ten_ports_in_network_events_graph_config);

            }).fail(function (jqXHR, textStatus, errorThrown) {
                document.getElementById('error_msg').innerHTML = jqXHR.responseText;
                if (errorThrown == "BAD REQUEST") {
                }
                if (errorThrown == "UNAUTHORIZED") {
                }
            });


            // 7 days ago config
            // request all events number by date for past week
            for (var counter = 0; counter < week_dates_array.length; counter++) {

                $.ajax({
                    type: "GET",
                    url: "/api/events/count-all-events?date=" + week_dates_array[counter],
                }).done(function (res) {
                    dates_all_events_json[res["date"].toString().split(" ")[0]] = res["count_all_events_by_date"];

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
                    url: "/api/events/count-network-events?date=" + week_dates_array[counter],
                }).done(function (res) {
                    dates_network_events_json[res["date"].toString().split(" ")[0]] = res["count_network_events_by_date"];
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
                    url: "/api/events/count-honeypot-events?date=" + week_dates_array[counter],
                }).done(function (res) {
                    dates_honeypot_events_json[res["date"].toString().split(" ")[0]] = res["count_honeypot_events_by_date"];
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
