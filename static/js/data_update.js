function fetchData() {
  fetch("/api/scoreboard")
    .then((response) => response.json())
    .then((data) => {
      // Update the scoreboard on the page
      updateScoreboard(data);
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
}

function updateScoreboard(data) {
  // Update the scoreboard container on the page
  const scoreboardBody = document.getElementById("scoreboard-body");

  // Clear the container
  scoreboardBody.innerHTML = "";

  // Create rows and append them to the container
  data.forEach((entry) => {
    const rowElement = document.createElement("tr");

    const posCell = document.createElement("td");
    posCell.textContent = entry["pos"];
    rowElement.appendChild(posCell);

    const nameCell = document.createElement("td");
    nameCell.textContent = entry["name"];
    rowElement.appendChild(nameCell);

    const scoreCell = document.createElement("td");
    scoreCell.textContent = entry["score"];
    rowElement.appendChild(scoreCell);

    // Apply styles based on position
    if (entry["pos"] === 1) {
      rowElement.style.color = "gold";
    } else if (entry["pos"] === 2) {
      rowElement.style.color = "silver";
    } else if (entry["pos"] === 3) {
      rowElement.style.color = "orange";
    }

    scoreboardBody.appendChild(rowElement);
  });
}

// Fetch data initially
fetchData();

// Fetch data every 5 seconds (adjust as needed)
setInterval(fetchData, 5000);
