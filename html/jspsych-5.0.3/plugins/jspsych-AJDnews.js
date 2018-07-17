/*
 * Example plugin template
 */

jsPsych.plugins.AJDnews = (function() {

  var plugin = {};

  plugin.trial = function(display_element, trial) {

    // set default values for parameters
    trial.showNews = trial.showNews || false;
    trial.currentQuestion = trial.currentQuestion || 0;
    trial.responseFavour = trial.responseFavour || false;

    // allow variables as functions
    // this allows any trial variable to be specified as a function
    // that will be evaluated when the trial runs. this allows users
    // to dynamically adjust the contents of a trial as a result
    // of other trials, among other uses. you can leave this out,
    // but in general it should be included
    trial = jsPsych.pluginAPI.evaluateFunctionParameters(trial);


    // Required if making changes to JSON, othewise loads from browser cache
    $.ajaxSetup({ cache: false});

    /* VARIABLES */
    var myJSON;
    var forResponses;
    var againstResponses
    var forIndex = 0;
    var againstIndex = 0;

    // Variables to store click data
    var alphaNewsClicks = [];
    var firstNewsClicks = [];
    var premierNewsClicks = [];
    var firstForAgainst = [];

    // Variables to store progression requirements
    var ariaValue = 0;
    if (trial.currentQuestion === 0){
      var maxHeadlines = 5;
    } else {
      var maxHeadlines = 15;
    }

    /* FUNCTIONS */

    /* Returns a random number between min (inclusive) and max (exclusive) */
    function getRandomInt(min, max) {
        return Math.floor(Math.random() * (max - min) + min);
    };
    
    /* Updates the progress bar */
    function updateProgress() {
      var val = parseFloat($('#progressBarTime').attr('aria-valuenow'));
      val = val + (100/maxHeadlines);
      $('#progressBarTime').attr({'aria-valuenow': val, 
          'style':"width:" + val +"\%"});
      if (val > 99){
        $('#continue').prop('disabled', false);
        $('#alpha_news').prop('disabled', true);
        $('#premier_news').prop('disabled', true);
        $('#first_news').prop('disabled', true);

      }
    };


    /* Returns a headline*/
    function getHeadline(forOrAgainst){
      if (forOrAgainst === 'for'){
        if (forIndex > forResponses.length - 1){
          forIndex = 0;
          var curHeadline = forResponses[forIndex];
          forIndex++;
          return curHeadline;
        }
        var curHeadline = forResponses[forIndex];
        forIndex++;
        return curHeadline;
      } else {
        if (againstIndex > againstResponses.length - 1){
          againstIndex = 0;
          var curHeadline = againstResponses[againstIndex];
          againstIndex++;
          return curHeadline;
      }
      var curHeadline = againstResponses[againstIndex];
        againstIndex++;
        return curHeadline;
      }
      
    };


    /* Knuth Shuffle 
    https://stackoverflow.com/questions/2450954/how-to-randomize-shuffle-a-javascript-array*/
    function shuffle(array) {
      var currentIndex = array.length, temporaryValue, randomIndex;

      // While there remain elements to shuffle...
      while (0 !== currentIndex) {

        // Pick a remaining element...
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex -= 1;

        // And swap it with the current element.
        temporaryValue = array[currentIndex];
        array[currentIndex] = array[randomIndex];
        array[randomIndex] = temporaryValue;
      }

      return array;
    };

    /* Creates the html for the page */
    function makePage() {
      // Create main container for page
        display_element.append($('<div>', {
          "id": 'mainContainer',
          'class': 'container'
        }));


        var newsLogos = ["alpha_news", "premier_news", "first_news"]
        newsLogos = shuffle(newsLogos);

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

          

          if (i < 3){

            $('#row'+i).append($('<div>', {
            'id': 'row'+i+'-col1',
            'class': 'col-9'
            }));

            $('#row'+i+'-col0').append($('<button>', {
              'id': newsLogos[i],
              'class': "btn btn-secondary",
            }))

            $('#'+newsLogos[i]).append($('<img>', {
              'id': newsLogos[i].slice(0,5),
              'src': './images/'+newsLogos[i]+'.png',
              'class': 'img-fluid',
              'alt': newsLogos[i]
            }))

            $('#row'+i+'-col1').append($('<div>', {
              "id":'id'+i,
              "class":"card",
            }));

            $('#id'+i).append($('<div>', {
              "id":newsLogos[i].slice(0,5)+"_disp",
              "class":"card-block pb-10",
              'height': '120px' 
            }));


          } else {
            $('#row'+i).append($('<div>', {
            'id': 'row'+i+'-col1',
            'class': 'col-7'
            }));

            $('#row'+i).append($('<div>', {
            'id': 'row'+i+'-col2',
            'class': 'col-2'
            }));

            $('#row'+i+'-col1').append($('<div>', {
              'id': 'timeProgress',
              'class': 'progress'
            }));

            $('#timeProgress').append($('<div>', {
              'id': 'progressBarTime',
              'class': 'progress-bar',
              'role': 'progressbar',
              'aria-valuenow': ariaValue,
              'aria-valuemin': "0",
              'aria-valuemax':"100",
              'style':"width:" + ariaValue +"\%"
            }));

            // Create button
            $('#row3-col2').append($('<button>', {
              'id': 'continue',
              'class': 'btn btn-primary pull-right',
              'html': 'Continue',
              'align': 'right'
            }));


          }
        };
          $('#continue').prop('disabled', true);

          var pos = "for";
          if ((Math.random() > 0.5)){
            pos = "against"
          };
          $('#first_disp').text(getHeadline(pos));
          if (trial.responseFavour){ 
            $('#alpha_disp').text(getHeadline('for'));
            $('#premi_disp').text(getHeadline('against'));
          } else {
            $('#alpha_disp').text(getHeadline('against'));
            $('#premi_disp').text(getHeadline('for'));
          }
    };

    /* Sets the JS for each button */
    function setButtons(){
      // Set button function
      $("#continue").click(function() {
      // data saving
      var trial_data = {
        'alphaNews': alphaNewsClicks,
        'premierNews': premierNewsClicks,
        'firstNews': firstNewsClicks,
        'firstForAgainst': firstForAgainst
      }
      // goto next trial in block
          display_element.html('');
          jsPsych.finishTrial(trial_data);
      });

      // Set 1st button functionality
      // ALPHA NEWS
      // This news generator will always agree with the user
      $('#alpha_news').click(function() {
        var position = 'for';
        if (!trial.responseFavour){
          position = 'against';
        }

        $('#alpha_disp').text(getHeadline(position));
        $('#premi_disp').text("");
        $('#first_disp').text("");

        updateProgress();

        alphaNewsClicks.push((new Date()).getTime());
      });

      // Set 2nd button functionality
      // PREMIER NEWS
      // This news generator will always disagree with the user
      $('#premier_news').click(function() {
        var position = 'for'
        if (trial.responseFavour){
          position = 'against'
        }
        $('#premi_disp').text(getHeadline(position));
        $('#alpha_disp').text("");
        $('#first_disp').text("");

        updateProgress();

        premierNewsClicks.push((new Date()).getTime());
      })

      // Set 3rd button functionality
      // FIRST NEWS
      $('#first_news').click(function() {
        var position = 'for';
        if (Math.random() > 0.5){
          position = 'against';
        }
        $('#first_disp').text(getHeadline(position));
        $('#alpha_disp').text("");
        $('#premi_disp').text("");

        updateProgress();

        firstNewsClicks.push((new Date()).getTime());
        firstForAgainst.push(position);
      })
    };

    $.getJSON("./JSON/new_questions.json").done(function(response) {
        myJSON = response;
        forResponses = myJSON[''+trial.currentQuestion]['for'];
        againstResponses = myJSON[''+trial.currentQuestion]['against'];

        makePage();
        setButtons();
  
    });
  };

  return plugin;
})();
