document.addEventListener('DOMContentLoaded', function() {
  const inputField1 = document.querySelector('#input-field-1');
  const inputField2 = document.querySelector('#input-field-2');
  const buttons = document.querySelectorAll('.key');
  const deleteBtn = document.querySelector('#dl');
  const spaceBtn = document.querySelector('#sp');
  const atBtn = document.querySelector('#at');
  const shiftBtn = document.querySelector('#up');
  let shift = false;

  buttons.forEach(button => {
    button.addEventListener('click', function() {
      if (inputField1.focused) {
        inputField1.value += this.innerHTML;
      } else if (inputField2.focused) {
        inputField2.value += this.innerHTML;
      }
    });
  });

  deleteBtn.addEventListener('click', function() {
    if (inputField1.focused) {
      inputField1.value = inputField1.value.substring(0, inputField1.value.length - 1);
    } else if (inputField2.focused) {
      inputField2.value = inputField2.value.substring(0, inputField2.value.length - 1);
    }
  });

  spaceBtn.addEventListener('click', function() {
    if (inputField1.focused) {
      inputField1.value += ' ';
    } else if (inputField2.focused) {
      inputField2.value += ' ';
    }
  });

  atBtn.addEventListener('click', function() {
    let focusedInputField;
    if (inputField1.matches(':focus')) {
      focusedInputField = inputField1;
    } else if (inputField2.matches(':focus')) {
      focusedInputField = inputField2;
    }
  
    if (focusedInputField) {
      focusedInputField.value += '@';
    }
  });
  

  shiftBtn.addEventListener('click', function() {
    shift = !shift;
    if (shift) {
      buttons.forEach(button => {
        button.innerHTML = button.innerHTML.toUpperCase();
      });
    } else {
      buttons.forEach(button => {
        button.innerHTML = button.innerHTML.toLowerCase();
      });
    }
  });

  inputField1.addEventListener('focus', function() {
    inputField2.focused = false;
    inputField1.focused = true;
  });

  inputField2.addEventListener('focus', function() {
    inputField1.focused = false;
    inputField2.focused = true;
  });
});

const button = document.getElementById("up");
const icon = document.getElementById("icon");

button.addEventListener("click", function() {
  if (icon.style.backgroundImage === "url(${assets/stroke.png})") {
    icon.style.backgroundImage = "url(${assets/full.png})";
  } else {
    icon.style.backgroundImage = "url(${assets/stroke.png})";
  }
});
