const amount = document.getElementById("amount");

amount.addEventListener("input", comma_number);
amount.addEventListener("input", no_korea);
amount.addEventListener("input", noEnglish);

function comma_number(e) {
  let value = e.target.value.replace(/,/g, ""); // 기존 콤마 제거
  value = Number(value).toLocaleString(); // 콤마 추가
  e.target.value = value;
}

// 한글 입력 방지
function no_korea(e) {
  e.target.value = e.target.value.replace(/[ㄱ-ㅎㅏ-ㅣ가-힣]/g, "");
}

// 영어입력 방지
function noEnglish(e) {
  e.target.value = e.target.value.replace(/[a-zA-Z]/g, "");
}
