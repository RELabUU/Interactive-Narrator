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

    // populate the dropdown multiselect for sprints with spritn name + ID
    $.getJSON('/getsprints', {}, function (data) {
        console.log(data);
        var i;
        for (i = 0; i < data.length; i++) {
            var sprintValue = data[i];
            $("#sprintselector").append($("<option></option>").attr("value", sprintValue[1]).attr('selected','selected').text(sprintValue[0] + " (" + sprintValue[1] + ")"));

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
    console.log('testing of the search field');
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




//This document contains the functions to select nodes based on the user interface elements in the sidebar

window.onresize = function() {
    network.fit();
};

function showDataSet(data) {

    console.log(data);

    var nodes_dataset = new vis.DataSet();
    var edges_dataset = new vis.DataSet();

    nodes_dataset.add(data.nodes);
    edges_dataset.add(data.edges);
    console.log(nodes);
    console.log(edges);
    console.log(nodes_dataset);
    console.log(edges_dataset);

    // updating the nodes //
    nodes.forEach(function (node) {
        var selected = nodes_dataset.get(node.id);
        // console.log(node.id);
        // console.log(selected);
        // if nothing is selected, make everything grey. NOT WORKING!
        if (!selected) {

            nodes.update({id: node.id, color: '#E8E8E8', font:{color:'#E8E8E8'}});
        }
        // else if a node is selected make it blue
        else {
            if (node.group == 'Role') {
                nodes.update({id: node.id, color: '#4A87F4', font:{color:'#343434'}});

            }
            else {
                nodes.update({id: node.id, color: '#97C2FC', font:{color:'#343434'}});
            }
        }
    });

    // if no roles are selected, return to the default appearance
    if (nodes_dataset.length == 0) {
        nodes.forEach(function (node) {
            nodes.update({id: node.id, color: '#97C2FC', font:{color:'#343434'}});

            if (node.group == 'Role') {
                nodes.update({id: node.id, color: '#4A87F4', font:{color:'#343434'}});

            }
        });

    }

    // updating the edges //
    edges.forEach(function (edge) {
        var selected = edges_dataset.get(edge.id);
        // console.log(edge.id);
        // if edges are not part of the selection, make them grey
        if (!selected) {
            edges.update({id: edge.id, color: '#E8E8E8', font:{color:'#E8E8E8'} });
        }
        //else make all edges blue
        else {
            edges.update({id: edge.id, color: '#5898ED', font:{color:'#343434'}} );
        }

    });

    // if no roles are selected or a selected role has no relationships, return to the default appearance
    if (edges_dataset.length == 0 && nodes_dataset.length == 0) {
        edges.forEach(function (edge) {
            edges.update({id: edge.id, color: '#5898ED', font:{color:'#343434'}});
        });

    }

    // console.log(nodes_dataset);

}

//    ROLE SELECTION
function makeRoleSelector() {
    $('#roleselector').multiselect({
        enableClickableOptGroups: true,
        enableCollapsibleOptGroups: true,
        enableFiltering: true,
        includeSelectAllOption: true,
        maxHeight: 400,
        enableCaseInsensitiveFiltering: true,
        buttonContainer: '<div id="roleselector-btn-group" class="btn-group" />',
        buttonText: function (options, select) {
            return 'Roles';
        },
        onSelectAll: function (option, checked, select) {		//use the onChange event to listen to changes in the listbox
            var role_values = $('#roleselector option:selected');//add the selected options to a var
            var sprint_values = $('#sprintselector option:selected');

            var selectedRoles = $(role_values).map(function (index, option) {
                return $(option).val();		//put the values in the array
            });
            var selectedSprints = $(sprint_values).map(function (index, option) {
                return $(option).val();
            });

            console.log('SELECTEDROLES', selectedRoles);
            console.log('SELECTEDSPRINTS', selectedSprints);
            // Array to keep track of selected checkboxes i.e. selected themes
            selectedRoles = selectedRoles.toArray();
            selectedSprints = selectedSprints.toArray();

            $.getJSON('/query', {
                    roles: JSON.stringify(selectedRoles),
                    sprints: JSON.stringify(selectedSprints)
                }, showDataSet);
        },
        onInitialized: function (select, container) {
            var $button = container.find("button").eq(0);
            $button.append('<span class="multiselect_icon sub_icon glyphicon glyphicon-user" aria-hidden="true"></span>');
            console.log($button);
        },
        onChange: function (option, checked, select) {		//use the onChange event to listen to changes in the listbox
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

            $.getJSON('/query', {
                    roles: JSON.stringify(selectedRoles),
                    sprints: JSON.stringify(selectedSprints)
                }, showDataSet);
        }
    });
}

// SPRINT SELECTION
function makeSprintSelector() {

    $('#sprintselector').multiselect({
        enableClickableOptGroups: true,
        enableCollapsibleOptGroups: true,
        enableFiltering: true,
        includeSelectAllOption: true,
        maxHeight: 400,
        enableCaseInsensitiveFiltering: true,
        buttonContainer: '<div id="sprintselector-btn-group" class="btn-group" />',
        buttonText: function (options, select) {
            return 'Sprints';
        },
        onSelectAll: function (option, checked, select) {		//use the onChange event to listen to changes in the listbox
            var role_values = $('#roleselector option:selected');//add the selected options to a var
            var sprint_values = $('#sprintselector option:selected');

            var selectedRoles = $(role_values).map(function (index, option) {
                return $(option).val();		//put the values in the array
            });
            var selectedSprints = $(sprint_values).map(function (index, option) {
                return $(option).val();
            });
            console.log('SELECTED SPRINTS FIRST TIME', selectedSprints);
            // Array to keep track of selected checkboxes i.e. selected themes
            selectedRoles = selectedRoles.toArray();
            selectedSprints = selectedSprints.toArray();
            console.log('SELECTED SPRINTS SECOND TIME', selectedSprints);
            $.getJSON('/query', {
                    roles: JSON.stringify(selectedRoles),
                    sprints: JSON.stringify(selectedSprints)
                }, showDataSet);
        },
        onInitialized: function (select, container) {
            var $button = container.find("button").eq(0);
            $button.append('<span class="multiselect_icon sub_icon glyphicon glyphicon-dashboard" aria-hidden="true"></span>');
            console.log($button);

        },
        onChange: function (option, checked, select) {
            var sprint_values = $('#sprintselector option:selected');
            var role_values = $('#roleselector option:selected');
            console.log('CHECK THIS', role_values, sprint_values);
            var selectedSprints = $(sprint_values).map(function (index, option) {
                return $(option).val();
                //put the values in the array
            });
            var selectedRoles = $(role_values).map(function (index, option) {
                return $(option).val();		//put the values in the array
            });
            // Array to keep track of selected checkboxes i.e. selected themes
            selectedRoles = selectedRoles.toArray();

            //an array that keeps track of the selected chechboxes
            selectedSprints = selectedSprints.toArray();
            console.log('SELECTED SPRINTS THIRD TIME', selectedSprints);
            // function(){

            $.getJSON('/query', {
                sprints: JSON.stringify(selectedSprints),
                roles: JSON.stringify(selectedRoles)
            }, showDataSet);
            // return false;

        }


    });
}

// THEME SELECTION, NOT WORKING YET
$(document).ready(function () {
    $('#themeselector').multiselect({

        // dropRight: true
        enableClickableOptGroups: true,
        enableCollapsibleOptGroups: true,
        enableFiltering: true,
        includeSelectAllOption: true,
        maxHeight: 400,
        enableCaseInsensitiveFiltering: true,
        onChange: function (option, checked, select) {		//use the onChange event to listen to changes in the listbox
            var values = $('#themeselector option:selected');//add the selected options to a var

            var selectedThemes = $(values).map(function (index, option) {			//???
                return $(option).val();		//put the values in the array
            });
            // Array to keep track of selected checkboxes i.e. selected themes
            selectedThemes = selectedThemes.toArray();

            // window.s = selectedThemes;
            // console.log(selectedThemes);

            // show all edges
            edges.forEach(function (edge) {
                edges.update({id: edge.id, hidden: false});
            });

            nodes.forEach(function (node) {
                //The indexOf() method returns the position of the first occurrence of a specified value in a string.
                //This method returns -1 if the value to search for never occurs.
                var groupIsSelected = (selectedThemes.indexOf(node.theme) != -1);
                nodes.update({id: node.id, hidden: groupIsSelected});

                edges.forEach(function (edge) {
                    // arrows
                    // edges.update({id: edge.id, arrows: { to: { enabled: true}}});
                    var isConnectedToNode = (edge.from == node.id) || (edge.to == node.id);

                    if (isConnectedToNode && groupIsSelected) {
                        edges.update({id: edge.id, hidden: true});
                    }
                });
            });
        },

        buttonText: function (options, select) {
            return 'Themes';
        },
        onInitialized: function (select, container) {
            var $button = container.find("button").eq(0);
            $button.append('<span class="multiselect_icon sub_icon glyphicon glyphicon-tags" aria-hidden="true"></span>');
            console.log($button);
        }

    });


});

