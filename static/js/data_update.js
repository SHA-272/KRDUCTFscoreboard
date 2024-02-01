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
  let html = '';

  data.forEach(entry => {
    html += `
      <tr class="${getClass(entry)}">
        <td>${entry.pos}</td> 
        <td>${entry.name}</td>
        <td>${entry.score}</td>
      </tr>
    `;
  });

  const scoreboardBody = document.getElementById("scoreboard-body");
  scoreboardBody.innerHTML = html;
}

function getClass(entry) {
  if(entry.pos === 1) return 'text-golden';
  if(entry.pos === 2) return 'text-silver';
  if(entry.pos === 3) return 'text-bronze';
  return '';
}

fetchData();

setInterval(fetchData, 2000);
