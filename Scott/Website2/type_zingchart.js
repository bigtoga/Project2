// full ZingChart schema can be found here:
// https://www.zingchart.com/docs/api/json-configuration/
// Chart Data

d3.csv("chicago_primary_type.csv", function (data) {

  data.forEach(function (parse) {
    // parse.primary_type = +parse.primary_type;
    parse.index = +parse.index;
    // parse.year = +parse.year;
    // parse.latitude = +parse.latitude
    // parse.longitude = +parse.longitude
  });

  console.log(data[1]);
  var burglary_20 = []
  var burglary_19 = []
  var robbery_20 = []
  var robbery_19 = []
  var homicide_20 = []
  var homicide_19 = []
  var theft_20 = []
  var theft_19 = []

  for (var i = 0; i < data.length; i++) {
    if (data[i].primary_type === "Burglary" && data[i].year === '2020') {
      burglary_20.push(data[i].index)
    }
    else if (data[i].primary_type === "Burglary" && data[i].year === '2019') {
      burglary_19.push(data[i].index)
    }
    else if (data[i].primary_type === "Robbery" && data[i].year === '2020') {
      robbery_20.push(data[i].index)
    }
    else if (data[i].primary_type === "Robbery" && data[i].year === '2019') {
      robbery_19.push(data[i].index)
    }
    else if (data[i].primary_type === "Homicide" && data[i].year === '2020') {
      homicide_20.push(data[i].index)
    }
    else if (data[i].primary_type === "Homicide" && data[i].year === '2019') {
      homicide_19.push(data[i].index)
    }
    // else if (data[i].primary_type === "Theft" && data[i].year === '2020') {
    //   theft_20.push(data[i].index)
    // }
    // else if (data[i].primary_type === "Theft" && data[i].year === '2019') {
    //   theft_19.push(data[i].index)
    // }
  }

  console.log(burglary_20)
  // console.log(non_domestic_20)
  // console.log(domestic_19)
  // console.log(non_domestic_19)

  // Chart Configuration
  let chartConfig = {
    type: 'area',
    globals: {
      fontFamily: 'Poppins',
      fontColor: '#333'
    },
    title: {
      text: 'Comparison between Domestic and Non-domestic crimes',
      align: 'center',
      padding: '5px'
    },
    subtitle: {
      text:
        '',
      align: 'center',
      fontColor: '#505050',
      padding: '10px'
    },
    legend: {
      align: 'center',
      verticalAlign: 'bottom',
      layout: '3x2',
      border: 'none',
      item: {
        fontSize: '18px'
      },
      marker: {
        type: 'circle'
      }
    },
    tooltip: {
      callout: true,
      text: '%t:<br>%v Requests received<br>',
      backgroundColor: '#F7F9FA',
      fontColor: '#505050',
      fontSize: '18px',
      padding: '20px 35px',
      borderRadius: '4px'
    },
    plot: {
      aspect: 'spline'
    },
    scaleX: {
      values: '0:3:1',
      transform: {
        type: "date",
        all: "%m.%d.%Y",
      },
      labels: [
        'Jan',
        'Feb',
        'Mar',
        'Apr',
      ]
    },
    scaleY: {
      values: '0:850:1'
    },
    series: [
      {
        values: burglary_20,
        text: 'Burglary 2020',
        zIndex: 1,
        alphaArea: 1,
        lineColor: '#ffffff',
        lineWidth: '1.5px',
        backgroundColor: '#62E9D8',
        marker: {
          size: '0px'
        },
        hoverMarker: {
          size: '10px',
          backgroundColor: '#fff',
          borderColor: '#eee'
        }
      },
      {
        values: burglary_19,
        text: 'Burglary 2019',
        zIndex: 0,
        alphaArea: 1,
        lineColor: '#ffffff',
        backgroundColor: '#70DE99',
        marker: {
          size: '0px'
        },
        hoverMarker: {
          size: '10px',
          backgroundColor: '#fff',
          borderColor: '#eee'
        }
      },
      {
        values: robbery_20,
        text: 'Robbery 2020',
        zIndex: 2,
        alphaArea: 1,
        lineColor: '#ffffff',
        backgroundColor: '#B2DC93',
        marker: {
          size: '0px'
        },
        hoverMarker: {
          size: '10px',
          backgroundColor: '#fff',
          borderColor: '#eee'
        }
      },
      {
        values: robbery_19,
        text: 'Robbery 2019',
        zIndex: 3,
        alphaArea: 1,
        lineColor: '#ffffff',
        backgroundColor: '#FFE295',
        marker: {
          size: '0px'
        },
        hoverMarker: {
          size: '10px',
          backgroundColor: '#fff',
          borderColor: '#eee'
        }
      },
      {
        values: homicide_20,
        text: 'Homicide 2020',
        zIndex: 0,
        alphaArea: 4,
        lineColor: '#ffffff',
        backgroundColor: '#FFE295',
        marker: {
          size: '0px'
        },
        hoverMarker: {
          size: '10px',
          backgroundColor: '#fff',
          borderColor: '#eee'
        }
      },
      {
        values: homicide_19,
        text: 'Homicide 2019',
        zIndex: 5,
        alphaArea: 1,
        lineColor: '#ffffff',
        backgroundColor: 'red',
        marker: {
          size: '0px'
        },
        hoverMarker: {
          size: '10px',
          backgroundColor: '#fff',
          borderColor: '#eee'
        }
      },
      // {
      //   values: theft_20,
      //   text: 'Theft 2019',
      //   zIndex: 0,
      //   alphaArea: 1,
      //   lineColor: '#ffffff',
      //   backgroundColor: '#FFE295',
      //   marker: {
      //     size: '0px'
      //   },
      //   hoverMarker: {
      //     size: '10px',
      //     backgroundColor: '#fff',
      //     borderColor: '#eee'
      //   }
      // },
      // {
      //   values: theft_19,
      //   text: 'Theft 2019',
      //   zIndex: 0,
      //   alphaArea: 1,
      //   lineColor: '#ffffff',
      //   backgroundColor: '#FFE295',
      //   marker: {
      //     size: '0px'
      //   },
      //   hoverMarker: {
      //     size: '10px',
      //     backgroundColor: '#fff',
      //     borderColor: '#eee'
      //   }
      // }
    ]
    // {
    //   values: governmentRequests,
    //   text: 'Government Requests',
    //   zIndex: 6,
    //   alphaArea: 1,
    //   lineColor: '#ffffff',
    //   backgroundColor: '#FF9C85',
    //   marker: {
    //     size: '0px'
    //   },
    //   hoverMarker: {
    //     size: '10px',
    //     backgroundColor: '#fff',
    //     borderColor: '#eee'
    //   }

  };

  // Render Method
  zingchart.render({
    id: 'myChart',
    data: chartConfig,
    height: '100%',
    width: '100%',
  });
});