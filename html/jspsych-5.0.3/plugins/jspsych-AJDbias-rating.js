/*
 * Example plugin template
 */

jsPsych.plugins["AJDbias-rating"] = (function() {

  var plugin = {};

  plugin.trial = function(display_element, trial) {

    // set default values for parameters
    trial.intervals = 100;
    trial.show_ticks = false;
    trial.labels = ["Completely biased", "Moderately biased", "Completely non-biased"]

    // allow variables as functions
    // this allows any trial variable to be specified as a function
    // that will be evaluated when the trial runs. this allows users
    // to dynamically adjust the contents of a trial as a result
    // of other trials, among other uses. you can leave this out,
    // but in general it should be included
    trial = jsPsych.pluginAPI.evaluateFunctionParameters(trial);
    var startTime = (new Date()).getTime();

    var slider1 = false;
    var slider2 = false;
    var slider3 = false;

    function setButtonOn(id){
      if (id === '0'){
        slider1 = true;
      } else if (id === '1'){
        slider2 = true;
      } else {
        slider3 = true;
      }

      if (slider1 === true && slider2 === true && slider3 === true){
        $("#next").prop('disabled', false);
      }

    };


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

        // Create question element
        $('#mainContainer').append($('<div>', {
        "id": 'instructions',
        "class": 'jumbotron text-center'
        }));

        $('#instructions').text('Now, using the sliders, please indicate how '+
                                'biased you believe each news source to be.')

        var newsLogos = ['alpha_news', 'premier_news', 'first_news'];

        // Create page rows and columns
        for(var i=0; i < 4; i++){
          $('#mainContainer').append($('<div>', {
            'id': 'row'+i,
            'class': 'row mt-3'
          }));

          $('#row'+i).append($('<div>', {
            'id': 'row'+i+'-col0',
            'class': 'col-3 my-auto',
            'align': 'center'
          }));

          $('#row'+i).append($('<div>', {
            'id': 'row'+i+'-col1',
            'class': 'col-9'
          }));

          if (i < 3){
            $('#row'+i+'-col0').append($('<img>', {
              'id': newsLogos[i].slice(0,5),
              'src': './images/'+newsLogos[i]+'.png',
              'class': 'img-fluid',
              'alt': newsLogos[i]
            }));


          } else {
            // Create button
            $('#row3-col1').append($('<button>', {
              'id': 'next',
              'class': 'btn btn-default pull-right',
              'html': 'Continue'
            }));

            $("#next").prop('disabled', true);

          }

          $("#next").click(function() {
            var endTime = (new Date()).getTime();
            var response_time = endTime - startTime;

            var trial_data = {
              'alphaBias': $('#sliderrow0-col1').slider('value'),
              'premierBias': $('#sliderrow1-col1').slider('value'),
              'firstBias': $('#sliderrow2-col1').slider('value'),
              "rt": response_time
            };
            // goto next trial in block
            display_element.html('');
            jsPsych.finishTrial(trial_data);
          });

        };

    };


    function show_response_slider(display_element, trial, divID) {

      // create slider
      $('#'+divID).append($('<div>', {
        "id": 'slider'+divID,
        "class": 'col'
      }));

      $("#slider"+divID).slider({
        value: Math.ceil(trial.intervals / 2),
        min: 1,
        max: trial.intervals,
        step: 1,
        slide: function(event, ui){
          setButtonOn(divID.slice(3,4));
        }
        
      });

      $('#slider'+divID + '> .ui-slider-handle').on('click', function() {
        setButtonOn(divID.slice(3,4));
      });

      // $('.ui-slider-handle').on('click', function() {
      //       console.log($(this).closest("div").attr("id"));
      //       $('#next').prop('disabled', false);
      //     });

      // show tick marks
      if (trial.show_ticks) {
        for (var j = 1; j < trial.intervals - 1; j++) {
          $('#slider'+divID).append('<div class="slidertickmark"></div>');
        }

        $('#slider'+divID+' .slidertickmark').each(function(index) {
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
      $('#'+divID).append($('<ul>', {
        "id": "sliderlabels"+divID,
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
        $("#sliderlabels"+divID).append('<li>' + trial.labels[j] + '</li>');
      }

      // position labels to match slider intervals
      var slider_width = $("#slider"+divID).width();
      var num_items = trial.labels.length;
      var item_width = (slider_width / num_items) / 2;
      var spacing_interval = slider_width / (num_items - 1);

      $("#sliderlabels"+divID+" li").each(function(index) {
        $(this).css({
          'display': 'inline-block',
          'width': item_width + 'px',
          'margin': '0px',
          'padding': '0px',
          'text-align': 'center',
          'position': 'absolute',
          'left': (spacing_interval * index) - (item_width / 2) +30
        });
      });

    };



    makePage();
    show_response_slider(display_element, trial, 'row0-col1');
    show_response_slider(display_element, trial, 'row1-col1');
    show_response_slider(display_element, trial, 'row2-col1');

    // // end trial
    // jsPsych.finishTrial(trial_data);
  };

  return plugin;
})();
