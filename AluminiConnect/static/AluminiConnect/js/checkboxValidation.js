function insertBefore(el, referenceNode) {
    referenceNode.parentNode.insertBefore(el, referenceNode);
  }

  var button = document.getElementById('submit-id-submit');
  button.disabled = true;
  var form = button.parentElement;

  var checkbox1 = document.createElement('div');
  checkbox1.classList.add('form-group');
  checkbox1.innerHTML = '<input class="form-check-input" onclick="cb1f()" type="checkbox" value="" id="form-checkbox1"></input>' +
    '<label class="form-check-labels" for="form-checkbox1">' +
    'I agree to the Terms and Conditions' +
    '</label>'


  var checkbox2 = document.createElement('div');
  checkbox2.classList.add('form-group');

  checkbox2.innerHTML = '<input class="form-check-input" onclick="cb2f()" type="checkbox" value="false" id="form-checkbox2">' +
    '<label class="form-check-labels" for="defaultCheck1">' +
    'I will update my profile' +
    '</label>'

  insertBefore(checkbox1, button);
  insertBefore(checkbox2, button);
  
  let cb1checked = false;
  let cb2checked = false;


  function updateButton(){
    if(cb1checked && cb2checked){
      button.disabled = false;
    }
    else{
      button.disabled = true;
    }
  }

  function cb1f(){
    var chkPassport = document.getElementById("form-checkbox1");
        if (chkPassport.checked) {
          cb1checked = true;
        } else {
          cb1checked = false;
        }
        updateButton();
  }

  function cb2f(){
    var chkPassport = document.getElementById("form-checkbox2");
        if (chkPassport.checked) {
          cb2checked = true;
        } else {
          cb2checked = false;
        }
        updateButton();
  }