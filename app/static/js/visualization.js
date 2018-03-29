/**
 * Created by Govert-Jan on 29-4-2016.
 * the Javascript code for our data visualization
 */
    //this file helps obtaining the json data from the visualization and takes care of the
    // visualization itself**??


//Create an object for a HTTP-request
var HttpClient = function () {
        this.get = function (aUrl, aCallback) {
            var anHttpRequest = new XMLHttpRequest();
            anHttpRequest.onreadystatechange = function () {
                if (anHttpRequest.readyState == 4 && anHttpRequest.status == 200)
                    aCallback(anHttpRequest.responseText);
            };

            anHttpRequest.open("GET", aUrl, true);
            anHttpRequest.send(null);
        }
    };

// Obtain the concepts from the back-end with an HTTP-request
aClient = new HttpClient();
var nodes_parsed;
var nodes = new vis.DataSet([]); //make a new DataSet to put the list of objects in as nodes

aClient.get('/concepts', function (response) { //actually execute the HTTP-request
    var nodes_parsed = JSON.parse(response); //make an array of objects from the obtained string
    // var nodes_parsed = response['json_concepts'];
    // console.log('repsone tuple', response.clusters);
    console.log(nodes_parsed);
    nodes.add(nodes_parsed); // add the parsed data to the DataSet
    console.log(nodes)
});

// HTTP-request to obtain the edges (relationships between concepts)
var edges = new vis.DataSet([]);
bClient = new HttpClient();
bClient.get('/relationships', function (response) {
    var edges_parsed = JSON.parse(response);
    // console.log(edges_parsed);
    edges.add(edges_parsed);
});


//Original JS starts here
var clusters = [];
var lastClusterZoomLevel = 0;
var clusterFactor = 1.0;

// create a network
var container = document.getElementById('visualization');
var data = {
    nodes: nodes,
    edges: edges
};
var options = {
    interaction:{
    dragNodes:true,
    dragView: true,
    hideEdgesOnDrag: false,
    hideNodesOnDrag: false,
    hover: false,
    hoverConnectedEdges: true,
    keyboard: {
      enabled: false,
      speed: {x: 10, y: 10, zoom: 0.02},
      bindToWindow: true
    },
    multiselect: true,
    navigationButtons: true,
    selectable: true,
    selectConnectedEdges: true,
    // tooltipDelay: 300,
    zoomView: true
  },

         physics:{
           enabled:true,
           adaptiveTimestep:true,
    //      //   minVelocity:0.75,
           maxVelocity:35,
           barnesHut: {gravitationalConstant: -10000,
               avoidOverlap: 0.9
                // centralGravity: 0
               // springConstant: 0
               // damping: 0
               },
           stabilization: {
               enabled: true,
                  iterations: 1500,
        //       //   updateInterval: 100,
    // //          //   onlyDynamicEdges: false,
               fit: true
            },
             timestep:0.5
    // //
         },
    //
    layout:{
      improvedLayout:true,
      // randomSeed:1
     randomSeed:undefined
    //   hierarchical: {
    //    enabled:true}
        },

    scaling: {
        label: {enabled: true}
    },
    nodes: {
        // color:{background:'#97C2FC'},
        color: {background: '#97C2FC', highlight: {background: '#5898ED'}},
        hover: {border: '#2B7CE9', background: '#D2E5FF'},
        shape: 'dot',
        font: {
            size:16,
            bold: {color: '#0077aa'}
      }
        // size: 20,
        // widthConstraint: {minimum: 25, maximum: 50}
    },
    groups: {
        Role:{shape: 'icon',
            icon: {
              face: 'FontAwesome',
              code: '\uf007',
              size: 50,
              color: '#084ef4'
            }
        }

    },

    edges: {
        labelHighlightBold: true,
        width: 1,
        length: 200, //undefined, //the lenght of the edges is set here. standard:undefined
        arrows: {
            to: {enabled: true, scaleFactor: 1, type: 'arrow'},
            middle: {enabled: false, scaleFactor: 1, type: 'arrow'},
            from: {enabled: false, scaleFactor: 1, type: 'arrow'}
        },
        font: {
        size: 16,
            bold: true
      }
    }

};


