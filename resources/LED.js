
function toggleLED(img) {
  var id = img.id;
  var state = img.getAttribute("data-state");

  alert(id + state);

  if (state == "off"){
	  img.setAttribute("data-state", "on");
	  img.src =  "LEDOn.png";
  }
  else{
	  img.setAttribute("data-state", "off");
	  img.src= "LEDOff.png";
  }
}

function submitLED(img){
	var id = img.id;
	var state = img.getAttribute("data-state");
	var fmState = document.getElementById("fmState");
	var formID = document.getElementById("toggle");
	
	if (state == "off"){
	  img.setAttribute("data-state", "on");
	  img.src =  "LEDOn.png";
	  fmState.value = "on"
	}
	else{
		img.setAttribute("data-state", "off");
		img.src= "LEDOff.png";
		fmState.value= "off"
		}
	formID.submit();
}


