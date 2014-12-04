w = 4000;
console.log(w)
var margin1 = {top: 20, right: 20, bottom: 30, left: 50},
    widthl = w - margin1.left - margin1.right,
    heightl = 500 - margin1.top - margin1.bottom;

//defines a function to be used to append the title to the tooltip.  you can set how you want it to display here.
var maketip = d3.tip()
  .attr('class', 'd3-tip')
  //.offset([-10, 0])
  .html(function(d) {
    return "<strong>Func:</strong> <span style='color:red'>" + d.request_id + "</span><br><strong>Time:</strong> <span style='color:red'>" + d.duration + "</span>";
  });


var x1 = d3.scale.ordinal()
    .rangePoints([10, widthl]);

var y1 = d3.scale.linear()
    .range([heightl, 0]);


var x1Axis = d3.svg.axis()
    .scale(x1)
    .orient("bottom");

var y1Axis = d3.svg.axis()
    .scale(y1)
    .orient("left");

var line1 = d3.svg.line()
    .x(function(d) { return x1(d.request_id); })
    .y(function(d) { return y1(d.duration); });

//d3.select("#svg-line").remove();

var svg1 = d3.select(".rallychart").append("svg")
    .attr("id", "svg-line")
    .attr("width", widthl + margin1.left + margin1.right)
    .attr("height", heightl + margin1.top + margin1.bottom)
  .append("g")
    .attr("transform", "translate(" + margin1.left + "," + margin1.top + ")");

  jQuery.ajax(
   {
      type: "GET",
      url: 'http://127.0.0.1:8989/rally',
      success: function(data1) {
  data1 = data1["body"];
  console.log(data1);
  for(var i=0;i<data1.length;i++){
      data1[i].request_id = i+1;
      data1[i].duration = data1[i].duration;  
};

var svg2 = svg1.append("g")
    .attr("class", "thegraph")

svg2.call(maketip);  
  
  x1.domain(data1.map(function(d) { return d.request_id; }));
  y1.domain([0, d3.max(data1, function(d) { return d.duration; })]);

  svg1.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + heightl + ")")
      .call(x1Axis);

  svg1.append("g")
      .attr("class", "y axis")
      .call(y1Axis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("time");

  svg1.append("path")
      .datum(data1)
      .attr("class", "line1")
      .attr("d", line1);

  svg2.selectAll("thegraph").data(data1).enter().append("circle")
	                .attr("class","tipcircle")
	                .attr("cx", function(d){return x1(d.request_id)})
	                .attr("cy",function(d){return y1(d.duration)})
	                .attr("r",18)
	                .style('opacity', 1e-6)//1e-6
	                .on("mouseover", maketip.show)
	                .on("mouseout", maketip.hide);
}});


