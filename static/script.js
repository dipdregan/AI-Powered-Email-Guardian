// script.js
function addUserMessage(message) {
    var userMessages = document.getElementById("userMessages");
    var li = document.createElement("li");
    li.textContent = message;
    userMessages.appendChild(li);
    
    if (userMessages.children.length > 4) {
        userMessages.removeChild(userMessages.children[0]);
    }
}

function predict() {
    var message = document.getElementById("message").value;
    addUserMessage(message);

    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var response = JSON.parse(xhr.responseText);
            displayPrediction(response);
        }
    };
    xhr.open("POST", "/", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.send("message=" + encodeURIComponent(message));
}

function displayPrediction(prediction) {
    var resultDiv = document.getElementById("result");
    resultDiv.innerHTML = "<p class='prediction'>Prediction: " + prediction.prediction + "</p>" +
                           "<p class='probability'>Probability: " + prediction.probability + "</p>";
}
