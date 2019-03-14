$(document).ready(function() {
    $(".top-menuitem.nav-link:eq(2)").addClass("active");

    // Initialize markdown editor and tags in Search Tab.
    var simplemde = new SimpleMDE({
        autofocus: true, 
        element: $("#blogcontent")[0],
        forceSync: true,
        spellChecker: false
    });
    InitTags();
    ChangeActiveTab(parseInt($(".activepanel").text()));

    // Common function: Change Active Tab by id. eg. 0,1,2...
    function ChangeActiveTab(id) {
        $(".list-group-item").eq(id).tab("show")
    }

    // Common function: Set response message
    function SetResponse(jquery, msg) {
        insertHTML = "<div class=\"alert alert-warning alert-dismissible fade show\" role=\"alert\"><strong>" +
            msg + "</strong><button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\">" +
            "<span aria-hidden=\"true\">&times;</span></button></div>";
        jquery.append($(insertHTML).delay(2500).fadeOut(500));
    }

    // Home/Search Tab: Blog's 'Edit' button click function
    $("div").on("click", "a.blog-edit", function(event) {
        event.preventDefault();
        var blogid = $(this).attr("href");
        $.get("/blog/edit/" + blogid, function(data) {
            resObj = JSON.parse(data);
            if (resObj.resCode === 0) {
                ChangeActiveTab(1);
                SetWriteTabBlogData(resObj.data);
            } else {
                alert(resObj.resMsg);
            }
        });
    });

    // Home Tab: Blog's 'Delete' button click function
    $("div#home").on("click", "a.blog-delete", function(event) {
        event.preventDefault();
        if (confirm("Are you sure to delete this blog?")) {
            var blogid = $(this).attr("href");
            var blogwrap = $(this).parent().parent().parent();
            $.get("/blog/delete/" + blogid, function(data) {
                resObj = JSON.parse(data);
                if (resObj.resCode === 0) {
                    if (blogwrap.hasClass("blog-wrap")) {
                        SetResponse(blogwrap, resObj.resMsg);
                        var off = parseInt($("button#loadmore").attr("offset"));
                        $("button#loadmore").attr("offset", off-1);
                        setTimeout(function(){
                            blogwrap.remove();
                            if ($(".blog-wrap:first").children(":first").hasClass("hr-separator")) {
                                $(".blog-wrap:first").children(":first").remove();
                            }
                        }, 3000);
                    }
                } else {
                    alert(resObj.resMsg);
                }
            });
        }
    });

    // Home Tab: Append blog for loadmore
    function appendBlog(blogdata) {
        for (id=0; id<blogdata.bloglist.length; id++) {
            insertHTML = "<div class=\"blog-wrap\">" +
                "<hr class=\"mt-3 mb-3 mt-lg-5 mb-lg-5\">";
            insertHTML += "<div class=\"custom-blog-title mb-4\">" +
                "<span class=\"h3\">" +
                blogdata.bloglist[id].title + "</span><small><a href=\"" + 
                blogdata.bloglist[id].id +
                "\" class=\"blog-edit\">Edit</a></small></div>" +
                "<div class=\"mb-3\"><ul class=\"list-inline\">" +
                "<li class=\"list-inline-item\"><span>" +
                blogdata.bloglist[id].time + "</span></li>";
            for(tagid=0; tagid<blogdata.bloglist[id].tags.length; tagid++) {
                insertHTML += "<li class=\"list-inline-item\">" +
                    "<span class=\"badge badge-pill badge-warning\">" +
                    blogdata.bloglist[id].tags[tagid] + "</span></li>";
            }
            insertHTML += "</ul></div><div class=\"custom-blog-content\">" +
                blogdata.bloglist[id].content + "</div>";
            insertHTML += "<div class=\"text-right\"><small><a href=\"" + 
                blogdata.bloglist[id].id +
                "\" class=\"blog-delete\">Delete</a></small></div></div>";
            $("div#home").append($(insertHTML));
        }
        if (blogdata.nextpage > 0) {
            insertHTML = "<div class=\"mt-3 mb-3 mt-lg-5 mb-lg-5 text-center nextab\">" +
                "<button id=\"loadmore\" class=\"btn btn-success\" nextpage=\"" + 
                blogdata.nextpage + "\" offset=\"" +
                blogdata.offset + "\">Load More ...</button></div>";
            $("div#home").append($(insertHTML));
        }
    }

    // Home Tab: Load more blogs... 
    $("div#home").on("click", "button#loadmore", function() {
        var nextp = $(this).attr("nextpage");
        var off = $(this).attr("offset");
        $.get("/blog/loadmore/" + nextp + "?off=" + off, function(data) {
            resObj = JSON.parse(data);
            if (resObj.resCode === 0) {
                $("div.nextab").remove();
                appendBlog(resObj.data);
            } else {
                alert(resObj.resMsg);
            }
        });
    });

    // Write Tab: Reset object tags.
    // Note: The document elements used by this function 
    //       could be found in 'widget_tags.html'.
    function ResetObjectTags(tags) {
        $(".custom-tag-container").children(".custom-tag").remove();
        for (tagid = 0; tagid < tags.length; tagid++) {
            insertHTML = "<li class=\"list-inline-item custom-tag\">" +
                "<span class=\"badge badge-primary\"><span class=\"h6\">" +
                tags[tagid] + " &times;</span></span>";
            insertHTML += "<input type=\"hidden\" name=\"tags\" id=\"tags\" value=\"" +
                tags[tagid] + "\"></li>";
            $(".custom-tag-container").append($(insertHTML));
        }
    }

    // Write Tab: Set blog's EDIT flag and object info.
    function SetWriteTabBlogData(data) {
        if (data !== undefined) {
            $("span#action").text("EDIT");
            $("span#action").removeClass("text-primary");
            $("span#action").addClass("text-danger");
            $("input#blogid").val(data.id);
            $("input#blogtitle").val(data.title);
            ResetObjectTags(data.tags);
            // $("textarea#blogcontent").val(data.content);
            simplemde.value(data.content);  // SimpleMDE set values.
        }
    }

    // Write Tab: set NEW flag.
    $("a#newblog").click(function() {
        $("span#action").text("NEW");
        $("span#action").removeClass("text-danger");
        $("span#action").addClass("text-primary");
    });

    // Write Tab: event fired when the new active tab shown.
    $("a[data-toggle=\"list\"]").on("shown.bs.tab", function (e) {
        if ($(e.target).attr("id") === "newblog") {
            simplemde.codemirror.focus();   // SimpleMDE focus.
            $("html").scrollTop($("header").height());
        }
    });

    // Write Tab: Response for new/edit.
    function responseForWriteTab(data) {
        resObj = JSON.parse(data);
        if (resObj.resCode === 0) {
            SetResponse($("#writetabresponse"), resObj.resMsg);
            setTimeout(function () {
                window.document.location.reload();
            }, 3000);
        } else {
            alert(resObj.resMsg);
        }
    }

    // Write Tab: Submit new blog.
    $("#writeform").submit(function(event) {
        event.preventDefault();
        var newflag = $("span#action").text();
        if (newflag === "NEW") {
            $.post("/blog/new", $("#writeform").serialize()).done(function(data) {
                responseForWriteTab(data);
            });
        } else {
            $.post("/blog/edit/save", $("#writeform").serialize()).done(function(data) {
                responseForWriteTab(data);
            });
        }
    });

    // Search Tab: Initialize tags.
    function InitTags() {
        $("#taglist").children(".custom-option-tag").each(function() {
            if ($(this).val() !== "") {
                $(".custom-search-tag-container").append($("<li class=\"list-inline-item custom-search-tag\">" +
                    "<span class=\"badge badge-pill badge-warning\">" +
                    $(this).val() + " &times;</span><input type=\"hidden\" name=\"searchtags\" id=\"searchtags\" value=\"" +
                    $(this).val() + "\"></li>")); 
            }
        });
    }

    // Search Tab: Remove tag.
    $(".custom-search-tag-container").on("click", ".custom-search-tag", function() {
        $(this).remove();
    });

    // Search Tab: Reset options.
    $("#reset").click(function(event) {
        event.preventDefault();
        $("#searchterms").val("");
        $(".custom-search-tag-container").children(".custom-search-tag").remove();
        InitTags();
    });

    // Search Tab: Submit search.
    $("#searchform").submit(function(event) {
        event.preventDefault();
        $.post("/blog/search", $("#searchform").serialize()).done(function(data) {
            resObj = JSON.parse(data);
            if (resObj.resCode === 0) {
                $("div#custom-search-result-count").html("");
                $("div#custom-search-result-list").children().remove();
                appendSearchBlog(resObj.data);
            } else {
                alert(resObj.resMsg);
            }
        });
    });

    // Home Tab: Load more blogs... 
    $("div#search").on("click", "button#custom-search-loadmore", function() {
        var nextp = $(this).attr("nextpage");
        var off = $(this).attr("offset");
        $.post("/blog/search/loadmore/" + nextp + "?off=" + off, 
            $("#searchform").serialize()).done(function(data) {
            resObj = JSON.parse(data);
            if (resObj.resCode === 0) {
                $("div.custom-search-nextab").remove();
                appendSearchBlog(resObj.data);
            } else {
                alert(resObj.resMsg);
            }
        });
    });

    // Search Tab: Append blog for search/loadmore
    function appendSearchBlog(blogdata) {
        // Show counts of search result
        insertHTML = "Search Result: <strong>" + blogdata.count + "</strong> articles found.";
        $("div#custom-search-result-count").html(insertHTML);
        // Append blogs
        for (id=0; id<blogdata.bloglist.length; id++) {
            insertHTML = "<div class=\"custom-search-blog-wrap\">" +
                "<hr class=\"mt-3 mb-3 mt-lg-5 mb-lg-5\">";
            insertHTML += "<div class=\"custom-blog-title mb-4\">" +
                "<span class=\"h3\">" +
                blogdata.bloglist[id].title + "</span><small><a href=\"" + 
                blogdata.bloglist[id].id +
                "\" class=\"blog-edit\">Edit</a></small></div>" +
                "<div class=\"mb-3\"><ul class=\"list-inline\">" +
                "<li class=\"list-inline-item\"><span>" +
                blogdata.bloglist[id].time + "</span></li>";
            for(tagid=0; tagid<blogdata.bloglist[id].tags.length; tagid++) {
                insertHTML += "<li class=\"list-inline-item\">" +
                    "<span class=\"badge badge-pill badge-warning\">" +
                    blogdata.bloglist[id].tags[tagid] + "</span></li>";
            }
            insertHTML += "</ul></div><div class=\"custom-blog-content\">" +
                blogdata.bloglist[id].content + "</div></div>";
            $("div#custom-search-result-list").append($(insertHTML));
        }
        if (blogdata.nextpage > 0) {
            insertHTML = "<div class=\"mt-3 mb-3 mt-lg-5 mb-lg-5 text-center custom-search-nextab\">" +
                "<button id=\"custom-search-loadmore\" class=\"btn btn-success\" nextpage=\"" + 
                blogdata.nextpage + "\" offset=\"" +
                blogdata.offset + "\">Load More ...</button></div>";
            $("div#custom-search-result-list").append($(insertHTML));
        }
    }
});
