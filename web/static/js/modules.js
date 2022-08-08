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
            console.log(result)
            let module_data = `<tr>\n` +
                ` <th>S.No</th>\n` +
                ` <th>Image</th>\n` +
                ` <th>Networks</th>\n` +
                ` <th>Ports</th>\n` +
                ` <th>Running For</th>\n` +
                ` <th>Size</th>\n` +
                ` <th>State</th>\n` +
                ` <th>Status</th>\n` +
                `<th> CreatedAt</th> \n` +
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
            }
        },
        error: function (jqXHR, textStatus, errorThrown) {
            displayErrorMessageForModules(translations.modules_api_error_message, html_element_id)
        }
    });
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
