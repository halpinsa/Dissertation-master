/* jspsych-text.js
 * Josh de Leeuw
 *
 * This plugin displays text (including HTML formatted strings) during the experiment.
 * Use it to show instructions, provide performance feedback, etc...
 *
 * documentation: docs.jspsych.org
 *
 *
 */

jsPsych.plugins['AJDrandom-code'] = (function() {

  var plugin = {};

  plugin.trial = function(display_element, trial) {

    trial.randomCode = trial.randomCode;

    // if any trial variables are functions
    // this evaluates the function and replaces
    // it with the output of the function
    trial = jsPsych.pluginAPI.evaluateFunctionParameters(trial);

    // set the HTML of the display target to replaced_text.
    display_element.append($('<div>', {
        "id": 'mainContainer',
        'class': 'container'
      }));

    $('#mainContainer').append($('<div>', {
      "id": 'codeDiv',
      "class": 'jumbotron text-center'
    }));

    // Set question
      $('#codeDiv').append($('<h2>', {
        'id': 'codeH2'
      }));

      $('#codeDiv').append($('<div>', {
        'id': 'cardTop',
        "class": 'card'
      }));

      $('#cardTop').append($('<div>', {
        'id': 'cardContent',
        "class": 'card-block'
      }));

      $('#codeDiv').append($('<div>', {
        'id': 'extLink',
        "class": 'text'
      }));



      $('#codeH2').text("Thank you. Your trial code is:");
      $('#cardContent').html("<h1> " +trial.randomCode + "</h1>");
      $('#extLink').html("<p></p><p> For more information on this experiment "+
        'please click <a href="http://groups.inf.ed.ac.uk/online_questions/test.html" target="_blank">here</a></p>');



      var trialdata = {
        "randomCode": trial.randomCode
      };

      jsPsych.finishTrial(trialdata);

    };
    return plugin;
  })();

  
