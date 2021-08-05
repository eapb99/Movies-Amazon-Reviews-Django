const dates = []
const scores = []
const ayuda = []
let graph = document.querySelector('#graph')
graph.style.display = 'none'
let myChart;
let mean_healp = 0

function llenar(data, id) {
    $(`#${id}`).DataTable({
        "data": data,
        responsive: true,
        "paging": false,
        autoWidth: true,
        paginate: true,
        destroy: true,
        searching: false,
        "ordering": false,
        "columns": [{"data": 0}, {"data": 1}, {"data": 2}, {"data": 3}, {"data": 4}, {"data": 5}, {"data": 6}]
    });
}

function createcards(data) {
    let left = document.querySelector('#top')
    left.innerHTML = ''
    let information = [{'icon': 'user', 'color': 'warning'}, {
        'icon': 'sort-up',
        'color': 'success'
    }, {'icon': 'sort-down', 'color': 'info'}, {'icon': 'sort', 'color': 'lightblue'}]
    let c = 0;
    if (data != '') {
        for (const property in data['cantidad']) {
            let valor = information[c]
            let plantilla = `
                            <div class="col-sm-6 col-md-3">
                                <div class="info-box mb-3 bg-${valor['color']}">
                                    <span class="info-box-icon"><i class="fas fa-${valor['icon']}"></i></span>
                                    <div class="info-box-content">
                                        <span class="info-box-text">${property}</span>
                                        <span class="info-box-number">${data['cantidad'][property]}</span>
                                    </div>
                                </div>
                            </div>`
            left.innerHTML += plantilla
            c++;
        }
    } else {
        left.innerHTML = ''
    }

}

function graficar(data, scores, prom, ayuda, meanhelp, graph) {
    console.log(graph)
    if (data != '') {
        graph.style.display = 'block'
        let ctx = document.getElementById('myChart').getContext('2d');
        if (myChart)
            myChart.destroy()
        myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data,
                datasets: [{
                    label: 'Score por fecha',
                    data: scores,
                    borderColor: 'rgb(75, 192, 192)',
                    yAxisID: 'y',
                }, {
                    label: 'Promedio de Score',
                    data: Array(dates.length).fill(prom),
                    borderColor: 'rgb(94, 83, 81)'
                },
                    {
                        label: 'Helfulness por Fecha',
                        data: ayuda,
                        borderColor: 'rgb(244, 83, 81)',
                        yAxisID: 'y1',
                    },
                    {
                        label: 'Promedio de HelpFulness',
                        data: Array(dates.length).fill(meanhelp),
                        borderColor: 'rgb(100, 25, 81)'
                    }

                ]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        type: 'linear',
                        display: true,
                        position: 'right',
                    },
                    y1: {
                        beginAtZero: true,
                        type: 'linear',
                        display: true,
                        position: 'left',
                    }
                }
            }
        })
    } else {
        console.log("wq")
        graph.style.display = 'none'
    }
}


function extracted(array1, array2, dates, scores, ayuda) {

    for (let i = 0; i < array1.length; i++) {
        let value = array1[i][6].split('T')[0]
        let value2 = array2[i][6].split('T')[0]
        if (!dates.includes(value)) {
            dates.push(value)
            scores.push(array1[i][4])
            ayuda.push(array1[i][3])
        }
        if (!dates.includes(value2)) {
            dates.push(value2)
            scores.push(array2[i][4])
            ayuda.push(array1[i][3])
        }
    }
}


function responseData(data) {
    if (data['data'] != '') {
        let array1 = data['data'][1]
        let array2 = data['data'][0]
        extracted(array1, array2, dates, scores, ayuda);
        let sum = 0;
        for (var i = 0; i < ayuda.length; i++) {
            sum += ayuda[i];
        }
        mean_healp = sum / ayuda.length;
        createcards(data);
        llenar(data['data'][1], 'best')
        llenar(data['data'][0], 'worst')
        graficar(dates, scores, data['cantidad']['Score Promedio'], ayuda, mean_healp, graph)
    } else {
        Swal.fire({
            title: 'Error!',
            text: 'No existe informacion para ese registro',
            icon: 'error',
        })
        createcards('');
        llenar([], 'best')
        llenar([], 'worst')
        graficar('', scores, data['cantidad']['Score Promedio'], ayuda, mean_healp, graph)
    }

}