// Get the modal
var modal = document.getElementById('id01');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

function openNav() {
  document.getElementById("mySidepanel").style.width = "39%";
  document.getElementById("mySidepanel").style.height = "100%";
}

function closeNav() {
  document.getElementById("mySidepanel").style.width = "0";
}

