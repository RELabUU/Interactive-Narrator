// insert the names of the roles into the checkbox labels of the ROLE and SPRINT MULTI-SELECTS
$(document).ready(function () {
    $.getJSON('/getroles', {}, function (data) {
        console.log(data);
        var i;
        for (i = 0; i < data.length; i++) {
            // console.log(data[i]);
            var roleValue = data[i];
            $("#roleselector").append($("<option></option>").attr("value", roleValue).attr('selected', 'selected').text(roleValue));

        }

        makeRoleSelector();
    });

    // populate the dropdown multiselect for sprints with spritn name + ID
    $.getJSON('/getsprints', {}, function (data) {
        console.log(data);
        var i;
        for (i = 0; i < data.length; i++) {
            var sprintValue = data[i];
            $("#sprintselector").append($("<option></option>").attr("value", sprintValue[1]).attr('selected', 'selected').text(sprintValue[0] + " (" + sprintValue[1] + ")"));

        }
        makeSprintSelector();
    });


});

// Show the help modal screen the first time a user logs in
$( document ).ready(function() {
  if (document.cookie.indexOf('visited=true') == -1){
    // load the overlay
    $('#helpModal').modal({show:true});

    var year = 1000*60*60*24*365;
    var expires = new Date((new Date()).valueOf() + year);
    document.cookie = "visited=true;expires=" + expires.toUTCString();

  }
});

//SLIDER JS
shown_edges = new vis.DataSet();

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
        nodes.update({id: node.id, hidden: false});
    });
    edges.forEach(function (edge) {
        edges.update({id: edge.id, hidden: false});
    });
    var relationshipsLabel = document.getElementById("relationships-on-off");
    relationshipsLabel.innerHTML = "ON";
}

//
$('#weightSlider').change(function () {
    var weight = $(this).val();
    var startTime1 = new Date();
    showAllNodes();
    var endTime1 = new Date() - startTime1;
    console.log(endTime1);
    // hide the nodes that are below weight
    nodes.forEach(function (node) {
        var nodeWeightBelowThreshold = (node.weight < weight);
        var nodeIsHidden = nodeWeightBelowThreshold;
        toggleNode(node, nodeIsHidden);


    });
    var endTime2 = new Date() - startTime1;
    console.log(endTime2);
    // edges.forEach(function(edge){
    //     if (!edge.hidden){
    //         shown_edges.add(edge);
    //     }
    //     // if(edge.hidden){
    //     //     shown_edges.remove(edge);
    //     // }
    //
    // });

    if (weight == 0) {
        showAllNodes();
    }
});

// var visible = true;
// toggle relationships on and off


$('#relationships').click(function () {

    shown_nodes = new vis.DataSet();

    var weight = $('#weightSlider').val();
    console.log(weight);
    //check if nodes are currenly hidden by the weightslider or not
    nodes.forEach(function (node) {

        var nodeWeightBelowThreshold = (node.weight < weight);
        console.log(nodeWeightBelowThreshold);
        var nodeIsHidden = nodeWeightBelowThreshold;

        if (!nodeIsHidden) {
            shown_nodes.add(node);
        }
        if (nodeIsHidden) {
            shown_nodes.remove(node);
        }
    });
    // if the weightslider is at 0, just turn all edges on/off
    if (weight == 0) {
        console.log('WEIGHT IS 0');

        edges.forEach(function (edge) {
            if (!edge.hidden) {
                edges.update({id: edge.id, hidden: true});
            }
            if (edge.hidden) {
                edges.update({id: edge.id, hidden: false});
            }

        });
    }
    //but if the weightslider has been moved...
    else {
        // console.log('WEIGHT IS NOT 0');

        node_names = [];
        //put all the shown nodes in an array
        shown_nodes.forEach(function (node) {

            node_names.push(node.id);

        });
        console.log('NODE NAMES OF SHOWN NODES', node_names);
        //if an edge is connected to a node that is shown (by to AND from) then it can be turned on/off
        edges.forEach(function (edge) {
            console.log(edge.from);
            edge_to_and_from = [];
                edge_to_and_from.push(edge.from);
                edge_to_and_from.push(edge.to);
                console.log('edge to and from:', edge_to_and_from);
                //if the edges to and from are in the array both:
                var success = edge_to_and_from.every(function(val) {
                    return node_names.indexOf(val) !== -1;
                });
            if (success) {
            // if ($.inArray(edge.from && edge.to, node_names) !== -1) {
                console.log('in there', edge.label, edge.from, edge.to);
                var edge_is_present = true;
                if (edge_is_present && edge.hidden) {
                    edges.update({id: edge.id, hidden: false});
                }
                else if (edge_is_present && !edge.hidden) {
                    edges.update({id: edge.id, hidden: true});
                }
            }
            else {
                console.log('not in there');
                edge_is_present = false;

            }


        });
    }
    var x = document.getElementById("relationships-on-off");
    if (x.innerHTML === "OFF") {
        console.log('label on');
        x.innerHTML = "ON";
    } else if (x.innerHTML === "ON"){
        x.innerHTML = "OFF";
        console.log('label off');
    }
    // console.log(shown_nodes, node_names);
});

