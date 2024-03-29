// ################### ADD_TRICK.js ###################
// ################### EDIT_TRICK.js ###################
// Show Preview Screen
function showPreview(){
    var viewport = document.getElementById('screen');
    var htmlInput = document.getElementById('html_input').value
    var cssInput = document.getElementById('css_input').value
    var jsInput = document.getElementById('js_input').value
    var scale = document.getElementById('scale').value

    // Clear existing content
    viewport.innerHTML = "";

    // Create new iframe element
    var iframe = document.createElement("iframe");
    iframe.style.width = "100%";
    iframe.style.height = "100%";
    iframe.style.border = "0";
    viewport.appendChild(iframe);

    // Write HTML and CSS to the iframe document
    var doc = iframe.contentDocument || iframe.contentWindow.document;
    doc.open();
    doc.write("<body>" + htmlInput + "</body>");
    doc.write("<style> body{transform: scale("+scale+"); background-color:black; overflow: hidden;}" + cssInput + "</style>");
    doc.write("<script>" + jsInput + "</" + "script>");
    doc.close();
}

// Character Count
var trickNameInput = document.getElementById('trickNameInput');
var trickNameCharCount = document.getElementById('trickNameCharCount');
var trickDescriptionInput = document.getElementById('trickDescriptionInput');
var trickDescriptionCharCount = document.getElementById('trickDescriptionCharCount');

function countChar(){
    var nameCount = trickNameInput.value.length;
    var descriptionCount = trickDescriptionInput.value.length;
    trickNameCharCount.innerText = nameCount;
    trickDescriptionCharCount.innerText = descriptionCount;
}

// Validate Trick
function validateTrick(){
    var validate = document.getElementById('validate');
    validate.onsubmit = function(e){
        e.preventDefault();
        var form = new FormData(validate);
        fetch('/create/trick', { method :'POST', body : form})
        .then( response => response.json() )
        .then( msgs => {
                if (msgs.length == 0){
                    window.location.href = "/home";
                }
                var validation_msgs = document.getElementById('validation_msgs');
                while (validation_msgs.firstChild) {
                    validation_msgs.removeChild(validation_msgs.firstChild);
                }
                for (var i=0; i< msgs.length; i++){
                    let message = document.createElement('p');
                    message.innerText = msgs[i];
                    validation_msgs.appendChild(message);
                }
            } )
    }
}

// ################### INDEX.js ##################
// ################### HOME.js ###################
// Get Tricks & Make Screen
function get_tricks(){
    fetch('/get/tricks', {
        headers: {
            'X-Requested-With': 'XMLHttpRequest' // Add a custom header to indicate the request is from JavaScript
        }
    })
        .then(response => response.json())
        .then(tricks => {
            for(i = 0; i<tricks.length; i++){
                if(tricks[i].is_private == 0){
                    var viewport = document.getElementById("trick_id_"+tricks[i].id);
                
                    // Decodes the code to be written into iframe document
                    var decodedHtml = decodeURIComponent(tricks[i].html);
                    var decodedCss = decodeURIComponent(tricks[i].css);
                    var decodedJs = decodeURIComponent(tricks[i].js);
                    decodedHtml = decodedHtml.replaceAll("xyz956zyx","Select");
                    decodedHtml = decodedHtml.replaceAll("abc452cba","select");
                    decodedCss = decodedCss.replaceAll("xyz956zyx","Select");
                    decodedCss = decodedCss.replaceAll("abc452cba","select");
                    decodedJs = decodedJs.replaceAll("xyz956zyx","Select");
                    decodedJs = decodedJs.replaceAll("abc452cba","select");
                    // Clear existing content
                    // viewport.innerHTML = "";
                
                    // Create new iframe element
                    var iframe = document.createElement("iframe");
                    iframe.style.width = "100%";
                    iframe.style.height = "100%";
                    iframe.style.border = "0";
                    viewport.appendChild(iframe);

                    // Create transparent overlay element
                    var overlay = document.createElement("div");
                    overlay.style.position = "absolute";
                    overlay.style.top = "10%";
                    overlay.style.left = "0";
                    overlay.style.width = "400px";
                    overlay.style.height = "225px";
                    overlay.style.backgroundColor = "transparent";
                    viewport.appendChild(overlay);

                
                    // Write HTML and CSS to the iframe document
                    var doc = iframe.contentDocument || iframe.contentWindow.document;
                    doc.open();
                    doc.write("<body>" + decodedHtml + "</body>");
                    doc.write("<style> body{transform: scale("+ tricks[i].scale +"); background-color:black; background-image: radial-gradient(#B0F8CD20 1px, transparent 1px); background-position: 50% 50%; background-size: 20px 20px; overflow: hidden;}" + decodedCss + "</style>");
                    doc.write("<script>" + decodedJs + "</" + "script>");
                    doc.close();
                }
            }
        });
}

