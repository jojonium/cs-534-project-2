function main(): void {
  const testMessage = document.createElement("p");
  testMessage.innerText = "Successfully ran compiled TypeScript";
  document.body.appendChild(testMessage);
}

window.onload = main;
