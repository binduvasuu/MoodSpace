let selectedMood = '';
const calmTips = [
  "Take 3 deep breaths slowly 🌬️",
  "Listen to soft music 🎶",
  "Write one thing you're grateful for ✨",
  "Close your eyes for 60 seconds 🧘‍♀️",
  "Drink a glass of water 🚰",
  "Stretch your body gently 🧎"
];

function selectMood(mood) {
  selectedMood = mood;
  alert("Mood selected: " + mood);
}

function saveMood() {
  const note = document.getElementById("note").value;
  const date = new Date().toLocaleString();

  if (!selectedMood) {
    alert("Please select a mood first.");
    return;
  }

  const entry = {
    mood: selectedMood,
    note: note,
    date: date
  };

  let data = JSON.parse(localStorage.getItem("moodEntries")) || [];
  data.push(entry);
  localStorage.setItem("moodEntries", JSON.stringify(data));

  document.getElementById("note").value = '';
  selectedMood = '';
  showHistory();
  showRandomTip();
}

function showHistory() {
  const list = document.getElementById("historyList");
  list.innerHTML = '';
  const data = JSON.parse(localStorage.getItem("moodEntries")) || [];

  data.reverse().forEach(entry => {
    const item = document.createElement('li');
    item.textContent = `${entry.date} — ${entry.mood} — ${entry.note}`;
    list.appendChild(item);
  });
}

function showRandomTip() {
  const tip = calmTips[Math.floor(Math.random() * calmTips.length)];
  document.getElementById("calmTip").textContent = tip;
}

// Load mood history on page load
window.onload = () => {
  showHistory();
  showRandomTip();
};