// ################### PROFILE.js ##################
// Get Other's Tricks and make Screen
function getOtherTricks(){
    fetch('/get/other_tricks', {
        headers: {
            'X-Requested-With': 'XMLHttpRequest' // Add a custom header to indicate the request is from JavaScript
        }
    })
        .then(response => response.json())
        .then(tricks => {
            for(i = 0; i<tricks.length; i++){
                
                    var viewport = document.getElementById("trick_id_"+tricks[i].id);
                
                    // Decodes the code to be written into iframe document
                    var decodedHtml = decodeURIComponent(tricks[i].html);
                    var decodedCss = decodeURIComponent(tricks[i].css);
                    var decodedJs = decodeURIComponent(tricks[i].js);
                    decodedHtml = decodedHtml.replaceAll("xyz956zyx","Select");
                    decodedHtml = decodedHtml.replaceAll("abc452cba","select");
                    decodedCss = decodedCss.replaceAll("xyz956zyx","Select");
                    decodedCss = decodedCss.replaceAll("abc452cba","select");
                    decodedJs = decodedJs.replaceAll("xyz956zyx","Select");
                    decodedJs = decodedJs.replaceAll("abc452cba","select");
                    // Clear existing content
                    // viewport.innerHTML = "";
                
                    // Create new iframe element
                    var iframe = document.createElement("iframe");
                    iframe.style.width = "100%";
                    iframe.style.height = "100%";
                    iframe.style.border = "0";
                    viewport.appendChild(iframe);

                    // Create transparent overlay element
                    var overlay = document.createElement("div");
                    overlay.style.position = "absolute";
                    overlay.style.top = "10%";
                    overlay.style.left = "0";
                    overlay.style.width = "400px";
                    overlay.style.height = "225px";
                    overlay.style.backgroundColor = "transparent";
                    viewport.appendChild(overlay);
                
                    // Write HTML and CSS to the iframe document
                    var doc = iframe.contentDocument || iframe.contentWindow.document;
                    doc.open();
                    doc.write("<body>" + decodedHtml + "</body>");
                    doc.write("<style> body{transform: scale("+ tricks[i].scale +"); background-color:black; background-image: radial-gradient(#B0F8CD20 1px, transparent 1px); background-position: 50% 50%; background-size: 20px 20px; overflow: hidden; }" + decodedCss + "</style>");
                    doc.write("<script>" + decodedJs + "</" + "script>");
                    doc.close();
                }
        });
}