//The function for the searchfield
$('#searchfield').change(function () {
    console.log('testing of the search field');
    var formInput = document.getElementById("searchfield").value;
    // foundItem = null; //we'll store the matching value here

    if (formInput === '') {
        nodes.forEach(function (node) {
            if (node.color == '#ECC348') {

                nodes.update({id: node.id, color: '#97C2FC', icon: {color:'#084ef4'}})
            }
        });
        edges.forEach(function (edge) {
            if (edge.color == '#ECC348') {
                edges.update({id: edge.id, color: '#97C2FC'})
            }
        });
        alert('Search results cleared');
        return false;
    }
    else {
        nodes.forEach(function (node) {
            // var selected = nodes.get(node.id);
            if (node.label == formInput) {
                console.log("i found it!");
                // var selected_nodes = [];
                // selected_nodes[0] = node.id;
                console.log(node);
                // nodes.selectNode(node);
                // node.color = undefined;
                // node.trigger('click');
                nodes.update({id: node.id, color: '#ECC348', icon: {color:'#ECC348'}});
                //color gets reset after 20 seconds
                setTimeout(function(){nodes.update({id: node.id, color: '#97C2FC', icon: {color:'#084ef4'}}) }, 20000);
            }
            else {
                nodes.update({id: node.id, color: '#97C2FC'})
            }
        });
        edges.forEach(function (edge) {
            if (edge.label == formInput) {
                edges.update({id: edge.id, color: '#ECC348'})
            }
            // else {
                // edges.update({id: edge.id, color: '#97C2FC'})

            // }
        });
    }
});
// network.on("selectNode", function (params) {
//
// }


//This document contains the functions to select nodes based on the user interface elements in the sidebar

window.onresize = function () {
    network.fit();
};

function showDataSet(data) {

    console.log('showDataSet is being executed', data);

    var nodes_dataset = new vis.DataSet();
    var edges_dataset = new vis.DataSet();

    nodes_dataset.add(data.nodes);
    edges_dataset.add(data.edges);
    console.log(nodes);
    console.log(edges);
    console.log(nodes_dataset);
    console.log(edges_dataset);

    var startTime2 = new Date();
    // updating the nodes //
    nodes.forEach(function (node) {
        var selected = nodes_dataset.get(node.id);
        // console.log(node.id);
        // console.log(selected);
        // if nothing is selected, make everything grey. NOT WORKING!
        if (!selected) {

            nodes.update({id: node.id, color: '#E8E8E8', font: {color: '#E8E8E8'}});
        }
        // else if a node is selected make it blue
        else {
            if (node.group == 'Role') {
                nodes.update({id: node.id, color: '#4A87F4', font: {color: '#343434'}});

            }
            else {
                nodes.update({id: node.id, color: '#97C2FC', font: {color: '#343434'}});
            }
        }
    });

    // if no roles are selected, return to the default appearance
    if (nodes_dataset.length == 0) {
        nodes.forEach(function (node) {
            nodes.update({id: node.id, color: '#97C2FC', font: {color: '#343434'}});

            if (node.group == 'Role') {
                nodes.update({id: node.id, color: '#4A87F4', font: {color: '#343434'}});

            }
        });

    }

    // updating the edges //
    edges.forEach(function (edge) {
        var selected = edges_dataset.get(edge.id);
        // console.log(edge.id);
        // if edges are not part of the selection, make them grey
        if (!selected) {
            edges.update({id: edge.id, color: '#E8E8E8', font: {color: '#E8E8E8'}});
        }
        //else make all edges blue
        else {
            edges.update({id: edge.id, color: '#5898ED', font: {color: '#343434'}});
        }

    });

    // if no roles are selected or a selected role has no relationships, return to the default appearance
    if (edges_dataset.length == 0 && nodes_dataset.length == 0) {
        edges.forEach(function (edge) {
            edges.update({id: edge.id, color: '#5898ED', font: {color: '#343434'}});
        });

    }

    // console.log(nodes_dataset);
    var endTime3 = new Date() - startTime2;
    console.log(endTime3);
}

