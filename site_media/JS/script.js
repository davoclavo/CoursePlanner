/********************** get the mouse coordinates **********************/
// Detect if the browser is IE or not.
// If it is not IE, we assume that the browser is NS.
var IE = document.all?true:false

// If NS -- that is, !IE -- then set up for mouse capture
if (!IE) document.captureEvents(Event.MOUSEMOVE)
document.onmousemove = getMouseXY;

// mouseorary variables to hold mouse x-y pos.s
var mouseX = 0
var mouseY = 0

// Main function to retrieve mouse x-y pos.s

function getMouseXY(e) {
  if (IE) { // grab the x-y pos.s if browser is IE
    mouseX = event.clientX + document.body.scrollLeft
    mouseY = event.clientY + document.body.scrollTop
  } else {  // grab the x-y pos.s if browser is NS
    mouseX = e.pageX + 15
    mouseY = e.pageY + 15
  }  
  // catch possible negative values in NS4
  if (mouseX < 0){mouseX = 0}
  if (mouseY < 0){mouseY = 0}  
}

/********************** hide the frame **********************/
function hide(frame)
 {
 	var height = document.getElementById(frame).style.height
 	if(height == "0px"){
		document.getElementById(frame).style.height = "auto";
 		document.getElementById(frame).style.visibility = "visible";
 	}
	else{
		document.getElementById(frame).style.height = "0px";
 		document.getElementById(frame).style.visibility = "hidden";
	}
 }
 
 // Browser safe opacity handling function

function closeMyPopup() {
 document.getElementById("styled_popup").style.display = "none";
}

function fireMyPopup(title) {
 document.getElementById("styled_popup").style.top = mouseY + "px";
 document.getElementById("styled_popup").style.left = mouseX + "px";
 document.getElementById("styled_popup").style.display = "block";
 document.getElementById("title").value = title;
}

function fireSMSPopup() {
 document.getElementById("sms_popup").style.display = "block";
}

function closeSMSPopup() {
 document.getElementById("sms_popup").style.display = "none";
}

