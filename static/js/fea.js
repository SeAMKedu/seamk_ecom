//=========================================================================
// API Configurations
//=========================================================================
const apiHost = window.location.hostname;
const apiPort = 8000;
const baseURL = `http://${apiHost}:${apiPort}/api`;
const urlFEA = `${baseURL}/fea`;
const urlData = `${baseURL}/fea/image-data`;
const urlFile = `${baseURL}/fea/image-file`;

//=========================================================================
// HTTP request
//=========================================================================
/**
 * Send a HTTP request.
 * @param {string} method The HTTP request method.
 * @param {string} url The HTTP request URL.
 * @param {object} body The HTTP request body.
 * @param {function} callback The function to be called on response.
 */
function sendRequest(method, url, body, callback, fetchFile = false) {
    var request = new XMLHttpRequest();
    request.open(method, url, true);
    // Handle the response from the server.
    request.onreadystatechange = function() {
        if (this.readyState === 4) {
            // Success.
            if (this.status === 200) {
                callback(this);
            // Bad Request, Validation Error, Server Error.
            } else {
                console.error(this);
            }
        }
    };
    // Expect an image file as a response.
    // Also, prevent web browser for fetching the image file from the cache.
    if (fetchFile) {
        request.responseType = "blob";
        request.setRequestHeader("Cache-Control", "no-cache");
    }
    // Send a HTTP request.
    if (method == "POST" && url == urlFEA) {
        request.setRequestHeader("Content-type", "application/json; charset=UTF-8");
        request.send(JSON.stringify(body));
    } else {
        request.send(body);
    }
};

//=========================================================================
// Finite Element Analysis (FEA)
//=========================================================================
/**
 * Post the input parameters of the FEA.
 */
function postFEA() {
    const info = document.getElementById("fea-info");

    // Read the input parameters of the FEA.
    const dist1 = parseInt(document.getElementById("input-d1").value);
    const dist2 = parseInt(document.getElementById("input-d2").value);
    const dist3 = parseInt(document.getElementById("input-d3").value);
    const force = parseInt(document.getElementById("input-f").value);

    // Check that the inputs are valid.
    let validInputs = false;
    if (50 <= dist1 && dist1 <= 120) {
        if (50 <= dist2 && dist2 <= 120) {
            if (50 <= dist3 && dist3 <= 120) {
                if (10 <= force && force <= 1000) {
                    validInputs = true;
                }
            }
        }
    }

    if (validInputs === true) {
        info.innerHTML = "";
        const button = document.getElementById("btn-post");
        const image = document.getElementById("img-support");
        const spinner = document.getElementById("spinner");
        // Disable the button for posting the inputs for the FEA.
        button.disabled = true;
        // Hide the geometry of the support and show the spinner instead.
        image.hidden = true;
        spinner.hidden = false;

        const feaInputs = {
            d1: dist1,
            d2: dist2,
            d3: dist3,
            f: force
        };
        sendRequest("POST", urlFEA, feaInputs, callbackPostFEA);
    } else {
        info.innerHTML = "Invalid value detected! Please, check the inputs.";
    }
};
//-------------------------------------------------------------------------
/**
 * Show the output of the Finite Element Analysis.
 * @param {XMLHttpRequest} response Response from the server.
 */
function callbackPostFEA(response) {
    const button = document.getElementById("btn-post");
    const image = document.getElementById("img-support");
    const spinner = document.getElementById("spinner");
    // Enable the button for posting the inputs for the FEA.
    button.disabled = false;
    // Show the geometry of the support and hide the spinner.
    image.hidden = false;
    spinner.hidden = true;
    // Show the output of the FEA.
    const responseJSON = JSON.parse(response.responseText);
    document.getElementById("input-r1").value = responseJSON.r1;
    document.getElementById("input-r2").value = responseJSON.r2;
    document.getElementById("input-area").value = responseJSON.area;
    document.getElementById("input-stress").value = responseJSON.stress;
    // Fetch the geometry of the support as an image file.
    getFile();
};

//=========================================================================
// Image File
//=========================================================================
/**
 * Fetch the optimized geometry of the support as a PNG image file.
 */
function getFile() {
    sendRequest("GET", urlFile, null, callbackGetFile, true);
};
//-------------------------------------------------------------------------
/**
 * Show the image file on the web page.
 * @param {XMLHttpRequest} response Response from the server.
 */
function callbackGetFile(response) {
    const image = document.getElementById("img-support");
    image.src = URL.createObjectURL(response.response);
    getData();
};

//=========================================================================
// Image Data
//=========================================================================
/**
 * Fetch the image data that will be stored to the field of the Sale Order
 * record (see the file 'controllers.py').
 */
function getData() {
    sendRequest("GET", urlData, null, callbackGetData);
};
//-------------------------------------------------------------------------
/**
 * Save the image data to the hidden HTML input element.
 * @param {XMLHttpRequest} response Response from the server.
 */
function callbackGetData(response) {
    document.getElementById("input-img").value = response.responseText;
};