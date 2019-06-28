var $getCamera,
    mediaStreamTrack,
    front = false,
    video,
    canvas,
    hwFile,
    hwResult,
    promise;

$(function(){
    $("#getMedia").click(function(){
        $getCamera = $("#getCamera");
        $getCamera.show();

        canvas = document.getElementById("canvas");
        video = document.getElementById("video");

        var constraints = {
            video: { facingMode: (front? "user" : "environment"),
            width: 300, height: 300},
            audio: false
        };
        // var constraintsComm = {
        //     video: { width: 300, height: 300},
        //     audio: false
        // };
        var constraintsComm = {
            video: true,
            audio: false
        };
        // alert("300,300");

        // 获取媒体方法（旧方法）
        navigator.getMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMeddia || navigator.msGetUserMedia;

        //获得video摄像头区域
        video = document.getElementById("video");
        //这里介绍新的方法，返回一个 Promise对象
        // 这个Promise对象返回成功后的回调函数带一个 MediaStream 对象作为其参数
        // then()是Promise对象里的方法
        // then()方法是异步执行，当then()前的方法执行完后再执行then()内部的程序
        // 避免数据没有获取到
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            // alert("getmedia new");
            promise = navigator.mediaDevices.getUserMedia(constraints);
            promise.then(function (MediaStream) {
                mediaStreamTrack = typeof MediaStream.stop === 'function' ? MediaStream : MediaStream.getTracks()[0];
                console.log(mediaStreamTrack);
                video.srcObject = MediaStream;
                video.play();
            });
        }else if (navigator.getMedia) {
            // alert("getmedia old");
            navigator.getMedia({
                video: true
            }, function(stream) {
                mediaStreamTrack = stream.getTracks()[0];

                video.src = (window.URL || window.webkitURL).createObjectURL(stream);
                video.play();
            }, function(err) {
                console.log(err);
            });
        }
    });

    function uploadMathImg(next){
        dMath = {homework: canvas.toDataURL('image/png')};
        $.ajax({
            url: "/mathcorrection/uploadMath",
            type: "POST",
            data: dMath
        }).done(function(rs){
            hwFile = rs.mathFile;
            if (next){
                next();
            } else {
                alert("上传作业成功。");
            }
        }).fail(function(){
            alert("上传作业失败。")
        })
    }

    function correct(){
        $.ajax({
            url: "/mathcorrection/correct/",
            type: "POST",
            data: {hwImg: hwFile}
        }).done(function(rs){
            hwResult = rs.mathCorrection;
            // alert("mark result: "+hwResult);
            markResult(hwResult);
            // alert("作业批改成功。")
        }).fail(function(){
            alert("作业批改失败。")
        })
    }

    function markResult(hw){
        items = hw["Items"];
        var res = "\2713";
        // alert("mark items" + items);
        ctx = canvas.getContext("2d");
        var x,y,w,h;
        var itemNum = errNum = 0;
        $.each(items, function(i, n){
            itemNum++;
            // alert(n);
            res = "\2713";

            x = n["ItemCoord"]["X"];
            y = n["ItemCoord"]["Y"];
            w = n["ItemCoord"]["Width"];
            h = n["ItemCoord"]["Height"];
            if (n["Item"] === "NO") {
                res = "\2717";
                errNum++;
                ctx.fillStyle = "rgb(200,0,0,0.5)";
                ctx.fillRect (x, y, w, h);
            }

            // alert("markresult: "+res +"("+x+","+y+")");
            // ctx.fillText(res, x, y)
        });
        if (errNum === 0){
            alert(itemNum + "题全部正确！")
        }else{
            alert("共"+itemNum + "题，错"+ errNum + "题！")
        }
    }

    $("#save").click(uploadMathImg);

    // 作业批改
    $("#correct").click(function(){
        // alert("correct math homework");
        // alert(hwFile);
        // hwFile = "mathImg_20190627064622";
        if(!hwFile){
            // alert("upload img");
            uploadMathImg(correct);
        } else{
            correct();
        }

    });

    $("#answerBtn").click(function(){
        items = hwResult["Items"];

        ctx = canvas.getContext("2d");
        var sAnswer="";
        $.each(items, function(i, n){
            // alert(n["Item"]);
            if (n["Item"] === "NO") {
                sAnswer += n["Answer"]+"<br>";
            }else{
                sAnswer += n["ItemString"]+"<br>";
            }
        });
        // alert(sAnswer);
        $("#answerDiv").html(sAnswer)
    });

    $("#snap").click(function(){
        $getCamera.hide();

        //获得Canvas对象
        // var video = document.getElementById("video");

        // var canvas = document.getElementById("canvas");
        var ctx = canvas.getContext('2d');
        ctx.drawImage(video,0,0,300,300);
        hwFile = null;

        // close camera
        mediaStreamTrack && mediaStreamTrack.stop();
    });

    $("#switch").click(function(){
        front = !front;
        var constraints = {
            video: { facingMode: (front? "user" : "environment"),
            width: 300, height: 300},
            audio: false
        };

        mediaStreamTrack && mediaStreamTrack.stop();
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            // alert("getmedia new");
            promise = navigator.mediaDevices.getUserMedia(constraints);
            promise.then(function (MediaStream) {
                mediaStreamTrack = typeof MediaStream.stop === 'function' ? MediaStream : MediaStream.getTracks()[0];
                console.log(mediaStreamTrack);
                video.srcObject = MediaStream;
                video.play();
            });
        }else if (navigator.getMedia) {
            // alert("getmedia old");
            navigator.getMedia({
                video: true
            }, function(stream) {
                mediaStreamTrack = stream.getTracks()[0];

                video.src = (window.URL || window.webkitURL).createObjectURL(stream);
                video.play();
            }, function(err) {
                console.log(err);
            });
        }

    });

    $("#exit").click(function(){
        $getCamera.hide();
        // close camera
        mediaStreamTrack && mediaStreamTrack.stop();
    });

    $("#disPop").click(function(){
        $getCamera.show();
    })

});