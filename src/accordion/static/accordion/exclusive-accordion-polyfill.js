document.querySelectorAll("details[name]").forEach(($details) => {
  $details.addEventListener("toggle", (e) => {
    const name = $details.getAttribute("name");

    if (e.newState == "open") {
      document
        .querySelectorAll(`details[name=${name}][open]`)
        .forEach(($openDetails) => {
          if (!($openDetails === $details)) {
            $openDetails.removeAttribute("open");
          }
        });
    }
  });
});

