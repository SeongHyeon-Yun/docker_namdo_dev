function updateWalletCount() {
  fetch("/manage/api/wallet-count/")
    .then((res) => res.json())
    .then((data) => {
      document.getElementById("wallet_count").innerText = data.wallet_count;
    });
}

setInterval(updateWalletCount, 5000);
