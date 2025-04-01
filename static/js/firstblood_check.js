const container = document.getElementById("notifications-container");
const shownSubmissions = new Set();

function playConfetti() {
  confetti({
    particleCount: 200,
    spread: 200,
    origin: { y: 0.5 },
  });
}

function showNotification(userName, challengeName) {
  const note = document.createElement("div");
  note.className = "notification-popup";
  note.innerHTML = `Первое решение задания <b>"${challengeName}"</b> от <b>"${userName}"</b>`;

  container.appendChild(note);
  playConfetti();

  setTimeout(() => {
    note.classList.add("fade-out");
    setTimeout(() => note.remove(), 1000);
  }, 29000);
}

async function checkNewSubmissions() {
  try {
    const res = await fetch("/api/get_firstbloods");
    const data = await res.json();

    if (Array.isArray(data) && data.length > 0) {
      data.forEach((sub) => {
        if (!shownSubmissions.has(sub.id)) {
          shownSubmissions.add(sub.id);

          const user = sub.user?.name || "Неизвестный";
          const task = sub.challenge?.name || "Неизвестно";
          showNotification(user, task);
        }
      });
    }
  } catch (e) {
    console.error("Ошибка при получении новых решений:", e);
  }
}

setInterval(checkNewSubmissions, 2000);
