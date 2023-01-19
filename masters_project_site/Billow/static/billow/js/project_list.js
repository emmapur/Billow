/* Formatting function for row details - modify as you need */
function format(d) {
    // `d` is the original data object for the row
    return (
        '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">' +
        '<tr>' +
        '<td>Full name:</td>' +
        '<td>' +
        d.name +
        '</td>' +
        '</tr>' +
        '<tr>' +
        '<td>Extension number:</td>' +
        '<td>' +
        d.extn +
        '</td>' +
        '</tr>' +
        '<tr>' +
        '<td>Extra info:</td>' +
        '<td>And any further details here (images etc)...</td>' +
        '</tr>' +
        '</table>'
    );
}

$(document).ready(function () {
    var table = $('#datatable-instance-list').DataTable();
    var tr = $(this).closest('tr');
    var row = table.row(tr);
    var row_data = row.data()
  //  var cloud_name = row_data[3]
    var instance_name = row_data[1]

    var team_name = project_list[instance_name]['team']
  //  var ra = athlone_project_list[cloud_name][project_name]['ra']

};

    // Add event listener for opening and closing details
    $('#datatable-instance-list tbody').on('click', 'td.dt-control', function () {
        var tr = $(this).closest('tr');
        var row = table.row(tr);

        if (row.child.isShown()) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        } else {
            // Open this row
            row.child(format(row.data())).show();
            tr.addClass('shown');
        }
    });
});
