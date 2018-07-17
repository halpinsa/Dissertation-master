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

jsPsych.plugins['JMMinstructions'] = (function() {

  var plugin = {};

  plugin.trial = function(display_element, trial) {

      trial.key_forward = trial.key_forward || 'rightarrow';
      trial.key_backward = trial.key_backward || 'leftarrow';
      trial.allow_backward = (typeof trial.allow_backward === 'undefined') ? true : trial.allow_backward;
      trial.allow_keys = (typeof trial.allow_keys === 'undefined') ? true : trial.allow_keys;
      trial.show_clickable_nav = (typeof trial.show_clickable_nav === 'undefined') ? false : trial.show_clickable_nav;

      // if any trial variables are functions
      // this evaluates the function and replaces
      // it with the output of the function
      trial = jsPsych.pluginAPI.evaluateFunctionParameters(trial);

      trial.pages = ['page_1', 'page_2'];

      var current_page = 0;

      var view_history = [];

      var start_time = (new Date()).getTime();

      var last_page_update_time = start_time;

      display_element.append($('<div>', {
          "id": 'mainContainer',
          'class': 'container'
      }));

      function show_current_page() {
          $('#mainContainer').html('');
          if (trial.pages[current_page] == 'page_1') {
              var html_page1 = '<div class="card">' +
                  '<div class="card-header">' +
                  'Game Instructions' +
                  '</div>' +
                  '<div class="card-block">' +
                  '<p class="card-text">' +
                  'In this part you will have to play a simple card game. ' +
                  'Two rows of two cards will be displayed to you. ' +
                  'To win coins (points), you will need to guess which row satisfies a given condition. ' +
                  'The two conditions are Biggest Multiple and Smallest Multiple meaning you need to guess which row is greater/smaller when multiplied. ' +
                       'An example of the Biggest Multiple condition is shown below. '
                      + '<p></p>'
                      + '<img src="./images/game_screen.png" class="img-thumbnail">'
                  + '<p></p>'
                  + 'At the beginning of each game stage, you will be shown which condition applies. ' +
                  'After that, you will be shown the two rows of cards face down. ' +
                  'One card, with a 0 shown on it, can be flipped over for free. ' +
                  'To flip over subsequent cards, you must pay the number of coins shown on the card. ' +
                  '<p></p>' +
                  'You can make a guess at any point. If you guess correctly then you win 60 coins. ' +
                  'If your guess is incorrect, then you will lose 50 coins. ' +

                  '<p></p>' +
                  '<b>Picture cards have been removed from the deck and Ace cards have been replaced with One cards.</b>'
                  + '<p></p>' + '<b>' +
                  'An instructional video showing an example round follows on the next page.' +
                  '</b>' +
                  '</div>' +
                  '</div>';
              $('#mainContainer').append(html_page1);
          }
          else if (trial.pages[current_page] == 'page_2') {
              var html_page2= '<div class="card">' +
                  '<div class="card-header">' +
                  'Game Instructions' +
                  '</div>' +
                  '<div class="card-block">' +
                  '<p class="card-text">' +
                  '<video width="960" height="540" class="img-thumbnail" controls>' +
              '<source src="./videos/instructional_video.mp4" type="video/mp4">' +
                  'Your browser does not support the video tag.' +
              '</video>' + '<p></p>' +
              'A $1 bonus will be awarded to all Turkers with an above average score. ' +
                  'Additional prizes will also be offered to the three highest scorers as follows:' +
                  '<ul><li>3rd Place: $4</li><li>2nd Place: $6</li><li><b>1st Place: $10</b></li></ul>' + '<p></p>' +
              'The task will begin once you click <b>Begin</b>.' + '<p></p>' +
              'You will not be able to view these instructions again, so please review '+
              'them if you are unsure of anything. '
              '</p>' +
                  '</div></div>';
              $('#mainContainer').append(html_page2);
          }




          if (trial.show_clickable_nav) {
              var nav_html = "<div class='jspsych-instructions-nav'>";
              if (current_page != 0 && trial.allow_backward) {
                  nav_html += "<button id='jspsych-instructions-back' class='jspsych-btn'>&lt; Previous</button>";
              }
              if (current_page === (trial.pages.length - 1)){
                  nav_html += "<button id='jspsych-instructions-next' class='jspsych-btn'>Begin</button></div>"
              } else {
                  nav_html += "<button id='jspsych-instructions-next' class='jspsych-btn'>Next &gt;</button></div>"
              }

              $('#mainContainer').append(nav_html);

              if (current_page != 0 && trial.allow_backward) {
                  $('#jspsych-instructions-back').on('click', function() {
                      clear_button_handlers();
                      back();
                  });
              }

              $('#jspsych-instructions-next').on('click', function() {
                  clear_button_handlers();
                  next();
              });

          }
      }


      function clear_button_handlers() {
          $('#jspsych-instructions-next').off('click');
          $('#jspsych-instructions-back').off('click');
      }

      function next() {

          add_current_page_to_view_history()

          current_page++;

          // if done, finish up...
          if (current_page >= trial.pages.length) {
              endTrial();
          } else {
              show_current_page();
          }

      }

      function back() {

          add_current_page_to_view_history()

          current_page--;

          show_current_page();
      }

      function add_current_page_to_view_history() {

          var current_time = (new Date()).getTime();

          var page_view_time = current_time - last_page_update_time;

          view_history.push({
              page_index: current_page,
              viewing_time: page_view_time
          });

          last_page_update_time = current_time;
      }

      function endTrial() {

          if (trial.allow_keys) {
              jsPsych.pluginAPI.cancelKeyboardResponse(keyboard_listener);
          }

          display_element.html('');

          var trial_data = {
              "view_history": JSON.stringify(view_history),
              "rt": (new Date()).getTime() - start_time
          };

          jsPsych.finishTrial(trial_data);
      }

      var after_response = function (info) {

          // have to reinitialize this instead of letting it persist to prevent accidental skips of pages by holding down keys too long
          keyboard_listener = jsPsych.pluginAPI.getKeyboardResponse({
              callback_function: after_response,
              valid_responses: [trial.key_forward, trial.key_backward],
              rt_method: 'date',
              persist: false,
              allow_held_key: false
          });
          // check if key is forwards or backwards and update page
          if (info.key === trial.key_backward || info.key === jsPsych.pluginAPI.convertKeyCharacterToKeyCode(trial.key_backward)) {
              if (current_page !== 0 && trial.allow_backward) {
                  back();
              }
          }

          if (info.key === trial.key_forward || info.key === jsPsych.pluginAPI.convertKeyCharacterToKeyCode(trial.key_forward)) {
              next();
          }

      };

      show_current_page();

      if (trial.allow_keys) {
          var keyboard_listener = jsPsych.pluginAPI.getKeyboardResponse({
              callback_function: after_response,
              valid_responses: [trial.key_forward, trial.key_backward],
              rt_method: 'date',
              persist: false
          });
      }
      ;
  };
  return plugin;
})();
