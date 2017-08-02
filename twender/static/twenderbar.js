/*
 * twenderbar.js
 *
 * javascript to create a d3 stacked, horizontal, bar chart of the male/female tweets for the
 * searched for user
 *
 */

window.addEventListener('load', function () {

    console.log("loaded");
    var femaleTweets = d3.selectAll('.tweet.girl'),
        maleTweets = d3.selectAll('.tweet.boy'),
        numFemale = femaleTweets.size(),
        numMale = maleTweets.size(),
        totalTweets = numFemale + numMale,
        tweetData = [ { 'male': numMale / totalTweets, 'female': numFemale / totalTweets } ];

    console.log('Female Tweets', numFemale,
                'Male Tweets', numMale,
                'All Tweets', totalTweets);

    // make sure we have some tweets to count and use
    // for the bar chart
    if(totalTweets){
        var margin = {top: 20, right: 20, bottom: 20, left: 20},
            width = 400 - margin.left - margin.right,
            height = 200 - margin.top - margin.bottom;

        var y = d3.scaleBand()
            .rangeRound([height, 0]);

        var x = d3.scaleLinear()
            .rangeRound([0, width]);

        // use baby blue and pink for colors
        var color = d3.scaleOrdinal()
            .range(["#89cff0", "#ffb6c1"]);

        var svg = d3.select(".pie-container").append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


        var layers = d3.stack()
            .keys(['male', 'female'])
            .offset(d3.stackOffsetExpand)(tweetData);

        console.log(layers);

        y.domain(layers[0].map(function(d) { return d.x; }));

        var layer = svg.selectAll(".layer")
            .data(layers)
            .enter().append("g")
            .attr("class", "layer")
            .style("fill", function(d, i) { return color(i); });

        layer.selectAll("rect")
            .data(function(d) { return d; })
            .enter().append("rect")
            .attr("x", function(d) { return x(d[0]); })
            .attr("y", function(d) { return 0; })
            .attr("width", function(d) { return x(d[1]) - x(d[0]); })
            .attr("height", y.bandwidth());

        //svg.append("g")
        //    .attr("class", "axis axis--y")
        //    .attr("transform", "translate(0,0)")
        //    .call(d3.axisLeft(y));

        svg.append("g")
            .attr("class", "axis axis--x")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x).ticks(10, '%'));

    }
});


