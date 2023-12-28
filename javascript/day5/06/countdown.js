let dayTen = document.querySelector("[data-days-tens]");
let dayOne = document.querySelector("[data-days-ones]");
let hourTen = document.querySelector("[data-hours-tens]");
let hourOne = document.querySelector("[data-hours-ones]");
let minuteTen = document.querySelector("[data-minutes-tens]");
let minuteOne = document.querySelector("[data-minutes-ones]");
let secondTen = document.querySelector("[data-seconds-tens]");
let secondOne = document.querySelector("[data-seconds-ones]");

const second = 1000,
  minute = second * 60,
  hour = minute * 60,
  day = hour * 24;

window.addEventListener("load", function () {
  setInterval(remainTime, 1000);
});

function remainTime() {
  let today = new Date();
  let newYear = new Date(2024, 0, 1, 0, 0, 0);

  let betweenDates = newYear.getTime() - today.getTime();
  flipAllCards(betweenDates);
}

function flipAllCards(timeLeft) {
  const seconds = Math.floor((timeLeft % minute) / second);
  const minutes = Math.floor((timeLeft % hour) / minute);
  const hours = Math.floor((timeLeft % day) / hour);
  const days = Math.floor(timeLeft / day);

  flip(dayTen, Math.floor(days / 10));
  flip(dayOne, days % 10);
  flip(hourTen, Math.floor(hours / 10));
  flip(hourOne, hours % 10);
  flip(minuteTen, Math.floor(minutes / 10));
  flip(minuteOne, minutes % 10);
  flip(secondTen, Math.floor(seconds / 10));
  flip(secondOne, seconds % 10);
}

function flip(flipCard, newNumber) {
  const topHalf = flipCard.querySelector(".top");
  const startNumber = parseInt(topHalf.textContent);
  if (newNumber === startNumber) return;

  const bottomHalf = flipCard.querySelector(".bottom");
  const topFlip = document.createElement("div");
  topFlip.classList.add("top-flip");
  const bottomFlip = document.createElement("div");
  bottomFlip.classList.add("bottom-flip");

  top.textContent = startNumber;
  bottomHalf.textContent = startNumber;
  topFlip.textContent = startNumber;
  bottomFlip.textContent = newNumber;

  topFlip.addEventListener("animationstart", (e) => {
    topHalf.textContent = newNumber;
  });
  topFlip.addEventListener("animationend", (e) => {
    topFlip.remove();
  });
  bottomFlip.addEventListener("animationend", (e) => {
    bottomHalf.textContent = newNumber;
    bottomFlip.remove();
  });
  flipCard.append(topFlip, bottomFlip);
}
