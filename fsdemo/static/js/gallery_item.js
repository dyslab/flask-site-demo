$(document).ready(function() {
    $(".top-menuitem.nav-link:eq(1)").addClass("active");
    
    // Init form upload file elements.
    bsCustomFileInput.init();
    resetFormFile($("#photo"), $(".custom-file-label"));

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
        insertHTML = "<div class=\"alert alert-warning alert-dismissible mb-3 fade show\" role=\"alert\"><strong>" +
            msg + "</strong><button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\">" +
            "<span aria-hidden=\"true\">&times;</span></button></div>";
        $("#response").append($(insertHTML).delay(2000).fadeOut(500));
        insertHTML = "<div><figure class=\"figure\"><img src=\"" +
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
        $("#preview").empty();
        if(!isValidFileExtension(filename)) {
            alert('Select IMAGE file please.');
            resetFormFile($("#photo"), $(".custom-file-label"));
        }
        else {
            const img = document.createElement("img");
            img.file = $(this);
            img.classList.add('custom-upload-image-preview'); // CSS style comes from "/static/css/style.css"
            $("#preview").append(img);
            // preview.appendChild(img); // Assuming that "preview" is the div output where the content will be displayed.
            const reader = new FileReader();
            reader.onload = (e) => {
                img.src = e.target.result;
            };
            reader.readAsDataURL(document.getElementById('photo').files[0]);
        }
    });

    // Ajax upload file.
    $("#uploadform").submit(function(event) {
        event.preventDefault();
        var photoid = parseInt($("input#photoid").val());

        if (photoid > 0) {
            // Edit save process.
            $.post('/gallery/edit/save/' + photoid, $(this).serialize()).done(function(data) {
                resObj = JSON.parse(data);
                if (resObj.resCode === 0) {
                    insertHTML = "<div class=\"alert alert-warning alert-dismissible mt-3 fade show\" role=\"alert\"><strong>" +
                        resObj.resMsg + "</strong><button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\">" +
                        "<span aria-hidden=\"true\">&times;</span></button></div>";
                    $("#response").append($(insertHTML).delay(2000).fadeOut(500));
                } else {
                    alert(resObj.resMsg);
                }
            });
        } else {
            // Upload process.
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
        }
    });
});
