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

jsPsych.plugins['AJDseparator'] = (function() {

  var plugin = {};

  plugin.trial = function(display_element, trial) {

    trial.cont_key = 'mouse';

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
      "id": 'statement',
      "class": 'jumbotron text-center'
        }));

    $('#statement').html('<h2>'+ trial.text+' complete!</h2><p>'+
                          'Please tap or click in this box to continue</p>')

    var start_time = (new Date()).getTime();

    var after_response = function(info) {

      display_element.html(''); // clear the display

      var trialdata = {
        "rt": info.rt,
        "key_press": info.key
      }

      jsPsych.finishTrial(trialdata);

    };

    $('#mainContainer').click(function() {
        var rt = (new Date()).getTime() - start_time;
        after_response({
          key: 'mouse',
          rt: rt
        });
    })
  };

  return plugin;
})();
