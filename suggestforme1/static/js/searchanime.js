var cat;

  document.getElementById("name").addEventListener("click", function() {
    cat = "name";
    document.getElementById("cat-input").value = cat;  
  });

  document.getElementById("genre").addEventListener("click", function() {
    cat = "genres";
    document.getElementById("cat-input").value = cat;  
  });

  document.getElementById("year").addEventListener("click", function() {
    cat = "year";
    document.getElementById("cat-input").value = cat;  
  });

  document.getElementById("format").addEventListener("click", function() {
    cat = "format";
    document.getElementById("cat-input").value = cat;  
  });

  document.getElementById("status").addEventListener("click", function() {
    cat = "status";
    document.getElementById("cat-input").value = cat;  
  });

const buttons = document.getElementsByClassName('filterbutton');

for (let i = 0; i < buttons.length; i++) {
  buttons[i].addEventListener('click', function() {
    buttons[i].classList.add('clicked'); // Add the 'clicked' class to the clicked button
  });
}