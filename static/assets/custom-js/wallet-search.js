
// $(document).ready(function() {
//   $('#walletListTableId').DataTable();
// } );


$(document).ready(function() {
  $('#walletListTableId').DataTable();

  $.fn.dataTable.ext.search.push(function(settings, data, dataIndex) {
    // Get the value entered in the filter input field (assuming you have an input field with ID "nameFilter")
    var filterValue = $('#searchMobile').val().trim().toLowerCase();
    
    // Get the value in the "Name" column for the current row
    var nameColumnValue = data[2].toLowerCase();

    // Perform the filtering based on your criteria (e.g., simple substring matching)
    if (nameColumnValue.includes(filterValue)) {
      return true; // Display the row in the table
    }

    return false; // Hide the row from the table
  });

  // Trigger the custom filter when the user types in the filter input field
  $('#searchMobile').on('keyup', function() {
    $('#walletListTableId').DataTable().draw(); // Redraw the table to apply the filter
  });


  $.fn.dataTable.ext.search.push(function(settings, data, dataIndex) {
    // Get the value entered in the filter input field (assuming you have an input field with ID "nameFilter")
    var filterValue = $('#searchType').val().trim().toLowerCase();
    
    // Get the value in the "Name" column for the current row
    var nameColumnValue = data[5].toLowerCase();

    // Perform the filtering based on your criteria (e.g., simple substring matching)
    if (nameColumnValue.includes(filterValue)) {
      return true; // Display the row in the table
    }

    return false; // Hide the row from the table
  });

  // Trigger the custom filter when the user types in the filter input field
  $('#searchType').on('change', function() {
    $('#walletListTableId').DataTable().draw(); // Redraw the table to apply the filter
  });



  $.fn.dataTable.ext.search.push(function(settings, data, dataIndex) {
    // Get the value entered in the filter input field (assuming you have an input field with ID "nameFilter")
    var filterValue = $('#searchMethod').val().trim().toLowerCase();
    
    // Get the selected value from the 9th column (index 8) of the data array
    var nameColumnValue = data[8].toLowerCase();
    console.log(nameColumnValue);
    // Perform the filtering based on your criteria (e.g., simple substring matching)
    if (nameColumnValue.includes(filterValue)) {
      return true; // Display the row in the table
    }

    return false; // Hide the row from the table
  });

  // Trigger the custom filter when the user types in the filter input field
  $('#searchMethod').on('change', function() {
    $('#walletListTableId').DataTable().draw(); // Redraw the table to apply the filter
  });
  


  $.fn.dataTable.ext.search.push(function(settings, data, dataIndex) {
    // Get the value entered in the filter input field (assuming you have an input field with ID "nameFilter")
    var filterValue = $('#searchUTR').val().trim().toLowerCase();
    
    // Get the selected value from the 10th column (index 9) of the data array
    var nameColumnValue = data[9].toLowerCase();
    console.log(nameColumnValue);
    // Perform the filtering based on your criteria (e.g., simple substring matching)
    if (nameColumnValue.includes(filterValue)) {
      return true; // Display the row in the table
    }
    return false; // Hide the row from the table
  });

  // Trigger the custom filter when the user types in the filter input field
  $('#searchUTR').on('keyup', function() {
    $('#walletListTableId').DataTable().draw(); // Redraw the table to apply the filter
  });

});


// Search data by date range (for orders and view delivery delivered) 
// $(function() {
//   var table = $("#walletListTableId").DataTable();    
//   // Date range vars
//   minDateFilter = "";
//   maxDateFilter = "";  
//   $("#reservation").daterangepicker();
//   $("#reservation").on("apply.daterangepicker", function(ev, picker) {
//     minDateFilter = Date.parse(picker.startDate);
//     maxDateFilter = Date.parse(picker.endDate);
//     $.fn.dataTable.ext.search.push(function(settings, data, dataIndex) {
//     var date = Date.parse(data[6]);  
//     if (
//     (isNaN(minDateFilter) && isNaN(maxDateFilter)) ||
//     (isNaN(minDateFilter) && date <= maxDateFilter) ||
//     (minDateFilter <= date && isNaN(maxDateFilter)) ||
//     (minDateFilter <= date && date <= maxDateFilter)
//     ) {
//     return true;
//     }
//     return false;
//   });
//   table.draw();
//   });
// });