var network = new vis.Network(container, data, options);

//function to close the user story pop up
function closeWindow() {
	$("#userstorytable").css('display', 'none');
	$("#userstorytable").remove();
	$("#userstoryinfo").remove();
	$('.closeWindow').remove();
}

// Retrieve the user stories that belong to the node that is clicked, and put them in a table
network.on( 'doubleClick', function(properties) {
    var ids = properties.nodes;
    // console.log(ids);
    var clickedNodes = nodes.get(ids);
    console.log('clicked nodes:', clickedNodes);
    labelBold = clickedNodes[0].label;

    if (clickedNodes[0].color == '#ECC348'){
        nodes.update({id: clickedNodes[0].id, color: '#97C2FC'})
    }

    var role_values = $('#roleselector option:selected');//add the selected options to a var
    var sprint_values = $('#sprintselector option:selected');

    var selectedRoles = $(role_values).map(function (index, option) {
        return $(option).val();		//put the values in the array
            });
    var selectedSprints = $(sprint_values).map(function (index, option) {
        return $(option).val();
            });
                // Array to keep track of selected checkboxes i.e. selected themes
    selectedRoles = selectedRoles.toArray();
    selectedSprints = selectedSprints.toArray();

    console.log('selectedroles and sprints', selectedRoles, selectedSprints);
    $.getJSON('/clickquery', {
                    nodes: JSON.stringify(clickedNodes),
                    roles: JSON.stringify(selectedRoles),
                    sprints: JSON.stringify(selectedSprints)
    },function (data) {


        //remove the previously created table
        $("#userstoryinfo").remove();
        $("#userstorytable").remove();
        //add the newly created table
        $("body").append('<div id="userstoryinfo"></div>');
        $("#userstoryinfo").append('<div id="userstorytable"></div>');

        console.log(data);

        $("#userstorytable tr").remove();

        for (var i = 0; i < data.length; i++) {
            if (i== 0){
                console.log('succes creating table');
                $('#userstorytable').append("<tr><th>Spr.</th><th>US</th><th>Text</th></tr>");

            }

            var s = data[i].text;

            var newText = s.replace(RegExp(labelBold, "ig"), '<b>' + labelBold + '</b>');

            tr = $('<tr/>');
            tr.append("<td>" + data[i]['in sprint'] + "</td>");
            tr.append("<td>" + data[i].id + "</td>");
            tr.append("<td>" + newText + "</td>");

            $('#userstorytable').append(tr);
            $("#userstorytable").css('display', 'block');



        }
                //remove the close button
                $('.closeWindow').remove();
                //add the close button
                $('#userstoryinfo').append("<div onclick='closeWindow()' class='closeWindow'><span class='glyphicon glyphicon-remove-circle'></span></div>");

                //make div draggable with JQuery UI
                $('#userstoryinfo').draggable({
                    start: function(event, ui){
                        $('.ui-draggable').css('height', $(event.target).height());}
   });
                // $('#userstoryinfo').resizable();
        }
    );
    // $('#userstorytable tbody').after('<tr><th>Sprint</th><th>more data</th></tr>');
});


// network.on( 'click', function(){
//     nodes.update({id: node.id, color: '#97C2FC'});
//     edges.update({id: node.id, color: '#97C2FC'});
// });



