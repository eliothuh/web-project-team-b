function toggleDropdownStatesVisibility() {
  var x = document.getElementById("dropDownStates");
  var y = document.getElementById("mainContainer");
  if (x.style.display === "none") {
	x.style.display = "flex";
	y.style.marginTop = x.offsetHeight;
  } else {
	x.style.display = "none";
	y.style.marginTop = "-10px";
  }
}
function toggleDropdownYearsVisibility() {
  var x = document.getElementById("dropDownYears");
  var y = document.getElementById("mainContainer");
  if (x.style.display === "none") {
	x.style.display = "flex";
	y.style.marginTop = x.offsetHeight;
  } else {
	x.style.display = "none";
	y.style.marginTop = "-10px";
  }
}