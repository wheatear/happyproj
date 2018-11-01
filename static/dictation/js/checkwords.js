
var aWords=[];
$(function(){
    $.get('/dictation/qryTestWords/', function(dic){
		aWords = dic.words;
        // alert('get words')
		hWords = $('#words');
		fillWords(aWords,hWords);
    });

    $('.word').click(function(){
        // $(this).attr({'code':1});
        // alert($(this).attr('code'));
        $(this).toggleClass("se");
    })

    $('#saveTest').click(function(){
        wdResult = [];
        $('.word').each(function(i){
            if(this.className.indexOf('.un') >= 0) {
                wdResult.push([this.code,false])
            } else {
                wdResult.push([this.code,true])
            }
        });
        $.post('/dictation/saveTest/',{'test':wdResult});

    })
});

function fillWords(aWords,hWords){
    hWords.empty();
    $.each(aWords, function(i,aWd){
        var code = aWd[0];
        // alert(aWd);
        var dispName = aWd[1];
        hWords.append('<label class="word un" code='+code+'>'+dispName+'</label>');

    });
    $('.word').click(function(){
        $(this).toggleClass("se");
    })
}


