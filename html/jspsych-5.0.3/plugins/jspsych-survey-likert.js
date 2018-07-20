/**
 * jspsych-survey-likert
 * a jspsych plugin for measuring items on a likert scale
 *
 * Josh de Leeuw
 *
 * documentation: docs.jspsych.org
 *
 */

jsPsych.plugins['survey-likert'] = (function() {

  var plugin = {};

  plugin.trial = function(display_element, trial) {

    

    // default parameters for the trial
    trial.preamble = typeof trial.preamble === 'undefined' ? "" : trial.preamble;
    trial.question = trial.question

    // if any trial variables are functions
    // this evaluates the function and replaces
    // it with the output of the function
    trial = jsPsych.pluginAPI.evaluateFunctionParameters(trial);
    display_element.append($('<div>', {
      "id": 'questiondiv'
    }))
    $.getJSON("./JSON/new_questions.json").done(function(response) {
      myJSON = response;
      
  
      $('#questiondiv').html(myJSON[''+trial.question]['question'])
      
  })
    
    // show preamble text
    
    display_element.append($('<div>', {
      "id": 'jspsych-survey-likert-preamble',
      "class": 'jspsych-survey-likert-preamble'
    }));

    $('#jspsych-survey-likert-preamble').html(trial.preamble);

    
    // add likert scale questions
    for (var i = 0; i < trial.questions.length; i++) {
      display_element.append('<form id="jspsych-survey-slider-form">');
      form_element = $('#jspsych-survey-slider-form');
      // add question
      form_element.append('<label class="jspsych-survey-likert-statement">' + trial.questions[i] + '</label>');
      // add options
      var width = 100 / trial.labels[i].length;
      form_element.append($('<div>', 
      { "id" : 'slider'+i,
        'class': 'slidecontainer'
      }));

      $('#slider'+i).append($('<input>', {
        'type': "range",
        'min' : "1",
        'max':"100", 
        'value':"50", 
        'class':"slider", 
        'id':"myRange"
      }))
      var options_string = '<ul class="jspsych-survey-likert-opts">';
      for (var j = 0; j < trial.labels[i].length; j++) {
              // modification1: I added "required"
        options_string +='<li display = "inline" style="width:' + width + '%">' + trial.labels[i][j] + '</li>';
      }
      options_string += '</ul>';
      form_element.append(options_string);
    }

        // modification2
    form_element.append($('<input>', {
      'type': 'submit',
      'class': 'jspsych-survey-likert jspsych-btn',
      'value': 'Submit Answers'
    }));

        form_element.submit(function(event) { // modification3

      event.preventDefault(); // modification4

          // measure response time
      var endTime = (new Date()).getTime();
      var response_time = endTime - startTime;

      // create object to hold responses
      var question_data = {};
      $("#jspsych-survey-likert-form .jspsych-survey-likert-opts").each(function(index) {
        var id = $(this).data('radio-group');
        var response = $('input[name="' + id + '"]:checked').val();
        if (typeof response == 'undefined') {
          response = -1;
        }
        var obje = {};
        obje[id] = response;
        $.extend(question_data, obje);
      });

      // save data
      var trial_data = {
        "rt": response_time,
        "responses": JSON.stringify(question_data)
      };

      display_element.html('');

      // next trial
      jsPsych.finishTrial(trial_data);
    });

    var startTime = (new Date()).getTime();
  };

  return plugin;
})();