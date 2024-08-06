const monthEl = document.getElementById("month");
const yearEl = document.getElementById("year");
const daysEl = document.getElementById("days");
const selectedDateEl = document.getElementById("selected-date");
const taskInput = document.getElementById("task-input");
const addTaskButton = document.getElementById("add-task");
const taskList = document.getElementById("task-list");

const months = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
];

const now = new Date();
let currentMonth = now.getMonth();
let currentYear = now.getFullYear();
let selectedDate = null;
let tasks = {};

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
        dateDiv.addEventListener("click", () => selectDate(date, month, year));
        daysEl.appendChild(dateDiv);
    }
}

function selectDate(date, month, year) {
    selectedDate = `${date}/${month + 1}/${year}`;
    selectedDateEl.textContent = selectedDate;
    renderTasks();
}

function renderTasks() {
    taskList.innerHTML = "";
    const tasksForDate = tasks[selectedDate] || [];
    tasksForDate.forEach(task => {
        const taskItem = document.createElement("li");
        taskItem.textContent = task;
        taskList.appendChild(taskItem);
    });
}

addTaskButton.addEventListener("click", () => {
    if (selectedDate && taskInput.value) {
        if (!tasks[selectedDate]) {
            tasks[selectedDate] = [];
        }
        tasks[selectedDate].push(taskInput.value);
        taskInput.value = "";
        renderTasks();
    }
});

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
