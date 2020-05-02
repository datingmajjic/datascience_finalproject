// document.getElementById('date').innerHTML = new Date().toDateString();

function generate() {
    var x = document.getElementById("myform");
    var i;
    // alert('Hello');
    var p1_name = x.p1_name.value;
    var p1_sex = x.p1_sex.value;
    var p1_race = x.p1_race.value;
    var p1_degree = x.p1_degree.value;
    var p1_career = x.p1_career.value;

    console.log(p1_name)
    console.log(p1_sex)
    console.log(p1_race)
    console.log(p1_degree)
    console.log(p1_career)

    var p2_name = x.p2_name.value;
    var p2_sex = x.p2_sex.value;
    var p2_race = x.p2_race.value;
    var p2_degree = x.p2_degree.value;
    var p2_career = x.p2_career.value;

    console.log(p2_name)
    console.log(p2_sex)
    console.log(p2_race)
    console.log(p2_degree)
    console.log(p2_career)


    // console.log("hi");
    var results_labels = ["Attractiveness score:", "Likeability score:", "Likelihood of going on a second date:"];

    var p1_results = ["9.5", "3", "10"];
    var p2_results = ["5", "5", "5"];

    var p1_result_string = p1_name + " will rate " + p2_name + "<br>";
    var p2_result_string = p2_name + " will rate " + p1_name + "<br>";
    for (i = 0; i < results_labels.length ;i++) {
        p1_result_string += results_labels[i] + p1_results[i] + "<br>";
        p2_result_string += results_labels[i] + p2_results[i] + "<br>";
        // text += x.elements[i].value + "<br>";
        // console.log(text);
    }

    document.getElementById('results').style.visibility = 'visible';

    document.getElementById('p1').innerHTML=p1_name;
    document.getElementById('p2').innerHTML=p2_name;
    document.getElementById('p11').innerHTML=p1_name;
    document.getElementById('p22').innerHTML=p2_name;

    document.getElementById("p1Attract").value = p1_results[0];
    document.getElementById('p1AtextInput').innerHTML=p1_results[0];
    document.getElementById("p1Like").value = p1_results[1];
    document.getElementById('p1LtextInput').innerHTML=p1_results[1];
    document.getElementById("p1Date").value = p1_results[2];
    document.getElementById('p1DtextInput').innerHTML=p1_results[2];

    document.getElementById("p2Attract").value = p2_results[0];
    document.getElementById('p2AtextInput').innerHTML=p2_results[0];
    document.getElementById("p2Like").value = p2_results[1];
    document.getElementById('p2LtextInput').innerHTML=p2_results[1];
    document.getElementById("p2Date").value = p2_results[2];
    document.getElementById('p2DtextInput').innerHTML=p2_results[2];


    document.getElementById("evaluation_results").innerHTML = p1_result_string + "<br>"+ p2_result_string;
}
