function moviedata(movie) {
    var url = "/movies/" + `${movie}`;

    // Use d3 to select the div panel with class of `#jumbotron`
    var movie_data = d3.select("div.jumbotron");

    d3.json(url).then(function (response) {
        // Use `.html("") to clear any existing data
        movie_data.html("");

        movie_data.select('h1')
            .data(response)
            .enter()
            .append('h1')
            .attr('class', 'title_heading')
            .text(response.movie_title);

        movie_data.select('img')
            .data(response)
            .enter()
            .append('img')
            .attr('src', response.img);
    });
}

function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#dataSet");

  // Use the list of movies to populate the select options
  d3.json("/movie_title").then((movie_list) => {
    movie_list.forEach((movie) => {
      selector
        .append("option")
        .text(movie)
        .property("value", movie);
    });

    // Use the first movie to initialize
    const firstmovie = movie_list[0][0];
    moviedata(firstmovie);
  });
}

// Initialize the dashboard
init();

function optionChanged(newMovie) {
    // Fetch new data each time a new movie is selected
    moviedata(newMovie)
}   

//$('select').on('change', function () {
//    var team = this.value;
//    localStorage.setItem("x", team);
//});