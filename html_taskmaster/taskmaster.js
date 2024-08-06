const monthEl = document.getElementById("month");
const yearEl = document.getElementById("year");
const daysEl = document.getElementById("days");

const months = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
];

const now = new Date();
let currentMonth = now.getMonth();
let currentYear = now.getFullYear();

function renderCalendar(month, year) {
    monthEl.textContent = months[month];
    yearEl.textContent = year;

    daysEl.innerHTML = "";
    const firstDay = new Date(year, month, 1).getDay();
    const lastDate = new Date(year, month + 1, 0).getDate();

    for (let i = 0; i < firstDay; i++) {
        const emptyDiv = document.createElement("div");
        daysEl.appendChild(emptyDiv);
    }

    for (let date = 1; date <= lastDate; date++) {
        const dateDiv = document.createElement("div");
        dateDiv.textContent = date;
        daysEl.appendChild(dateDiv);
    }
}

document.querySelector(".prev").addEventListener("click", () => {
    currentMonth--;
    if (currentMonth < 0) {
        currentMonth = 11;
        currentYear--;
    }
    renderCalendar(currentMonth, currentYear);
});

document.querySelector(".next").addEventListener("click", () => {
    currentMonth++;
    if (currentMonth > 11) {
        currentMonth = 0;
        currentYear++;
    }
    renderCalendar(currentMonth, currentYear);
});

renderCalendar(currentMonth, currentYear);