// ################### GUEST_PROFILE.js ##################
// Get Other's Tricks and make Screen
function guestGetOtherTricks(){
    fetch('/guest/get/other_tricks', {
        headers: {
            'X-Requested-With': 'XMLHttpRequest' // Add a custom header to indicate the request is from JavaScript
        }
    })
        .then(response => response.json())
        .then(tricks => {
            for(i = 0; i<tricks.length; i++){
                if (tricks[i].is_private == 0){
                    var viewport = document.getElementById("trick_id_"+tricks[i].id);
                
                    // Decodes the code to be written into iframe document
                    var decodedHtml = decodeURIComponent(tricks[i].html);
                    var decodedCss = decodeURIComponent(tricks[i].css);
                    var decodedJs = decodeURIComponent(tricks[i].js);
                    decodedHtml = decodedHtml.replaceAll("xyz956zyx","Select");
                    decodedHtml = decodedHtml.replaceAll("abc452cba","select");
                    decodedCss = decodedCss.replaceAll("xyz956zyx","Select");
                    decodedCss = decodedCss.replaceAll("abc452cba","select");
                    decodedJs = decodedJs.replaceAll("xyz956zyx","Select");
                    decodedJs = decodedJs.replaceAll("abc452cba","select");
                    // Clear existing content
                    // viewport.innerHTML = "";
                
                    // Create new iframe element
                    var iframe = document.createElement("iframe");
                    iframe.style.width = "100%";
                    iframe.style.height = "100%";
                    iframe.style.border = "0";
                    viewport.appendChild(iframe);

                    // Create transparent overlay element
                    var overlay = document.createElement("div");
                    overlay.style.position = "absolute";
                    overlay.style.top = "10%";
                    overlay.style.left = "0";
                    overlay.style.width = "400px";
                    overlay.style.height = "225px";
                    overlay.style.backgroundColor = "transparent";
                    viewport.appendChild(overlay);
                
                    // Write HTML and CSS to the iframe document
                    var doc = iframe.contentDocument || iframe.contentWindow.document;
                    doc.open();
                    doc.write("<body>" + decodedHtml + "</body>");
                    doc.write("<style> body{transform: scale("+ tricks[i].scale +"); background-color:black; background-image: radial-gradient(#B0F8CD20 1px, transparent 1px); background-position: 50% 50%; background-size: 20px 20px; overflow: hidden; }" + decodedCss + "</style>");
                    doc.write("<script>" + decodedJs + "</" + "script>");
                    doc.close();
                }
            }
        });
}

// ################### FAVORITES.js ##################
// Get Favorite Tricks & Make Screen
function getFavoriteTricks(){
    fetch('/get/favorite_tricks', {
        headers: {
            'X-Requested-With': 'XMLHttpRequest' // Add a custom header to indicate the request is from JavaScript
        }
    })
        .then(response => response.json())
        .then(faveTricks => {
            for(i = 0; i<faveTricks.length; i++){
                if (faveTricks[i].is_private == 0){
                    var viewport = document.getElementById("trick_id_"+faveTricks[i].id);
                    // Decodes the code to be written into iframe document
                    var decodedHtml = decodeURIComponent(faveTricks[i].html);
                    var decodedCss = decodeURIComponent(faveTricks[i].css);
                    var decodedJs = decodeURIComponent(faveTricks[i].js);
                    decodedHtml = decodedHtml.replaceAll("xyz956zyx","Select");
                    decodedHtml = decodedHtml.replaceAll("abc452cba","select");
                    decodedCss = decodedCss.replaceAll("xyz956zyx","Select");
                    decodedCss = decodedCss.replaceAll("abc452cba","select");
                    decodedJs = decodedJs.replaceAll("xyz956zyx","Select");
                    decodedJs = decodedJs.replaceAll("abc452cba","select");
                    // Clear existing content
                    // viewport.innerHTML = "";
                
                    // Create new iframe element
                    var iframe = document.createElement("iframe");
                    iframe.style.width = "100%";
                    iframe.style.height = "100%";
                    iframe.style.border = "0";
                    viewport.appendChild(iframe);

                    // Create transparent overlay element
                    var overlay = document.createElement("div");
                    overlay.style.position = "absolute";
                    overlay.style.top = "10%";
                    overlay.style.left = "0";
                    overlay.style.width = "400px";
                    overlay.style.height = "225px";
                    overlay.style.backgroundColor = "transparent";
                    viewport.appendChild(overlay);
                
                    // Write HTML and CSS to the iframe document
                    var doc = iframe.contentDocument || iframe.contentWindow.document;
                    doc.open();
                    doc.write("<body>" + decodedHtml + "</body>");
                    doc.write("<style> body{transform: scale("+ faveTricks[i].scale +"); background-color:black; background-image: radial-gradient(#B0F8CD20 1px, transparent 1px); background-position: 50% 50%; background-size: 20px 20px; overflow: hidden; }" + decodedCss + "</style>");
                    doc.write("<script>" + decodedJs + "</" + "script>");
                    doc.close();
                }
            }
        });
}

