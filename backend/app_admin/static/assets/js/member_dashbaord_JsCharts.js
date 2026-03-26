
// Bill Payment Chart
new Chart(document.getElementById('bill_payment_method'), {
    type: 'doughnut',
    data: {
        datasets: [{
            label: 'Types of Billing',
            data: [
            {% for p in  billing_detail %}
        '{{p.count}}',
        {%endfor%}  
          ],
          backgroundColor: [
        {% for c in billing_detail %}
          random(),
          {% endfor %}
        ],
    }],
    labels: [
    {% for p in  billing_detail %}
   '{{p.payment_method__name}}',
     {%endfor%}
      

        ]
    },
    legend: {
        display: false
    },

    options: {
        responsive: true,

        cutoutPercentage: 60,
        legend: {
            position: 'bottom',
            display: true,
           
            
        },

        tooltips: {
            enabled: true,
            cornerRadius: 0,
            bodyFontColor: '#fff',
            bodyFontSize: 14,
            fontStyle: 'bold',

            backgroundColor: 'rgba(34, 34, 34, 0.73)',
            borderWidth: 0,

            caretSize: 5,

            xPadding: 12,
            yPadding: 12,

            callbacks: {
                label: function (tooltipItem, data) {
                    var label = data.labels[tooltipItem.index]
                    return ' ' + label + " " + data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index] + ''
                }
            }
        }
    }
})

// Installment Payment Chart
new Chart(document.getElementById('installment_payment_method'), {
type: 'doughnut',
data: {
    datasets: [{
        label: 'Types of Billing',
        data: [
        {% for p in  payment_detail %}
        '{{p.count}}',
        {%endfor%}  
          ],
          backgroundColor: [
        {% for c in payment_detail %}
          random(),
          {% endfor %}
        ],
    }],
    labels: [
    {% for p in  payment_detail %}
   '{{p.payment_method__name}}',
     {%endfor%}
      

    ]
},
legend: {
    display: false
},

options: {
    responsive: true,
    cutoutPercentage: 60,
    legend: {
        position: 'bottom',
        display: true,
    },

    tooltips: {
        enabled: true,
        cornerRadius: 0,
        bodyFontColor: '#fff',
        bodyFontSize: 14,
        fontStyle: 'bold',

        backgroundColor: 'rgba(34, 34, 34, 0.73)',
        borderWidth: 0,

        caretSize: 5,

        xPadding: 12,
        yPadding: 12,

        callbacks: {
            label: function (tooltipItem, data) {
                var label = data.labels[tooltipItem.index]
                return ' ' + label + ":" + data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index] + ''
            }
        }
    }
}
})

// Current Bills Chart
new Chart(document.getElementById('current_bills'), {
type: 'doughnut',
data: {
    datasets: [{
        label: 'Types of Billing',
        data: [
        {% for b in  billing_status_detail %}
        '{{b.count}}',
        {%endfor%}  
          ],
          backgroundColor: [
        {% for b in billing_status_detail %}
          random(),
          {% endfor %}
        ],
    }],
    labels: [
    {% for b in  billing_status_detail %}
   '{{b.status__name}}',
     {%endfor%}

    ]
},

options: {
    responsive: true,
    cutoutPercentage: 60,
    legend: {
        position: 'bottom',
        display: true,
    },

    tooltips: {
        enabled: true,
        cornerRadius: 0,
        bodyFontColor: '#fff',
        bodyFontSize: 14,
        fontStyle: 'bold',

        backgroundColor: 'rgba(34, 34, 34, 0.73)',
        borderWidth: 0,

        caretSize: 5,

        xPadding: 12,
        yPadding: 12,

        callbacks: {
            label: function (tooltipItem, data) {
                var label = data.labels[tooltipItem.index]
                return ' ' + label + ":" + data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index] + ''

            }
        }
    }
}
})

// Current Bills Chart
new Chart(document.getElementById('current_installment'), {
type: 'doughnut',
data: {
    datasets: [{
        label: 'Types of Billing',
        data: [
        {% for s in  status_detail %}
        '{{s.count}}',
        {%endfor%}  
          ],
          backgroundColor: [
        {% for c in status_detail %}
          random(),
          {% endfor %}
        ],
    }],
    labels: [
    {% for s in  status_detail %}
   '{{s.status__name}}',
     {% endfor %}
    ]
},

options: {
    responsive: true,
    cutoutPercentage: 60,
    legend: {
        position: 'bottom',
        display: true,
    },

    tooltips: {
        enabled: true,
        cornerRadius: 0,
        bodyFontColor: '#fff',
        bodyFontSize: 14,
        fontStyle: 'bold',

        backgroundColor: 'rgba(34, 34, 34, 0.73)',
        borderWidth: 0,

        caretSize: 5,

        xPadding: 12,
        yPadding: 12,

        callbacks: {
            label: function (tooltipItem, data) {
                var label = data.labels[tooltipItem.index]
                return ' ' + label + ":" + data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index] + ''
            }
        }
    }
}
})

