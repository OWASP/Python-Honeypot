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
    cyan: "rgb(0, 255, 255)"
};

var colors_array = ["rgb(255, 0, 0)", "rgb(255, 0, 191)", "rgb(255, 159, 64)", "rgb(255, 205, 86)", "rgb(75, 192, 192)",
    "rgb(191, 255, 0)", "rgb(54, 162, 235)", "rgb(153, 102, 255)", "rgb(201, 203, 207)", "rgb(0, 255, 255)"]

var color = Chart.helpers.color;
var chartColors = window.chartColors;

// check number of total events if updated then renew the graph
var old_number_of_total_events;
var new_number_of_total_events;

var week_dates_array = [];

// Data to plot
var top_values_to_plot = {};
var date_wise_event_counts = {};

/**
 * Function to get total event counts and set the Element value
 * @param {*} event_type
 * @param {*} html_element_id
 */
function get_event_count(event_type, html_element_id) {
    $.ajax({
        type: "GET",
        url: "/api/events/count/" + event_type,
        success: function (result, status, xhr) {
            new_number_of_total_events = (event_type === "all") ? result["count"] : new_number_of_total_events;
            document.getElementById(html_element_id).innerHTML = result["count"];
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log(jqXHR.responseText)
        }
    });
}

/**
 * Create object structure for the given event type and element, if it doesn't already exist
 * @param {*} event_type
 * @param {*} element
 */
function create_top_values_to_plot_structure(event_type, element) {
    !(event_type in top_values_to_plot) ? top_values_to_plot[event_type] = {} : true;
    !(element in top_values_to_plot[event_type]) ? top_values_to_plot[event_type][element] = {} : true;
    !("keys" in top_values_to_plot[event_type][element]) ? top_values_to_plot[event_type][element].keys = [] : true;
    !("values" in top_values_to_plot[event_type][element]) ? top_values_to_plot[event_type][element].values = [] : true;
    !("colors" in top_values_to_plot[event_type][element]) ? top_values_to_plot[event_type][element].colors = [] : true;
}


/**
 * Get top 10 element values in the given event type and plot them.
 * @param {*} event_type
 * @param {*} element
 * @param {*} html_element_id
 */
