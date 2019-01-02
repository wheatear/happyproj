
var dictater= {

    musicDom: null, //播放器对象
    aWords: [],        //歌曲目录，用数组来存储
    announce: [],
    cur: 0,
    status: 0,     //0:未开始  1:开始   2：暂停    3：继续   9：结束
    t: null,
    repeat: 0,

    //初始化音乐盒
    init: function () {
        this.musicDom = document.createElement('audio');
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
        if (this.status==0) {
            this.status = 1;
            this.playStart();
            this.t = setTimeout("dictater.play()", 5000);
            return;
        }
        if (this.status == 2){
            return;
        }
        if (this.status == 9){
            this.stop();
            return;
        }
        if (i>=this.aWords.length){
            this.playEnd();
            this.stop();
            return;
        }
        playWord = this.aWords[i];
        this.playOne(playWord);
        if (this.repeat == 0){ this.repeat++;}
        else {
            this.repeat = 0;
            this.cur++;
        }
        slpTime=3000*playWord[1].length;
        this.t = setTimeout("dictater.play()", slpTime)
    },

    playOne: function(playWord){
        this.musicDom.src = playWord[3];
        this.musicDom.play();
    },

    playStart: function(){
        this.playAnnounce(0);
    },

    playEnd: function(){
        this.playAnnounce(1);
    },

    playAnnounce: function(index){
        // alert('announce: ' + this.announce[index]);
        // alert('announce file: ' + this.announce[index][3]);
        this.musicDom.src = this.announce[index][3];
        this.musicDom.play();
    },

    //暂停
    pause: function(){
        this.status = 2;
        this.repeat = 0;
    },

    //继续
    continue: function(){
        this.status = 3;
        this.repeat = 0;
        this.play();
    },

    //结束
    stop: function () {
        // this.musicDom.pause();
        this.status = 9;
        this.cur = 0;
        this.repeat = 0;
    },

    //下一首（待编写）
    next: function () {
        this.cur++;
        this.repeat = 0;
    },

    //上一首（待编写）
    prev: function () {
        this.cur--;
        this.repeat = 0;
    }
};
