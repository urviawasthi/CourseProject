
window.onload = init;

  function init() {
    // the code to be called when the dom has loaded
    var link = document.getElementById('to-change-link-of');
    var lecture = localStorage.getItem('lecture_number')
    const myArray = lecture.split(" ");

    console.log(myArray);
    var link_part = "";
    
    var arrayLength = myArray.length;
    first = true
    for (var i = 0; i < arrayLength; i++) {
        if (myArray[i] == "-" && first == false) {
            link_part += myArray[i] + "+"
        } else if (myArray[i] == "-" && first == true) {
            first = false
        } else if (myArray[i] != "-") {
            link_part += myArray[i] + "+"
        }
    }

    link_part = link_part.slice(0, -1);
    link_part += ".mp4"

    console.log(link_part);

    link.setAttribute("src", `https://s3.us-east-2.amazonaws.com/smartmoocs.illinois.edu/textretrieval/${link_part}`);
  
  }