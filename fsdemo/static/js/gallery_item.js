$(document).ready(function() {
    $(".top-menuitem.nav-link:eq(1)").addClass("active");
    
    // Init form upload file elements.
    bsCustomFileInput.init();
    resetFormFile($("#photo"), $(".custom-file-label"));
    var defaultResponse = $("#response").html();

    // Validate upload file extension.
    function isValidFileExtension(filename) {
        var validFileExtensionList = ".jpg|.jpeg|.gif|.svg|.png";
        if (validFileExtensionList.search(filename.slice(-4).toLocaleLowerCase()) >= 0) {
            return true;
        } else {
            return false;
        }
    }

    // Empty form file object and its label object.
    function resetFormFile(fileobj, labelobj) {
        fileobj.val("");
        labelobj.text("JPG/JPEG/GIF/SVG/PNG accepted");
    }

    // Set response content.
    function setResponse(msg, data) {
        $("#response").children().remove();
        insertHTML = "<div class=\"alert alert-warning alert-dismissible fade show\" role=\"alert\"><strong>" +
            msg + "</strong><button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\">" +
            "<span aria-hidden=\"true\">&times;</span></button></div>";
        insertHTML += "<div><figure class=\"figure\"><img src=\"" +
            data.link + "\" class=\"figure-img img-fluid rounded\" alt=\"" +
            data.link + "\"><figcaption class=\"figure-caption\">" +
            data.caption + "</figcaption></figure></div>"
        insertHTML += "<div><ul class=\"list-inline\">" +
            "<li class=\"list-inline-item\">Tags: </li>";
        for (index in data.tags) {
            insertHTML += "<li class=\"list-inline-item\"><span class=\"badge badge-primary\">" +
                data.tags[index] + "</span></li>";
        }
        insertHTML += "</ul></div>";

        $("#response").append($(insertHTML));
    }

    // Validate form file when its content changed.
    $("#photo").change(function () {
        var filename = $(this).val();
        if(!isValidFileExtension(filename)) {
            alert('Select IMAGE file please.');
            resetFormFile($("#photo"), $(".custom-file-label"));
        }
    });

    // Ajax upload file.
    $("#uploadform").submit(function(event) {
        event.preventDefault();

        var formData = new FormData($(this)[0]);
        $.ajax({
            url: "/gallery/do/upload",
            type: "POST",
            data: formData,
            async: true, // false,
            cache: false,
            contentType: false,
            processData: false,
        }).done(function(data) {
            resObj = JSON.parse(data);
            if (resObj.resCode === 0) {
                setResponse(resObj.resMsg, resObj.data);
            } else {
                alert(resObj.resMsg);
            }
            resetFormFile($("#photo"), $(".custom-file-label"));
        }).fail(function(err) {
            alert(err);
        });
    });
});
