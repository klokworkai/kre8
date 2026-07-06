const outputBox = document.getElementById("output-box");
const btnClose = document.getElementById("btn-close");

btnClose.addEventListener("click", async () => {
  btnClose.disabled = true;
  try {
    await fetch("/shutdown", { method: "POST" });
  } catch (err) {
    // server closes the connection as part of shutdown — expected
  }
  outputBox.textContent = "kiosk stopped, you can close this tab";
  document.getElementById("intent-input").disabled = true;
  document.getElementById("btn-design").disabled = true;
  document.getElementById("btn-konnekt").disabled = true;
});