//    ROLE SELECTION
function makeRoleSelector() {
    $('#roleselector').multiselect({
        enableClickableOptGroups: true,
        enableCollapsibleOptGroups: true,
        enableFiltering: true,
        includeSelectAllOption: false,
        maxHeight: 400,
        enableCaseInsensitiveFiltering: true,
        buttonContainer: '<div id="roleselector-btn-group" class="btn-group" />',
        buttonText: function (options, select) {
            return 'Roles';
        },

        onSelectAll: function (option, checked, select) {		//if all boxes in a listbox are checked...
            console.log('onSelectAll is being executed');
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
        includeSelectAllOption: false,
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

//some functions to help keep the sidebar and its menus open on certain clicks
$('.sidebar-nav > a').click(function (e) {
    e.stopPropagation();
    });


$(".sidebar-nav").on('click', function (e) {
    if(!$("#wrapper").hasClass("toggled")){
        $("#wrapper").addClass("toggled");
        }
        });



if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
    deviceEventType = 'touchstart'
} else {
//If its not a mobile device use 'click'
    deviceEventType = 'click'
}

console.log(deviceEventType);
//Keep the dropdowns open when clicking anywhere but a dropdown button
$('body').on('click', function (e) {
    // $(this).parent().is(".open") && e.stopPropagation();
    console.log(e);
    if ($("div#roleselector-btn-group.btn-group").is(e.target)){
        console.log('log this');
    }
    if (!$(".multiselect.dropdown-toggle.btn.btn-default").is(e.target)){
        if ($("#roleselector-btn-group").hasClass("open")) {
            e.stopPropagation();
        }
        if ($("#sprintselector-btn-group").hasClass("open")) {
            e.stopPropagation();
        }
    }
});




// EXPERIMENTAL CODE TO KEEP SIDEBAR AND ITS MENUS OPEN ON CLICKS

// $(document).on('click', 'someyourContainer .dropdown-menu', function (e) {
//   e.stopPropagation();
// });
//
// $('#roleselector').on('hide.bs.dropdown', function (e) {
//     var target = $(e.target);
//     if(target.hasClass("keepopen") || target.parents(".keepopen").length){
//         return false; // returning false should stop the dropdown from hiding.
//     }else{
//         return true;
//     }
// });


// $("body").on( "click", ".multiselect.dropdown-toggle.btn.btn-default", function( event ) {
//     console.log(event);
//   event.stopPropagation();
// });

// $(function() {
//     var closeble = false;
//     $('body').on('click', function (e) {
//         if (!$(event.target).is("a.dropdown-toggle")) {
//             closeble = false;
//         }
//
//     });
//
//     $('.dropdown').on({
//         "click": function (event) {
//             if ($(event.target).closest('.dropdown-toggle').length) {
//                 closeble = true;
//             } else {
//                 closeble = false;
//             }
//         },
//         "hide.bs.dropdown": function () {
//             return closeble;
//         }
//     });
// });


// $('#roleselector').on('hide.bs.dropdown', function (e) {
//     var target = $(e.target);
//     console.log('target', target);
//     if(target.hasClass("keepopen") || target.parents(".keepopen").length){
//         return false; // returning false should stop the dropdown from hiding.
//     }else{
//         return true;
//     }
// });
          // Keep the dropdowns open when clicking on the visualization
// $('body').on('touchstart', function() {
//     console.log("touch on visualization registered");
//     if ($("#roleselector-btn-group").hasClass("open")) {
//         console.log('it has open class');
//         $('.multiselect.dropdown-toggle.btn.btn-default').dropdown('toggle');
//
//         // setTimeout(function () {
//         //     $("#roleselector-btn-group").addClass('open');
//         //     console.log('timeout function works');
//         // })
//     }
//     if ($("#sprintselector-btn-group").hasClass("open")) {
//
//         setTimeout(function () {
//             $("#sprintselector-btn-group").addClass('open');
//         })
//     }
//     else{
//         console.log('do nothing');
//         // $("#roleselector-btn-group").addClass('open');
//     }
//  });

          // Keep the dropdowns open when clicking elsewhere
          // $('body').on('click.hideMenu', function(e) {
          //     // console.log("click on body registered");
          //     // console.log('target from click.hidemenu', e.target, e.target.class);
          //     var target = $(e.target);
          //
          //     if ($(target).is('#relationships')) {
          //         console.log('relationships button clicked');
          //            if ($('#sprintselector-btn-group').hasClass('open')) {
          //               setTimeout(function () {
          //                     $("#sprintselector-btn-group").addClass('open');
          //                 })
          //            }
          //               if ($('#roleselector-btn-group').hasClass('open')) {
          //               setTimeout(function () {
          //                     $("#roleselector-btn-group").addClass('open');
          //                 })
          //            }
          //            if ($('#roleselector-btn-group' && '#sprintselector-btn-group').hasClass('open')) {
          //                                      console.log("both are open");
          //                setTimeout(function () {
          //                     $("#roleselector-btn-group" && "#sprintselector-btn-group").addClass('open');
          //                 })
          //
          //            }
          //     }
          //
          //         if ($('#sprintselector-btn-group').has(target).length) {
          //             console.log("event target is button");
          //
          //
          //             if ($('#roleselector-btn-group').hasClass('open')) {
          //                 console.log("roles has class open");
          //
          //                 setTimeout(function () {
          //                     $("#roleselector-btn-group").addClass('open');
          //                 })
          //             }
          //         }
          //
          //         if ($('#roleselector-btn-group').has(target).length) {
          //
          //             if ($('#sprintselector-btn-group').hasClass('open')) {
          //                 console.log("sprints has class open");
          //
          //                 setTimeout(function () {
          //                     $("#sprintselector-btn-group").addClass('open');
          //                 })
          //
          //             }
          //         }
          //
          //     });
