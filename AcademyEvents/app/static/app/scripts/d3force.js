

var json = {
    "nodes": [
      {
          "name": "Clacton Coastal Academy",
          //"url": "http://www.nasaspaceflight.com",
          "group": 0
      },
      {
          "name": "Richmond Park Academy",
          "group": 0
      },
      {
          "name": "Everest Community Academy",
          "group": 0
      },
      {
          "name": "Felixstowe Academy",
          "group": 0
      },
      {
          "name": "Academies Enterprise Trust",
          "group": 1
      },
      {
          "name": "THE WHITE HORSE FEDERATION",
          "group": 1
      },
      {
          "name": "Inspiration Trust",
          "group": 2
      },
      {
          "name": "THE DUSTON EDUCATION TRUST",
          "group": 2
      }
    ], "links": [

      { "source": 1, "target": 5 },
      { "source": 2, "target": 7 },
      { "source": 2, "target": 4 },
      { "source": 3, "target": 4 },
      { "source": 3, "target": 6 }

    ]
}

var width = 600,
    height = 700

var svg = d3.select("#svg").append("svg")
    .attr("width", width)
    .attr("height", height);

var fill = d3.scale.category20();

var force = d3.layout.force()
    .gravity(0.05)
    .distance(50)
    .charge(-100)
    .size([width, height]);

force
      .nodes(json.nodes)
      .links(json.links)
      .start();

var link = svg.selectAll("link")
      .data(json.links)
      .enter().append("line")
      .attr("class", "link");

var node = svg.selectAll("node")
      .data(json.nodes)
      .enter().append("g")
      .attr("class", "node")
      .style("fill", function (d) {
          return fill(d.group);
      })
      .call(force.drag)
//.on("mouseover", fade(.1)).on("mouseout", fade(1));

node.append("circle")
    //.attr("cx", function(d) { return d.x; })
    .attr("r", 8)

node.append("text")
      .attr("dx", 0)
      .attr("dy", 15)
      .text(function (d) { return d.name });

var labels = svg.selectAll('text')
    .data(json.links)
    .enter().append('text')
    .attr("x", function (d) { return (d.source.y + d.target.y) / 2; })
    .attr("y", function (d) { return (d.source.x + d.target.x) / 2; })
    .attr("text-anchor", "middle")
    .text(function (d) { return d.count; });

force.on("tick", function () {
    node.each(function (d) {
        //if(d.fixedx>0) { d.x = d.px = d.fixedx; }

        if (d.group == 1) { d.x = d.px = .8 * width }
        if (d.group == 2) { d.x = d.px = .2 * width }
    });

    link.attr("x1", function (d) { return d.source.x; })
        .attr("y1", function (d) { return d.source.y; })
        .attr("x2", function (d) { return d.target.x; })
        .attr("y2", function (d) { return d.target.y; });


    labels.attr("x", function (d) { return (d.source.x + d.target.x + 10) / 2; })
        .attr("y", function (d) { return (d.source.y + d.target.y + 10) / 2; })

    node.attr("transform", function (d) { return "translate(" + d.x + "," + d.y + ")"; });


});