const apiRandomDogs = "https://dog.ceo/api/breeds/image/random/20";
const apiAllBreeds = "https://dog.ceo/api/breeds/list/all";
const request1 = new XMLHttpRequest();
const request2 = new XMLHttpRequest();

const header = document.getElementById("header");
const main = document.getElementById("main");
const input = document.getElementById("filter-text");
const button = document.getElementById("filter-button");
const select = document.getElementById("filter-select");
const more = document.getElementById("more");
const tothetop = document.getElementById("tothetop");
const reset = document.getElementById("reset");

let currentDogs = [];

function setDogs(list) {
  list.forEach(function (item) {
    currentDogs.push(item);
    displayDogs(item);
  });
}

function displayDogs(item) {
  const dogImgDiv = document.createElement("div");
  dogImgDiv.classList.add("flex-item");
  dogImgDiv.innerHTML = `<img src=${item}>`;
  main.appendChild(dogImgDiv);
}

window.addEventListener("load", function () {
  // add dog img list
  request1.open("get", apiRandomDogs);
  request1.onload = function () {
    const response = JSON.parse(request1.response);
    setDogs(response.message);
  };
  request1.send();

  // add select list
  request2.open("get", apiAllBreeds);
  request2.onload = function () {
    const response = JSON.parse(request2.response);
    Object.keys(response.message).forEach(function (item) {
      const option = document.createElement("option");
      option.textContent = item;
      option.value = item;
      select.appendChild(option);
    });
  };
  request2.send();
});

button.addEventListener("click", function () {
  main.innerHTML = "";
  input.value = "";

  let filteredDogs = currentDogs.filter(function (item) {
    return item.indexOf(input.value) !== -1;
  });

  filteredDogs.forEach(function (item) {
    displayDogs(item);
  });
});

select.addEventListener("change", function () {
  main.innerHTML = "";
  let filteredDogs = currentDogs.filter(function (item) {
    return item.indexOf(select.value) !== -1;
  });

  filteredDogs.forEach(function (item) {
    displayDogs(item);
  });
});

more.addEventListener("click", function () {
  request1.open("get", apiRandomDogs);
  request1.onload = function () {
    const response = JSON.parse(request1.response);
    setDogs(response.message);
  };
  request1.send();
});

tothetop.addEventListener("click", function () {
  window.scrollTo({ top: 0 });
});

reset.addEventListener("click", function () {
  main.innerHTML = "";
  currentDogs = [];

  request1.open("get", apiRandomDogs);
  request1.onload = function () {
    const response = JSON.parse(request1.response);
    setDogs(response.message);
  };
  request1.send();
});
