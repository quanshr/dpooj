function about() {
    window.location.href = "./about";
}
function feedback() {
    window.location.href = "./feedback";
}
function login() {
    window.location.href = "./login";
}
function signup() {
    window.location.href = "./signup";
}
function logout() {
    if (confirm("Are you sure?")) {
        var data = {};
        $.ajax({
            url: '/logout',
            type: 'post',
            data: data,
            dataType: 'json',
            success: function (result) {
                window.location.href = "./";
            }
        });
    }
}
// window.onload = function () {
//     if($("#amount")[0].value==""){
//         $("#amount")[0].value="20(标准)"
//     }
// }
// $("#amountInput")[0].onmousedown = function () {
//     $("#amount")[0].value = "";
// }
// $("#amount")[0].onmousedown = function () {
//     $("#amount")[0].value = "";
// }

var upload= async function () {
    var fi = $("#filePath")[0];
    var uploadf = 1;
    // var amount = $("#amount").val().split('(')[0];
    var n = $("#n").val().split('(')[0];
    var m = $("#m").val().split('(')[0];
    var student_count = $("#student_count").val().split('(')[0];
    // if (amount == ""|| parseInt(amount)<1 || parseInt(amount) > 5||isNaN(parseInt(amount))) {
    //     $("#amount")[0].className += " invalid";
    //     $("#amount")[0].value = "请输入[1,5]之间的数";
    //     return;
    // }
    console.log(n);
    if (n == "" || isNaN(parseInt(n)) || parseInt(n) < 1 || parseInt(n) > 100) {
        $("#n")[0].className += " invalid";
        $("#n")[0].value = "请输入[1,100]之间的数";
        return;
    }
    if (m == "" || isNaN(parseInt(m)) || parseInt(m) < 1 || parseInt(m) > 100) {
        $("#m")[0].className += " invalid";
        $("#m")[0].value = "请输入[1,100]之间的数";
        return;
    }
    if (student_count == "" || isNaN(parseInt(student_count)) 
            || parseInt(student_count) < 1 || parseInt(student_count) > 100) {
        $("#student_count")[0].className += " invalid";
        $("#student_count")[0].value = "请输入[1,100]之间的数";
        return;
    }
    var jarfile = $('#jarFile')[0].files[0];
    if (jarfile == undefined&&typeof(isuploaded)=='undefined') {
        fi.className += " invalid";
        fi.value = "文件不能为空！";
        return;
    }
    
    if (uploadf&&typeof(isuploaded)=='undefined') {
        var filename = jarfile.name;
        var expname = filename.split('.');
        expname = expname[expname.length - 1];
        if (expname != "jar" || filename == expname) {
            fi.className += " invalid";
            fi.value = "请上传.jar文件！";
            uploadf = 0;
        }
    }
    if(jarfile == undefined) uploadf=0;
    var formdata = new FormData();
    formdata.append('havefile',uploadf);
    if(uploadf){
        formdata.append('file', jarfile);
        fi.value = "正在上传，请等候";
    } 
    else formdata.append('file', null);
    // formdata.append('amount', amount);
    formdata.append('n', n);
    formdata.append('m', m);
    formdata.append('student_count', student_count);
    // $("#amount")[0].value=$("#amount")[0].value.replace("(参数上传成功！)","");
    await $.ajax({
        url: '/uploader',
        type: 'post',
        contentType: false,
        processData: false,
        data: formdata,
        success: function (data) {
            fi.value = data.info;
            if(data.code=="0"){
                fi.placeholder = "您已上传文件，重新上传会覆盖原文件"
                // $("#amount")[0].value=$("#amount")[0].value.replace("(参数上传成功！)","");
                // $("#amount")[0].value+="(参数上传成功！)";
                $("#canStart")[0].style.display = "block";
                isuploaded=1;
            }
        }
    });
}
$("#submitBtn").on('click',upload);
var started=0;
$("#startBtn").on('click',async function(){
    await upload()
    
    if(started){
        $("#startCallback")[0].innerHTML="评测已开始,请等待评测完成后可再次开始";
        return;
    }
    //console.log("st");
    started=1;
    $("#canUpdate")[0].style.display="block";
    $("#canDownload")[0].style.display = "none";
    $("#startCallback")[0].innerHTML="评测已开始";
    is_start=1;
    $.ajax({
        url: '/start',
        data: {},
        type: 'post',
        success:function(result){
            $("#startCallback")[0].innerHTML = result;
            started=0;
            //console.log("finished");
        },
    });
});

$("#downloadBtn").on('click', function () {
    var data = {}
    $("#downloadCallback")[0].innerHTML = "";
    $.ajax({
        url: '/download',
        data: data,
        type: 'post',
        success: function (result) {
            if (result.code == "0") {
                $("#downloadCallback")[0].innerHTML = "下载成功!";
                let a = document.createElement('a');
                let url = result.path;
                a.href = url;
                a.download = result.filename;
                a.click();
                window.URL.revokeObjectURL(url);
            }
            if (result.code == "1") {
                $("#downloadCallback")[0].innerHTML = "暂无可下载评测信息!";
            }
        },
        error: function (result) {
            console.log("err");
        }
    })
});

$("#updateBtn").on('click', async function () {
    var data = {}
    $("#result")[0].innerHTML="正在查询最新评测结果，请稍后...";
    $.ajax({
        url: '/update',
        data: data,
        type: 'post',
        success: function (result) {
            $("#result")[0].innerHTML = result.info;
            if (result.code == "0") {
                var json_data=JSON.parse(result.info.replace(/'/g, '"'))
                //console.log(json_data)
                $("#result")[0].innerHTML="共"+json_data['all']+"组测试: "
                $("#result")[0].innerHTML+='<span class="green-text">AC</span>: '+json_data['ac']
                $("#result")[0].innerHTML+='&nbsp;&nbsp;<span class="red-text">WA</span>: '+json_data['wa']
                $("#result")[0].innerHTML+='&nbsp;&nbsp;<span class="purple-text">RE</span>: '+json_data['re']
                $("#result")[0].innerHTML+='&nbsp;&nbsp;<span class="blue-text text-darken-3">TLE</span>: '+json_data['tle']
                $("#result")[0].innerHTML+='&nbsp;&nbsp;<span class="blue-grey-text">UKE</span>: '+json_data['uke']
                if (result.is_wrong == "1") {
                    $("#canDownload")[0].style.display = "block";
                }
                else $("#canDownload")[0].style.display = "none";
                if (json_data['is_running'] == "0") {
                    $("#startCallback")[0].innerHTML = "评测结束，再次评测会覆盖上次评测结果";
                    started = 0;
                }
            }
            else $("#canDownload")[0].style.display = "none";
        },
        error: function (result) {
            console.log("err");
        }
    })
});
