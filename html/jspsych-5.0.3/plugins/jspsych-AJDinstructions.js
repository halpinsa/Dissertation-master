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

jsPsych.plugins['AJDinstructions'] = (function() {

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

    if (trial.part === 1){
      trial.pages = ['page_1', 'page_2', 'page_3', 'page_4']
    } else if (trial.part === 3) {
      trial.pages = ['page_1', 'page_2']
    } else if (trial.part === 4) {
      trial.pages = ['page_1']
    };
    
    var current_page = 0;

    var view_history = [];

    var start_time = (new Date()).getTime();

    var last_page_update_time = start_time;

    display_element.append($('<div>', {
        "id": 'mainContainer',
        'class': 'container'
    }));

    function show_current_page() {
      if (trial.part === 1) {
        if (trial.pages[current_page] === 'page_1') {
          $('#mainContainer').html('');
          var html_page1 = '<div class="card">'+
                        '<div class="card-header">'+
                          'Instructions - Welcome'+
                        '</div>'+
                        '<div class="card-block">'+
                          '<h4 class="card-title">Welcome!</h4>'+
                          '<p class="card-text">'+
                          'This is an experiment with two separate parts:'+
                          '<ul>Part 1: Responses to statements</ul>'+
                          '<ul>Part 2: Completing a survey</ul>'+
                          'You must complete both '+
                          'parts to complete the HIT</p>'+
                        '</div>'+
                      '</div>'
          $('#mainContainer').append(html_page1);
        
        } else if (trial.pages[current_page] === 'page_2') {
          $('#mainContainer').html('');
          var html_page2 = '<div class="card">'+
                        '<div class="card-header">'+
                          'Instructions - Part 1'+
                        '</div>'+
                        '<div class="card-block">'+
                          '<p class="card-text">'+
                          'In this part you will be presented with a statement. '+
                          'You will use a slider to express how strongly '+
                          'you agree or disagree with it. If you want to choose a neutral '+
                          'response, click on the slider button.' +
                          '<p></p>'+
                          'You will then be presented with a series of questions about '+
                          'the statement and your response.'+
                          '<p></p>'+
                          '</div>'+
                          '</div>'
          $('#mainContainer').append(html_page2);

        } else if (trial.pages[current_page] === 'page_3') {
          $('#mainContainer').html('');
          var html_page3 = '<div class="card">'+
                        '<div class="card-header">'+
                          'Instructions - Part 1'+
                          '</div>'+
                          '<div class="card-block">'+
                          'You will then be shown a screen with three news logos on it. '+
                          'Each of these news logos represents a news agency. We\'ve '+
                          'hidden the identity of the news agency, but the headlines are real.'+
                          '<p></p>'+
                          'Each time you click on these logos you will see a news '+
                          'headline from that news agency in the box beside it.'+
                          '<p></p>'+
                          'There is a minimum number of headlines you need to view '+
                          'before you can continue.'+
                          '<p></p>'+
                          'You will then be shown the first screen again to which '+
                          'you can adjust your response.'+
                          '<p></p>'+
                          'There will be 16 statements in total.'+
                          '<p></p>'+
                          '<strong>The first statement is a practice one to help you to understand the interface</strong>'
                        '</div>'+
                      '</div>'  
          $('#mainContainer').append(html_page3);
        } else {
          $('#mainContainer').html('');
          var html_page4 = '<div class="card">'+
                        '<div class="card-header">'+
                          'Consent Form'+
                        '</div>'+
                        '<div class="card-block">'+
                          '<p class="card-text">'+
                          'The instructions for Part 1 are now complete.  A consent form follows. Please read the following information carefully. ' +
                          'You may also like to print a copy for your records.'+
                          '<p></p>'+
                          '<h3 class="card-title">Consent Form </h3>'+
                          '<h4 class="card-title">Description </h4>' +
                          '<p class="card-text">'+
                          ' By completing this HIT, you are agreeing to participate in a research study on the cognitive processes ' +
                          'involved in human information processing and decision making. ' +
                          'We are not aiming to test participants ability in any of the following task but are instead' +
                          ' attempting to discover and test general patterns in human reasoning ' +
                          'and their relationship with certain survey results.' +
                            '</p>' +
                            '<h4 class="card-title">Risks and benefits</h4>' +
                            '<p class="card-text">' +
                            'The first section of this task should not entail any significant risk to the participant. However, ' +
                                'the surveys at the end of the study require the participant to give personal information regarding their personality traits. '
                                + 'Appropriate steps will be taken to ensure that any published data or research is anonymised so that individual participants cannot be identified.' +
                           '<h4 class="card-title">Time Involvement</h4>' +
                            '<p class="card-text">' +
                            'You will have an hour to complete the task. It should take around 40 minutes to complete.' +
                            '</p>' +
                            '<h4 class="card-title">Subject Rights</h4>' +
                            '<p class="card-text">' +
                            'If you have read this form and have decided to participate in this HIT, please understand that if you find any of the HIT objectionable you can discontinue it at any time. ' +
                            'No data will be collected from you if you discontinue the HIT but you will not receive payment. ' +
                            'As previously stated, your individual privacy will be maintained in all published and written data resulting from our study. ' +
                            '</p>' +

                            '<p></p>'+
                          'By clicking <b>Accept</b> you are agreeing to participate in this study and give your consent for data to be collected and published subject to the conditions above. ' +
                  'You are also agreeing that you meet the following conditions: ' +
                  '<ul><li>You are fluent in English.</li><li>You are over 18 years old.</li> <li>You have read the above consent form, understood it and you agree to it.</li>' +
                    '<li>You want to participate in our study.</li></ul>' +

                    'The task will begin once you click <b>Accept</b>.' + '<p></p>' +
              'You will not be able to view these instructions again, so please review '+
              'them if you are unsure of anything. ' +
                          'Enjoy!' +
                        '</div>'+
                      '</div>';
          $('#mainContainer').append(html_page4);
        
        }
      
      } else if (trial.part === 3) {
        if (trial.pages[current_page] === 'page_1') {
          $('#mainContainer').html('');
          var html_page1 = '<div class="card">'+
                        '<div class="card-header">'+
                          'Instructions - Part 2'+
                        '</div>'+
                        '<div class="card-block">'+
                          '<p class="card-text">'+
                          'In this part you will be presented with three brief surveys. '+
                          'Each question will have a multiple choice answer.' +
                          '<p></p>'+
                          'Once you click "submit" you cannot change your answers. ' +
                          'You must fill in all the answers to '+
                          'complete this part.'+
                        '</div>'+
                      '</div>'
          $('#mainContainer').append(html_page1);
        
        } else {
          $('#mainContainer').html('');
          var html_page2 = '<div class="card">'+
                        '<div class="card-header">'+
                          'Instructions - Part 2 Complete'+
                        '</div>'+
                        '<div class="card-block">'+
                          '<p class="card-text">'+
                          'That completes the instructions for part 2. '+
                          '<p></p>'+
                          'Once you click begin '+
                          'you will not be able to view them again, so please review '+
                          'them if you are unsure of anything.'
                          '<p></p>'+
                          'Enjoy!'
                        '</div>'+
                      '</div>'
          $('#mainContainer').append(html_page2);
        
        }
      
      } else if (trial.part === 4) {
        if (trial.pages[current_page] === 'page_1') {
          $('#mainContainer').html('');
          var html_page1 = '<div class="card">'+
                        '<div class="card-header">'+
                          'Purpose'+
                        '</div>'+
                        '<div class="card-block">'+
                          '<p class="card-text">'+
                          'Thank you for taking part!' +
                          '<p></p>'+
                          'The purpose of this experiment was to attempt to '+
                          'measure the effects of the confirmation bias in online media and its relationship with ' +
                          'emotion and personality traits ' +
                        'If you feel that you have been affected by any of the issues raised in these surveys, more information can be found <a href="./info.html">here</a>. ' +
                        'This study is being conducted as part of an MSc dissertation in Informatics at the University of Edinburgh.' +
                          '<p></p>'+
                          '<p></p>' +
                          'We would greatly appreciate if you could keep the purpose '+
                          'of this HIT confidential.' +
                          '<p></p>'+
                          'Thanks,' +
                          '<p></p>'+
                          '<p></p>'+
                          'Sarah' + '<p></p>'
                  + 'If you have any questions about this research, please feel free to contact Sarah at s1773706 at ed.ac.uk' +
                        '</div>'+
                      '</div>';
          $('#mainContainer').append(html_page1);
      }
    }

    
      

      if (trial.show_clickable_nav) {

        var nav_html = "<div class='jspsych-instructions-nav'>";
        if (current_page != 0 && trial.allow_backward) {
          nav_html += "<button id='jspsych-instructions-back' class='jspsych-btn'>&lt; Previous</button>";
        }
        var end_button_text;
        if (trial.part === 1) {
          end_button_text = 'Accept';
        }
        else {
          end_button_text ='Begin';
        }
        if (current_page === trial.pages.length - 1){
          nav_html += "<button id='jspsych-instructions-next' class='jspsych-btn'>" + end_button_text + "</button></div>"
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
    };

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

    var after_response = function(info) {

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
  };

  return plugin;
})();
