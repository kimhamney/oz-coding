const todoList = document.getElementById("todo-list");
const todoForm = document.getElementById("todo-form");

let todoArr = [];

function saveTodos() {
  const todoString = JSON.stringify(todoArr);
  localStorage.setItem("myTodos", todoString);
}

function loadTodos() {
  const myTodos = localStorage.getItem("myTodos");
  if (myTodos !== null) {
    todoArr = JSON.parse(myTodos);
    displayTodos();
  }
}
loadTodos();

function handleTodoDelBtnClick(clickedId) {
  todoArr = todoArr.filter(function (aTodo) {
    return aTodo.todoId !== clickedId;
  });
  displayTodos();
  saveTodos();
}

function handleTodoItemClick(clickedId) {
  todoArr = todoArr.map(function (aTodo) {
    if (aTodo.todoId === clickedId) {
      return {
        ...aTodo,
        todoDone: !aTodo.todoDone,
      };
    } else {
      return aTodo;
    }
  });
  displayTodos();
  saveTodos();
}

function displayTodos() {
  todoList.innerHTML = "";
  todoArr.forEach(function (aTodo) {
    const todoItem = document.createElement("li");
    const todoDelBtn = document.createElement("span");
    todoDelBtn.textContent = "x";
    todoItem.textContent = aTodo.todoText;
    todoItem.title = "클릭하면 완료됨";
    todoDelBtn.title = "클릭하면 삭제됨";
    if (aTodo.todoDone) {
      todoItem.classList.add("done");
    } else {
      todoItem.classList.add("yet");
    }
    todoItem.addEventListener("click", function () {
      handleTodoItemClick(aTodo.todoId);
    });
    todoDelBtn.addEventListener("click", function () {
      handleTodoDelBtnClick(aTodo.todoId);
    });
    todoItem.appendChild(todoDelBtn);
    todoList.appendChild(todoItem);
  });
}

todoForm.addEventListener("submit", function (e) {
  e.preventDefault();
  const toBeAdded = {
    todoText: todoForm.todo.value,
    todoId: new Date().getTime(),
    todoDone: false,
  };
  todoForm.todo.value = "";
  todoArr.push(toBeAdded);
  displayTodos();
  saveTodos();
});
