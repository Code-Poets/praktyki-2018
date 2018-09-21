function cancelFunction() {
  var url = window.location.href;
  var lastPart = url.substr(url.lastIndexOf('/') + 1);

  if (lastPart === "order") {
    window.location.href = path1;
  }
  else {
    window.location.href = path2;
  }
}
