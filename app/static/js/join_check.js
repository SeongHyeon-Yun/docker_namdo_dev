const allCheck = document.getElementById("all_check");
const checks = document.querySelectorAll("#check_1, #check_2");
const nextBtn = document.getElementById("next_btn");

/* 전체 동의 */
allCheck.addEventListener("change", function () {
  checks.forEach(function (check) {
    check.checked = allCheck.checked;
  });
});

/* 개별 체크하면 전체 동의 자동 반영 */
checks.forEach(function (check) {
  check.addEventListener("change", function () {
    allCheck.checked = [...checks].every((c) => c.checked);
  });
});

/* 다음 버튼 */
nextBtn.addEventListener("click", function () {
  if (!allCheck.checked) {
    alert("약관에 모두 동의해야 회원가입이 가능합니다.");
    return;
  }

  // 동의했으면 이동
  window.location.href = "/join"; // 원하는 페이지로 변경
});
