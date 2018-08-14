function displayResults(data) {
    var results = JSON.parse(data);
    console.log(data);
  }

$( document ).ready(function() {
    const searchForm = document.getElementById('search-form');
    const searchUrl = '/api/search';
    /* listen for form submit */
    $(searchForm).on('submit', function(e){
      console.log( $( this ).serialize() );
      e.preventDefault();
      const searchReq = $( this ).serialize();
      $.getJSON("https://ide50-richardsa1.cs50.io:8080/api/search?" + searchReq, function(json) {
        console.log(json.length);
        let html = ""
          if(json === 'Unable to find any books.'){
              html += '<div class="alert alert-danger col" role="alert">'
              html += json;
              html += '</div>'
          } else {
            for (var i = 0; i < json.length; i++) {
              html += "<div class='result'>";
              html += "<a href='books/" + json[i].id + "'><h3 class='resultTitle'>" + json[i].title + "</h3></a>";
              html += "<div class='resultSnippet'>" + json[i].author + "</br>"
              html += json[i].year + "</br>"
              html += json[i].isbn + "</div>"
              html += "</div>";

            }
        }
        $("#results").html(html);
        });

  });

/* document ready closing tag */
});