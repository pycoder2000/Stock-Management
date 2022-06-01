function graph(){
	
	d3.select("svg").remove();
	
	var margin = { top: 20, right: 100, bottom: 40, left: 100 };
	var height = 500 - margin.top - margin.bottom;
	var width = 960 - margin.left - margin.right;

	var svg = d3.select("body").append("svg")
			.attr("width",width + margin.left + margin.right)
			.attr("height",height + margin.top + margin.bottom)
			.attr("style",'border-style: solid;')
		.append("g")
			.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	// setup scales - the domain is specified inside of the function called when we load the data
	var xScale = d3.time.scale().range([0, width]);
	var yScale = d3.scale.linear().range([height, 0]);
	var color = d3.scale.category10();

	// setup the axes
	var xAxis = d3.svg.axis().scale(xScale).orient("bottom");
	var yAxis = d3.svg.axis().scale(yScale).orient("left");

	// create function to parse dates into date objects
	var parseDate = d3.time.format("%Y-%m-%d").parse;
	var formatDate = d3.timeFormat("%Y-%m-%d");
	var bisectDate = d3.bisector(function(d) { return d.Date; }).left;

	// set the line attributes
	var line = d3.svg.line()
		.interpolate("basis")
		.x(function(d) { return xScale(d.Date); })
		.y(function(d) { return yScale(d.Close); });

	var focus = svg.append("g").style("display","none");

	// import data and create chart
	d3.csv("static/csvfile.csv", function(d) {
        // console.log(d.Date)    
        // console.log(typeof  Date.parse(d.Date));
        return {
				Date: Date.parse(d.Date),
                Open: +d.Open,
                // Volumn: +d.Volumn,
				// High: +d.High,
                // Low: +d.Low,
			};
		}, 
		function(error,data) {
			
			// sort data ascending - needed to get correct bisector results
			data.sort(function(a,b) {return a.Date - b.Date;});

			// color domain
			color.domain(d3.keys(data[0]).filter(function(key) { return key !== "Date"; }));

			// create stocks array with object for each company containing all data
			var stocks = color.domain().map(function(name) {
				return {
					name: name,
					values: data.map(function(d){
                        d_date = new Date(d.Date)
						return {Date: d_date, Close: d[name]};
					})
				};
			});

			// add domain ranges to the x and y scales
			xScale.domain([
				d3.min(stocks, function(c) {
                    return d3.min(c.values, function(v) {return v.Date; }); }),
				d3.max(stocks, function(c) { return d3.max(c.values, function(v) { return v.Date; }); })
			]);
			yScale.domain([0,d3.max(stocks, function(c) { return d3.max(c.values, function(v) { return v.Close; }); })]);

			// add the x axis
			svg.append("g")
				.attr("class", "x axis")
				.attr("transform", "translate(0," + height + ")")
				.call(xAxis);

			// add the y axis
			svg.append("g")
					.attr("class", "y axis")
					.call(yAxis)
				.append("text")
					.attr("transform","rotate(-90)")
					.attr("y",-60)
					.attr("dy",".71em")
					.style("text-anchor","end")
					.text("Price ($)");
			
			// add the line groups
			var stock = svg.selectAll(".stockXYZ")
					.data(stocks)
				.enter().append("g")
					.attr("class","stockXYZ");

			// add the stock price paths
			stock.append("path")
				.attr("class","line")
				.attr("id",function(d,i){ return "id" + i; })
				.attr("d", function(d) {
					return line(d.values); 
				})
				.style("stroke", function(d) { return color(d.name); });            

	});
}