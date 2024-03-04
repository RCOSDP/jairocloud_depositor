function closeError() {
    document.getElementById("errors").innerHTML = "";
}
  
function showMsg(msg , success=false) {
    text = '<div class="alert ' + (success? "alert-success":"alert-danger") + ' alert-dismissable" id="alert">' +
    '<button type="button" class="close" data-dismiss="alert" aria-hidden="true" onclick=closeError()>' +
    '&times; </button>' + msg + '</div>';
    document.getElementById("errors").insertAdjacentHTML('afterbegin',text);
        
}

async function componentDidMount() {
/** set errorMessage Area */
    const header = document.getElementsByClassName("content-header")[0];
    if (header) {
        const errorElement = document.createElement('div');
        errorElement.setAttribute('id', 'errors');
        header.insertBefore(errorElement, header.firstChild);
    }
}

function handleAddSubmit(){
    closeError();
    const form ={
        'affiliation_name': document.getElementById("affiliation_name").value,
        'affiliation_idp_url': document.getElementById("affiliation_idp_url").value,
    }
      let pattern = /^(https?|ftp)(:\/\/[\w\/:%#\$&\?\(\)~\.=\+\-]+)/
      if(pattern.test(form.affiliation_idp_url)){
        fetch("/admin_setting/add" ,{method:'POST' ,headers:{'Content-Type':'application/json'} ,credentials:"include", body: JSON.stringify(form)})
        .then(res => {
          if(!res.ok){
            console.log(etext);
        }
          console.log("ok");
          showMsg("Successfully Registered Settings." , true);
        })
        .catch(error => {
          console.log(error);
          showMsg("Failed To Register Settings" , false);
        });
      }else{
        showMsg("Idp URL: Please input in URL format." , false);
      }
}
componentDidMount();