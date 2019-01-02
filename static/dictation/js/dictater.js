
var dictater= {

    musicDom: null, //播放器对象
    songs: [],        //歌曲目录，用数组来存储
    announce: [],
    cur: 0,
    status: 0,

    //初始化音乐盒
    init: function () {
        this.musicDom = document.createElement('audio');
    },

    setWords: function(words) {
        this.songs = words;
    },

    //添加一首音乐
    add: function (src) {
        this.songs.push(src);
    },

    //根据数组下标决定播放哪一首歌
    play: function () {
        i = this.cur;
        if (i == 0) {
            this.playStart();
        }
        for (; i<len; i++) {
            this.cur = i;
            this.playOne(i);
            this.playOne(i);
        }

        this.cur++;
    },

    playOne: function(index){
        this.musicDom.src = this.songs[index];
        this.musicDom.play();
    },

    playStart: function(){
        this.playAnnounce(0);
    },

    playEnd: function(){
        this.playAnnounce(1);
    },

    playAnnounce: function(index){
        this.musicDom.src = this.announce[index];
        this.musicDom.play();
    },

    //暂停音乐
    stop: function () {
        this.musicDom.pause();
    },

    //下一首（待编写）
    next: function () {

    },

    //上一首（待编写）
    prev: function () {

    }
}
