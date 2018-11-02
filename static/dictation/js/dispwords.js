
var aWords=[];
$(function(){
    $.get('/dictation/qryWords/', function(dic){
		aWords = dic.words;
        // alert('get words')
		hWords = $('#words');
		fillWords(aWords,hWords);
    });

    $('.word').click(function(){
        // $(this).attr({'code':1});
        // alert($(this).attr('code'));
        $(this).toggleClass("se");
    });

    $('#next').click(function(){
        window.location.href = '/dictation/dictating/'
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


