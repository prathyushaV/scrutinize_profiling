/*body {
  font: 10px sans-serif;
}

.axis path,
.axis line {
  fill: none;
  stroke: #000;
  shape-rendering: crispEdges;
}

.x.axis path {
  display: none;
}

.line {
  fill: none;
  stroke: steelblue;
  stroke-width: 1.5px;
}

</style>
<script src="d3.v3.min.js"></script>
<script src="jquery.min.js"></script>
<script>*/

var margin = {top: 20, right: 20, bottom: 30, left: 50},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var x = d3.scale.ordinal()
    .rangeRoundBands([0, width], .2);

var y = d3.scale.linear()
    .rangeRound([height, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");

var line = d3.svg.line()
    .x(function(d) { return x(d.request_id); })
    .y(function(d) { return y(d.time); });

var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

//d3.tsv("data.tsv", function(error, data) {
//  data.forEach(function(d) {
//    d.date = parseDate(d.date);
//   d.close = +d.close;
//  });
var dt = Object();

jQuery.ajax(
   {
      type: "GET",
      //url: 'http://127.0.0.1:8989/',
      url: './root.json',
      success: function(data) {  
           //console.log(data['body']);
           //console.log(data.length)
           //console.log(data["request_id"])
        
      //for(var ) {
         //d.req_id = (data["request_id"]);
         //d.time = data["time"];
     //});
  //for( var i=0 ; i< data['body'].length; i++){
  //     console.log(data['body'][i]['request_id']);
  //     dt. = data['body'][i]['request_id'];
  //     dt['time'] = data['body'][i]['time'];
  
  data = data["body"]

  /*data.forEach(function(d) {
     d.request_id = d.request_id;
     //d.time = d.time;
  });*/

  x.domain(d3.extent(data, function(d) {/* alert(d.request_id);*/ return d.request_id; }));
  y.domain(d3.extent(data, function(d) { return d.time; }));
 
  //alert(xAxis);
  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);
      
      //.attr("x", 6)
      //.attr("dx", "1.71em")
      //.text("Request_id");
  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("time");


  svg.append("path")
      .datum(data)
      .attr("class", "line")
      .attr("d", line);
}
}
);

/*</script>*/
