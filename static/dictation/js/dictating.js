
var aWords=[];
var aPlayList=[];
var sPlayList='[';
var player;
var indx=0;
var playState=1;   //0: paused   1:playing   2:stop
var repeat=0;
<<<<<<< HEAD
var hWords;
=======
>>>>>>> aa6d4ef93ff8a8685cdc22698230e47973a66b44
$(function(){
    $.get('/dictation/qryVoice/', function(dic){
		aWords = dic.words;
		alert(aWords);
		hWords = $('#words');
		makePlayList(aWords,hWords);
		alert(aPlayList);
		playerSet(player,aPlayList)
    });
    player = cyberplayer("playercontainer");
    //player set
<<<<<<< HEAD
    function playerSet(ply, list) {
        ply.setup({
                width: 300,   //680, // 宽度，也可以支持百分比(不过父元素宽度要有)
                height: 80,  //448, // 高度，也可以支持百分比
=======
    player = cyberplayer("playercontainer").setup({
                width: 20,   //680, // 宽度，也可以支持百分比(不过父元素宽度要有)
                height: 20,  //448, // 高度，也可以支持百分比
>>>>>>> aa6d4ef93ff8a8685cdc22698230e47973a66b44
                title: "开心听写", // 标题
                //file: "/static/dictation/voice/4e5e6c42_05212.mp3", // 播放地址
                //file: "/static/dictation/voice/4e0058f04e0d54cd_05212.mp3", // 播放地址
                //播放列表
                // playlist: [{sources: [{file: "/static/dictation/voice/6ee160004fe15fc3_05212.mp3"}],},
                //     {sources: [{file: "/static/dictation/voice/7acb523b_05212.mp3"}],},
                //     {sources: [{file: "/static/dictation/voice/8b66544a_05212.mp3"}],},
                //     {sources: [{file: "/static/dictation/voice/8d5e626c_05212.mp3"}],},
                //     {sources: [{file: "/static/dictation/voice/81ea8c6a_05212.mp3"}],},
                //     ],
<<<<<<< HEAD
                playlist: list,
                // playlist: aPlayList,
=======
                playlist: aPlayList,
>>>>>>> aa6d4ef93ff8a8685cdc22698230e47973a66b44
                // playlist: sPlayList,
                //image: "http://gcqq450f71eywn6bv7u.exp.bcevod.com/mda-hbqagik5sfq1jsai/mda-hbqagik5sfq1jsai.jpg", // 预览图
                autostart: false, // 是否自动播放
                // stretching: "uniform", // 拉伸设置
                repeat: false, // 是否重复播放 true false
                volume: 100, // 音量
                controls: false, // controlbar是否显示 true   false
                starttime: 0, // 视频开始播放时间点(单位s)，如果不设置，则可以从上次播放时间点续播
                // logo: { // logo设置
                //     linktarget: "_blank",
                //     margin: 8,
                //     hide: false,
                //     position: "top-right", // 位置
                //     file: "./img/logo.png" // 图片地址
                // },
                // ak: "xxxxxxxxxxxxxxxx" // 公有云平台注册即可获得accessKey
        });
    }

    function makePlayList(aWords){
    // hWords.empty();
        var i = 0;
        $.each(aWords, function(i,aWd) {
            i++;
            var code = aWd[0];          //word id
            var word = aWd[1];          //word
            var pinyin = aWd[2];        //pinyin
            var voicefile = aWd[3];     //voice file
            var dispName = pinyin;
            var voiceFile =  '/static/dictation/voice/' + voicefile ;
            aPlayList.push({sources: [{file: voiceFile}],});
        //     }
        // hWords.append('<label class="word un" code='+code+'>'+dispName+'</label>');
        // if(i > 5){
        //     return
        // }
        });
    }

    $('.word').click(function(){
        // $(this).attr({'code':1});
        alert($(this).attr('code'));
        $(this).toggleClass("se");
    });

    $('#toPlay').click(function(){
        player.play();
        // len = aPlayList.length;
        // alert(len)
        // hWords = $('#words');
        // for(indx;indx<5;indx++) {
        //     var i = indx;
        //     var item = player.playlistItem(i);
        //     // player.playlistNext();
        //     wd = aWords[i];
        //     alert(i+wd[1]);
        //     alert(aPlayList[i].sources[0].file);
        //     code = wd[0];
        //     dispName = wd[2];
        //     hWords.append('<label class="word un" code='+code+'>'+dispName+'</label>');
        //     // $('.word').click(function(){
        //     //     $(this).toggleClass("se");
        //     // });
        //     sleep(10000);
        //     // player.playlistItem(i);
        // }
        // indx = 0;
            // var item = player.playlistItem(2);
            //player.stop()
            //player.playlistNext();
    });

    function sleep(n) {
        var start = new Date().getTime();
        //  console.log('休眠前：' + start);
        while (true) {
            if (new Date().getTime() - start > n) {
                break;
            }
        }
<<<<<<< HEAD
=======
        // console.log('休眠后：' + new Date().getTime());
>>>>>>> aa6d4ef93ff8a8685cdc22698230e47973a66b44
    }

    $('#nextWord').click(function(){
        // indx++;
        player.playlistNext()
            //player.stop()
            //player.playlistNext();
    });

    $('#prevWord').click(function(){
        // indx--;
<<<<<<< HEAD
        player.playlistPrev()
        // hWords = $('#words');
        // var i = indx;
        //     var item = player.playlistItem(i);
        //     // player.playlistNext();
        //     wd = aWords[i];
        //     alert(i+wd[1]);
        //     alert(aPlayList[i].sources[0].file);
        //     code = wd[0];
        //     dispName = wd[2];
        //     hWords.append('<label class="word un" code='+code+'>'+dispName+'</label>');
        //     indx++;
=======
        // player.playlistPrev()
        hWords = $('#words');
        var i = indx;
            var item = player.playlistItem(i);
            // player.playlistNext();
            wd = aWords[i];
            alert(i+wd[1]);
            alert(aPlayList[i].sources[0].file);
            code = wd[0];
            dispName = wd[2];
            hWords.append('<label class="word un" code='+code+'>'+dispName+'</label>');
            indx++;
>>>>>>> aa6d4ef93ff8a8685cdc22698230e47973a66b44
            //player.stop()
            //player.playlistNext();
    });

    $('#pause').click(function(){
        // var state = myPlayer.getState(); //state：{“playing”,“paused”,“idle”,“buffering”}
        if(playState==0) {
            playState = 1;
        } else if(playState==1) {
            playState = 0;
        }
    });

    $('#stop').click(function(){
        // playState = 2;
            player.stop()
            //player.playlistNext();
    });

    player.onComplete(function(event){
        sleep(2000);
        if (repeat == 0) {
            repeat = 1;
<<<<<<< HEAD
            var i = player.getPlaylistIndex();
            player.playlistItem(i)
        } else {
            repeat = 0;
        }
    });

    player.onPlay(function(event){
        // alert(repeat )
        if(repeat==0 ) {
            var i = player.getPlaylistIndex();
            var word = aWords[i];
            alert(i+wd[1]);
            // alert(aPlayList[i].sources[0].file);
            code = wd[0];
            dispName = wd[2];
            hWords.append('<label class="word un" code='+code+'>'+dispName+'</label>');
        }
    })

    // player.onPlaylistItem(function(event){
    //             //alert("onPlaylistItem");
    //            // player.stop()
    //     sleep(2000);
    //     if(repeat==0) {
    //         repeat=1;
    //         player.playlistPrev();
    //     } else {
    //         repeat=0;
    //     }
    // });
});


=======
            var playlistIndex = player.getPlaylistIndex();
            player.playlistItem(playlistIndex)
        } else {
            repeat = 0;
        }
    })

    // player.onPlay(function(event){
    //     // alert(repeat )
    //     if(repeat==0 ) {
    //         repeat=1;
    //     } else if(repeat==1){
    //         repeat=2;
    //         player.playlistPrev();
    //     } else if(repeat==2){
    //         repeat=0;
    //     }
    //
    // })

    // player.onPlaylistItem(function(event){
    //             //alert("onPlaylistItem");
    //            // player.stop()
    //     sleep(2000);
    //     if(repeat==0) {
    //         repeat=1;
    //         player.playlistPrev();
    //     } else {
    //         repeat=0;
    //     }
    // });
});

function makePlayList(aWords){
    // hWords.empty();
    var i = 0;
    $.each(aWords, function(i,aWd) {
        i++;
        var code = aWd[0];          //word id
        var word = aWd[1];          //word
        var pinyin = aWd[2];        //pinyin
        var voicefile = aWd[3];     //voice file
        var dispName = pinyin;
        // var voiceFile = '"' + '/static/dictation/voice/' + voicefile + '"';
        var voiceFile =  '/static/dictation/voice/' + voicefile ;
        if (i < 5) {
            var dfile = {file:voiceFile};
            var afile = [dfile];
            var dsour = {sources: afile,}
            aPlayList.push(dsour);
        // aPlayList.push({sources: [{file: voiceFile}],});
        // sPlayList += ('{sources: [{file: ' + voiceFile + '}],},');
        }
        // hWords.append('<label class="word un" code='+code+'>'+dispName+'</label>');
        // if(i > 5){
        //     return
        // }
    });
    sPlayList += ']';
    // alert(sPlayList)
}
>>>>>>> aa6d4ef93ff8a8685cdc22698230e47973a66b44
