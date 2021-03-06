
var dictater= {

    musicDom: null, //播放器对象
    aWords: [],        //歌曲目录，用数组来存储
    announce: [],
    cur: 0,
    status: 0,     //0:未开始  1:开始   2：暂停    3：继续   4：结束    9:完毕
    t: null,
    repeat: 0,

    // events
    onLoad: null,
    onComplete: null,

    //初始化音乐盒
    init: function () {
        this.musicDom = document.createElement('audio');
        // this.musicDom
    },

    setWords: function(words, announce) {
        this.aWords = words;
        this.announce = announce;
    },

    //添加一首音乐
    add: function (src) {
        this.aWords.push(src);
    },

    //根据数组下标决定播放哪一首歌
    play: function () {
        i = this.cur;
        if (i>=this.aWords.length){
            this.complete();
            return;
        }
        playWord = this.aWords[i];
        // dispStr = playWord[1];
        // alert('disp word ' + dispStr);
        // if (this.onLoad) {this.onLoad(dispStr);}

        // alert('dictating word ' + dispStr);

        if (this.repeat == 0){
            this.setSrc(playWord);
            this.dispWord(playWord);
            this.repeat++;
        } else {
            this.repeat = 0;
            this.cur++;
        }
        this.playOne(playWord);
        slpTime=3000*playWord[1].length;
        this.t = setTimeout("dictater.play()", slpTime)
    },

    setSrc: function(playWord){
        this.musicDom.src = playWord[3];
    },

    playOne: function(playWord){
        // this.musicDom.src = playWord[3];
        // this.musicDom.load();
        // setTimeout("dictater.play()", 1000);
        this.musicDom.play();
    },

    playStart: function(){
        this.playAnnounce(0);
    },

    playEnd: function(){
        this.playAnnounce(1);
    },

    playStop: function(){
        this.playAnnounce(4);
    },

    playPause: function(){
        this.playAnnounce(2);
    },

    playContinue: function(){
        this.playAnnounce(3);
    },

    playAnnounce: function(index){
        // alert('announce: ' + this.announce[index]);
        // alert('announce file: ' + this.announce[index][3]);
        this.musicDom.src = this.announce[index][3];
        this.musicDom.play();
    },

    //开始听写
    start: function(){
        this.status = 1;
        this.playStart();
        this.t = setTimeout("dictater.play()", 3000);
    },

    //暂停
    pause: function(){
        clearTimeout(this.t);
        this.status = 2;
        this.repeat = 0;
        this.playPause();
    },

    //继续
    continue: function(){
        this.playContinue();
        this.status = 3;
        this.repeat = 0;
        // this.status = 1;

        this.t = setTimeout("dictater.play()", 3000);
    },

    //结束
    stop: function () {
        // this.musicDom.pause();
        clearTimeout(this.t);

        this.status = 4;
        this.cur = 0;
        this.repeat = 0;
        this.playStop();

        hCheck = $('#checkWord');
        hCheck.removeAttr("disabled");
    },

    //完毕
    complete: function () {
        // this.musicDom.pause();
        this.status = 9;
        this.cur = 0;
        this.repeat = 0;
        this.playEnd();

        hCheck = $('#checkWord');
        hCheck.removeAttr("disabled");
    },

    //下一个
    next: function () {
        clearTimeout(this.t);
        this.cur++;
        this.repeat = 0;
        this.play();
    },

    //上一个
    prev: function () {
        clearTimeout(this.t);
        this.cur--;
        this.repeat = 0;
        this.play();
    },

    dispWord: function(sWord){
        hWords = $('#words');
        code = sWord[0];
        sPinyin = sWord[2];
        plen = sPinyin.length;
        dispStr = sPinyin.join(' ');
        hWords.append('<label class="py'+plen+' un" code='+code+'>'+dispStr+'</label>');
    }


};
