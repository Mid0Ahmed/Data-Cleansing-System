var chart = document.querySelector("#chart")
var pers = document.getElementById("pers").value
console.log(pers);
if (!pers){
  pers=100
}
console.log(pers);
var options = {

  series: [pers],
  chart: {
  height: 200,
  type: 'radialBar',
  toolbar: {
    show: true
  }
},
plotOptions: {
  radialBar: {
    startAngle: -135,
    endAngle: 225,
     hollow: {
      margin: 0,
      size: '70%',
      background: '',
      image: undefined,
      imageOffsetX: 0,
      imageOffsetY: 0,
      position: 'front',
      dropShadow: {
        enabled: true,
        top: 3,
        left: 0,
        blur: 4,
        opacity: 0.24
      }
    },
    track: {
      background: '',
      strokeWidth: '67%',
      margin: 0, // margin is in pixels
      dropShadow: {
        enabled: true,
        top: -3,
        left: 0,
        blur: 4,
        opacity: 0.35
      }
    },

    dataLabels: {
      show: true,
      name: {
        offsetY: -10,
        show: true,
        color: 'white',
        fontSize: '17px'
      },
      value: {
        formatter: function(val) {
          return parseInt(val);
        },
        color: 'white',
        fontSize: '36px',
        show: true,
      }
    }
  }
},
fill: {
  type: 'gradient',
  gradient: {
    shade: 'dark',
    type: 'horizontal',
    shadeIntensity: 0.5,
    gradientToColors: ['#45D075'],
    inverseColors: true,
    opacityFrom: 1,
    opacityTo: 1,
    stops: [0, 100]
  }
},
stroke: {
  lineCap: 'round'
},
labels: ['%'],
};

var chart = new ApexCharts(document.querySelector("#chart"), options);
chart.render();

 // jQuery to toggle visibility of code container
function toggleCodeContainer() {
var codeContainer = document.getElementById("codeContainer");
if (codeContainer.style.display === "none") {
    codeContainer.style.display = "block";
} else {
    codeContainer.style.display = "none";
}
}




// Function to save selected options to local storage
function saveSelectedOptions() {
var selectedTable = document.querySelector('select[name="table"]').value;
var selectedFillIntType = document.querySelector('select[name="fill-int-type"]').value;
var selectedFillStrValue = document.querySelector('input[name="fill-str-value"]').value;

localStorage.setItem('selectedTable', selectedTable);
localStorage.setItem('selectedFillIntType', selectedFillIntType);
localStorage.setItem('selectedFillStrValue', selectedFillStrValue);
}

// Function to retrieve and set selected options from local storage
function setSelectedOptionsFromLocalStorage() {
var selectedTable = localStorage.getItem('selectedTable');
var selectedFillIntType = localStorage.getItem('selectedFillIntType');
var selectedFillStrValue = localStorage.getItem('selectedFillStrValue');

if (selectedTable) {
  document.querySelector('select[name="table"]').value = selectedTable;
}
if (selectedFillIntType) {
  document.querySelector('select[name="fill-int-type"]').value = selectedFillIntType;
}
if (selectedFillStrValue) {
  document.querySelector('input[name="fill-str-value"]').value = selectedFillStrValue;
}
}

// Call the function to set selected options from local storage when the page loads
setSelectedOptionsFromLocalStorage();

// Function to toggle visibility of code container
function toggleCodeContainer() {
var codeContainer = document.getElementById("codeContainer");
if (codeContainer.style.display === "none") {
    codeContainer.style.display = "block";
} else {
    codeContainer.style.display = "none";
}
}

// Add an event listener to the form to save selected options before submitting
document.querySelector('form').addEventListener('submit', saveSelectedOptions);
