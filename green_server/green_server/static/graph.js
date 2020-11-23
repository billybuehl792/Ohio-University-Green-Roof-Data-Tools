// colors
const green = "rgb(24, 116, 90)";
const black = "rgb(32, 33, 35)";
const white = "rgb(240, 240, 240)";
const transparent = "rgba(0, 0, 0, 0)";

// fetch data from "/data" | get options | build chart
function getData(parameter_ids, timeValues) {

    var reqData = {                                     // request parameters
        parameter_ids: parameter_ids,                   // parameter_id
        averages: 1,                                    // request average data if long time range
        data_start: timeValues[0],                      // start of requested data
        data_end: timeValues[1]                         // end of requested data
    };

    $.ajax({
        method: "GET",                                  // request method
        url: "/data",                                   // request location
        dataType: "JSON",
        traditional: true,
        data: reqData,
        success: function(res) {                        // data from request to "/data"
            var title = res["data_title"];              // get title from result
            var descr = res["data_descr"];              // get data description from result
            var ops = getChartOptions(title, descr);    // get chart options
            buildChart(res, ops);                       // build chart with result and options
        },
        error: function() {
            fillChart("400 Bad Request!");
        }
    });

}

// return chart options dictionary
function getChartOptions(title, descr) {
    // var toolTipContent = "<strong>{name}</strong><br>{x}<br>{y}";

    // Chart docs: https://canvasjs.com/docs/charts/chart-types/html5-stacked-area-chart/
    // Better to construct options first and then pass it as a parameter
    var options = {
        zoomEnabled: true,                          // allow zoom
        zoomType: "xy",                             // enable x and y zoom
        animationEnabled: true,                     // allow animation
        animationDuration: 600,                     // chart render time
        exportEnabled: true,                        // allow image export
        exportFileName: title,                      // export name
        backgroundColor: transparent,               // chart bg color
        title:{
            // https://canvasjs.com/docs/charts/basics-of-creating-html5-chart/title/
            text: title,
            fontFamily: "courier",                  // title font family
            fontSize: 15,                           // title font size
            fontColor: green,                       // tooltip font color
            horizontalAlign: "left",
            padding: 10,
            dockInsidePlotArea: true
        },
        toolTip: {
            // https://canvasjs.com/docs/charts/basics-of-creating-html5-chart/tool-tip/
            // content: toolTipContent,
            contentFormatter: function (e) {
                let content = "";
				for (var i = 0; i < e.entries.length; i++) {
                    content += "<strong>";
                    if (e.entries[i].dataPoint.y.length == 2) {
                        content += e.entries[i].dataSeries.name + " range: ";
                        content += "</strong>";
                        content += e.entries[i].dataPoint.y;
                    } else {
                        content += e.entries[i].dataSeries.name + ": ";
                        content += "</strong>";
                        content += Number(e.entries[i].dataPoint.y).toFixed(3);
                    }
					content += "<br/>";
                }
                let date = "";
                date += e.entries[0].dataPoint.x.getFullYear() + "-";
                date += e.entries[0].dataPoint.x.getMonth() + "-";
                date += e.entries[0].dataPoint.x.getDate() + " ";
                date += e.entries[0].dataPoint.x.getHours() + ":";
                date += e.entries[0].dataPoint.x.getMinutes() + ":";
                date += e.entries[0].dataPoint.x.getSeconds();
                content += date;
				return content;
			},
            shared: true,
            fontFamily: "courier",                  // tooltip font family
            fontColor: black,                       // tooltip font color
            borderColor: green,                     // border color
            cornerRadius: 5                         // tooltip border radius
        },
        legend: {
            // https://canvasjs.com/docs/charts/basics-of-creating-html5-chart/legend/
            fontColor: green,
            fontFamily: "courier"
        },
        axisY: {
            // https://canvasjs.com/docs/charts/chart-options/axisy/
            title: descr,
            titleFontColor: green,
            titleFontSize: 14,
            titleFontFamily: "courier",
            margin: 10,
            lineColor: green,                       // line color
            labelFontFamily: "courier",             // font
            labelFontSize: 10,                      // Y Axis line thickness
            labelFontColor: green,                  // label font
            gridThickness: .3,                      // grid line thickness
            gridColor: white                        // grid line color
        },
        axisX:{
            // https://canvasjs.com/docs/charts/chart-options/axisx/
            margin: 15,
            valueFormatString: "DD/MMM/YY HH:MM:ss",
            lineColor: green,                       // line color
            labelFontFamily: "courier",             // font family
            labelFontSize: 10,                      // font size
            labelAutoFit: true,                     // auto fit X labels
            labelFontColor: green,                  // font color
            gridThickness: .1,                      // X grid thickness
            gridColor: white                        // grid line color
        },
        data: []
    };

    return options;
}

