
var dChoiceSelected = new Object();
var aLesson=[];
$(function(){
            $.get('/dictation/initQry/', function(dic){
                dChoiceSelected = dic.choiceSelected;

                aPress = dic.press;
                aBook = dic.book;
                aUnit = dic.unit;
                aLesson = dic.lesson;
                // alert(aLesson)
                hPress = $('#press');
                hBook = $('#book');
                hUnit = $('#unit');
                hLesson = $('#lesson');
                fillSelect(aPress,hPress,dChoiceSelected['press']);
                fillSelect(aBook,hBook,dChoiceSelected['book']);
                fillSelect(aUnit,hUnit,dChoiceSelected['unit']);

                fillRadio(aLesson,hLesson,dChoiceSelected['lesson']);
            });

            $('#unit').change(function(){
                alert('unit changed');
                hLesson = $('#lesson');
                hLesson.empty();
                unitCode = $(this).val();
                aLesson.push(unitCode);
                // alert(aLesson);
                qry = 'qryLesson/?unit='+unitCode;
                alert(qry);
                $.get(qry,function(dic){
                    aLesson = dic.lesson;
                    // alert(aLesson);
                    fillRadio(aLesson,hLesson,'None');
                })
            });

            $('#next').click(function(){
                // alert('submit');
                hSubmit=$('#submit');
                hSubmit.trigger("click");
            })
});

        //fill select
        function fillSelect(aOptions,hSele,selectedKey){
                hSele.empty();
                $.each(aOptions, function(i,dOpt){
                    //fill head
                    // alert(i);
                    // alert(dOpt);
                    code = dOpt[0];
                    // alert(code);
                    dispName = dOpt[1];
                    // alert(dispName);
                    if(code == selectedKey) {
                        hSele.append('<option selected="selected" value='+code+'>'+dispName+'</option>');
                    }
                    else{
                        hSele.append('<option value='+code+'>'+dispName+'</option>');
                    }

                });
        }

        //fill ul
        function fillUl(aNames,hUl){
                hUl.empty();
                hUl.append('<label>课文</label>');
                $.each(aNames, function(i,dName){
                    //fill head
                    code = dName[0];
                    dispName = dName[1];
                    hUl.append('<li value='+code+'>'+dispName+'</li>');
                });
        }

        //fill radio
        function fillRadio(aNames,hRadio,checkKey){
                hRadio.empty();
                hRadio.append('<label>课文</label><br>');
                $.each(aNames, function(i,dName){
                    //fill head
                    code = dName[0];
                    dispName = dName[1];
                    if(code == checkKey) {
                        hRadio.append('<label>'+ dispName +'<input type="radio" name="lesson" value=' + code + ' checked></label><br>');
                    }
                    else{
                        hRadio.append('<label>' + dispName + '<input type="radio" name="lesson" value=' + code + '></label><br>');
                    }
                });
        }

