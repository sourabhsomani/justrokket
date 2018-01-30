
// Add Competitive Exam Fields
var count = 1;
jQuery(".add").on("click", function () {
    jQuery(".c_hide" + String(count)).fadeIn();
    if (count == 2) {
        jQuery(".add").css("color", "rgba(0,0,0,0)");
    }
    jQuery(this).remove();
    count++
});

jQuery(window).bind("pageshow", function() {
    jQuery(".clear_on_load").val("");
});

jQuery(document).ready(function () {
    jQuery("#id_location").select2({
        placeholder: "Where you want to study",
        minimumInputLength: 3
    });
});

function populate_qualifying_exam(course_option_chosen) {
    var level = jQuery('input[name=level]:checked').val();
    // jQuery('select[name=q_exm]').empty().trigger('change');
    console.log("Fetching QExams");
    // jQuery("select[name=compt_exm_type]").empty().trigger('change');
    jQuery.ajax({
        data :{'level': level, 'course': course_option_chosen},
        url: "/populate/qualification/exam/",
        dataType: "json",
        success: function (response) {
            jQuery.each(response, function (key, value) {

                jQuery('select[name=q_exm]').append('<option value="' + value.id + '">' + value.name + '</option>');
                // console.log('<option value="' + value.id + '">' + value.name + '</option>')

                jQuery('#compt_exm_type').append('<option value="' + value.c_id + '">' + value.c_name + '</option>');
                console.log(value.c_name);

            });
        }
    });
}

function populate_competitive_exam(level, course, q_exam) {
    jQuery.ajax({
        url: "/populate/qualification/exam/?level=" + level + "&course=" + course + "&q_exam=" + q_exam,
        dataType: "json",
        success: function (data) {
            jQuery.each(data, function (key, value) {
                jQuery('#compt_exm_type').append('<option value="' + value.c_id + '">' + value.c_name + '</option>');
            });
        }
    });
}

jQuery("#id_g_level").click(function () {
    jQuery('select[name=q_exm]').empty().trigger('change');
    jQuery('#compt_exm_type_1').empty().trigger('change');
    jQuery('#compt_exm_type_2').empty().trigger('change');
});
jQuery("#id_pg_level").click(function () {
    jQuery('select[name=q_exm]').empty().trigger('change');
    jQuery('#compt_exm_type_1').empty().trigger('change');
    jQuery('#compt_exm_type_2').empty().trigger('change');
});


function formatCourseCategory(repo) {
    var markup = '<div class="clearfix">' +
            '<div class="col-sm-6">' + repo.name + '</div>' +
            '</div>';
    var course_id = repo.id;
    return markup;
}

function formatCourseCategorySelection(repo) {
    return repo.name || repo.text;
}

jQuery("#id_populate_course_categories").select2({
    allowClear: false,
    ajax: {
        url: "/populate/course/categories/",
        dataType: 'json',
        delay: 0,
        data: function (params) {
            return {
                q: params.term, // search term
                page: jQuery('input[name=level]:checked').val(),
            };
        },
        processResults: function (data, params) {
            params.page = params.page || 1;

            return {
                results: data,
                pagination: {
                    more: (params.page * 30) < data.total_count
                }
            };
        },
        cache: true
    },
    escapeMarkup: function (markup) {
        return markup;
    },
    "language": {
       "noResults": function(){
           return "No Courses Found. Try Another Query? ";
       }
    },
    minimumInputLength: 3,
    templateResult: formatCourseCategory,
    templateSelection: formatCourseCategorySelection,
    placeholder: "Course ?",
}).on("change", function (e) {
    var option_chosen = jQuery("#select2-id_populate_course_categories-container").text();
    jQuery("input[name='course_type']").val(option_chosen);
    console.log(jQuery(this).text());
    jQuery(".select2-selection__clear").html("");
    jQuery("select[name='course'] ~ .select2-container ").css('border', '1px solid rgb(251, 251, 251)');
});




function formatQualification(repo) {
    var markup = '<div class="clearfix">' +
            '<div class="col-sm-6">' + repo.name + '</div>' +
            '</div>';
    var q_exm_id = repo.c_id;
    return markup;
}

function formatQualificationSelection(repo) {
    return repo.name || repo.text;
}


