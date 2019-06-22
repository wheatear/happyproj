$(function(){
    $("#getMedia").click(function(){

        var constraints = {
            video: {width: 500, height: 500},
            audio: true
        };
        // 获取媒体方法（旧方法）
        navigator.getMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMeddia || navigator.msGetUserMedia;

        //获得video摄像头区域
        var video = document.getElementById("video");
        //这里介绍新的方法，返回一个 Promise对象
        // 这个Promise对象返回成功后的回调函数带一个 MediaStream 对象作为其参数
        // then()是Promise对象里的方法
        // then()方法是异步执行，当then()前的方法执行完后再执行then()内部的程序
        // 避免数据没有获取到
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            // alert("getmedia new");
            var promise = navigator.mediaDevices.getUserMedia(constraints);
            promise.then(function (MediaStream) {
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

    $("#snap").click(function(){
        //获得Canvas对象
      var video = document.getElementById("video");
      var canvas = document.getElementById("canvas");
      var ctx = canvas.getContext('2d');
      ctx.drawImage(video,0,0,300,300);
    })
});