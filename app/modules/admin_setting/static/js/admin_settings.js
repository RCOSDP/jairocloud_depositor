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


function handleSelect(){
  closeError();
  const aff_repository_dict = document.getElementById("aff_repository_dict").value;
  const aff_repository_info = JSON.parse(aff_repository_dict);
  const affiliation_name_id = document.getElementById("affiliation_name").value;
  const repogitory_url = document.getElementById("repository_url");
  const access_token = document.getElementById("access_token");
  if(affiliation_name_id in aff_repository_info){
    repogitory_url.value = aff_repository_info[affiliation_name_id]["repository_url"];
    access_token.value = aff_repository_info[affiliation_name_id]["access_token"];
  }else{
    repogitory_url.value = "";
    access_token.value = "";
  }
}

function handleAffiliSubmit(){
    closeError();
    const form ={
        'affiliation_name': document.getElementById("affiliation_name").value,
        'repository_url': document.getElementById("repository_url").value,
        'access_token': document.getElementById("access_token").value
    }
      let pattern = /^(https?|ftp)(:\/\/[\w\/:%#\$&\?\(\)~\.=\+\-]+)/
      if(pattern.test(form.repository_url)){
        fetch("/admin_setting/" ,{method:'POST' ,headers:{'Content-Type':'application/json'} ,credentials:"include", body: JSON.stringify(form)})
        .then(res => {
          if(!res.ok){
            console.log(etext);
        }
          console.log("ok");
          showMsg("Successfully Changed Settings." , true);
        })
        .catch(error => {
          console.log(error);
          showMsg("Failed To Change Settings" , false);
        });
      }else{
        showMsg("登録先URL: Please input in URL format." , false);
      }
}
componentDidMount();