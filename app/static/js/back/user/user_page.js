const all_check = document.getElementById("all_check");
const check_input = document.querySelectorAll(".check_input");

all_check.addEventListener("change", function () {
  if (all_check.checked) {
    check_input.forEach((btn) => {
      btn.checked = true;
    });
  } else {
    check_input.forEach((btn) => {
      btn.checked = false;
    });
  }
});
