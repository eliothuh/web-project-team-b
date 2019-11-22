function toggleDropdownStatesVisibility() {
  var x = document.getElementById("dropDownStates");
  var y = document.getElementById("dropDownYears");
  if (x.style.display === "none") {
	x.style.display = "flex";
	y.style.display = "none";
  } else {
	x.style.display = "none";
  }
}

function turnOffAllCollapsibles() {
	var y = document.getElementById("dropDownStates");
	var x = document.getElementById("dropDownYears");
	x.style.display="none";
	y.style.display="none";
}

function toggleDropdownYearsVisibility() {
  var y = document.getElementById("dropDownStates");
  var x = document.getElementById("dropDownYears");
  if (x.style.display === "none") {
	x.style.display = "flex";
	y.style.display = "none";
  } else {
	x.style.display = "none";
  }
}

toggleDropdownStatesVisibility()	
turnOffAllCollapsibles()
toggleDropdownYearsVisibility()