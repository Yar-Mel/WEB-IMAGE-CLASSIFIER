var modal = document.getElementById("upload-dialog");
var start_btn = document.getElementById("start-btn");
var close_btn = document.getElementById("close-btn");
var cancel_btn = document.getElementById("cancel-btn");

start_btn.onclick = function() {
  modal.style.display = "block";
}

close_btn.onclick = function() {
  modal.style.display = "none";
}

cancel_btn.onclick = function() {
  modal.style.display = "none";
}

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}