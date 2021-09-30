window.onload = function() {
  var c = document.getElementById('dateSel')
  c.onchange = function() {
    if (c.checked == true) {document.getElementById('cdate').style.display = 'inline';}
    else {document.getElementById('cdate').style.display = '';
    }
  }
}