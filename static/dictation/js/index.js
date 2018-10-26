        $(function(){
            $.get('initQry', function(dic){
                aChoiceSelected = dic.choiceSelected;
                aPress = dic.press;
                hPress = $('#press');
                hBook = $('#book');
                hUnit = $('#unit');
                hLesson = $('#lesson');
                fillSele(aPress,hPress);
                // hNet = $('#ne');
                // hRes = $('#result');

            });


        });

        //fill select
        function fillSelect(aNames,hSele){
                hSele.empty();
                $.each(aNames, function(i,dName){
                    //fill head
                    code = dName['id'];
                    dispName = dName['name'];
                    hSele.append('<option value='+code+'>'+dispName+'</option>');
                });
        }

        //fill ul
        function fillUl(aNames,hUl){
                hUl.empty();
                $.each(aNames, function(i,dName){
                    //fill head
                    code = dName['id'];
                    dispName = dName['name'];
                    hUl.append('<li value='+code+'>'+dispName+'</li>');
                });
        }

