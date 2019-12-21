var url = "http://127.0.0.1:5000/";
var url2 = "http://127.0.0.1:5000/f";
var tbody = d3.select("tbody");




$(document).ready(function() {
    fetch(url)
        .then(d => d.json())
        .then(data => {
            console.log(data)
            let sliced = data.result.slice(0,200);
            
            $('#data-table').DataTable( {
                data: data.result,
                deferRender: true,
                responsive: true,
                // scrollX: true,
                scrollCollapse: true,
                autoWidth: true,  
                paging: true,
                columnDefs: [
                    {targets: 2,
                    render: function ( data, type, row ) {
                        return type === 'display' && data.length > 10 ?
                            data.substr( 0, 250) +'…' :
                            data}
                    }],
                columns: [
                    { data : "Title"},
                    { data : "JobCategory"},
                    { data : "Description"}
                ]
            });
        });

});

d3.json(url2).then(function(data) {
    var category = data[0];
    var Jobs_added = data[1];
    var jobs_filled = data[2];
    var date = data[3];
    console.log(date);
    // console.log(Jobs_added.newJ)
    // console.log(Jobs_added.newJ.length)
    

    let new_J = [];
    for (var i = 0; i < Jobs_added.newJ.length; i++) {
        new_J.push(Jobs_added.newJ[i].Jobs_added)
    };

    let new_D = [];
    for (var i = 0; i < date.dates.length; i++) {
        new_D.push(date.dates[i].Dates)
    };


    // var trace1 = {
    //     x: new_D,
    //     y: new_J,
    //     type: "scatter"
    // };

    // var data = trace1

    // var layout = {
    //     title: "Yey"
    // };

    // Plotly.newPlot("plot", data, layout)


    datax = [{
        x: new_D,
        y: new_J}]
    var LINE = document.getElementById("plot");
    Plotly.plot(LINE, datax);
    


});












//             // tbody = $("#tbody")
//             // let title = $("#title") 
//             // let description = $("#description") 
//             // let category = $("#category") 
//             // data.result.forEach(element => {
//             //     console.log(element)
//             //     tbody.append("<tr><td>" + element.Title + "</td>"  + "<td>" + element.JobCategory + "</td>" + "<td><div><div class=turnicatedData>" + element.Description + "</div><button class='btn btn-primary'>more</button></div></td> </tr>")



//             // });
            
       
    
// });



// $('#exampleModal').on('show.bs.modal', function (event) {
//     var button = $(event.relatedTarget) // Button that triggered the modal
//     var recipient = button.data('obj') // Extract info from data-* attributes
//     // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
//     // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
//     console.log(recipient);
//     // read values from row according to number (data-obj)
//     var modal = $(this)
//     modal.find('.modal-title').text('New message to ' + recipient)
//     modal.find('.modal-body').text(recipient)
//   });



// d3.json(url).then(function(data) {
//     // sliced = data.result.slice(0,100)
//     data.result.forEach(function(job, i) {
//         var row = tbody.append("tr").attr("data-obj",i);
//         row.append("td").text(job.Title)
//         row.append("td").text(job.JobCategory)
//         wrapper = row.append("td").append("div");
//         wrapper.append("div").attr("class","turnicatedData").text(job.Description)
//         wrapper.append("button")
//             .attr("class", "btn btn-primary")
//             .attr("data-toggle", "modal")
//             .attr("data-target", "#exampleModal")
//             .attr("data-obj", i)
//             .text("see more")
        
//     });
// });

// $(document).ready(function() {
//     $('#data-table').DataTable( {
//         "ajax": {
//             "url": url,
//             "dataSrc": 'result'
//         },
//         "columns": [ 
//             {"result": "Category"},
//             {"result": "Title"},
//             {"result": "Description"}
//         ]

//     });


// });
