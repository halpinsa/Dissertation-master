jsPsych.plugins["JMMcardgame"] = (function() {

    var plugin = {};

    plugin.trial = function(display_element, trial) {
        display_element.append($('<div>', {
            "id": 'mainContainer',
            'class': 'container'
        }));

        $('#mainContainer').append($('<div>', {
            "id": "game_div",
            'class': "gameDiv"
        }));

        var onEnd = function() {
            var trial_data = {game_choices: gameChoices};
            jsPsych.finishTrial(trial_data);
        };
        startGame(onEnd);
    };

    return plugin;
})();
