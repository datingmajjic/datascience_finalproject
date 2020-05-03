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

    if (p1_race === p2_race) {
        var same_race = 1
    } else {
        var same_race = 0
    }

    if (p1_degree === p2_degree) {
        var same_degree = 1
    } else {
        var same_degree = 0
    }

    if (p1_career === p2_career) {
        var same_career = 1
    } else {
        var same_career = 0
    }

    var p1L_field_code = [0, -0.81, -0.28, 0.11, -0.41, -0.87, -0.64, -0.44,
    -0.37, -0.44, 0.02, -1.18, -0.38, -.57, -0.96, -1.09, -2.87, -1.38]
    var p2L_field_code = [0, -0.03, 0.21, 1.17, 0.18, 0.17, 0.42, 0.58, 0.34,
    0.38, 0.08, 0.45, 0.53, 0.35, 0.06, 0.75, 0.40, 0.67]
    var p1L_race_code = [0, -0.58, -0.81, -0.66, 0, -0.29]
    var p2L_race_code = [0, 0.13, 0.35, -0.25, 0, 0.11]
    var p1L_career_code = [0, 0.03, -0.19, -0.34, -0.39, 0.18, -0.21, -0.15,
    -0.46, -0.13, -0.90, -0.93, -0.06, 0.04, 0.37, -0.12, 0]
    var p2L_career_code = [0, -0.46, -0.35, -0.46, -0.35, -0.31, -0.41, 0.38,
    -0.38, -0.31, -0.43, -0.73, -0.74, -1.13, -0.57, -0.11, 0]

    var p1A_field_code = [0, -0.37, -0.19, 0.24, -0.29, -0.47, -0.33, -0.37, -0.18,
    -0.32, 0.24, -0.95, -0.06, -0.04, -0.20, -1.03, -1.05, -1.12]
    var p2A_field_code = [0, 0.42, 0.47, 2.06, 0.64, 0.28, 0.80, 1.04, 0.75, 0.93,
    0.38, 1.30, 1.10, 0.32, 0.35, 1.18, -0.05, 1.32]
    var p1A_race_code = [0, -0.34, -0.52, -0.42, 0, -0.07]
    var p2A_race_code = [0, 0.34, 0.32, -0.31, 0, 0.08]
    var p1A_career_code = [0, 0.29, 0.29, -0.19, 0.05, 0.15, -0.05, 0.29, -0.34,
    0.26, -0.89, 0.02, -0.08, 0.54, 0.33, -0.44, 0]
    var p2A_career_code = [0, -1.03, -0.71, -1.04, -0.99, -0.55, -0.67, 0.28, -0.63,
    -0.89, -0.77, -1.60, -1.45, -1.43, -0.63, -0.41, 0]

    var p1D_field_code = [0, -0.52, 0.13, 0.72, -0.09, -0.29, -0.13, -0.44, 0.23,
    -0.05, -0.38, -0.99, -0.28, 0.17, -0.41, 0.30, -1.25, 0.11]
    var p2D_field_code = [0, 0.43, 0.43, 1.76, 0.44, 0.29, 0.53, 0.87, 0.27, 0.63,
    0.04, 0.92, 0.60, 0.46, 0.15, 1.86, -0.08, 0.98]
    var p1D_race_code = [0, -0.66, -0.38, -0.23, 0, -0.10]
    var p2D_race_code = [0.21, 0.16, -0.33, 0, 0.13]
    var p1D_career_code = [0, 0.08, 0.19, -0.43, -0.07, 0.15, 0.22, -0.71, 0.06,
    -0.17, 0.50, -0.94, -0.84, 0.33, -0.21, 0.34, 0]
    var p2D_career_code = [0, -0.78, -1.05, -0.95, -0.81, -0.70, -0.66, -0.62, -0.57,
    -0.79, -0.78, -2.63, -0.87, -0.13, -0.44, -0.64, 0]

    var likeability_p1 = 6.91696 +
    (0.34865 * p1_sex) +
    (0.45928 * same_degree) +
    (0.1622107 * same_race) +
    (0.1531757  * same_career) +
    (p1L_field_code[p1_degree - 1]) +
    (p2L_field_code[p2_degree - 1]) +
    (p1L_race_code[p1_race - 1]) +
    (p2L_race_code[p2_race - 1]) +
    (p1L_career_code[p1_career - 1]) +
    (p2L_career_code[p2_career - 1])

    var likeability_p2 = 6.91696 +
    (0.34865 * p2_sex) +
    (0.45928 * same_degree) +
    (0.1622107 * same_race) +
    (0.1531757  * same_career) +
    (p1L_field_code[p2_degree - 1]) +
    (p2L_field_code[p1_degree - 1]) +
    (p1L_race_code[p2_race - 1]) +
    (p2L_race_code[p1_race - 1]) +
    (p1L_career_code[p2_career - 1]) +
    (p2L_career_code[p1_career - 1])

    likeability_p1 = likeability_p1.toFixed(2)
    likeability_p2 = likeability_p2.toFixed(2)

    var attractiveness_p1 = 6.02308 +
    (0.80449 * p1_sex) +
    (0.28916 * same_degree) +
    (0.07185 * same_race) +
    (0.03203  * same_career) +
    (p1A_field_code[p1_degree - 1]) +
    (p2A_field_code[p2_degree - 1]) +
    (p1A_race_code[p1_race - 1]) +
    (p2A_race_code[p2_race - 1]) +
    (p1A_career_code[p1_career - 1]) +
    (p2A_career_code[p2_career - 1])

    var attractiveness_p2 = 6.02308 +
    (0.80449 * p2_sex) +
    (0.28916 * same_degree) +
    (0.07185 * same_race) +
    (0.03203  * same_career) +
    (p1A_field_code[p2_degree - 1]) +
    (p2A_field_code[p1_degree - 1]) +
    (p1A_race_code[p2_race - 1]) +
    (p2A_race_code[p1_race - 1]) +
    (p1A_career_code[p2_career - 1]) +
    (p2A_career_code[p1_career - 1])

    attractiveness_p1 = attractiveness_p1.toFixed(2)
    attractiveness_p2 = attractiveness_p2.toFixed(2)

    var decision_p1 = -0.24965 +
    (0.85714 * p1_sex) +
    (0.29056 * same_degree) +
    (0.23242 * same_race) +
    (-0.05814  * same_career) +
    (p1D_field_code[p1_degree - 1]) +
    (p2D_field_code[p2_degree - 1]) +
    (p1D_race_code[p1_race - 1]) +
    (p2D_race_code[p2_race - 1]) +
    (p1D_career_code[p1_career - 1]) +
    (p2D_career_code[p2_career - 1])

    var decision_p2 = -0.24965 +
    (0.85714 * p2_sex) +
    (0.29056 * same_degree) +
    (0.23242 * same_race) +
    (-0.05814  * same_career) +
    (p1D_field_code[p2_degree - 1]) +
    (p2D_field_code[p1_degree - 1]) +
    (p1D_race_code[p2_race - 1]) +
    (p2D_race_code[p1_race - 1]) +
    (p1D_career_code[p2_career - 1]) +
    (p2D_career_code[p1_career - 1])

    decision_p1 = 1 / (1 + Math.exp(-decision_p1))
    decision_p1 = decision_p1.toFixed(2)
    decision_p2 = 1 / (1 + Math.exp(-decision_p2))
    decision_p2 = decision_p2.toFixed(2)

    var p1_results = [attractiveness_p1, likeability_p1, decision_p1];
    var p2_results = [attractiveness_p2, likeability_p2, decision_p2];

    var p1_result_string = p1_name + " will rate " + p2_name + "<br>";
    var p2_result_string = p2_name + " will rate " + p1_name + "<br>";
    for (i = 0; i < results_labels.length ;i++) {
        p1_result_string += results_labels[i] + p1_results[i] + "<br>";
        p2_result_string += results_labels[i] + p2_results[i] + "<br>";
        // text += x.elements[i].value + "<br>";
        // console.log(text);
    }
    //makes the results show up
    document.getElementById('results').style.visibility = 'visible';

    //sets the name of person 1 and person 2 in the results
    document.getElementById('p1').innerHTML=p1_name;
    document.getElementById('p2').innerHTML=p2_name;
    document.getElementById('p11').innerHTML=p1_name;
    document.getElementById('p22').innerHTML=p2_name;

    //sets the results of person 1
    document.getElementById("p1Attract").value = p1_results[0];
    document.getElementById('p1AtextInput').innerHTML=p1_results[0];
    document.getElementById("p1Like").value = p1_results[1];
    document.getElementById('p1LtextInput').innerHTML=p1_results[1];
    document.getElementById("p1Date").value = p1_results[2];
    document.getElementById('p1DtextInput').innerHTML=p1_results[2];

    //sets the results of person 2
    document.getElementById("p2Attract").value = p2_results[0];
    document.getElementById('p2AtextInput').innerHTML=p2_results[0];
    document.getElementById("p2Like").value = p2_results[1];
    document.getElementById('p2LtextInput').innerHTML=p2_results[1];
    document.getElementById("p2Date").value = p2_results[2];
    document.getElementById('p2DtextInput').innerHTML=p2_results[2];


    // document.getElementById("evaluation_results").innerHTML = p1_result_string + "<br>"+ p2_result_string;
}
