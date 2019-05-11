function dummyScript() {
  console.log('dummy')
}

document.onreadystatechange = function() {
  if (document.readyState == "interactive") {
    dummyScript()
  }
}
