const user_id = document.getElementById("id");
const phone = document.getElementById("phone");
const boss_name = document.getElementById("boss_name");
const email = document.getElementById("email");
const company_num = document.getElementById("company_num");
const bank_num = document.getElementById("bank_num");

// 한글 입력 방지
function no_korea(e) {
  e.target.value = e.target.value.replace(/[ㄱ-ㅎㅏ-ㅣ가-힣]/g, "");
}

// 하이폰 입력 방지
function noHyphen(e) {
  e.target.value = e.target.value.replace(/-/g, "");
}

// 영어입력 방지
function noEnglish(e) {
  e.target.value = e.target.value.replace(/[a-zA-Z]/g, "");
}

user_id.addEventListener("input", no_korea);
phone.addEventListener("input", noHyphen);
phone.addEventListener("input", no_korea);
phone.addEventListener("input", noEnglish);
boss_name.addEventListener("input", noEnglish);
email.addEventListener("input", no_korea);
company_num.addEventListener("input", no_korea);
company_num.addEventListener("input", noEnglish);
company_num.addEventListener("input", noHyphen);
bank_num.addEventListener("input", no_korea);
bank_num.addEventListener("input", noEnglish);
bank_num.addEventListener("input", noHyphen);
