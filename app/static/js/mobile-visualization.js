/**
 * Created by Govert-Jan on 29-4-2016.
 * the Javascript code for our data visualization
 */

     var clusters = [];
     var lastClusterZoomLevel = 0;
     var clusterFactor = 1.0;

  var nodes = new vis.DataSet([{"id": 1, "label": "Language Label", "weight": ""}, {"id": 2, "label": "Label", "weight": 1.5}, {"id": 3, "label": "Language", "weight": 9.660000000000002}, {"id": 4, "label": "Site Part", "weight": ""}, {"id": 5, "label": "Part", "weight": 1.2}, {"id": 6, "label": "Site", "weight": 1.2}, {"id": 7, "label": "Editor", "weight": 16.2}, {"id": 8, "label": "System Administrator", "weight": ""}, {"id": 9, "label": "Administrator", "weight": 3}, {"id": 10, "label": "System", "weight": 1.98}, {"id": 11, "label": "Filter", "weight": 1.5}, {"id": 12, "label": "Marketeer", "weight": 10}, {"id": 13, "label": "Title", "weight": 2}, {"id": 14, "label": "Url", "weight": 2.5}, {"id": 15, "label": "Conflict", "weight": 1.5}, {"id": 16, "label": "Product Page", "weight": ""}, {"id": 17, "label": "Page", "weight": 7.16}, {"id": 18, "label": "Product", "weight": 1.2}, {"id": 19, "label": "Attribute", "weight": 1.7}, {"id": 20, "label": "Tag", "weight": 1}, {"id": 21, "label": "Medium Item", "weight": ""}, {"id": 22, "label": "Item", "weight": 8.06}, {"id": 23, "label": "Medium", "weight": 5.58}, {"id": 24, "label": "Audience", "weight": 1}, {"id": 25, "label": "Keywords", "weight": 1}, {"id": 26, "label": "Refferals", "weight": 1}, {"id": 27, "label": "What", "weight": 1.5}, {"id": 28, "label": "Page Section", "weight": ""}, {"id": 29, "label": "Section", "weight": 2.7}, {"id": 30, "label": "Type", "weight": 1.2}, {"id": 31, "label": "Image", "weight": 1.5}, {"id": 32, "label": "Flash Version", "weight": ""}, {"id": 33, "label": "Version", "weight": 1.5}, {"id": 34, "label": "Flash", "weight": 1.6600000000000001}, {"id": 35, "label": "Flash Presentation", "weight": ""}, {"id": 36, "label": "Presentation", "weight": 4.22}, {"id": 37, "label": "Developer", "weight": 3}, {"id": 38, "label": "File", "weight": 2.4}, {"id": 39, "label": "Environment Language", "weight": ""}, {"id": 40, "label": "Environment", "weight": 1.3599999999999999}, {"id": 41, "label": "Content Language", "weight": ""}, {"id": 42, "label": "Content", "weight": 7.26}, {"id": 43, "label": "Presentation Variant", "weight": ""}, {"id": 44, "label": "Variant", "weight": 2}, {"id": 45, "label": "Presentation Configuration", "weight": ""}, {"id": 46, "label": "Configuration", "weight": 1.4}, {"id": 47, "label": "Item Title", "weight": ""}, {"id": 48, "label": "Web Initiative", "weight": ""}, {"id": 49, "label": "Initiative", "weight": 1.9}, {"id": 50, "label": "Web", "weight": 1.9}, {"id": 51, "label": "Thesaurus", "weight": 1.2}, {"id": 52, "label": "Workflow", "weight": 2}, {"id": 53, "label": "Medium Level", "weight": ""}, {"id": 54, "label": "Level", "weight": 1.4}, {"id": 55, "label": "Performance", "weight": 1}, {"id": 56, "label": "Editor Environment", "weight": ""}, {"id": 57, "label": "Text", "weight": 1}, {"id": 58, "label": "Faq", "weight": 1}, {"id": 59, "label": "Time", "weight": 2.2}, {"id": 60, "label": "Link", "weight": 1.9}, {"id": 61, "label": "Ranking", "weight": 2.5}, {"id": 62, "label": "Website", "weight": 3.7}, {"id": 63, "label": "Duplication", "weight": 1.2}, {"id": 64, "label": "Data", "weight": 1}, {"id": 65, "label": "Week", "weight": 2.0999999999999996}, {"id": 66, "label": "Action", "weight": 1}, {"id": 67, "label": "Result", "weight": 2}, {"id": 68, "label": "Traffic", "weight": 1}, {"id": 69, "label": "Xml", "weight": 1.4}, {"id": 70, "label": "Term", "weight": 1.2}, {"id": 71, "label": "Way", "weight": 2.0999999999999996}, {"id": 72, "label": "Order", "weight": 1.5}, {"id": 73, "label": "Manager", "weight": 1}, {"id": 74, "label": "Maker", "weight": 1}, {"id": 75, "label": "French", "weight": 1.5}, {"id": 76, "label": "Channel Manager", "weight": ""}, {"id": 77, "label": "Business Maker", "weight": ""}]


 );

   // create an array with edges
   // create an array with edges
     var edges = new vis.DataSet(
         [{"from": 1, "label": "isa", "to": 2}, {"from": 3, "label": "Label", "to": 1}, {"from": 4, "label": "isa", "to": 5}, {"from": 6, "label": "Part", "to": 4}, {"from": 7, "label": "Maintain", "to": 1}, {"from": 7, "label": "Search", "to": 1}, {"from": 8, "label": "isa", "to": 9}, {"from": 10, "label": "Administrator", "to": 8}, {"from": 8, "label": "Deploy", "to": 11}, {"from": 12, "label": "Set", "to": 13}, {"from": 12, "label": "Switch", "to": 14}, {"from": 12, "label": "Solve", "to": 15}, {"from": 16, "label": "isa", "to": 17}, {"from": 18, "label": "Page", "to": 16}, {"from": 12, "label": "Create", "to": 14}, {"from": 12, "label": "Set", "to": 19}, {"from": 12, "label": "Set", "to": 20}, {"from": 12, "label": "Avoid", "to": 14}, {"from": 21, "label": "isa", "to": 22}, {"from": 23, "label": "Item", "to": 21}, {"from": 12, "label": "Analyze", "to": 24}, {"from": 12, "label": "View", "to": 25}, {"from": 12, "label": "View", "to": 26}, {"from": 12, "label": "See", "to": 27}, {"from": 28, "label": "isa", "to": 29}, {"from": 17, "label": "Section", "to": 28}, {"from": 7, "label": "Assign", "to": 28}, {"from": 7, "label": "Manage", "to": 28}, {"from": 7, "label": "Access", "to": 22}, {"from": 7, "label": "Have", "to": 30}, {"from": 7, "label": "Crop", "to": 31}, {"from": 7, "label": "Edit", "to": 31}, {"from": 32, "label": "isa", "to": 33}, {"from": 34, "label": "Version", "to": 32}, {"from": 35, "label": "isa", "to": 36}, {"from": 34, "label": "Presentation", "to": 35}, {"from": 37, "label": "Check", "to": 32}, {"from": 37, "label": "Adjust", "to": 35}, {"from": 37, "label": "Pass On", "to": 38}, {"from": 39, "label": "isa", "to": 3}, {"from": 40, "label": "Language", "to": 39}, {"from": 7, "label": "Set", "to": 39}, {"from": 7, "label": "Login In", "to": 3}, {"from": 41, "label": "isa", "to": 3}, {"from": 42, "label": "Language", "to": 41}, {"from": 7, "label": "Set", "to": 41}, {"from": 43, "label": "isa", "to": 44}, {"from": 36, "label": "Variant", "to": 43}, {"from": 45, "label": "isa", "to": 46}, {"from": 36, "label": "Configuration", "to": 45}, {"from": 37, "label": "Define", "to": 43}, {"from": 37, "label": "Deploy", "to": 36}, {"from": 8, "label": "Define", "to": 43}, {"from": 8, "label": "Deploy", "to": 36}, {"from": 47, "label": "isa", "to": 13}, {"from": 22, "label": "Title", "to": 47}, {"from": 7, "label": "Search On In In", "to": 47}, {"from": 48, "label": "isa", "to": 49}, {"from": 50, "label": "Initiative", "to": 48}, {"from": 7, "label": "Show", "to": 21}, {"from": 7, "label": "Have", "to": 51}, {"from": 7, "label": "Configure", "to": 52}, {"from": 7, "label": "Control", "to": 27}, {"from": 53, "label": "isa", "to": 54}, {"from": 23, "label": "Level", "to": 53}, {"from": 7, "label": "Control", "to": 22}, {"from": 7, "label": "Translate", "to": 21}, {"from": 7, "label": "Produce", "to": 42}, {"from": 7, "label": "Maintain", "to": 21}, {"from": 8, "label": "Monitor", "to": 55}, {"from": 56, "label": "isa", "to": 40}, {"from": 7, "label": "Environment", "to": 56}, {"from": 7, "label": "Search", "to": 57}, {"from": 7, "label": "Find", "to": 42}, {"from": 7, "label": "Maintain", "to": 58}]
);

     // create a network
     var container = document.getElementById('visualization');
     var data = {
         nodes: nodes,
         edges: edges
     };
      var options = {
        physics:{
          adaptiveTimestep:false,
            enabled:true,
            maxVelocity:5
        },

   layout:{
     improvedLayout:true,
     hierarchical: {
      enabled:false}},

   scaling:{
     label:{enabled:true}
   },
   nodes:{
     shape:'dot'
   },
   edges:{
     labelHighlightBold:true,
	 length:100 //the lenght of the edges is set here. standard:undefined
   }

   };
     var network = new vis.Network(container, data, options);


     // // set the first initial zoom level
     // network.once('initRedraw', function() {
     //     if (lastClusterZoomLevel === 0) {
     //         lastClusterZoomLevel = network.getScale();
     //     }
     // });

     // // we use the zoom event for our clustering
     // network.on('zoom', function (params) {
     //     if (params.direction == '-') {
     //         if (params.scale < lastClusterZoomLevel*clusterFactor) {
 		// 		var totalCID = 8;
 		// 		for (var i = 1; i <= totalCID; i++) {
 		// 			makeClusters(params.scale, i);
 		// 		}
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
     //             clusterOptions.font = {size: childrenCount*3+10}  //size of the label is calculated based on number of childnodes
		// 		 clusterOptions.size = childrenCount*2+10; //size of the node is calculated based on number of childnodes
     //             clusterOptions.id = 'cluster:' + clusterIndex;
     //             clusters.push({id:'cluster:' + clusterIndex, scale:scale});
     //             return clusterOptions;
     //         },
 		// 	joinCondition:function(childOptions) {
 		// 		return childOptions.cid == clusterIndex;
 		// 	},
     //         clusterNodeProperties: {borderWidth: 3, shape: 'dot', font: {size: 30}}
     //     }
     //     network.cluster(clusterOptionsByData);
     //    //  if (document.getElementById('stabilizeCheckbox').checked === true) {
     //    //      network.stabilize();
     //    //  }
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

     //function for selecting node with theme 10
     //function selectTheme(){
     //}
     //nodes.get({filter: function(node) {return node.group == "theme1"}});
