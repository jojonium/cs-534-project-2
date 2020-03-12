function main(): void {
  const csvMessage = document.createElement("p");
  csvMessage.innerText = "Select the Sample Data File";
  document.body.appendChild(csvMessage);

  const csvInput = document.createElement("input");
  csvInput.type = "file";
  csvInput.id = "csv";
  csvInput.accept = ".csv";
  document.body.appendChild(csvInput);

  const outputArea = document.createElement("output");
  outputArea.id = "out";
  outputArea.innerHTML = "Results will go here";
  document.body.appendChild(outputArea);
}

window.onload = main;

const dataPoints = [];

const fileInput = document.getElementById("csv");

const readFile = function() {
  const reader = new FileReader();
  reader.onload = function() {
    document.getElementById("out").innerHTML = reader.result;
  };
  reader.readAsBinaryString(fileInput.files[0]);
};

fileInput?.addEventListener("change", readFile);