// return formatted data -> [x: timestamp, y: value]
function formatData(dataList) {
    var data = [];
    for (var p = 0; p < dataList.length; p += 1) {    
        data.push(
            {
                "x": new Date(dataList[p]["timestamp"].replace(/-/g, "/")),
                "y": dataList[p]["value"]
            }
        );
    }
    return data;
}

// temporary fill chart
function fillChart(chartElem) {
    var chartContainer = document.getElementById("chartContainer");
    var filler = "";

    filler += "<div class='center-container'>";
    filler += chartElem;
    filler += "</div>";
    chartContainer.innerHTML = filler;
}

// build chart to page
function buildChart(dataResult, options) {
        
    let dataSet;
    let dataType;

    // iterate through data sets from ajax request and add formatted to options
    for (set in dataResult["data"]) {
        dataType = dataResult["data"][set]["type"];
        dataSet = {
            type: "line",
            color: white,
            lineColor: green,
            lineThickness: 1,
            markerSize: 0,
            showInLegend: true,
            name: dataResult["data"][set]["parameter_name"],
            dataPoints: formatData(dataResult["data"][set]["data_points"])
        };

        // change options if average or minimum/ max set
        if (dataType == "average") {
            dataSet["lineColor"] = white;
        } else if (dataType == "range") {
            dataSet["type"] = "rangeArea";
            dataSet["lineColor"] = green;
            dataSet["color"] = green;
            dataSet["showInLegend"] = false
        }

        if (dataResult["parameter_ids"].length > 1) {
            delete dataSet["lineColor"];
            delete dataSet["color"];
        }

        // push to options variable
        options["data"].unshift(dataSet);
    }
    
    // build chart with options var
    // Chart docs: https://canvasjs.com/docs/charts/basics-of-creating-html5-chart/
    var chart = new CanvasJS.Chart("chartContainer", options);
    var startTime = new Date();
    chart.render();
    var endTime = new Date();
    console.log("graph render time: " + (endTime - startTime) + "ms");
}

// return time from hourly selection
function getHourlyTime(hours) {
    dataStart = new Date();                             // new date elem
    dataStart.setHours(dataStart.getHours() - hours);   // subtract hours
    dataStart = Math.round(Number(dataStart) / 1000);   // round to 10 digits
    dataEnd = Math.round(Number(new Date()) / 1000);    // round to 10 digits

    return [dataStart, dataEnd];
}

// return time from custom selection
function getCustomTime(startField, endField) {
    dataStart = Math.round(Number(new Date(startField)) / 1000);
    dataEnd = Math.round(Number(new Date(endField)) / 1000);

    return [dataStart, dataEnd];
}

// return parameters from parameter selection
function getParameters() {
    var pidBoxes = $('input[name="parameterSelection"]:checked');
    let parameter_ids = [];

    for (var p=0; p<pidBoxes.length; p++) {
        parameter_ids.push(Number(pidBoxes[p].value));
    }

    return parameter_ids;
}

const graph = () => {
    var timeValues;
    var parameter_ids;
    var chartElem = "<h3>Building Chart!</h3>";

    // run hourly on document load
    $(document).ready(function() {
        fillChart(chartElem);
        parameter_ids = getParameters($('input[name="parameterSelection"]:checked'));
        let hours = Number($('input[name="graphTime"]:checked').val());
        timeValues = getHourlyTime(hours);
        getData(parameter_ids, timeValues);

        // run hourly on "time-item input" click
        $(".time-item input").click(function() {
            fillChart(chartElem);
            parameter_ids = getParameters($('input[name="parameterSelection"]:checked'));
            let hours = Number($('input[name="graphTime"]:checked').val());
            timeValues = getHourlyTime(hours);
            getData(parameter_ids, timeValues);
        });

        // run custom on "custom-data-time" button click
        $("#custom-data-time").click(function() {
            fillChart(chartElem);
            parameter_ids = getParameters($('input[name="parameterSelection"]:checked'));
            let startField = document.getElementById("start-data").value;
            let endField = document.getElementById("end-data").value;
            timeValues = getCustomTime(startField, endField);
            getData(parameter_ids, timeValues);
        });

        // run custom on "custom-data-time" button click
        $(".parameter-item input").click(function() {
            fillChart(chartElem);
            parameter_ids = getParameters($('input[name="parameterSelection"]:checked'));
            let hours = Number($('input[name="graphTime"]:checked').val());
            timeValues = getHourlyTime(hours);
            getData(parameter_ids, timeValues);
        });
    });

}