//CLUSTERING. NOT IMPLEMENTED YET, BUT IS READY FOR IT WITH MINOR WORK
//
// // set the first initial zoom level
// network.once('initRedraw', function () {
//     if (lastClusterZoomLevel === 0) {
//         lastClusterZoomLevel = network.getScale();
//     }
// });
//
// // we use the zoom event for our clustering
// network.on('zoom', function (params) {
//     if (params.direction == '-') {
//         if (params.scale < lastClusterZoomLevel * clusterFactor) {
//             var totalCID = 8;
//             for (var i = 1; i <= totalCID; i++) {
//                 makeClusters(params.scale, i);
//             }
//             lastClusterZoomLevel = params.scale;
//         }
//     }
//     else {
//         openClusters(params.scale);
//     }
// });
//
// // if we click on a node, we want to open it up!
// network.on("selectNode", function (params) {
//     if (params.nodes.length == 1) {
//         if (network.isCluster(params.nodes[0]) == true) {
//             network.openCluster(params.nodes[0])
//         }
//     }
// });
//
//
// // make the clusters
// function makeClusters(scale, clusterIndex) {
//     var clusterOptionsByData = {
//         processProperties: function (clusterOptions, childNodes) {
//             var childrenCount = 0;
//             for (var i = 0; i < childNodes.length; i++) {
//                 childrenCount += childNodes[i].childrenCount || 1;
//             }
//             clusterOptions.childrenCount = childrenCount;
//             clusterOptions.label = "cid: " + clusterIndex + " (" + childrenCount + ")";
//             clusterOptions.font = {size: childrenCount * 3 + 10};  //size of the label is calculated based on number of childnodes
//             clusterOptions.size = childrenCount * 1.5 + 10; //size of the node is calculated based on number of childnodes
//             clusterOptions.id = 'cluster:' + clusterIndex;
//             clusters.push({id: 'cluster:' + clusterIndex, scale: scale});
//             return clusterOptions;
//         },
//         joinCondition: function (childOptions) {
//             return childOptions.cid == clusterIndex;
//         },
//         clusterNodeProperties: {borderWidth: 3, shape: 'dot', font: {size: 30}}
//     };
//     network.cluster(clusterOptionsByData);
//     //  if (document.getElementById('stabilizeCheckbox').checked === true) {
//     //      network.stabilize();
//     //  }
// }
//
// // open them back up!
// function openClusters(scale) {
//     var newClusters = [];
//     var declustered = false;
//     for (var i = 0; i < clusters.length; i++) {
//         if (clusters[i].scale < scale) {
//             network.openCluster(clusters[i].id);
//             lastClusterZoomLevel = scale;
//             declustered = true;
//         }
//         else {
//             newClusters.push(clusters[i])
//         }
//     }
//     clusters = newClusters;
//     if (declustered === true) {
//         network.stabilize();
//     }
// }


//document.getElementById("testarea").innerHTML = nodes;
//function for selecting node with theme 10
//function selectTheme(){
//}
//nodes.get({filter: function(node) {return node.group == "theme1"}});



// obtain de clusters from the back-end
// $.getJSON('/clusters',
//     function (data) {
//     console.log(data.nodes);
//
// });


//put the link to the screenshot of the network diagram in the download png button
network.on("afterDrawing", function (ctx) {
    var dataURL = ctx.canvas.toDataURL('image/png').replace("image/png", "image/octet-stream");
    var download = document.getElementById('canvasImg');
    download.setAttribute("href", dataURL);
    // var w = window.open(dataURL);
    // w.document.write("<img src='"+dataURL+"' alt='from canvas'/>");
    });





// EXPERIMENTAL CODE for rendering the PNG with another background color
    // context = canvas.getContext("2d");

// set to draw behind current content
// context.globalCompositeOperation = "destination-over";

// set background color
// context.fillStyle = '#fff'; // <- background color

// draw background / rect on entire canvas
// context.fillRect(0, 0, canvas.width, canvas.height);

    // change non-opaque pixels to white
    // var imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    // var data = imgData.data;
    // for (var i = 0; i < data.length; i += 4) {
    //     if (data[i + 3] == 0) {
    //         data[i] = 255;
    //         data[i + 1] = 255;
    //         data[i + 2] = 255;
    //         data[i + 3] = 255;
    //     }
    // }
    // ctx.putImageData(imgData, 0, 0);

    // var c=document.getElementsByName("canvas");
// var d=c.toDataURL("image/png");
// window.open(c.toDataURL('image/png'));
// var w=window.open('about:blank','image from canvas');
// w.document.write("<img src='"+d+"' alt='from canvas'/>");

