let startTime;
let endTime;

function fetchStartTime() {
  fetch("/api/start")
    .then((response) => response.json())
    .then((data) => {
      startTime = new Date(data * 1000).getTime();
      updateStartTime();
    })
    .catch((error) => {
      console.error("Error fetching start time:", error);
    });
}

function fetchEndTime() {
  fetch("/api/end")
    .then((response) => response.json())
    .then((data) => {
      endTime = new Date(data * 1000).getTime();
      updateEndTime();
    })
    .catch((error) => {
      console.error("Error fetching end time:", error);
    });
}

fetchStartTime();
fetchEndTime();

setInterval(function () {
  let now = new Date().getTime();
  let distance = startTime - now;

  if (distance > 0) {
    document.getElementById("time").innerHTML =
      "До начала:<div class='time-countdown'>" + timeToStr(distance) + "</div>";
  } else {
    distance = endTime - now;

    if (distance > 0) {
      document.getElementById("time").innerHTML =
        "До окончания:<div class='time-countdown'>" +
        timeToStr(distance) +
        "</div>";
    }
  }
}, 1);

function timeToStr(time) {
  let days = Math.floor(time / (1000 * 60 * 60 * 24));
  let hours = Math.floor((time % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  let minutes = Math.floor((time % (1000 * 60 * 60)) / (1000 * 60));
  let seconds = Math.floor((time % (1000 * 60)) / 1000);
  let s = "";
  if (days > 0) s += days + ":";
  if (days > 0 || hours > 0) s += hours + ":";
  if (days > 0 || hours > 0 || minutes > 0) s += minutes + ":";
  s += seconds;
  if (minutes < 5 && hours < 0 && days < 0)
    s =
      "<span class='alert-red'>" +
      s +
      ":" +
      Math.floor(time % 1000) +
      "</span>";
  return s;
}
