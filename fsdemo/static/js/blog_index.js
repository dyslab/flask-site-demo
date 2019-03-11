$(document).ready(function() {
    $(".top-menuitem.nav-link:eq(2)").addClass("active");

    // Initialize markdown editor and tags in Search Tab.
    var simplemde = new SimpleMDE({ element: $("#blogcontent")[0] });
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
        jquery.append($(insertHTML).slideDown(500).delay(3000).fadeOut(500));
        setTimeout(function () {
            ChangeActiveTab(0);
        }, 3500);
    }

    // Home Tab: Blog's 'Edit' button click function
    $("div#home").on("click", "a.blog-edit", function(event) {
        event.preventDefault();
        alert($(this).attr("href"));
        ChangeActiveTab(1);
    });

    // Home Tab: Blog's 'Delete' button click function
    $("div#home").on("click", "a.blog-delete", function(event) {
        event.preventDefault();
        if (confirm("Are you sure to delete this blog?")) {
            alert($(this).attr("href"));
        }
    });

    // Home Tab: Append blog for loadmore
    function appendBlog(data) {
        if (data.resCode === 0) {
            blogdata = data.data;
            for (id=0; id<blogdata.bloglist.length; id++) {
                insertHTML = "<div class=\"blog-wrap\">" +
                    "<hr class=\"mt-3 mb-3 mt-lg-5 mb-lg-5\">";
                insertHTML += "<div class=\"custom-blog-title mb-4\">" +
                    "<span class=\"h3\">" +
                    blogdata.bloglist[id].title + "</span><small><a href=\"" + 
                    blogdata.bloglist[id].id +
                    "\" class=\"blog-edit\">Edit</a></small></div>" +
                    "<div class=\"row mb-3\">" +
                    "<div class=\"col-5 col-sm-3 col-md-2 custom-blog-time\">" +
                    blogdata.bloglist[id].time + "</div>" +
                    "<div class=\"col-7 col-sm-9 col-md-10 custom-blog-tags\">" +
                    "<ul class=\"list-inline\">";
                for(tagid=0; tagid<blogdata.bloglist[id].tags.length; tagid++) {
                    insertHTML += "<li class=\"list-inline-item\">" +
                        "<span class=\"badge badge-pill badge-warning\">" +
                        blogdata.bloglist[id].tags[tagid] + "</span></li>";
                }
                insertHTML += "</ul></div></div>" +
                    "<div class=\"custom-blog-content\">" +
                    blogdata.bloglist[id].content + "</div>";
                insertHTML += "<div class=\"text-right\"><small><a href=\"" + 
                    blogdata.bloglist[id].id +
                    "\" class=\"blog-delete\">Delete</a></small></div></div>";
                $("div#home").append($(insertHTML));
            }
            if (blogdata.nextpage > 0) {
                insertHTML = "<div class=\"mt-3 mb-3 mt-lg-5 mb-lg-5 text-center nextab\">" +
                    "<button id=\"loadmore\" class=\"btn btn-success\" nextpage=\"" + 
                    blogdata.nextpage + "\">Load More ...</button></div>";
                $("div#home").append($(insertHTML));
            }
        }
    }

    // Home Tab: Load more blogs... 
    $("div#home").on("click", "button#loadmore", function() {
        var nextp = $(this).attr("nextpage");
        $.get('/blog/loadmore/' + nextp, function(data) {
            $("div.nextab").remove();
            appendBlog(JSON.parse(data));
        });
    });

    // Write Tab: Ajax submit new blog.
    $("#writeform").submit(function(event) {
        event.preventDefault();
        $.post('/blog/new', $("#writeform").serialize()).done(function(data) {
            resObj = JSON.parse(data);
            if (resObj.resCode === 0) {
                SetResponse($("#writetabresponse"), resObj.resMsg);
            } else {
                alert(resObj.resMsg);
            }
        });      
    });

    // Search Tab: Initialize tags.
    function InitTags() {
        $("#taglist").children(".custom-option-tag").each(function() {
            if ($(this).val() !== "") {
                $(".custom-blog-search-tag-container").append($("<li class=\"list-inline-item custom-blog-search-tag\">" +
                    "<span class=\"badge badge-pill badge-warning\">" +
                    $(this).val() + " &times;</span></li>")); 
            }
        });
    }

    // Search Tab: Remove tag.
    $(".custom-blog-search-tag-container").on("click", ".custom-blog-search-tag", function() {
        $(this).remove();
    });

    // Search Tab: Reset options.
    $("#reset").click(function() {
        $("#searchterms").val("");
        $(".custom-blog-search-tag-container").children(".custom-blog-search-tag").remove();
        InitTags();
    });
});
