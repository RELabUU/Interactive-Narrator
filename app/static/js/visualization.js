/**
 * Created by Govert-Jan on 29-4-2016.
 * the Javascript code for our data visualization
 */
    //this file helps obtaining the json data from the app **??

//Create an object for a HTTP-request
var HttpClient = function () {
        this.get = function (aUrl, aCallback) {
            var anHttpRequest = new XMLHttpRequest();
            anHttpRequest.onreadystatechange = function () {
                if (anHttpRequest.readyState == 4 && anHttpRequest.status == 200)
                    aCallback(anHttpRequest.responseText);
            }

            anHttpRequest.open("GET", aUrl, true);
            anHttpRequest.send(null);
        }
    }

// Obtain the concepts from the back-end with an HTTP-request
aClient = new HttpClient();
var nodes_parsed;
var nodes = new vis.DataSet([]); //make a new DataSet to put the list of objects in as nodes

aClient.get('http://127.0.0.1:5000/concepts', function (response) { //actually execute the HTTP-request
    var nodes_parsed = JSON.parse(response); //make an array of objects from the obtained string
    // console.log(nodes_parsed);
    nodes.add(nodes_parsed); // add the parsed data to the DataSet
    console.log(nodes)
});

// HTTP-request to obtain the edges (relationships between concepts)
var edges = new vis.DataSet([]);
bClient = new HttpClient();
bClient.get('http://127.0.0.1:5000/relationships', function (response) {
    var edges_parsed = JSON.parse(response)
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
    //      physics:{
    //        enabled:true,
    // //        adaptiveTimestep:true,
    // //      //   minVelocity:0.75,
    //        maxVelocity:15,
    // //      //   barnesHut: {gravitationalConstant: 0,
    // //      //       centralGravity: 0, springConstant: 0},
    //        stabilization: {
    //            enabled: true,
    // //          //   iterations: 1000,
    // //          //   updateInterval: 100,
    // //          //   onlyDynamicEdges: false,
    //            fit: true
    //  }
    // //
    //      },
    //
    // layout:{
    //   improvedLayout:true,
    //  //  randomSeed:83040,
    //  randomSeed:undefined,
    //   hierarchical: {
    //    enabled:false}},

    scaling: {
        label: {enabled: true}
    },
    nodes: {
        // color:{background:'#97C2FC'},
        color: {background: '#42b3f4', highlight: {background: '#5898ED'}},
        hover: {
            border: '#2B7CE9',
            background: '#D2E5FF'
        },

        shape: 'dot',
        size: 20,
        widthConstraint: {minimum: 25, maximum: 40}
    },
    groups: {
        Role: {color: {background: '#97C2FC'}, borderWidth: 5}
        // selected_role_node: {color:{background:'#97C2FC'}},
        // greyed_out:{color:{background:'#E8E8E8'}, borderWidth:0},
        // selected_edge:{color:{color:'#97C2FC'}}

    },

    edges: {
        labelHighlightBold: true,
        width: 1,
        // length:200, //the lenght of the edges is set here. standard:undefined
        arrows: {
            to: {enabled: true, scaleFactor: 1, type: 'arrow'},
            middle: {enabled: false, scaleFactor: 1, type: 'arrow'},
            from: {enabled: false, scaleFactor: 1, type: 'arrow'}
        }
    }

};
var network = new vis.Network(container, data, options);
// network.setOptions(
//     {
//
//         physics: {enabled:false}
//     }
// );
//  var zaadje = network.getSeed();
//  console.log(zaadje)

// set the first initial zoom level
network.once('initRedraw', function () {
    if (lastClusterZoomLevel === 0) {
        lastClusterZoomLevel = network.getScale();
    }
});

// we use the zoom event for our clustering
network.on('zoom', function (params) {
    if (params.direction == '-') {
        if (params.scale < lastClusterZoomLevel * clusterFactor) {
            var totalCID = 8;
            for (var i = 1; i <= totalCID; i++) {
                makeClusters(params.scale, i);
            }
            lastClusterZoomLevel = params.scale;
        }
    }
    else {
        openClusters(params.scale);
    }
});

// if we click on a node, we want to open it up!
network.on("selectNode", function (params) {
    if (params.nodes.length == 1) {
        if (network.isCluster(params.nodes[0]) == true) {
            network.openCluster(params.nodes[0])
        }
    }
});


// make the clusters
function makeClusters(scale, clusterIndex) {
    var clusterOptionsByData = {
        processProperties: function (clusterOptions, childNodes) {
            var childrenCount = 0;
            for (var i = 0; i < childNodes.length; i++) {
                childrenCount += childNodes[i].childrenCount || 1;
            }
            clusterOptions.childrenCount = childrenCount;
            clusterOptions.label = "cid: " + clusterIndex + " (" + childrenCount + ")";
            clusterOptions.font = {size: childrenCount * 3 + 10}  //size of the label is calculated based on number of childnodes
            clusterOptions.size = childrenCount * 2 + 10; //size of the node is calculated based on number of childnodes
            clusterOptions.id = 'cluster:' + clusterIndex;
            clusters.push({id: 'cluster:' + clusterIndex, scale: scale});
            return clusterOptions;
        },
        joinCondition: function (childOptions) {
            return childOptions.cid == clusterIndex;
        },
        clusterNodeProperties: {borderWidth: 3, shape: 'dot', font: {size: 30}}
    }
    network.cluster(clusterOptionsByData);
    //  if (document.getElementById('stabilizeCheckbox').checked === true) {
    //      network.stabilize();
    //  }
}

// open them back up!
function openClusters(scale) {
    var newClusters = [];
    var declustered = false;
    for (var i = 0; i < clusters.length; i++) {
        if (clusters[i].scale < scale) {
            network.openCluster(clusters[i].id);
            lastClusterZoomLevel = scale;
            declustered = true;
        }
        else {
            newClusters.push(clusters[i])
        }
    }
    clusters = newClusters;
    if (declustered === true) {
        network.stabilize();
    }
}


//document.getElementById("testarea").innerHTML = nodes;
//function for selecting node with theme 10
//function selectTheme(){
//}
//nodes.get({filter: function(node) {return node.group == "theme1"}});