// ################### SIGNUP.js ##################
// Validate Signup
function validate_signup(){
    var validate = document.getElementById('validate');
    validate.onsubmit = function(e){
        e.preventDefault();
        var form = new FormData(validate);
        fetch('/create/user', { method :'POST', body : form})
        .then( response => response.json() )
        .then( msgs => {
                // redirects page to welcome if there are no messages
                if (msgs.length == 0){
                    window.location.href = "/home";
                }
                var validation_msgs = document.getElementById('validation_msgs');
                // removes msgs if there are previously existing msgs
                while (validation_msgs.firstChild) {
                    validation_msgs.removeChild(validation_msgs.firstChild);
                }
                // creates message elements if there are messages
                for (var i=0; i< msgs.length; i++){
                    let message = document.createElement('p');
                    message.innerText = msgs[i];
    
                    validation_msgs.appendChild(message);
                }
            } )
    }
}
// ################### LOGIN.js ##################
// Validate login
function validate_login(){
    var validate = document.getElementById('validate');
    validate.onsubmit = function(e){
        e.preventDefault();
        var form = new FormData(validate);
        fetch('/login/user', { method :'POST', body : form})
        .then( response => response.json() )
        .then( msgs => {
                // redirects page to welcome if there are no messages
                if (msgs.length == 0){
                    window.location.href = "/home";
                }
                var validation_msgs = document.getElementById('validation_msgs');
                // removes msgs if there are previously existing msgs
                while (validation_msgs.firstChild) {
                    validation_msgs.removeChild(validation_msgs.firstChild);
                }
                // creates message elements if there are messages
                for (var i=0; i< msgs.length; i++){
                    let message = document.createElement('p');
                    message.innerText = msgs[i];
    
                    validation_msgs.appendChild(message);
                }
            } )
    }
}

// ################### FAVORATE BUTTONS ##################
function favoriteTrick(element){
    data = {
        'trickID' : element.id
    }
    fetch('/favorite/trick', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            if (data.is_favorited == true){
                    var newElement = document.createElement('p');
                    newElement.textContent = 'ADDED';
                    newElement.id = element.id;
                    newElement.className = 'mk-green';
                    newElement.style.fontSize = '8px'
                    element.replaceWith(newElement);
                    setTimeout(function() {
                        newElement.replaceWith(element);
                        element.src = "static/assets/star_filled.png";
                        }, 800)
            }
            else{
                var newElement = document.createElement('p');
                newElement.textContent = 'REMOVED';
                newElement.id = element.id;
                newElement.className = 'mk-green';
                newElement.style.fontSize = '8px'
                element.replaceWith(newElement);
                setTimeout(function() {
                    newElement.replaceWith(element);
                    element.src = "static/assets/star_empty.png";
                    }, 800)
            }
        })
}

