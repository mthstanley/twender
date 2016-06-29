/*
 * twenderpie.js
 *
 * javascript to create a d3 pie chart of the male/female tweets for the
 * searched for user
 *
 * based on http://bl.ocks.org/mbostock/3887235 for basic pie chart and
 * http://bl.ocks.org/mbostock/5100636 for animation
 */

window.addEventListener('load', function () {

    console.log("loaded");
    var femaleTweets = d3.selectAll('.tweet.girl')[0],
        maleTweets = d3.selectAll('.tweet.boy')[0],
        tweets = femaleTweets.concat(maleTweets),
        numFemale = femaleTweets.length,
        numMale = maleTweets.length,
        tweetData = [ {'gender': 'male', 'numTweets': numMale},
                      {'gender': 'female', 'numTweets': numFemale} ];

    console.log('Female Tweets', femaleTweets.length,
                'Male Tweets', maleTweets.length,
                'All Tweets', tweets.length);

    // make sure we have some tweets to count and use
    // for the pie chart
    if(tweets.length){
        console.log(tweets.length);
        var width = 400,
            height = 400,
            radius = Math.min(width, height) / 2;

        // use baby blue and pink for colors
        var color = d3.scale.ordinal()
            .range(["#89cff0", "#ffb6c1"]);

        var arc = d3.svg.arc()
            .outerRadius(radius - 10)
            .innerRadius(0);

        var labelArc = d3.svg.arc()
            .outerRadius(radius - 40)
            .innerRadius(radius - 40);

        var pie = d3.layout.pie()
            .sort(null)
            .startAngle(0)
            .endAngle(2*Math.PI)
            .value(function(d) { return d.numTweets; });

        var svg = d3.select(".pie-container").append("svg")
            .attr("width", width)
            .attr("height", height)
            .append("g")
            .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

        // create a group element to hold the arcs
        var g = svg.selectAll(".arc")
            .data(pie(tweetData))
            .enter().append("g")
            .attr("class", "arc");

        g.append("path")
          .style("fill", function(d) { return color(d.data.gender); })
          .transition().delay(function(d,i){ return i*1000; }).duration(500)
          .attrTween('d', function(d) {
            // interpolate between 0 and 2pi to achieve on load animation
            var interpolate = d3.interpolate(d.startAngle, d.endAngle);
            return function(t) {
                d.endAngle = interpolate(t);
                return arc(d);
            }
          });

        g.append("text")
          .attr("transform", function(d) { return "translate(" + labelArc.centroid(d) + ")"; })
          .attr("dy", ".35em")
          .attr("fill-opacity", 0).transition().delay(1500).duration(700)
          .attr("fill-opacity", 1)
          .text(function(d) { 
            return d.data.gender + ' ' + 
                Math.round(d.data.numTweets / tweets.length * 100)  + '%'; 
          });
    }
});


