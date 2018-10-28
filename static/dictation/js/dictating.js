
var aWords=[];
var aPlayList=[]
$(function(){
    $.get('/dictation/qryVoice/', function(dic){
		aWords = dic.words;
		alert(aWords);
		hWords = $('#words');
		fillWords(aWords,hWords);
    });

    $('.word').click(function(){
        // $(this).attr({'code':1});
        alert($(this).attr('code'));
        $(this).toggleClass("se");
    });

    alert(aPlayList);
    var player = cyberplayer("playercontainer").setup({
                width: 0,   //680, // 宽度，也可以支持百分比(不过父元素宽度要有)
                height: 0,  //448, // 高度，也可以支持百分比
                title: "基本功能", // 标题
                //file: "/static/dictation/voice/4e5e6c42_05212.mp3", // 播放地址
                //file: "/static/dictation/voice/4e0058f04e0d54cd_05212.mp3", // 播放地址
                //播放列表
                playlist: [{sources: [{file: "/static/dictation/voice/6ee160004fe15fc3_05212.mp3"}],},
                    {sources: [{file: "/static/dictation/voice/7acb523b_05212.mp3"}],},
                    {sources: [{file: "/static/dictation/voice/8b66544a_05212.mp3"}],},
                    {sources: [{file: "/static/dictation/voice/8d5e626c_05212.mp3"}],},
                    {sources: [{file: "/static/dictation/voice/81ea8c6a_05212.mp3"}],},
                    ],
                //image: "http://gcqq450f71eywn6bv7u.exp.bcevod.com/mda-hbqagik5sfq1jsai/mda-hbqagik5sfq1jsai.jpg", // 预览图
                autostart: false, // 是否自动播放
                stretching: "uniform", // 拉伸设置
                repeat: false, // 是否重复播放 true false
                volume: 100, // 音量
                controls: false, // controlbar是否显示 true   false
                starttime: 0, // 视频开始播放时间点(单位s)，如果不设置，则可以从上次播放时间点续播
                logo: { // logo设置
                    linktarget: "_blank",
                    margin: 8,
                    hide: false,
                    position: "top-right", // 位置
                    file: "./img/logo.png" // 图片地址
                },
                ak: "xxxxxxxxxxxxxxxx" // 公有云平台注册即可获得accessKey
            });

            $('#toPlay').click(function(){
            var item = player.playlistItem(2);
            //player.stop()
            //player.playlistNext();
            });

            $('#next').click(function(){
            var item = player.playlistNext();
            //player.stop()
            //player.playlistNext();
            });

            $('#previous').click(function(){
            var item = player.playlistPrev();
            //player.stop()
            //player.playlistNext();
            });

            player.onPlaylistItem(function(event){
                //alert("onPlaylistItem");
               player.stop()
            });
});

function fillWords(aWords,hWords){
    // hWords.empty();
    $.each(aWords, function(i,aWd){
        var code = aWd[0];
        // alert(aWd);
        var dispName = aWd[2];
        var voiceFile = '/static/dictation/voice/' + aWd[3];
        aPlayList.append({sources: [{file: voiceFile}],})
        // hWords.append('<label class="word un" code='+code+'>'+dispName+'</label>');
        if(i > 5){
            return
        }
    });

    $('.word').click(function(){
        $(this).toggleClass("se");
    })
}

