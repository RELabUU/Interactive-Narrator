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
                nodes.update({id: node.id, color: '#97C2FC', font:{color:'#343434'}});

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
            console.log(selectedSprints);
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