// Property Catogory Charts

function random(){
return "#000000".replace(/0/g,function(){return (~~(Math.random()*16)).toString(16);});
}

new Chart(document.getElementById('property_category'), {
type: 'doughnut',
data: {
    datasets: [{
        label: 'Types of Billing',
        
        data: [
        {% for c in category_count_list %}
          '{{c.count}}',
          {% endfor %}
          ],
        
        backgroundColor: [
        {% for c in category_count_list %}
          random(),
            {% endfor %}
        ],
        
    }],
    labels: [
        {% for c in category_count_list %}
        '{{c.plot_size}}'
        {% endfor %}

    ]
},

options: {
    responsive: true,
    // maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height 
    cutoutPercentage: 60,
    legend: {
        position: 'bottom',
        display: true,
    },
    // animation: {
    //   // animateScale: true,
    //   animateRotate: true,
    //   duration: _animate ? 1000 : false
    // },
    tooltips: {
        enabled: true,
        cornerRadius: 0,
        bodyFontColor: '#fff',
        bodyFontSize: 14,
        fontStyle: 'bold',

        backgroundColor: 'rgba(34, 34, 34, 0.73)',
        borderWidth: 0,

        caretSize: 5,

        xPadding: 12,
        yPadding: 12,

        callbacks: {
            label: function (tooltipItem, data) {
                var label = data.labels[tooltipItem.index]
                return ' ' + label + ":" + data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index]

            }
        }
    }
}
})

// Property Status Charts
new Chart(document.getElementById('property_status'), {
type: 'doughnut',
data: {
    datasets: [{
        label: 'Property Status',
        data: [
        {% for c in property_status %}
          '{{c.count}}',
          {% endfor %}
          ],
        
        backgroundColor: [
        {% for c in property_status %}
          random(),
            {% endfor %}
        ],
        
    }],
    labels: [
        {% for c in property_status %}
        '{{c.status|title}}'
        {% endfor %}
    ]
},

options: {
    responsive: true,
    cutoutPercentage: 60,
    legend: {
        position: 'bottom',
        display: true,
    },
    // animation: {
    //   // animateScale: true,
    //   animateRotate: true,
    //   duration: _animate ? 1000 : false
    // },
    tooltips: {
        enabled: true,
        cornerRadius: 0,
        bodyFontColor: '#fff',
        bodyFontSize: 14,
        fontStyle: 'bold',

        backgroundColor: 'rgba(34, 34, 34, 0.73)',
        borderWidth: 0,

        caretSize: 5,

        xPadding: 12,
        yPadding: 12,

        callbacks: {
            label: function (tooltipItem, data) {
                var label = data.labels[tooltipItem.index]
                return ' ' + label + ":" + data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index]

            }
        }
    }
}
})