function get_top_ten_element_in_event(event_type, element, html_element_id) {
    $.ajax({
        type: "GET",
        url: "/api/events/count/groupby/" + event_type.toLowerCase() + "/" + element.toLowerCase(),
        success: function (result, status, xhr) {
            create_top_values_to_plot_structure(event_type, element);
            const keys = Object.keys(result);
            top_values_to_plot[event_type][element].keys = [];
            top_values_to_plot[event_type][element].values = [];
            top_values_to_plot[event_type][element].colors = [];
            for (let i = 0; i < keys.length; i++) {
                top_values_to_plot[event_type][element].keys.push(keys[i]);
                top_values_to_plot[event_type][element].values.push(result[keys[i]]);
                top_values_to_plot[event_type][element].colors.push(color(colors_array[i]).alpha(0.5).rgbString());
            }
            const top_ten_graph_config = {
                data: {
                    datasets: [{
                        data: top_values_to_plot[event_type][element].values,
                        backgroundColor: top_values_to_plot[event_type][element].colors,
                        label: translations['top_ten_' + element.toLowerCase() + 's-' + event_type.toLowerCase()]
                    }],
                    labels: top_values_to_plot[event_type][element].keys
                },
                options: {
                    responsive: true,
                    legend: {
                        position: 'right',
                    },
                    title: {
                        display: true,
                        text: translations['top_ten_' + element.toLowerCase() + 's-' + event_type.toLowerCase()]
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

            const ctx = document.getElementById(html_element_id);
            window.myPolarArea = Chart.PolarArea(ctx, top_ten_graph_config);
            const downloadButton = ctx.nextSibling.nextSibling;
            downloadButton.hidden = false;
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log(jqXHR.responseText)
        }
    });
}

/**
 * Plot date wise data to the graph
 * @param {*} event_type
 */
function plot_event_count_by_date(event_type) {

    for (let counter = 0; counter < week_dates_array.length; counter++) {
        $.ajax({
            type: "GET",
            url: "/api/events/count/" + event_type,
            data: {
                date: week_dates_array[counter]
            },
            success: function (result, status, xhr) {
                date_wise_event_counts[event_type][result["date"].toString().split(" ")[0]] = result["count"];
                const past_week_events_graph_config = {
                    type: 'line',
                    data: {
                        labels: week_dates_array,
                        datasets: [{
                            label: translations.all_events,
                            backgroundColor: window.chartColors.red,
                            borderColor: window.chartColors.red,
                            data: [
                                date_wise_event_counts.all[week_dates_array[0]],
                                date_wise_event_counts.all[week_dates_array[1]],
                                date_wise_event_counts.all[week_dates_array[2]],
                                date_wise_event_counts.all[week_dates_array[3]],
                                date_wise_event_counts.all[week_dates_array[4]],
                                date_wise_event_counts.all[week_dates_array[5]],
                                date_wise_event_counts.all[week_dates_array[6]]
                            ],
                            fill: false,
                        }, {
                            label: translations.honeypot_events,
                            fill: false,
                            backgroundColor: window.chartColors.blue,
                            borderColor: window.chartColors.blue,
                            data: [
                                date_wise_event_counts.honeypot[week_dates_array[0]],
                                date_wise_event_counts.honeypot[week_dates_array[1]],
                                date_wise_event_counts.honeypot[week_dates_array[2]],
                                date_wise_event_counts.honeypot[week_dates_array[3]],
                                date_wise_event_counts.honeypot[week_dates_array[4]],
                                date_wise_event_counts.honeypot[week_dates_array[5]],
                                date_wise_event_counts.honeypot[week_dates_array[6]]
                            ],
                        }, {
                            label: translations.network_events,
                            fill: false,
                            backgroundColor: window.chartColors.yellow,
                            borderColor: window.chartColors.yellow,
                            data: [
                                date_wise_event_counts.network[week_dates_array[0]],
                                date_wise_event_counts.network[week_dates_array[1]],
                                date_wise_event_counts.network[week_dates_array[2]],
                                date_wise_event_counts.network[week_dates_array[3]],
                                date_wise_event_counts.network[week_dates_array[4]],
                                date_wise_event_counts.network[week_dates_array[5]],
                                date_wise_event_counts.network[week_dates_array[6]]
                            ],
                        }, {
                            label: translations.credential_events,
                            fill: false,
                            backgroundColor: window.chartColors.purple,
                            borderColor: window.chartColors.purple,
                            data: [
                                date_wise_event_counts.credential[week_dates_array[0]],
                                date_wise_event_counts.credential[week_dates_array[1]],
                                date_wise_event_counts.credential[week_dates_array[2]],
                                date_wise_event_counts.credential[week_dates_array[3]],
                                date_wise_event_counts.credential[week_dates_array[4]],
                                date_wise_event_counts.credential[week_dates_array[5]],
                                date_wise_event_counts.credential[week_dates_array[6]]
                            ],
                        }, {
                            label: translations.file_events,
                            fill: false,
                            backgroundColor: window.chartColors.green,
                            borderColor: window.chartColors.green,
                            data: [
                                date_wise_event_counts.file[week_dates_array[0]],
                                date_wise_event_counts.file[week_dates_array[1]],
                                date_wise_event_counts.file[week_dates_array[2]],
                                date_wise_event_counts.file[week_dates_array[3]],
                                date_wise_event_counts.file[week_dates_array[4]],
                                date_wise_event_counts.file[week_dates_array[5]],
                                date_wise_event_counts.file[week_dates_array[6]]
                            ],
                        }, {
                            label: translations.data_events,
                            fill: false,
                            backgroundColor: window.chartColors.cyan,
                            borderColor: window.chartColors.cyan,
                            data: [
                                date_wise_event_counts.data[week_dates_array[0]],
                                date_wise_event_counts.data[week_dates_array[1]],
                                date_wise_event_counts.data[week_dates_array[2]],
                                date_wise_event_counts.data[week_dates_array[3]],
                                date_wise_event_counts.data[week_dates_array[4]],
                                date_wise_event_counts.data[week_dates_array[5]],
                                date_wise_event_counts.data[week_dates_array[6]]
                            ],
                        }, {
                            label: translations.pcap_events,
                            fill: false,
                            backgroundColor: window.chartColors.orange,
                            borderColor: window.chartColors.orange,
                            data: [
                                date_wise_event_counts.pcap[week_dates_array[0]],
                                date_wise_event_counts.pcap[week_dates_array[1]],
                                date_wise_event_counts.pcap[week_dates_array[2]],
                                date_wise_event_counts.pcap[week_dates_array[3]],
                                date_wise_event_counts.pcap[week_dates_array[4]],
                                date_wise_event_counts.pcap[week_dates_array[5]],
                                date_wise_event_counts.pcap[week_dates_array[6]]
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
                const past_week_events_graph_config_ctx = document.getElementById('past_week_events_graph').getContext('2d');
                window.myLine = new Chart(past_week_events_graph_config_ctx, past_week_events_graph_config);
                const downloadButton = document.getElementById('past_week_events_graph').nextSibling.nextSibling;
                downloadButton.hidden = false;
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log(jqXHR.responseText)
            }
        });
    }
}

function load_graphs() {
    // request all events number
    get_event_count("all", "count_all_events");

    // wait 3 seconds to get responded for the request
    setTimeout(function () {
        // if events number updated or its first time to load the graph
        if (old_number_of_total_events !== new_number_of_total_events) {
            week_dates_array = [];
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
            // request network related events number
            get_event_count("credential", "count_credential_events");
            // request network related events number
            get_event_count("file", "count_file_events");
            // request network related events number
            get_event_count("data", "count_data_events");
            // request network related events number
            get_event_count("pcap", "count_pcap_events");
            // request top ten ips in honeypot events
            get_top_ten_element_in_event("Honeypot", "Ip_dest", "top_ten_ips_in_honeypot_events_graph");
            // request top ten ips in network events
            get_top_ten_element_in_event("Network", "Ip_dest", "top_ten_ips_in_network_events_graph");
            // request top ten ports in honeypot events
            get_top_ten_element_in_event("Honeypot", "Port_dest", "top_ten_ports_in_honeypot_events_graph");
            // request top ten ports in network events
            get_top_ten_element_in_event("Network", "Port_dest", "top_ten_ports_in_network_events_graph");
            // 7 days ago config
            !("all" in date_wise_event_counts) ? date_wise_event_counts.all = {} : true;
            !("honeypot" in date_wise_event_counts) ? date_wise_event_counts.honeypot = {} : true;
            !("network" in date_wise_event_counts) ? date_wise_event_counts.network = {} : true;
            !("credential" in date_wise_event_counts) ? date_wise_event_counts.credential = {} : true;
            !("file" in date_wise_event_counts) ? date_wise_event_counts.file = {} : true;
            !("data" in date_wise_event_counts) ? date_wise_event_counts.data = {} : true;
            !("pcap" in date_wise_event_counts) ? date_wise_event_counts.pcap = {} : true;
            // request all events number by date for past week
            plot_event_count_by_date("all");
            // request network events number by date for past week
            plot_event_count_by_date("network");
            // request honeypot events number by date for past week
            plot_event_count_by_date("honeypot");
            // request credential events number by date for past week
            plot_event_count_by_date("credential");
            // request file events number by date for past week
            plot_event_count_by_date("file");
            // request data events number by date for past week
            plot_event_count_by_date("data");
            // request pcap events number by date for past week
            plot_event_count_by_date("pcap");


        }
    }, 3000);
}

/**
 * Function is used to convert canvas to image and download it
 * @param canvasId
 */
function downloadChart(canvasId) {
    const canvas = document.getElementById(canvasId);
    let downloadLink = document.createElement('a');
    const filename = canvasId + ".png";
    downloadLink.setAttribute('download', filename);
    canvas.toBlob(function (blob) {
        let url = URL.createObjectURL(blob);
        downloadLink.setAttribute('href', url);
        downloadLink.click();
    });
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
