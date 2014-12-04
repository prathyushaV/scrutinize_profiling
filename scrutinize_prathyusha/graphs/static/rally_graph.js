function rally_graph(){

/*var maketip = d3.tip()
  .attr('class', 'd3-tip')
 // .offset([-10, 0])
  .html(function(d) {
    return "<strong>Func:</strong> <span style='color:red'>" + d.request_id + "</span><br><strong>Time:</strong> <span style='color:red'>" + d.duration + "</span>";
  });*/

var margin = {top: 10, right: 10, bottom: 100, left: 40},
    margin2 = {top: 430, right: 10, bottom: 20, left: 40},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom,
    height2 = 500 - margin2.top - margin2.bottom;

var maketip = d3.tip()
  .attr('class', 'd3-tip')
 // .offset([-10, 0])
  .html(function(d) {
    return "<strong>Func:</strong> <span style='color:red'>" + d.request_id + "</span><br><strong>Time:</strong> <span style='color:red'>" + d.duration + "</span>";
  });



var x2 = d3.scale.linear().range([0, width]);
var x = d3.scale.linear().range([ 0,width]);
var y = d3.scale.linear().range([height, 0]);
var y2 = d3.scale.linear().range([height2, 0]);

//var x = d3.scale.ordinal()
//    .rangePoints([10, width]);

/*var x2 = d3.scale.ordinal()
    .rangePoints([10, width]);*/

var xAxis = d3.svg.axis().scale(x).orient("bottom"),//.tickValues(0,x.domain()),
    xAxis2 = d3.svg.axis().scale(x2).orient("bottom"),
    yAxis = d3.svg.axis().scale(y).orient("left");

var brush = d3.svg.brush()
    .x(x2)
    .on("brush", brushed);

/*var area = d3.svg.line()
    .x(function(d) { return x(d.request_id); })
    .y(function(d) { return y(d.duration); });

var area2 = d3.svg.line()
    .x(function(d) { return x2(d.request_id); })
    .y(function(d) { return y2(d.duration); });
*/
var area = d3.svg.area()
    .interpolate("monotone")
    .x(function(d) { return x(d.request_id); })
    .y0(height)
    .y1(function(d) { return y(d.duration); });

var area2 = d3.svg.area()
    .interpolate("monotone")
    .x(function(d) { return x2(d.request_id); })
    .y0(height2)
    .y1(function(d) { return y2(d.duration); });

var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom);

/*var svg2 = svg.append("g")
    .attr("class", "thegraph")

svg2.call(maketip);*/


svg.append("defs").append("clipPath")
    .attr("id", "clip")
  .append("rect")
    .attr("width", width)
    .attr("height", height);

var focus = svg.append("g")
    .attr("class", "focus")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var context = svg.append("g")
    .attr("class", "context")
    .attr("transform", "translate(" + margin2.left + "," + margin2.top + ")");


var svg2 = focus.append("g")
    .attr("class", "thegraph")

svg2.call(maketip);

//var data1 = null;
 jQuery.ajax(
   {
      type: "GET",
      //url: 'http://127.0.0.1:8989/rally',
      url: './json',
      success: function(data1) {
                data1 = data1["body"];
  		for(i=0;i<data1.length;i++){
      			data1[i].request_id = i+1;
      			//data1[i].duration = data1[i].duration;
                        //console.log(data1[i]);
		}

  //x.domain(data1.map(function(d) { return (d.request_id); }));
  x.domain([0, d3.max(data1, function(d) { return d.request_id; })]);  
  y.domain([0, d3.max(data1, function(d) { return d.duration; })]);  

x2.domain(x.domain());
  y2.domain(y.domain());

  focus.append("path")
      .datum(data1)
      .attr("class", "area")
      .attr("d", area);

  focus.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

  focus.append("g")
      .attr("class", "y axis")
      .call(yAxis);

  context.append("path")
      .datum(data1)
      .attr("class", "area")
      .attr("d", area2);

  context.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height2 + ")")
      .call(xAxis2);

  context.append("g")
      .attr("class", "x brush")
      .call(brush)
    .selectAll("rect")
      .attr("y", -6)
      .attr("height", height2 + 7);

  svg2.selectAll("thegraph").data(data1).enter().append("circle")
                        .attr("class","tipcircle")
                        .attr("cx", function(d){return x(d.request_id)})
                        .attr("cy",function(d){return y(d.duration)})
                        .attr("r",18)
                        .style('opacity', 0)//1e-6
                        .on("mouseover", maketip.show)
                        .on("mouseout", maketip.hide);

}

});
//});

function brushed() {
  x.domain(brush.empty() ? x2.domain() : brush.extent());
  focus.select(".area").attr("d", area);
  focus.select(".x.axis").call(xAxis);
  d3.select(".thegraph").remove();
  console.log(data1)  
svg2.selectAll("thegraph").data(data1).enter().append("circle")
                        .attr("class","tipcircle")
                        .attr("cx", function(d){return x(d.request_id)})
                        .attr("cy",function(d){return y(d.duration)})
                        .attr("r",18)
                        .style('opacity', 1e-6)//1e-6
                        .on("mouseover", maketip.show)
                        .on("mouseout", maketip.hide);

}

function type(d) {
  d.request_id = d.request_id;
  d.duration = d.duration;
  return d;
}

}
rally_graph()

