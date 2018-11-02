
var aWords=[];
var aPlayList=[];
var player;
var indx=0;
var playState=1;   //0: paused   1:playing   2:stop
var repeat=0;
var wordNum=2;
var hWords;

$(function(){
    $.get('/dictation/qryVoice/', function(dic){
        aWords = dic.words;
        // alert(aWords);
        hWords = $('#words');
        makePlayList(aWords,hWords);
        // alert(aPlayList);
        playerSet(player,aPlayList);
    });
    player = cyberplayer("playercontainer");
    //player set
    function playerSet(ply, list) {
        ply.setup({
            width: 0,   //680, // 宽度，也可以支持百分比(不过父元素宽度要有)
            height: 0,  //448, // 高度，也可以支持百分比

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

            playlist: aPlayList,

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
            ak: "a0dbd2b027ee45c0b6bfdf548e519727" // 公有云平台注册即可获得accessKey
        });

        ply.onComplete(function(event){
            slpTime=3000*wordNum;
            sleep(slpTime);
            // ply.pause();
            // setTimeout("playGo()",2000);
            if (repeat == 0) {
                repeat = 1;
                var i = ply.getPlaylistIndex();
                ply.playlistItem(i);
            } else {
                repeat = 0;
            }
        });

        function playGo(){
            if (repeat == 0) {
                repeat = 1;
                var i = player.getPlaylistIndex();
                player.playlistItem(i);
            } else {
                repeat = 0;
                player.play();
            }
        }

        ply.onPlay(function(event){
            // alert('play...' );
            // alert('playing...')
            if(repeat==0 ) {
                var i = ply.getPlaylistIndex();
                var word = aWords[i];
                code = word[0];
                pinyin = word[2];
                dispName = pinyin.join(' ');
                wordNum=pinyin.length;
                hWords.append('<label class="word un" code='+code+'>'+dispName+'</label>');
                // $('#pinyin').innerHTML=dispName;
            }
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
        // alert($(this).attr('code'));
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
    }

    $('#nextWord').click(function(){
        // indx++;
        player.playlistNext()
        //player.stop()
        //player.playlistNext();
    });

    $('#prevWord').click(function(){
        // indx--;
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

        //player.stop()
        //player.playlistNext();
    });

    $('#pause').click(function(){
        var state = player.getState(); //state：{“playing”,“paused”,“idle”,“buffering”}
        if(state=='playing') {
            player.pause();
        } else if(state=='paused') {
            player.play();
        }
    });

    $('#stop').click(function(){
        // playState = 2;
        player.stop()
        //player.playlistNext();
    });

    $('#next').click(function(){
        window.location.href = '/dictation/checkwords/'
    });

    // player.onPlaylistItem(function(event){
    //             //alert("onPlaylistItem");
    //            // player.stop()
    //     sleep(2000);
    //     alert('play one')
    //     // if(repeat==0) {
    //     //     repeat=1;
    //     //     player.playlistPrev();
    //     // } else {
    //     //     repeat=0;
    //     // }
    // });
});




