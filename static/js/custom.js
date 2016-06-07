/**
 * Created by chen on 16-6-5.
 */
$(document).ready(function(){


    function toggleDuoshuoComments(container, word_id, word_url){
    var el = document.createElement('div');//该div不需要设置class="ds-thread"
    el.setAttribute('data-thread-key', word_id);//必选参数
    el.setAttribute('data-url', word_url);//必选参数
    //el.setAttribute('data-author-key', learner_id);//可选参数
    DUOSHUO.EmbedThread(el);
    jQuery(container).append(el);
    }



    $("button#next").click(function(){
        // alert("The button was clicked.");
        // console.log("Next button is clicked.");
        var word_id = document.getElementById("word").getAttribute("word_id");
        // console.log("Word id is "+word_id);
        var id = parseInt(word_id);
        id = id +1;

        console.log(id);
        $.ajax({
            url: 'http://' + window.location.host + '/api/word/' + id,
            type: "GET",
            dataType: 'json',
            contentType: "application/json",
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function(response, statusText, xhr){
                console.log(response);
                var word_text = response.text;
                var word_desc = response.desc;
                var word_sen = response.sentence;
                if (xhr.status == 200 || xhr.status == 201){
                    $("h1#word").attr('word_id',id+"");
                    $("h1#word").text(word_text);
                    $("p#dec").text(word_desc);
                    $("p#sen").text(word_sen);
                    $("button#pre").text('Previous');
                    $("button#pre").attr('class', 'btn btn-primary');
                    //update duoshuo plugin
                    $("div#ds-thread").remove();
                    container = $("div.starter-template");
                    toggleDuoshuoComments(container,id,'/word/'+word_text);

                }
            },
            error: function (xhr, ajaxOptions, error) {
                if (xhr.status == 404){
                    $("button#next").text('End');
                    $("button#next").attr('class', 'btn btn-default');
                } else{
                    console.log(xhr.status);
                    console.log(xhr.responseText);
                }
            }
        })
    });



    $("button#pre").click(function(){
        // alert("The button was clicked.");
        // console.log("Next button is clicked.");
        var word_id = document.getElementById("word").getAttribute("word_id");
        // console.log("Word id is "+word_id);
        var id = parseInt(word_id);
        id = id -1;

        console.log(id);
        $.ajax({
            url: 'http://' + window.location.host + '/api/word/' + id,
            type: "GET",
            dataType: 'json',
            contentType: "application/json",
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function(response, statusText, xhr){
                console.log(response);
                var word_text = response.text;
                var word_desc = response.desc;
                var word_sen = response.sentence;
                if (xhr.status == 200 || xhr.status == 201){
                    $("h1#word").attr('word_id',id+"");
                    $("h1#word").text(word_text);
                    $("p#dec").text(word_desc);
                    $("p#sen").text(word_sen);
                    $("button#next").text('Next');
                    $("button#next").attr('class', 'btn btn-primary');
                    //update duoshuo plugin
                    $("div#ds-thread").remove();
                    container = $("div.starter-template");
                    toggleDuoshuoComments(container,id,'/word/'+word_text);
                }
            },
            error: function (xhr, ajaxOptions, error) {
                if (xhr.status == 404){
                    $("button#pre").text('End');
                    $("button#pre").attr('class', 'btn btn-default');
                } else{
                    console.log(xhr.status);
                    console.log(xhr.responseText);
                }
            }
        })
    });


    $("button#know").click(function () {
        var learnerId = document.getElementById("learner").getAttribute("learner_id");
        var wordName = document.getElementById("word").textContent;
        var msg = {
            "learnerId" : learnerId,
            "wordName": wordName
        };
        $.ajax({
            url: 'know',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(msg),
            dataType: 'text',
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function (response) {
                $("div.alert-info").remove();
                var ele = '<div class="alert alert-info"><a href="#" class="close" data-dismiss="alert" aria-label="close" title="close">×</a>You have learned this word.</div>'
                $("div.starter-template").prepend(ele);
                // console.log(response);
            },
            error: function (xhr) {
                console.log(xhr.status);
                console.log(xhr.responseText);
            }
        })

    });




});