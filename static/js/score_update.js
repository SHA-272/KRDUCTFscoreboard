const scoreboardBody = document.getElementById("scoreboard-body");

function fetchDataAndUpdateScoreboard() {
  fetch("/api/scoreboard")
    .then((response) => response.json())
    .then((data) => {
      let html = "";
      if (
        typeof data === "undefined" ||
        data === null ||
        !Array.isArray(data)
      ) {
        throw new Error("Invalid data format: Expected an array.");
      }
      for (const entry of data) {
        html += `
          <tr>
            <td>${entry.pos}</td> 
            <td>${entry.name}</td>
            <td>${entry.score}</td>
          </tr>
        `;
      }
      scoreboardBody.innerHTML = html;
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
}

fetchDataAndUpdateScoreboard();

setInterval(fetchDataAndUpdateScoreboard, 2000);
