const genres = {
  Action: 0,
  Adventure: 0,
  Animation: 0,
  Children: 0,
  Comedy: 0,
  Crime: 0,
  Documentary: 0,
  Drama: 0,
  Fantasy: 0,
  "Film-Noir": 0,
  Horror: 0,
  Musical: 0,
  Mystery: 0,
  Romance: 0,
  "Sci-Fi": 0,
  Thriller: 0,
  War: 0,
  Western: 0,
};

const months = {
  0: 0,
  1: 0,
  2: 0,
  3: 0,
  4: 0,
  5: 0,
  6: 0,
  7: 0,
  8: 0,
  9: 0,
  10: 0,
  11: 0,
};

let jsondata;

async function getJson(url) {
  let response = await fetch(url);
  let data = await response.json();
  return data;
}

async function main() {
  jsondata = await getJson("/data");

  for (var i = 0; i < jsondata.length; ++i) {
    genres[jsondata[i].genre] += 1;
  }

  for (var i = 0; i < jsondata.length; ++i) {
    const date = new Date(jsondata[i].v_date);
    const month = date.getMonth();
    months[month] += 1;
    month_keys = Object.keys(months);
    month_values = Object.values(months);
  }

  //TOP 6 GENRES
  const top6 = Object.entries(genres)
    .sort(([, a], [, b]) => b - a)
    .slice(0, 6);
  const top6Keys = top6.map(([n]) => n);
  const top6Values = top6.map(([, v]) => v);

  //BAR CHART
  var barChartOptions = {
    series: [
      {
        name: "Genres",
        data: top6Values,
      },
    ],
    chart: {
      height: 350,
      type: "bar",
    },
    plotOptions: {
      bar: {
        borderRadius: 10,
        dataLabels: {
          position: "top", // top, center, bottom
        },
        colors: {
          ranges: [
            {
              from: 0,
              to: 5,
              color: "#CA3BE0",
            },
            {
              from: 5,
              to: 10,
              color: "#E8DB11",
            },
            {
              from: 10,
              to: 20,
              color: "#992D2D",
            },
            {
              from: 20,
              to: 40,
              color: "#7217D6",
            },
          ],
          backgroundBarColors: [],
          backgroundBarOpacity: 1,
          backgroundBarRadius: 0,
        },
      },
    },
    dataLabels: {
      enabled: true,
      offsetY: -20,
      style: {
        fontSize: "12px",
        colors: ["#fff"],
      },
    },

    xaxis: {
      categories: top6Keys,
      position: "top",
      labels: {
        style: {
          colors: "#fff",
        },
      },
      axisBorder: {
        show: false,
      },
      axisTicks: {
        show: false,
      },
      crosshairs: {
        fill: {
          type: "gradient",
          gradient: {
            colorFrom: "#D8E3F0",
            colorTo: "#BED1E6",
            stops: [0, 100],
            opacityFrom: 0.2,
            opacityTo: 0.4,
          },
        },
      },
      tooltip: {
        enabled: true,
      },
    },
    yaxis: {
      axisBorder: {
        show: false,
      },
      axisTicks: {
        show: false,
      },
      labels: {
        show: false,
      },
    },
    title: {
      text: "Your 6 Most Watched Genres",
      floating: true,
      offsetY: 330,
      align: "center",
      style: {
        color: "#fff",
      },
    },
  };

  var barChart = new ApexCharts(
    document.querySelector("#bar-chart"),
    barChartOptions
  );
  barChart.render();

  //LINE CHART
  var lineChartOptions = {
    series: [
      {
        name: "Monthly Watched Movies",
        data: month_values,
      },
      /*{
        name: "Low - 2013",
        data: [12, 11, 14, 18, 17, 13, 13],
      },*/
    ],
    chart: {
      height: 350,
      type: "line",
      dropShadow: {
        enabled: true,
        color: "#000",
        top: 18,
        left: 7,
        blur: 10,
        opacity: 0.2,
      },
      toolbar: {
        show: false,
      },
    },
    colors: ["#C47B16", "#1846D6"],
    dataLabels: {
      enabled: true,
    },
    stroke: {
      curve: "smooth",
    },
    markers: {
      size: 1,
    },
    xaxis: {
      categories: [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
      ],
      title: {
        text: "Month",
        style: {
          color: "#9aa0ac",
        },
      },
      labels: {
        style: {
          colors: "#9aa0ac",
        },
      },
    },
    yaxis: {
      title: {
        text: "Number of Movies",
        style: {
          color: "#9aa0ac",
        },
      },
      labels: {
        style: {
          colors: "#9aa0ac",
        },
      },
      min: 0,
      max: Math.max(...month_values) + 5,
    },
    legend: {
      position: "top",
      horizontalAlign: "right",
      floating: true,
      offsetY: -25,
      offsetX: -5,
      labels: {
        useSeriesColors: true,
      },
    },
  };

  var lineChart = new ApexCharts(
    document.querySelector("#line-chart"),
    lineChartOptions
  );
  lineChart.render();
}

main();
