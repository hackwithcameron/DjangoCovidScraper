
// AutoFill search bar
var stateList = document.getElementById('stateList');

var request = new XMLHttpRequest();

request.onreadystatechange = function(response) {
    if (request.readyState === 4) {
        if (request.status === 200) {
            // Parse through JSON file
            var stateOptions = JSON.parse(request.responseText);

            // Loop over the JSON file
            stateOptions.forEach(element => {
                var state = document.createElement('option');
                state.value = element;
                stateList.appendChild(state);
            });
        }
    }
};

request.open('GET', './static/json/states.json', true);
request.send();

var dataList = document.getElementById('json-datalist');
var input = document.getElementById('ajax');




