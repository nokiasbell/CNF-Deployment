function getNewContent() {
    var formdata = new FormData(document.getElementById("form-deploy"));
    document.getElementById("form-deploy").submit();
    var request = new XMLHttpRequest();
    if (request) {
        request.open("POST", "/php/cnf_deploy.php", true);
        request.onreadystatechange = function (){
            if (request.readyState==4) {
                window.navigate(location);
            }
        };
        request.send(formdata);
    } else {
        alert("not support");
    }
}
// addLoadEvent(getNewContent);