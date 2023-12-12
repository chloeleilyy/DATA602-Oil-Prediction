var chart = echarts.init(document.getElementById('container'));

fetch('http://127.0.0.1:5000/all_oil_price')
    .then(response => response.json())
    .then(data => {
        var originalData = [];
        var predictionData = [];

        data.forEach(function (item) {
            var date = new Date(item.date.replace(/-/g, '/'));
            originalData.push([date, item.oil_price]);
            predictionData.push([date, item.prediction]);
        });

        var option = {
            title: {
                text: 'Original Price VS Predicted Price',
                left: 'center'
            },
            tooltip: {
                trigger: 'axis',
                formatter: function (params) {
                    var date = new Date(params[0].name);
                    return params[0].value[0] +
                        '<br>original: ' + params[0].value[1] +
                        '<br>predict: ' + params[1].value[1];
                },
                axisPointer: {
                    animation: false
                }
            },
            legend: {
                data: ['original data', 'predict data'],
                left: 'right'
            },
            xAxis: {
                type: 'time',
                name: 'Data',
                splitLine: {
                    show: false
                },
                axisLabel: {
                    fontWeight: 'bold',
                    fontSize: 12
                }
            },
            yAxis: {
                type: 'value',
                name: 'Oil Price',
                boundaryGap: [0, '100%'],
                splitLine: {
                    show: false
                },
                axisLabel: {
                    fontWeight: 'bold',
                    fontSize: 12
                }
            },
            dataZoom: [{
                type: 'inside',
                start: 0,
                end: 100
            }, {
                start: 0,
                end: 100,
                handleIcon: 'M10 0 L5 10 L0 0 L5 0 L5 10 Z',
                handleSize: '80%',
                handleStyle: {
                    color: '#fff',
                    shadowBlur: 3,
                    shadowColor: 'rgba(0, 0, 0, 0.6)',
                    shadowOffsetX: 2,
                    shadowOffsetY: 2
                }
            }],
            series: [{
                name: 'original data',
                type: 'line',
                showSymbol: false,
                hoverAnimation: false,
                data: originalData,
                lineStyle: {
                    color: 'red'
                }
            }, {
                name: 'predict data',
                type: 'line',
                showSymbol: false,
                hoverAnimation: false,
                data: predictionData,
                lineStyle: {
                    color: 'black'
                }
            }]
        };
        chart.setOption(option);
    });

window.addEventListener('resize', function () {
    chart.resize();
});

function updateCurrentDate() {
    var currentDateElement = document.getElementById('current-date');
    var currentDate = new Date();
    var formattedDate = currentDate.getFullYear() + '-' + (currentDate.getMonth() + 1) + '-' + currentDate.getDate();
    currentDateElement.innerHTML = 'Update Time:' + formattedDate;
}

updateCurrentDate();
setInterval(updateCurrentDate, 1000 * 60 * 60);

// Send update request to backend.
// 获取"Update"按钮元素
var updateButton = document.getElementById('update-button');

// 添加点击事件监听器
updateButton.addEventListener('click', function () {
    // 发送请求到后端
    fetch('http://127.0.0.1:5000/update_price', {
        method: 'POST', // 或 'POST'，根据您的后端路由方法选择
    })
    .then(response => {
        if (response.status === 200) {
            return response.json()
        } else {
            alert('Failed to update data');
            console.error('Failed to update data');
            return null;
        }
    })
    .then(data => {
        // 处理响应，根据需要更新前端数据或界面
            alert('Data updated successfully');
            console.log('Data updated successfully');
            var originalData = [];
            var predictionData = [];
            data.forEach(function (item) {
                var date = new Date(item.date.replace(/-/g, '/'));
                originalData.push([date, item.oil_price]);
                predictionData.push([date, item.prediction]);
            });
            chart.setOption({series: [{
                name: 'original data',
                type: 'line',
                showSymbol: false,
                hoverAnimation: false,
                data: originalData,
                lineStyle: {
                    color: 'red'
                }
            }, {
                name: 'predict data',
                type: 'line',
                showSymbol: false,
                hoverAnimation: false,
                data: predictionData,
                lineStyle: {
                    color: 'black'
                }
            }]})
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
