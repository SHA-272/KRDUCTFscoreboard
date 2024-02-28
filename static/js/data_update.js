function fetchData() {
  fetch("/api/scoreboard")
    .then((response) => response.json())
    .then((data) => {
      updateScoreboard(data);
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
}

function updateScoreboard(data) {
  let html = "";

  data.forEach((entry) => {
    html += `
      <tr>
        <td>${entry.pos}</td> 
        <td>${entry.name}</td>
        <td>${entry.score}</td>
      </tr>
    `;
  });

  const scoreboardBody = document.getElementById("scoreboard-body");
  scoreboardBody.innerHTML = html;
}

fetchData();

setInterval(fetchData, 2000);