// Bill Time Line Chart
$('canvas.bill-timeline-chart').each(function () {
var ctx = this.getContext('2d');
var gradientbg = ctx.createLinearGradient(0, 0, 0, 50);
gradientbg.addColorStop(0, 'rgba(109, 187, 109, 0.25)');
gradientbg.addColorStop(1, 'rgba(109, 187, 109, 0.05)');

let data = $(this).data('values');

new Chart(ctx, {
    type: 'line',
    data: {
        labels: ["Jan", "Feb", "Mar", "Apr", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        datasets: [{
                data: data,
                backgroundColor: gradientbg,
                hoverBackgroundColor: '#70bcd9',
                fill: true,

                borderColor: 'rgba(109, 187, 109, 0.8)',

                borderWidth: 2.25,
                pointRadius: 7,
                lineTension: 0.4,

                pointBackgroundColor: 'transparent',
                pointBorderColor: 'transparent',

                pointHoverBackgroundColor: 'rgba(109, 187, 109, 0.8)',
                pointHoverBorderColor: 'rgba(109, 187, 109, 0.8)',
            },
            {
                type: 'bar',
                data: data,
                backgroundColor: 'transparent',
                hoverBackgroundColor: 'transparent',
                fill: false,

                borderColor: 'transparent',

                barPercentage: 0.8
            },
        ]
    },

    options: {

        responsive: false,


        legend: {
            display: false
        },
        layout: {
            padding: {
                left: 10,
                right: 10,
                top: 0,
                bottom: -10
            }
        },
        scales: {
            yAxes: [{
                stacked: true,
                ticks: {
                    display: false,
                    beginAtZero: true,
                },
                gridLines: {
                    display: false,
                    drawBorder: false
                }
            }],

            xAxes: [{
                stacked: true,
                gridLines: {
                    display: false,
                    drawBorder: false
                },
                ticks: {
                    display: false //this will remove only the label
                }
            }, ]
        }, //scales

        tooltips: {
            // Disable the on-canvas tooltip, because canvas area is small and tooltips will be cut (clipped)
            enabled: false,
            mode: 'index',

            //use bootstrap tooltip instead
            custom: function (tooltipModel) {
                var title = '';
                var canvas = this._chart.canvas;

                if (tooltipModel.body) {
                    title = tooltipModel.title[0] + ': ' + Number(tooltipModel.body[0].lines[0]).toLocaleString();
                }
                canvas.setAttribute('data-original-title', title); //will be used by bootstrap tooltip

                $(canvas)
                    .tooltip({
                        placement: 'bottom',
                        template: '<div class="tooltip" role="tooltip"><div class="brc-info-d2 arrow"></div><div class="bgc-info-d2 tooltip-inner text-600 text-110"></div></div>'
                    })
                    .tooltip('show')
                    .on('hidden.bs.tooltip', function () {
                        canvas.setAttribute('data-original-title', ''); //so that when mouse is back over canvas's blank area, no tooltip is shown
                    });

            }
        } // tooltips

    }
})
})

// "Property Time Line Chart
var months = ["Jan", "Feb", "Mar", "Apr", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
var data = [];
var recieved_data =[]
{% for m in members %}
recieved_data.push('{{m.allotment_date|date:"M"}}')
// recieved_data.push('Nov')
recieved_data.push('Jan')

{% endfor %}
for(var i=0 ;i<months.length;i++){
for(var j=0; j<recieved_data.length; j++){
if(months[i] == recieved_data[j]){

data[i] = 1
}
else{
if(data[i] != null){
  break
}
else{
  data[i] = 0
}
}
}
}
console.log(recieved_data,data)

$('canvas.property-timeline-chart').each(function () {
    var ctx = this.getContext('2d');
    var gradientbg = ctx.createLinearGradient(0, 0, 0, 50);
    gradientbg.addColorStop(0, 'rgba(109, 187, 109, 0.25)');
    gradientbg.addColorStop(1, 'rgba(109, 187, 109, 0.05)');

    let data = $(this).data('values');

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ["Jan", "Feb", "Mar", "Apr", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            datasets: [{
                    data: data,
                    backgroundColor: gradientbg,
                    hoverBackgroundColor: '#70bcd9',
                    fill: true,

                    borderColor: 'rgba(109, 187, 109, 0.8)',

                    borderWidth: 2.25,
                    pointRadius: 7,
                    lineTension: 0.4,

                    pointBackgroundColor: 'transparent',
                    pointBorderColor: 'transparent',

                    pointHoverBackgroundColor: 'rgba(109, 187, 109, 0.8)',
                    pointHoverBorderColor: 'rgba(109, 187, 109, 0.8)',
                },
                {
                    type: 'bar',
                    data: data,
                    backgroundColor: 'transparent',
                    hoverBackgroundColor: 'transparent',
                    fill: false,

                    borderColor: 'transparent',

                    barPercentage: 0.8
                },
            ]
        },

        options: {

            responsive: false,


            legend: {
                display: false
            },
            layout: {
                padding: {
                    left: 10,
                    right: 10,
                    top: 0,
                    bottom: -10
                }
            },
            scales: {
                yAxes: [{
                    stacked: true,
                    ticks: {
                        display: false,
                        beginAtZero: true,
                    },
                    gridLines: {
                        display: false,
                        drawBorder: false
                    }
                }],

                xAxes: [{
                    stacked: true,
                    gridLines: {
                        display: false,
                        drawBorder: false
                    },
                    ticks: {
                        display: false //this will remove only the label
                    }
                }, ]
            }, //scales

            tooltips: {
                // Disable the on-canvas tooltip, because canvas area is small and tooltips will be cut (clipped)
                enabled: false,
                mode: 'index',

                //use bootstrap tooltip instead
                custom: function (tooltipModel) {
                    var title = '';
                    var canvas = this._chart.canvas;

                    if (tooltipModel.body) {
                        title = tooltipModel.title[0] + ': ' + Number(tooltipModel.body[0].lines[0]).toLocaleString();
                    }
                    canvas.setAttribute('data-original-title', title); //will be used by bootstrap tooltip

                    $(canvas)
                        .tooltip({
                            placement: 'bottom',
                            template: '<div class="tooltip" role="tooltip"><div class="brc-info-d2 arrow"></div><div class="bgc-info-d2 tooltip-inner text-600 text-110"></div></div>'
                        })
                        .tooltip('show')
                        .on('hidden.bs.tooltip', function () {
                            canvas.setAttribute('data-original-title', ''); //so that when mouse is back over canvas's blank area, no tooltip is shown
                        });

                }
            } // tooltips

        }
    })
})


