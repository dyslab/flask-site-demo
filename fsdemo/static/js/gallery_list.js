$(document).ready(function() {
    $(".top-menuitem.nav-link:eq(1)").addClass("active");
    
    // Init form upload file elements.
    ajaxInitPhotos($("a.custom-list-link[href=\"ALL\""));

    // Append photos in container 'div.custom-phots-container'.
    function appendPhotos(data) {
        for (id in data.photolist) {
            // Insert wrap begin.
            insertHTML = "<div class=\"col-md-6 col-lg-4 p-1\"><div class=\"card\"><div class=\"card-body\">";
            // Insert download, link.
            insertHTML += "<div class=\"text-right\"><ul class=\"list-inline m-0 p-0\">";
            insertHTML += "<li class=\"list-inline-item\"><a class=\"custom-photo-download\" href=\"" +
                data.photolist[id].id + "\"><small>Download</small></a></li>";
            insertHTML += "<li class=\"list-inline-item\"><a class=\"custom-photo-link\" href=\"" +
                data.photolist[id].link + "\" data-clipboard-target=\"page\"><small>Link</small></a></li>";
            insertHTML += "</ul></div>";
            // Insert image and its caption.
            insertHTML += "<figure class=\"figure\"><img class=\"figure-img img-fluid rounded\" src=\"" +
            data.photolist[id].link + "\"></img><figcaption class=\"figure-caption\">" +
            data.photolist[id].caption + "</figcaption></figure>";
            // Insert tags.
            insertHTML += "<div><ul class=\"list-inline\">";
            for (tagid in data.photolist[id].tags) {
                insertHTML += "<li class=\"list-inline-item\"><span class=\"badge badge-primary\">" +
                    data.photolist[id].tags[tagid] + "</span></li>";
            }
            insertHTML += "</ul></div>";
            // Insert edit and delete.
            insertHTML += "<div class=\"text-right\"><ul class=\"list-inline m-0 p-0\">";
            insertHTML += "<li class=\"list-inline-item\"><a class=\"custom-photo-edit\" href=\"" +
                data.photolist[id].id + "\"><small>Edit</small></a></li>";
            insertHTML += "<li class=\"list-inline-item\"><a class=\"custom-photo-delete\" href=\"" +
                data.photolist[id].id + "\"><small>Delete</small></a></li>";
            insertHTML += "</ul></div>";
            // Insert wrap end.
            insertHTML += "</div></div></div>";
            $("div.custom-photos-container").append($(insertHTML));
        }
        if (data.nextpage > 0) {
            insertHTML = "<div class=\"col-12 mt-3 mt-lg-5 text-center custom-photos-nextab\">" +
                "<button id=\"custom-photos-loadmore\" class=\"btn btn-success\">Load More ...</button></div>";
            $("div.custom-photos-container").append($(insertHTML));
        }
    }
    
    // Initialize photos when the navlink clicked.
    function ajaxInitPhotos(jquery) {
        var page = 1;
        var offset = 0;
        var keyword = jquery.attr("href");
        var tag = jquery.text();
        var year = jquery.text();
        $("input#keyword").val(keyword);
        $("input#tag").val(tag);
        $("input#year").val(year);

        $.post("/gallery/list/photos", 
            { keyword: keyword, tag: tag, year: year, page: page, offset: offset }
        ).done(function(data) {
            resObj = JSON.parse(data);
            if (resObj.resCode === 0) {
                $("div.custom-photos-container").children().remove();
                appendPhotos(resObj.data);
                $("input#nextpage").val(resObj.data.nextpage);
                $("input#offset").val(resObj.data.offset);
            } else {
                alert(resObj.resMsg);
            }
            $("a.custom-list-link").removeClass("active");
            jquery.addClass("active");
        });
    }

    // Validate upload file extension.
    $("a.custom-list-link").click(function(event) {
        event.preventDefault();
        ajaxInitPhotos($(this));
    })

    // Home Tab: Load more blogs... 
    $("div.custom-photos-container").on("click", "button#custom-photos-loadmore", function() {
        var page = $("input#nextpage").val();
        var offset = $("input#offset").val();
        var keyword = $("input#keyword").val();
        var tag = $("input#tag").val();
        var year = $("input#year").val();

        $.post("/gallery/list/photos", 
            { keyword: keyword, tag: tag, year: year, page: page, offset: offset }
        ).done(function(data) {
            resObj = JSON.parse(data);
            if (resObj.resCode === 0) {
                $("div.custom-photos-nextab").remove();
                appendPhotos(resObj.data);
                $("input#nextpage").val(resObj.data.nextpage);
                $("input#offset").val(resObj.data.offset);
            } else {
                alert(resObj.resMsg);
            }
        });
    });

    // Download photo.
    $("div.custom-photos-container").on("click", "a.custom-photo-download", function(event) {
        event.preventDefault();
        alert('Download: ' + $(this).attr("href"));
    });

    // Copy photo link.
    $("div.custom-photos-container").on("click", "a.custom-photo-link", function(event) {
        event.preventDefault();
        copyText($(this).attr("href"));
        $(this).tooltip({title: "Copied"});
        $(this).tooltip("show");
        setTimeout(function() {
            $("a.custom-photo-link").tooltip("dispose");
        }, 2000);
    });

    // Edit photo
    $("div.custom-photos-container").on("click", "a.custom-photo-edit", function(event) {
        event.preventDefault();
        alert('Edit: ' + $(this).attr("href"));
    });

    // Delete photo
    $("div.custom-photos-container").on("click", "a.custom-photo-delete", function(event) {
        event.preventDefault();
        if (confirm("Are you sure to delete this photo?")) {
            alert('Delete: ' + $(this).attr("href"));
        }
    });

    // Note: 'copyText' came from the following link.
    // https://github.com/by-syk/jquery-copy/blob/master/jquery.copy.js
    function copyText(obj) {
        if (!obj) {
            return false;
        }
        var text;
        if (typeof(obj) == 'object') {
            if (obj.nodeType) { // DOM node
                obj = $(obj); // to jQuery object
            }
            if (obj instanceof $) {
            if (!obj.length) { // nonexistent
                return false;
            }
            text = obj.text();
            if (!text) { // Maybe <textarea />
                text = obj.val();
            }
            } else { // as JSON
                text = JSON.stringify(obj);
            }
        } else { // boolean, number, string
            text = obj;
        }
        //var $temp = $('<input>'); // Line feed is not supported
        var $temp = $('<textarea>');
        $('body').append($temp);
        $temp.val(text).select();
        var res = document.execCommand('copy');
        $temp.remove();
        return res;
    }
});
