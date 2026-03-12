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

const addree_1 = document.getElementById("addree_1");
const addree_2 = document.getElementById("addree_2");
const addree_3 = document.getElementById("addree_3");
const addree_4 = document.getElementById("addree_4");

function open_post() {
  new kakao.Postcode({
    oncomplete: function (data) {
      // 팝업에서 검색결과 항목을 클릭했을때 실행할 코드를 작성하는 부분.

      // 각 주소의 노출 규칙에 따라 주소를 조합한다.
      // 내려오는 변수가 값이 없는 경우엔 공백('')값을 가지므로, 이를 참고하여 분기 한다.
      var addr = ""; // 주소 변수
      var extraAddr = ""; // 참고항목 변수

      //사용자가 선택한 주소 타입에 따라 해당 주소 값을 가져온다.
      if (data.userSelectedType === "R") {
        // 사용자가 도로명 주소를 선택했을 경우
        addr = data.roadAddress;
      } else {
        // 사용자가 지번 주소를 선택했을 경우(J)
        addr = data.jibunAddress;
      }

      // 사용자가 선택한 주소가 도로명 타입일때 참고항목을 조합한다.
      if (data.userSelectedType === "R") {
        // 법정동명이 있을 경우 추가한다. (법정리는 제외)
        // 법정동의 경우 마지막 문자가 "동/로/가"로 끝난다.
        if (data.bname !== "" && /[동|로|가]$/g.test(data.bname)) {
          extraAddr += data.bname;
        }
        // 건물명이 있고, 공동주택일 경우 추가한다.
        if (data.buildingName !== "" && data.apartment === "Y") {
          extraAddr +=
            extraAddr !== "" ? ", " + data.buildingName : data.buildingName;
        }
        // 표시할 참고항목이 있을 경우, 괄호까지 추가한 최종 문자열을 만든다.
        if (extraAddr !== "") {
          extraAddr = " (" + extraAddr + ")";
        }
        // 조합된 참고항목을 해당 필드에 넣는다.
        document.getElementById("addree_4").value = extraAddr;
      } else {
        document.getElementById("addree_4").value = "";
      }

      // 우편번호와 주소 정보를 해당 필드에 넣는다.
      document.getElementById("addree_1").value = data.zonecode;
      document.getElementById("addree_2").value = addr;
      // 커서를 상세주소 필드로 이동한다.
      document.getElementById("addree_3").focus();
    },
  }).open();
}
