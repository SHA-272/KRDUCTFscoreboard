let startTime;
let endTime;
const timeElement = document.getElementById("time");

function fetchData() {
  Promise.all([fetch("/api/start"), fetch("/api/end")])
    .then((responses) => Promise.all(responses.map((res) => res.json())))
    .then((data) => {
      startTime = data[0] ? new Date(data[0] * 1000).getTime() : null;
      endTime = data[1] ? new Date(data[1] * 1000).getTime() : null;
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
}

function updateTime() {
  let now = new Date().getTime();
  let distance;

  if (startTime && now < startTime) {
    distance = startTime - now;
    timeElement.innerHTML = `До начала:<div class='time-countdown'>${timeToStr(
      distance
    )}</div>`;
  } else if (endTime && now < endTime) {
    distance = endTime - now;
    timeElement.innerHTML = `До окончания:<div class='time-countdown'>${timeToStr(
      distance
    )}</div>`;
  } else {
    timeElement.innerHTML = "Соревнования окончены!";
    return;
  }
}

function timeToStr(time) {
  const days = Math.floor(time / (1000 * 60 * 60 * 24));
  const hours = Math.floor((time % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  const minutes = Math.floor((time % (1000 * 60 * 60)) / (1000 * 60));
  const seconds = Math.floor((time % (1000 * 60)) / 1000);

  let s = "";

  if (days > 0) s += `${days}:`;
  if (hours > 0 || days > 0) s += `${hours.toString().padStart(2, "0")}:`;
  if (minutes > 0 || hours > 0 || days > 0)
    s += `${minutes.toString().padStart(2, "0")}:`;
  s += seconds.toString().padStart(2, "0");

  if (minutes < 10 && hours <= 0 && days <= 0) {
    s = `<span class='alert-red'>${s}:${Math.floor(time % 1000).toString().padStart(3, "0")}</span>`;
  }
  return s;
}

fetchData();
setInterval(updateTime, 17);
