/**
 * jspsych-AJDquestion.js
 * Josh de Leeuw (amended by Alasdair J. Dalgarno)
 *
 * This plugin create a trial users are shown a statement,
 * and the subject rates how much they agree using a
 * slider controlled with the mouse.
 *
 * documentation: None
 *
 */


jsPsych.plugins.AJDquestion = (function() {

  var plugin = {};

  jsPsych.pluginAPI.registerPreload('similarity', 'stimuli', 'image');

  plugin.trial = function(display_element, trial) {

    // default parameters
    trial.labels = (typeof trial.labels === 'undefined') ? ["Not at all similar", "Identical"] : trial.labels;
    trial.intervals = trial.intervals || 100;
    trial.show_ticks = (typeof trial.show_ticks === 'undefined') ? false : trial.show_ticks;
    trial.show_response = trial.show_response || "SECOND_STIMULUS";
    trial.timing_second_stim = trial.timing_second_stim || 100; // -1 = inf time; positive numbers = msec to display second image.

    //Custom parameters
    trial.question = trial.question || 0;

    // if any trial variables are functions
    // this evaluates the function and replaces
    // it with the output of the function
    trial = jsPsych.pluginAPI.evaluateFunctionParameters(trial);

    // this array holds handlers from setTimeout calls
    // that need to be cleared if the trial ends early
    var setTimeoutHandlers = [];

    // Custom
    // Show the question
    $.ajaxSetup({ cache: false});
    var myJSON;

    /*
    Function uses JS to create the page layout. Uses Bootstrap
    Container as the body for content, which is appended to the main
    body <div> element by the plugin
    */
    function makePage() {
      // Create main container for page
      display_element.append($('<div>', {
        "id": 'mainContainer',
        'class': 'container'
      }));

      // Create rows for page
      for(var i=0; i < 3; i++){
        $('#mainContainer').append($('<div>', {
          'id': 'row'+i,
          'class': 'row justify-content-center'
        }))
      };

      // Create question element
      $('#row0').append($('<div>', {
      "id": 'questionDiv',
      "class": 'jumbotron text-center'
        }));

      // Set question
      $('#questionDiv').append($('<h2>', {
        'id': 'mainQuestionH2'
      }));
      $('#mainQuestionH2').text(myJSON[''+trial.question]['question']);

      //  create button
      $('#row2').append($('<button>', {
        'id': 'next',
        'class': 'btn btn-primary',
        'html': 'Submit Answer'
      }));

      $('#next').prop('disabled', true);

      $("#next").click(function() {

        // kill any remaining setTimeout handlers
        for (var i = 0; i < setTimeoutHandlers.length; i++) {
          clearTimeout(setTimeoutHandlers[i]);
        }

        var score = $("#slider").slider("value");
        var trial_data = {
          "statementResponse": score
        };
        // goto next trial in block
        display_element.html('');
        jsPsych.finishTrial(trial_data);
      });
    };

    function showStim() {

      $('#jspsych-sim-stim').css('visibility', 'visible');
      show_response_slider(display_element, trial);
    };


    function show_response_slider(display_element, trial) {

      // create slider
      $('#row1').append($('<div>', {
        "id": 'slider',
        "class": 'col'
      }));

      $("#slider").slider({
        value: Math.ceil(trial.intervals / 2),
        min: 1,
        max: trial.intervals,
        step: 1,
        slide: function(event, ui){
          $('#next').prop('disabled', false);
        }
      });

      $('.ui-slider-handle').on('click', function() {
       $('#next').prop('disabled', false);
      });

      // show tick marks
      if (trial.show_ticks) {
        for (var j = 1; j < trial.intervals - 1; j++) {
          $('#slider').append('<div class="slidertickmark"></div>');
        }

        $('#slider .slidertickmark').each(function(index) {
          var left = (index + 1) * (100 / (trial.intervals - 1));
          $(this).css({
            'position': 'absolute',
            'left': left + '%',
            'width': '1px',
            'height': '100%',
            'background-color': '#222222'
          });
        });
      }

      // create labels for slider
      $('#row1').append($('<ul>', {
        "id": "sliderlabels",
        "class": 'sliderlabels',
        "css": {
          "width": "100%",
          "height": "3em",
          "margin": "10px 0px 0px 0px",
          "padding": "0px",
          "display": "block",
          "position": "relative"
        }
      }));

      for (var j = 0; j < trial.labels.length; j++) {
        $("#sliderlabels").append('<li>' + trial.labels[j] + '</li>');
      }

      // position labels to match slider intervals
      var slider_width = $("#slider").width();
      var num_items = trial.labels.length;
      var item_width = (slider_width / num_items)/2;
      var spacing_interval = slider_width / (num_items - 1);

      $("#sliderlabels li").each(function(index) {
        $(this).css({
          'display': 'inline-block',
          'width': item_width + 'px',
          'margin': '0px',
          'padding': '0px',
          'text-align': 'center',
          'position': 'absolute',
          'left': (spacing_interval * index) - (item_width / 2)
        });
      });
    };

    $.getJSON("./JSON/new_questions.json").done(function(response) {
        myJSON = response;
        makePage();
        showStim();
    })
    .fail(function(jqXHR, textStatus, errorThrown) {
      console.log(errorThrown);
    })
  };
  return plugin;
})();