function favoriteTrickProfile(element){
    data = {
        'trickID' : element.id
    }
    fetch('/favorite/trick', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            if (data.is_favorited == true){
                    var newElement = document.createElement('p');
                    var star_unfilled = document.querySelector('#star-unfilled');
                    console.log(star_unfilled.id)
                    newElement.textContent = 'ADDED';
                    newElement.style.marginRight = '5px';
                    newElement.id = element.id;
                    newElement.className = 'mk-green';
                    newElement.style.fontSize = '8px'
                    element.replaceWith(newElement);
                    setTimeout(function() {
                        newElement.replaceWith(element);
                        if (element.contains(star_unfilled)) {
                            element.removeChild(star_unfilled);
                        }
                        }, 800)
            }
            else{
                var newElement = document.createElement('p');
                var star_filling_id = document.createElement('div');
                var star_filling_class = document.createElement('div');
                star_filling_id.id = 'star-unfilled';
                star_filling_class.className = 'star-unfilled';
                newElement.textContent = 'REMOVED';
                newElement.id = element.id;
                newElement.className = 'mk-green';
                newElement.style.fontSize = '8px'
                element.replaceWith(newElement);
                setTimeout(function() {
                    newElement.replaceWith(element);
                    element.appendChild(star_filling_id);
                    star_filling_id.appendChild(star_filling_class);
                    }, 800)
            }
        })
}

// ################### FOLLOW BUTTON ##################
function followUser(element){
    var otherID = element.id.match(/\d+/)[0];
    data = {
        'otherID' : otherID
    }
    fetch('/follow/user', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => { 
            if (data.is_following == true){
                    element.innerText = "UNFOLLOW"
            }
            else{
                element.innerText = "FOLLOW"

            }
        })
}


// ################### SEARCH.JS ##################
// ################### GUEST_SEARCH.JS ##################
function submitSearch(){
    var form = document.getElementById('search-form');
    form.submit();
}

function getSearchTricks(){
    fetch('/get/search/tricks', {
        headers: {
            'X-Requested-With': 'XMLHttpRequest' // Add a custom header to indicate the request is from JavaScript
        }
    })
        .then(response => response.json())
        .then(tricks => {
            for(i = 0; i<tricks.length; i++){
                if (tricks[i].is_private == 0){

                    var viewport = document.getElementById("trick_id_"+tricks[i].id);
                
                    // Decodes the code to be written into iframe document
                    var decodedHtml = decodeURIComponent(tricks[i].html);
                    var decodedCss = decodeURIComponent(tricks[i].css);
                    var decodedJs = decodeURIComponent(tricks[i].js);
                    decodedHtml = decodedHtml.replaceAll("xyz956zyx","Select");
                    decodedHtml = decodedHtml.replaceAll("abc452cba","select");
                    decodedCss = decodedCss.replaceAll("xyz956zyx","Select");
                    decodedCss = decodedCss.replaceAll("abc452cba","select");
                    decodedJs = decodedJs.replaceAll("xyz956zyx","Select");
                    decodedJs = decodedJs.replaceAll("abc452cba","select");
                    // Clear existing content
                    // viewport.innerHTML = "";
                
                    // Create new iframe element
                    var iframe = document.createElement("iframe");
                    iframe.style.width = "100%";
                    iframe.style.height = "100%";
                    iframe.style.border = "0";
                    viewport.appendChild(iframe);

                    // Create transparent overlay element
                    var overlay = document.createElement("div");
                    overlay.style.position = "absolute";
                    overlay.style.top = "10%";
                    overlay.style.left = "0";
                    overlay.style.width = "400px";
                    overlay.style.height = "225px";
                    overlay.style.backgroundColor = "transparent";
                    viewport.appendChild(overlay);
                
                    // Write HTML and CSS to the iframe document
                    var doc = iframe.contentDocument || iframe.contentWindow.document;
                    doc.open();
                    doc.write("<body>" + decodedHtml + "</body>");
                    doc.write("<style> body{transform: scale("+ tricks[i].scale +"); background-color:black; background-image: radial-gradient(#B0F8CD20 1px, transparent 1px); background-position: 50% 50%; background-size: 20px 20px; overflow: hidden;}" + decodedCss + "</style>");
                    doc.write("<script>" + decodedJs + "</" + "script>");
                    doc.close();
                }
            }
        });
}

// ################### VIEW_TRICK.js ###################
function reply(commentID){
    var replyElement = document.getElementById('reply' + commentID);
    replyElement.style.display = 'contents';
}
function commentText(textArea){
    textArea.style.height = textArea.scrollHeight + "px";
}