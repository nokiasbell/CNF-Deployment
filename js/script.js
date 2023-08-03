function close_dialog() {
    var para = document.getElementById("dialog-wrapper");
    para.style.display = "none";
}
function open_dialog() {
    var para = document.getElementById("dialog-wrapper");
    para.style.display = "block";
}
// function open_sidebar(){
//     var para1 = document.getElementById("sidebar-wrapper");
//     if (para1.style.display == "block") {
//         para1.style.display = "none";
//         para1.setAttribute("data-test","close")
//         // var para2 = document.getElementById("sidebar");
//         // para2.style.transform = "translate(0, -500%)";
//         // para2.style.right = "100%";
//     }else{
//         para1.style.display = "block";
//         para1.setAttribute("data-test","open")
//         // var para2 = document.getElementById("sidebar");
//         // para2.style.transform = "translate(0, 0)";
//         // para2.style.right = "80%";
//     }
// }
function open_sidebar(){
    var para1 = document.getElementById("sidebar-wrapper");
    if (para1.style.display == "block") {
        para1.style.display = "none";
    }else{
        para1.style.display = "block";
    }
}

function hide_workbench_modify() {
    var para = document.getElementById("workbench-modify");
    para.style.display = "none";
}
function display_workbench_modify() {
    var para = document.getElementById("workbench-modify");
    para.style.display = "block";
}

function display_workbench_deployment() {
    var para = document.getElementById("workbench-deploy");
    para.style.display = "block";
}