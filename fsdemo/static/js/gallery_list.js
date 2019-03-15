$(document).ready(function() {
    $(".top-menuitem.nav-link:eq(1)").addClass("active");
    
    // Init: Load all photos.
    ajaxInitPhotos($("a.custom-list-link[href=\"ALL\""));

    // Append search result in container 'div.custom-phots-container'.
    function appendResult(data) {
        insertHTML = "<div class=\"col-12 mb-3 font-italic\">Total <span class=\"font-weight-bold custom-photo-count\">" +
            data.count + "</span> photo(s) have been found in Gallery.</div>";
        $("div.custom-photos-container").append($(insertHTML));
    }

    // Append photos in container 'div.custom-phots-container'.
    function appendPhotos(data) {
        for (id in data.photolist) {
            // Insert wrap begin.
            insertHTML = "<div class=\"col-md-6 col-lg-4 p-1 photo-wrap\"><div class=\"card\"><div class=\"card-body\">";
            // Insert download, link.
            insertHTML += "<div class=\"text-right\"><ul class=\"list-inline m-0 p-0\">";
            insertHTML += "<li class=\"list-inline-item\"><a class=\"custom-photo-download\" href=\"/gallery/download/" +
                data.photolist[id].id + "\"><small>Download</small></a></li>";
            insertHTML += "<li class=\"list-inline-item\"><a class=\"custom-photo-link\" href=\"" +
                data.photolist[id].link + "\" data-clipboard-target=\"page\"><small>Link</small></a></li>";
            insertHTML += "</ul></div>";
            // Insert image and its caption.
            insertHTML += "<figure class=\"figure\"><a class=\"mfp-image-popup-zoom\" href=\"" +
            data.photolist[id].link + "\" title=\"" +
            data.photolist[id].caption + "\"><img class=\"figure-img img-fluid rounded\" src=\"" +
            data.photolist[id].link + "\"></img></a><figcaption class=\"figure-caption\">" +
            data.photolist[id].caption + "</figcaption></figure>";
            // Insert time and tags.
            insertHTML += "<div><ul class=\"list-inline\">";
            insertHTML += "<li class=\"list-inline-item text-muted font-italic\"><small>" +
                data.photolist[id].time + "</small></li>";
            for (tagid in data.photolist[id].tags) {
                insertHTML += "<li class=\"list-inline-item\"><span class=\"badge badge-primary\">" +
                    data.photolist[id].tags[tagid] + "</span></li>";
            }
            insertHTML += "</ul></div>";
            // Insert edit and delete.
            insertHTML += "<div class=\"text-right\"><ul class=\"list-inline m-0 p-0\">";
            insertHTML += "<li class=\"list-inline-item\"><a class=\"custom-photo-edit\" href=\"/gallery/edit/" +
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

        // Init Magnific Popup.
        $('.mfp-image-popup-zoom').magnificPopup({
            type: 'image',
            closeOnContentClick: true,
            closeBtnInside: false,
            fixedContentPos: true,
            mainClass: 'mfp-no-margins mfp-with-zoom', // class to remove default margin from left and right side
            image: {
            verticalFit: true
            },
            zoom: {
            enabled: true,
            duration: 300 // don't foget to change the duration also in CSS
            }
        });
    }
    
    // Initialize photos when the navlink clicked.
    function ajaxInitPhotos(jquery) {
        var page = 1;
        var offset = 0;
        if (jquery !== undefined) {
            var keyword = jquery.attr("href");
            var tag = jquery.text();
            var year = jquery.text();
            $("input#keyword").val(keyword);
            $("input#tag").val(tag);
            $("input#year").val(year);
        } else {
            var keyword = $("input#keyword").val();
            var tag = $("input#tag").val();
            var year = $("input#year").val();
        }

        $.post("/gallery/list/photos", 
            { keyword: keyword, tag: tag, year: year, page: page, offset: offset }
        ).done(function(data) {
            resObj = JSON.parse(data);
            if (resObj.resCode === 0) {
                $("div.custom-photos-container").children().remove();
                appendResult(resObj.data)
                appendPhotos(resObj.data);
                $("input#nextpage").val(resObj.data.nextpage);
                $("input#offset").val(resObj.data.offset);
            } else {
                alert(resObj.resMsg);
            }
            $("a.custom-list-link").removeClass("active");
            if (jquery !== undefined) {
                jquery.addClass("active");
            }
        });
    }

    // Load photos by tag or year when the nav-link item clicked.
    $("a.custom-list-link").click(function(event) {
        event.preventDefault();
        ajaxInitPhotos($(this));
    })

    // Load photos by custom tag.
    $("button#custom-search").click(function(event) {
        $("input#keyword").val("TAG");
        $("input#tag").val($("input#custom-tag").val());
        ajaxInitPhotos(undefined);
    })

    // Load more photos... 
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

    // Copy photo link.
    $("div.custom-photos-container").on("click", "a.custom-photo-link", function(event) {
        event.preventDefault();
        copyText($(this).attr("href"));
        $(this).tooltip({title: "Copied"});
        $(this).tooltip("show");
        setTimeout(function() {
            $("a.custom-photo-link").tooltip("hide");
        }, 2000);
    });

    // ensure the tooltip will only show up one time.
    $("div.custom-photos-container").on("hidden.bs.tooltip", "a.custom-photo-link", function() {
        $(this).tooltip("dispose");
    });

    // Delete photo
    $("div.custom-photos-container").on("click", "a.custom-photo-delete", function(event) {
        event.preventDefault();
        if (confirm("Are you sure to delete this photo?")) {
            var photoid = $(this).attr("href");
            var photowrap = $(this).parent().parent().parent().parent().parent().parent();
            $.get("/gallery/delete/" + photoid, function(data) {
                resObj = JSON.parse(data);
                if (resObj.resCode === 0) {
                    if (photowrap.hasClass("photo-wrap")) {
                        photowrap.remove();
                        var offset = parseInt($("input#offset").val());
                        $("input#offset").val(offset-1);
                        var count = parseInt($("span.custom-photo-count").text());
                        $("span.custom-photo-count").text(count-1);                        
                    }
                } else {
                    alert(resObj.resMsg);
                }
            });
        }
    });

    // Note: 'copyText' came from the following link.
    // https://github.com/by-syk/jquery-copy/blob/master/jquery.copy.js
    function copyText(obj) {
        if (!obj) {
            return false;
        }
        var text;
        if (typeof(obj) == "object") {
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
        //var $temp = $("<input>"); // Line feed is not supported
        var $temp = $("<textarea>");
        $("body").append($temp);
        $temp.val(text).select();
        var res = document.execCommand("copy");
        $temp.remove();
        return res;
    }
});
