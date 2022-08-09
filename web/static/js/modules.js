/**
 * Function to get total event counts and set the Element value
 * @param {*} event_type
 * @param {*} html_element_id
 */
function get_running_modules_details(html_element_id) {
    $.ajax({
        type: "GET",
        url: "/api/core/running/modules",
        success: function (result, status, xhr) {
            let module_data = `<tr>\n` +
                ` <th>S.No</th>\n` +
                ` <th>Image</th>\n` +
                ` <th>Networks</th>\n` +
                ` <th>Ports</th>\n` +
                ` <th>Running For</th>\n` +
                ` <th>Size</th>\n` +
                ` <th>State</th>\n` +
                ` <th>Status</th>\n` +
                ` <th>CreatedAt</th> \n` +
                ` </tr>`;
            if (result.length === 0) {
                displayErrorMessageForModules(translations.no_modules_running_message, html_element_id);
            } else {
                for (let i = 0; i < result.length; i++) {
                    module_data += ` <tr>\n` +
                        `                <th>${i + 1}</th>\n` +
                        `                <th>${result[i].Image}</th>\n` +
                        `                <th>${result[i].Networks}</th>\n` +
                        `                <th>${result[i].Ports}</th>\n` +
                        `                <th>${result[i].RunningFor}</th>\n` +
                        `                <th>${result[i].Size}</th>\n` +
                        `                <th>${result[i].State}</th>\n` +
                        `                <th>${result[i].Status}</th>\n` +
                        `                <th>${result[i].CreatedAt}</th>\n` +
                        `            </tr>`;
                }
                document.getElementById("error-message-element-modules").hidden = true;
                document.getElementById(html_element_id).hidden = false;
                document.getElementById(html_element_id).innerHTML = module_data;
                document.getElementById("download-module-report").hidden = false;
                document.getElementById("download-module-report-csv").hidden = false;
                document.getElementById("download-module-report-json").hidden = false;
                document.getElementById("download-module-report-excel").hidden = false;
                document.getElementById("export_module_heading").hidden = false;
            }
        },
        error: function (jqXHR, textStatus, errorThrown) {
            displayErrorMessageForModules(translations.modules_api_error_message, html_element_id)
        }
    });
}

function download_module_report_as_pdf(html_element_id) {
    let modules_window = window.open('', 'PRINT', 'height=650,width=900,top=100,left=150');

    modules_window.document.write(`<html><head><title>Running module details</title>`);
    modules_window.document.write(`<style>
        table,
        th,
        td {
            border: 1px solid black;
            border-collapse: collapse;
        };
        </style>`);
    modules_window.document.write('</head><body>');
    modules_window.document.write('<div style="text-align: center; width: 100%; margin: 1rem"><img width="100px"  src="../img/owasp-honeypot.png"/></div>');
    modules_window.document.write(document.getElementById(html_element_id).innerHTML);
    modules_window.document.write('<div style="text-align: center; width: 100%; margin: 1rem"><img width="100px"  src="../img/owasp.png"/></div>');
    modules_window.document.write('</body></html>');

    modules_window.document.close();
    modules_window.focus();

    modules_window.print();
    modules_window.close();

}

function download_module_report_as_csv() {
    let filename = "running_module_details.csv"
    let csv = [];
    let rows = document.querySelectorAll("table tr");

    for (let i = 0; i < rows.length; i++) {
        let row = [], cols = rows[i].querySelectorAll("td, th");

        for (let j = 0; j < cols.length; j++)
            row.push(cols[j].innerText);

        csv.push(row.join(","));
    }
    csv = csv.join("\n")

    let csvFile;
    let downloadLink;
    csvFile = new Blob([csv], {type: "text/csv"});
    downloadLink = document.createElement("a");
    downloadLink.download = filename;
    downloadLink.href = window.URL.createObjectURL(csvFile);
    downloadLink.style.display = "none";
    document.body.appendChild(downloadLink);
    downloadLink.click();
}


function download_module_report_as_json(html_element_id) {
    let data = get_json_from_table(html_element_id);
    const filename = "running_module_details.json"
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(data, undefined, 2));
    const downloadAnchorNode = document.createElement('a');
    downloadAnchorNode.setAttribute("href", dataStr);
    downloadAnchorNode.setAttribute("download", filename);
    document.body.appendChild(downloadAnchorNode);
    downloadAnchorNode.click();
}

function download_module_report_as_excel(html_element_id) {
    let data = get_json_from_table(html_element_id);
    const filename = "running_module_details.xlsx"
    let ws = XLSX.utils.json_to_sheet(data);
    let wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "running_module_details");
    XLSX.writeFile(wb, filename);
}

function get_json_from_table(html_element_id) {
    let table = document.getElementById(html_element_id);
    let data = [];
    let columns = [];
    for (let i = 0; i < table.rows.length; i++) {
        let tableRow = table.rows[i];
        for (let j = 0; j < tableRow.cells.length; j++) {
            columns.push(tableRow.cells[j].innerHTML);
        }
    }
    for (let i = 1; i < table.rows.length; i++) {
        let tableRow = table.rows[i];
        let rowData = {};
        for (let j = 0; j < tableRow.cells.length; j++) {
            rowData[columns[j]] = (tableRow.cells[j].innerHTML);
        }
        data.push(rowData);
    }

    return data;
}

function update_modules() {
    setTimeout(function () {
        get_running_modules_details("running-module-details");
        update_modules();
    }, 5000);
}


// load first time
get_running_modules_details("running-module-details");

// 30 seconds delay loop
update_modules();