jQuery('select[name=q_exm]').select2({
    ajax: {
        url: "/populate/qualification/exam/",
        dataType: 'json',
        delay: 250,
        data: function (params) {
            return {
                q: params.term, // search term
                level: jQuery('input[name=level]:checked').val(),
            };
        },
        processResults: function (data, params) {
            params.page = params.page || 1;

            return {
                results: data,
                pagination: {
                    more: (params.page * 30) < data.total_count
                }
            };
        },
        cache: true
    },
    escapeMarkup: function (markup) {
        return markup;
    },
    minimumInputLength: 3,
    templateResult: formatQualification,
    templateSelection: formatQualificationSelection,
    placeholder: "Qualifying Exam?"
});


jQuery("#q_exm").on("change", function (e) {
    var level = jQuery('input[name=level]:checked').val();
    var min_qualifying_exam = jQuery('select[name=q_exm]').val();
    var course = jQuery('select[name=course]').val();
    console.log(level, min_qualifying_exam, course);

});


function formatCompetitiveExam(repo) {
    var markup = repo.name
    //jQuery("#id_populate_course_categories").val(course_id);
    return markup;
}

function formatCompetitiveExamSelection(repo) {
    return repo.name || repo.text;
}


jQuery('select[name=compt_exm_type_1]').select2({
    ajax: {
        url: "/populate/competitve/exam/",
        dataType: 'json',
        delay: 250,
        data: function (params) {
            return {
                keyword: params.term, // search term
                level: jQuery('input[name=level]:checked').val(),
                course: jQuery("#select2-id_populate_course_categories-container").text()
            };
        },
        processResults: function (data, params) {
            params.page = params.page || 1;

            return {
                results: data,
                pagination: {
                    more: (params.page * 30) < data.total_count
                }
            };
        },
        cache: true
    },
    escapeMarkup: function (markup) {
        return markup;
    },
    minimumInputLength: 3,
    templateResult: formatQualification,
    templateSelection: formatQualificationSelection,
    placeholder: "Add Competitive Exam"
});

jQuery('select[name=compt_exm_type_2]').select2({
    ajax: {
        url: "/populate/competitve/exam/",
        dataType: 'json',
        delay: 250,
        data: function (params) {
            return {
                keyword: params.term, // search term
                level: jQuery('input[name=level]:checked').val(),
                course: jQuery("#select2-id_populate_course_categories-container").text()
            };
        },
        processResults: function (data, params) {
            params.page = params.page || 1;

            return {
                results: data,
                pagination: {
                    more: (params.page * 30) < data.total_count
                }
            };
        },
        cache: true
    },
    escapeMarkup: function (markup) {
        return markup;
    },
    minimumInputLength: 3,
    templateResult: formatQualification,
    templateSelection: formatQualificationSelection,
    placeholder: "Add Competitive Exam"
});

jQuery(".compt_exm_type").each(function (index) {
   jQuery(this).select2({'placeholder': "Competitive Exam " + String(index + 1)})
});

function print_course() {
    console.log(jQuery(".course").select2('data'))
}
jQuery(".add-exam-block").on("click", function () {
    jQuery(this).hide();
    console.log("Show Exam Block");
    jQuery(".exam_block").show();
});


jQuery("select[name='compt_exm_type_1'], select[name='compt_exm_type_2']").on("select2:select", function () {
    console.log("checking if ce is same");
   doNotRepeatCETwice(jQuery(this));
});
currentElement = 0;
jQuery("select[name='compt_exm_type_1']").on("select2:select", function () {
    currentElement = jQuery(this);
});

function doNotRepeatCETwice(currentElement){
    ce1 = jQuery("select[name='compt_exm_type_1']").select2('data')[0].id;
    ce2 = jQuery("select[name='compt_exm_type_2']").select2('data')[0].id;
    if (ce1==ce2 && ce1 != -1 && ce2 != -1 && currentElement != 0){
        jQuery(currentElement).select2("val", '-1');
        jQuery(".compt_exm_score_" + String(jQuery(this).data("related-score"))).val("");
        console.log("Please select a different CE")
    }
}

window.onload = function () {
    jQuery(".compt_exm_score_1, .compt_exm_score_2, .q_exm_score").val("");
};
