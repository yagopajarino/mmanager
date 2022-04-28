function myFunction() {
    var x = document.getElementById("myTopnav");
    if (x.className === "hd-container topnav") {
      x.className += " responsive";
    } else {
      x.className = "hd-container topnav";
    }
  }