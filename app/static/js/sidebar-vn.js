// insert the names of the roles into the checkbox labels of the ROLE and SPRINT MULTI-SELECTS
$(document).ready(function () {
    $.getJSON('/getroles', {}, function (data) {
        console.log(data);
        var i;
        for (i = 0; i < data.length; i++) {
            // console.log(data[i]);
            var roleValue = data[i];
            $("#roleselector").append($("<option></option>").attr("value", roleValue).attr('selected','selected').text(roleValue));

        }

        makeRoleSelector();
    });

    $.getJSON('/getsprints', {}, function (data) {
        console.log(data);
        var i;
        for (i = 0; i < data.length; i++) {
            // console.log(data[i]);
            var sprintValue = data[i];
            $("#sprintselector").append($("<option></option>").attr("value", sprintValue).attr('selected','selected').text(sprintValue));

        }
        makeSprintSelector();
    });


});


//SLIDER JS

function toggleNode(node, hideNode) {
    // huidige node verbergen of weergeven
    nodes.update({id: node.id, hidden: hideNode});

    // alle verbonden edges verbergen wanneer de node verborgen is
    edges.forEach(function (edge) {
        var isConnectedToNode = (edge.from == node.id) || (edge.to == node.id);

        if (isConnectedToNode && hideNode) {
            edges.update({id: edge.id, hidden: true});
        }
    });
}

function showAllNodes() {
    nodes.forEach(function (node) {
        edges.update({id: node.id, hidden: false});
    });
    edges.forEach(function (edge) {
        edges.update({id: edge.id, hidden: false});
    });
}

//
$('#weightSlider').change(function () {
    var weight = $(this).val();

    showAllNodes();

    // hide the nodes that are below weight
    nodes.forEach(function (node) {
        var nodeWeightBelowThreshold = (node.weight < weight);
        var nodeIsHidden = nodeWeightBelowThreshold;
        toggleNode(node, nodeIsHidden);


    });

    if (weight == 0) {
        showAllNodes();
    }
});

// toggle relationships on and off
$('#relationships').click(function () {
    edges.forEach(function (edge) {
        if (!edge.hidden) {
            edges.update({id: edge.id, hidden: true});
        }
        if (edge.hidden) {
            edges.update({id: edge.id, hidden: false});
        }
    });


});

//The function for the searchfield
$('#searchfield').change(function () {
    console.log('test');
    var formInput = document.getElementById("searchfield").value;
    // foundItem = null; //we'll store the matching value here

      if (formInput === '') {
        alert('Please Enter a Search Term');
        return false;
      }
      nodes.forEach(function(node){
          // var selected = nodes.get(node.id);
         if (node.label == formInput){
             console.log("i found it!");
             var selected_nodes = [];
             selected_nodes[0] = node.id;
             console.log(selected_nodes);
             // nodes.selectNode(node);
             // node.color = undefined;
            // node.trigger('click');
             nodes.update({id: node.id, borderWidth: 3, color: '#ECC348'})
         }
         else{
             nodes.update({id: node.id, color: '#97C2FC'})
         }
      });
      edges.forEach(function(edge){
          if (edge.label == formInput){
              edges.update({id: edge.id, color:'#ECC348'})
          }
          else{
              edges.update({id: edge.id, color:'#97C2FC'})
          }
      });
    });
// network.on("selectNode", function (params) {
//
// }