function moviedata(movie) {
    var url = "/movies/" + `${movie}`;

    // Use d3 to select the div panel with class of `#jumbotron`
    var movie_data_title = d3.select("body > div > div:nth-child(1) > div.col-lg-8 > div > div:nth-child(1) > div");
    var movie_data_img = d3.select("body > div > div:nth-child(1) > div.col-lg-8 > div > div:nth-child(2) > div:nth-child(1)");
    var movie_data = d3.select("body > div > div:nth-child(1) > div.col-lg-8 > div > div:nth-child(2) > div:nth-child(2)");

    d3.json(url).then(function (response) {
        // Use `.html("") to clear any existing data
        movie_data.html("");

        movie_data_title.selectAll('h1')
            .data(response)
            .enter()
            .append('h1')
            .attr('class', 'title_heading')
            .text(response[0].Title);

        movie_data_img.selectAll('img')
            .data(response)
            .enter()
            .append('img')
            .attr('src', response[0].Poster_Image)
            .attr('height', 'auto')
            .attr('width', 'auto');

        //movie_data.selectAll('p')
        //    .data(response)
        //    .enter()
        //    .append('p')
        //    .text(response[0].)
    });
}

function movieRecommender(movie) {
    var movieList_url = "/movie_recommendation/" + `${movie}`

    var carousel_1 = d3.select("#demo > div > div:nth-child(1)");
    var carousel_2 = d3.select("#demo > div > div:nth-child(2)");
    var carousel_3 = d3.select("#demo > div > div:nth-child(3)");

    var carousel_group = [carousel_1, carousel_2, carousel_3];

    d3.json(movieList_url).then(function (movieList) {
        carousel_1.html("");
        carousel_2.html("");
        carousel_3.html("");

        movieList.forEach(searchMovie);
        let carousel_count = 0;

        function searchMovie(movie) {
            var movie_url = "/movies/" + `${movie}`;

            d3.json(movie_url).then(function (response) {
                if (carousel_group[carousel_count]._groups[0][0].childElementCount < 7) {
                    console.log(carousel_group[carousel_count]);
                    carousel_group[carousel_count].selectAll('div')
                        .data(response)
                        .enter()
                        .append('div')
                        .attr('class', 'col-xs-2 col-sm-2 col-md-2')
                        .append('p')
                        .text(response[0].Title);
                }

                else {
                    carousel_count++;
                }
            });
        }
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
    movieRecommender(firstmovie);
  });
}

// Initialize the dashboard
init();

function optionChanged(newMovie) {
    // Fetch new data each time a new movie is selected
    //moviedata(newMovie)
    movieRecommender(newMovie)
}   

//$('select').on('change', function () {
//    var team = this.value;
//    localStorage.setItem("x", team);
//});