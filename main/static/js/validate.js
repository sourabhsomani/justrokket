var formValidated = false;
var errorborder = "1px solid red";

function CheckCoursePopulated(){
    element = jQuery(".course");
    val = element.val()
    if ( val && val != "" ){
        console.log("Course has been entered");
        jQuery(".course ~ .select2-container").css("border", "none");
        return true;
    }
    else{
        console.log("Course has not been populated");
        jQuery(".course ~ .select2-container").css("border", errorborder);
        return false;
    }
}


function CheckQEScorePopulated() {
    if (jQuery(".q_exm").val() && jQuery(".q_exm_score").val() == ""){
        console.log("Qexm is selected and score not entered");
        jQuery(".q_exm_score").css("border", errorborder);
        console.log("CheckQEScorePopulated false");
        return false;
    }
    else if(CheckLimits3()){
        jQuery(".q_exm_score").css("border", "1px solid rgb(170, 170, 170)");
        return true;
    }
}


function CheckQEXMPopulated() {
    if (!jQuery(".q_exm").val() && jQuery(".q_exm_score").val()){
        console.log("Qexm is not selected and score entered");
        jQuery(".q_exm ~ .select2-container").css("border", errorborder);
        console.log("CheckQEXMPopulated false");
        return false;
    }
    else{
        jQuery(".q_exm ~ .select2-container").css("border", "none");
        return true;
    }
}


function CheckCE1ScorePopulated() {
    if (jQuery(".compt_exm_type_1").val() && jQuery(".compt_exm_score_1").val() == ""){
        console.log("Qexm is selected and score not entered");
        jQuery(".compt_exm_score_1").css("border", errorborder);
        console.log("CheckCE1ScorePopulated false");
        return false;
    }
    else{
        jQuery(".compt_exm_score_1").css("border", "1px solid rgb(170, 170, 170)");
        return true;
    }
}


function CheckCEEXM1Populated() {
    if (!jQuery(".compt_exm_type_1").val() && jQuery(".compt_exm_score_1").val()){
        console.log("Qexm is not selected and score entered");
        jQuery(".compt_exm_type_1 ~ .select2-container").css("border", errorborder);
        console.log("CheckCEEXM1Populated false");
        return false;
    }
    else{
        jQuery(".compt_exm_type_1 ~ .select2-container").css("border", "none");
        return true;
    }
}

function CheckCE2ScorePopulated() {
    if (jQuery(".compt_exm_type_2").val() && jQuery(".compt_exm_score_2").val() == ""){
        console.log("Qexm is selected and score not entered");
        jQuery(".compt_exm_score_2").css("border", errorborder);
        console.log("CheckCE2ScorePopulated false");
        return false;
    }
    else{
        jQuery(".compt_exm_score_2").css("border", "1px solid rgb(170, 170, 170)");
        return true;
    }
}


function CheckCEEXM2Populated() {
    if (!jQuery(".compt_exm_type_2").val() && jQuery(".compt_exm_score_2").val()){
        console.log("Qexm is not selected and score entered");
        jQuery(".compt_exm_type_2 ~ .select2-container").css("border", errorborder);
        console.log("CheckCEEXM2Populated false");
        return false;
    }
    else{
        jQuery(".compt_exm_type_2 ~ .select2-container").css("border", "none");
        return true;
    }
}


function DynamicLimitValidation(){
    if (jQuery(".compt_exm_type_1").val()){
        console.log("dynamic 1")
        data=jQuery(".compt_exm_type_1").select2('data')[0];
        score_type = data.exam_type;
        if (score_type == "Rank"){
            console.log("settings minmax")
            jQuery(".compt_exm_score_1").attr("min", "1");
            jQuery(".compt_exm_score_1").attr("max", "9999999");
        }
        else if (score_type == "Score"){
            jQuery(".compt_exm_score_1").attr("min", "1");
            jQuery(".compt_exm_score_1").attr("max", "9999999");
        }
        else if (score_type == "Percentile"){
            jQuery(".compt_exm_score_1").attr("min", "1");
            jQuery(".compt_exm_score_1").attr("max", "100");
        }
        else if (score_type == "Percentage"){
            jQuery(".compt_exm_score_1").attr("min", "1");
            jQuery(".compt_exm_score_1").attr("max", "100");
        }
        return true;
    }
    else if (jQuery(".compt_exm_type_2").val()){
        console.log("dynamic 2")
        data=jQuery(".compt_exm_type_2").select2('data')[0];
        score_type = data.exam_type;
        if (score_type == "Rank"){
            console.log("data type rank")
            jQuery(".compt_exm_score_2").attr("min", "1");
            jQuery(".compt_exm_score_2").attr("max", "9999999");
        }
        else if (score_type == "Score"){
            jQuery(".compt_exm_score_2").attr("min", "1");
            jQuery(".compt_exm_score_2").attr("max", "9999999");
        }
        else if (score_type == "Percentile"){
            jQuery(".compt_exm_score_2").attr("min", "1");
            jQuery(".compt_exm_score_2").attr("max", "100");
        }
        else if (score_type == "Percentage"){
            jQuery(".compt_exm_score_2").attr("min", "1");
            jQuery(".compt_exm_score_2").attr("max", "100");
        }
        return true;
    }
    return true;
}

