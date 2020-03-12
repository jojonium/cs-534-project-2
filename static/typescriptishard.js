function main() {
    const csvMessage = document.createElement("p");
    csvMessage.innerText = "Select the Sample Data File";
    document.body.appendChild(csvMessage);

    const csvInput = document.createElement("input");
    csvInput.type = "file";
    csvInput.id = "csv";
    csvInput.accept = ".csv";
    csvInput.addEventListener("change", readFile);
    document.body.appendChild(csvInput);

    const outputArea = document.createElement("output");
    outputArea.id = "out";
    outputArea.innerHTML = "Results will go here";
    document.body.appendChild(outputArea);

}

window.onload = main;

let dataPoints = [];


const readFile = function () {
    const fileInput = document.getElementById("csv");
    const reader = new FileReader();
    reader.onload = function () {
        dataPoints = [];
        document.getElementById("out").innerHTML = '';
        dataPoints.pop();
        reader.result.split('\n').forEach(e => {
            if(e !== ''){
            document.getElementById("out").innerHTML += '<p>( ' + e + ')</p>';
            dataPoint = e.split(',');
            dataPoints.push(dataPoint.map(parseFloat));
            }
        });
    };
    reader.readAsBinaryString(fileInput.files[0]);
};


