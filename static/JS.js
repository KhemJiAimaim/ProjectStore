document.addEventListener("keypress", function(e) {
    if (e.target.tagName !== "INPUT") {
      var input = document.querySelector(".my-input");
      input.focus();
      input.value = e.key;
      e.preventDefault();
    }
  });

  