function CheckLimits1(){
    if (jQuery(".compt_exm_score_1").val()){
        if ( parseInt(jQuery(".compt_exm_score_1").val()) < parseInt(jQuery(".compt_exm_score_1").attr("min")) || parseInt(jQuery(".compt_exm_score_1").val()) > parseInt(jQuery(".compt_exm_score_1").attr("max"))){
            jQuery(".compt_exm_score_1").css("border", errorborder);
            console.log("CheckLimits1 false");
            return false;
        }
        else{
            jQuery(".compt_exm_score_1").css("border", "1px solid rgb(170, 170, 170)");
            return true;
        }
    }
    return true;
}

function CheckLimits2(){
    if (jQuery(".compt_exm_score_2").val()){
        if ( parseInt(jQuery(".compt_exm_score_2").val()) < parseInt(jQuery(".compt_exm_score_2").attr("min")) || parseInt(jQuery(".compt_exm_score_2").val()) > parseInt(jQuery(".compt_exm_score_2").attr("max"))){
            jQuery(".compt_exm_score_2").css("border", errorborder);
            console.log("CheckLimits2 false");
            return false;
        }
        else{
            jQuery(".compt_exm_score_2").css("border", "1px solid rgb(170, 170, 170)");
            return true;
        }
    }
    return true;
}

function CheckLimits3() {
    if (jQuery(".q_exm_score").val()){
        if ( parseInt(jQuery(".q_exm_score").val()) < parseInt(jQuery(".q_exm_score").attr("min")) || parseInt(jQuery(".q_exm_score").val()) > parseInt(jQuery(".q_exm_score").attr("max"))){
            jQuery(".q_exm_score").css("border", errorborder);
            console.log("CheckLimits2 false");
            return false;
        }
        else{
            jQuery(".q_exm_score").css("border", "1px solid rgb(170, 170, 170)");
            return true;
        }


    }
    else {
        jQuery(".q_exm_score").css("border", "1px solid rgb(170, 170, 170)");
        return true
    }
}

function validateAll(){
    if (
            CheckCoursePopulated() &&
            CheckQEScorePopulated() &&
            CheckQEXMPopulated() &&
            CheckCE1ScorePopulated() &&
            CheckCEEXM1Populated() &&
            CheckCE2ScorePopulated() &&
            CheckCEEXM2Populated() &&
            DynamicLimitValidation() &&
            CheckLimits1() &&
            CheckLimits2 &&
            CheckLimits3()
    ){
        console.log("validate all running");
        formValidated = true;
        return true;
    }
    else{
        formValidated = false;
        return false;
    }
}

jQuery(".course").on("select2:closing", function () {
   CheckCoursePopulated();
});

jQuery(".q_exm").on("select2:closing", function () {
   CheckQEXMPopulated();
});

jQuery(".compt_exm_type_1").on("select2:closing", function () {
   CheckCEEXM1Populated();
    DynamicLimitValidation();
    CheckLimits1();
});

jQuery(".compt_exm_type_2").on("select2:closing", function () {
    console.log("compt_exm_2 closing")
   CheckCEEXM2Populated();
    DynamicLimitValidation();
    CheckLimits2();
});

jQuery(".q_exm_score").on("change", function () {
   CheckQEXMPopulated();
   CheckLimits3();
});

jQuery(".compt_exm_score_1").on("change", function () {
   CheckCEEXM1Populated();
    CheckLimits1();
});

jQuery(".compt_exm_score_2").on("change", function () {
   CheckCEEXM2Populated();
    CheckLimits2();
});






