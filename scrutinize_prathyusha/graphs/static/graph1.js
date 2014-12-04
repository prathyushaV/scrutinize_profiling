var w = window.innerWidth;

var data;

function bar_graph(){
jQuery.ajax(
   {
      type: "GET",
      url: './json',
      success: function(data) {	
          key = Object.keys(data)[0]
	  data = data[key]
         //alert(data.length)
         //bar_width = data.length*70;
         if(data.length < 10)
	         bar_width = data.length*140;
         else 
		bar_width = w

         var margin = {top: 10, right: 30, bottom: 30, left: 40},
	  width = bar_width - margin.left - margin.right,
	  height = 350 - margin.top - margin.bottom;
	var barwidth = 30;
	var x = d3.scale.ordinal()
	    .rangeRoundBands([15, width], .05);

	var y = d3.scale.linear()
	    .range([height, 0]);

	var xAxis = d3.svg.axis()
	    .scale(x)
	    .orient("bottom");

	var yAxis = d3.svg.axis()
	    .scale(y)
	    .orient("left");

         //Create title 
	  d3.select(".barcharttitle").append("text")
		.attr("x", (margin.left /2))             
		.attr("y", 0 - (margin.top / 2))
		.style("margin-left", "40px")  
		.style("font-size", "18px") 
		.style("text-decoration", "bold")
                .attr("fill","grey")
                .text("Requests");
		//.text(key.toUpperCase());
	var chart = d3.select(".barchart").append("svg")
	    .attr("width", width + margin.left + margin.right)
	    .attr("height", height + margin.top + margin.bottom)
	  .append("g")
            .attr("fill","grey")
	    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	var tip = d3.tip()
	  .attr('class', 'd3-tip')
	  .offset([-10, 0])
	  .html(function(d) {
	    return "<strong>Time:</strong> <span style='color:red'>" + d.time + "</span>";
	  })

	chart.call(tip);

	  x.domain(data.map(function(d) { return d.request_id; }));
	  y.domain([0, d3.max(data, function(d) { return d.time; })]);
	  
	 
	  console.log(xAxis);
	  bar_width = -1*(250-(barwidth/2));
	  console.log(x.rangeBand());
	  chart.append("g")
	      .attr("class", "x axis")
	      .attr("transform", "translate(0," + height + ")")
	      .call(xAxis);
	      

	  chart.append("g")
	      .attr("class", "y axis")
	      .call(yAxis)
	    .append("text")
	      .attr("transform", "rotate(-90)")
	      .attr("y", 6)
	      .attr("dy", ".71em")
	      .style("text-anchor", "end")
	      .text("time");
	 
	  chart.selectAll(".bar")
	      .data(data)
	    .enter().append("rect")
	      .attr("class", "bar")
	      .attr("x", function(d) { return x(d.request_id); })
	      .attr("y", function(d) { return y(d.time); })
	      .attr("height", function(d) { return height - y(d.time); })
	      .attr("width", x.rangeBand())
	      //.attr("width", barwidth)
	      .on("click", function(data){ drawLinechart(data.request_id)})
	      .on("mouseover", tip.show)
	      .on("mouseout",tip.hide);
}});
}


function drawLinechart(request_id){

	var margin1 = {top: 20, right: 20, bottom: 30, left: 50},
	    widthl = w - margin1.left - margin1.right,
	    heightl = 350 - margin1.top - margin1.bottom;

	//defines a function to be used to append the title to the tooltip.  you can set how you want it to display here.
	var maketip = d3.tip()
	  .attr('class', 'd3-tip')
	  //.offset([-10, 0])
	  .html(function(d) {
	    return "<strong>Func:</strong> <span style='color:red'>" + d.fname + "</span><br><strong>Time:</strong> <span style='color:red'>" + d.time + "</span>";
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
	    .x(function(d) { return x1(d.fname); })
	    .y(function(d) { return y1(d.time); });

	d3.select("#svg-line").remove();

	var svg1 = d3.select(".chart").append("svg")
	    .attr("id", "svg-line")
	    .attr("width", widthl + margin1.left + margin1.right)
	    .attr("height", heightl + margin1.top + margin1.bottom)
	  .append("g")
	    .attr("transform", "translate(" + margin1.left + "," + margin1.top + ")");

	  jQuery.ajax(
	   {
	      type: "GET",
	      //url: 'http://127.0.0.1:8989/req/'+request_id,
              url: './json/'+request_id,
	      success: function(data1) {


	  data1 = data1["body"];
	  console.log(data1);
	  for(var i=0;i<data1.length;i++){
	      data1[i].fname = (data1[i].fname).split("#")[0]+i;  
	      data1[i].time = Number((data1[i].time).toFixed(2));
	};

	var svg2 = svg1.append("g")
	    .attr("class", "thegraph")

	svg2.call(maketip);  
	  
	  x1.domain(data1.map(function(d) { return d.fname; }));
	  y1.domain([0, d3.max(data1, function(d) { return d.time; })]);

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
		                .attr("cx", function(d){return x1(d.fname)})
		                .attr("cy",function(d){return y1(d.time)})
		                .attr("r",18)
		                .style('opacity', 1e-6)//1e-6
		                .on("mouseover", maketip.show)
		                .on("mouseout", maketip.hide);
	}});

}


bar_graph();
