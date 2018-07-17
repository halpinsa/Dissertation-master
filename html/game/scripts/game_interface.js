/**
 * Created by joelwork on 28/05/2017.
 */
var suitOffset = {};
suitOffset[SuitsEnum.Clubs] = 0;
suitOffset[SuitsEnum.Diamonds] = 10;
suitOffset[SuitsEnum.Hearts] = 20;
suitOffset[SuitsEnum.Spades] = 30;

var cardXPositions = [100, 450, 100, 450];
var cardYPositions = [100, 100, 500, 500];
var cardToFrame = function(suit, number) {
    return (suitOffset[suit] + number - 1);
};
var gameRound;
var testType;
var criteria;
var direction;
var nextBiggest = true;
var gameChoices = [];
var cardSprites = [];
var costTexts = [];
var gameTypeText;
var scoreText;
var guessBottom;
var guessTop;
var counter;
var giveTitle = true;
var initialiseNewRound = false;
var coins = 1000;
var rounds = 9;
var numOfGameTypes = 10;
var inPause = false;
var complete = false;
var game;
var onEnd;
var smallestRoundIndex = -1;
var biggestRoundIndex = -1;

function startGame(endFunction) {
     game = new Phaser.Game(1000, 800, Phaser.AUTO, 'game_div', { preload: preload, create: create, update: update });
     onEnd = endFunction;
}

function preload() {
    game.scale.scaleMode = Phaser.ScaleManager.SHOW_ALL;
    game.load.image('guessBottom', './game/assets/guessBottom.png')
    game.load.image('guessTop', './game/assets/guessTop.png');
    game.load.image('scoreIncreased', './game/assets/score_increased.png');
    game.load.image('scoreDecreased', './game/assets/score_decreased.png');
    game.load.spritesheet('cards', './game/assets/svg_cards.png', 140, 200, 41);
}
 var attachEvent = function(sprite, item, methodName) {
    sprite.events.onInputDown.add(function () {
        item[methodName]();
    });
 };

var smallestGames;
var biggestGames;
var dataLoadDone = false;
$.getJSON('./game/scripts/games.json', function(data) {
    smallestGames = jsPsych.randomization.shuffle(data.smallest);
    biggestGames = jsPsych.randomization.shuffle(data.biggest);
    dataLoadDone = true;
});

function create() {

}

var introTextLine1;
function update() {
    if (inPause || (!dataLoadDone)) {
        return;
    }

    if (numOfGameTypes === 0 || coins < 0 ||  (gameRound && gameRound.coins() < 0)) {
        game.destroy();
        complete = true;
        onEnd();
        return;
    }

    if (giveTitle) {
        TestTypes = $.grep(TestTypes, function(o,i) {return o === testType;}, true);
        criteria = TestCriteriaEnum.Multiple;
        if (nextBiggest) {
            direction = TestDirectionsEnum.Biggest;
        }
        else {
            direction = TestDirectionsEnum.Smallest;
        }

        nextBiggest = !nextBiggest;

        var textToDisplay = 'Find the row with the:\n'+ direction + ' ' + criteria;

        introTextLine1 = game.add.text(0, 0, textToDisplay, { font: 'Courier New', fontSize: '64px', boundsAlignH: "center", boundsAlignV: "middle", align: "center", fill:'#FFFFFF'});
        introTextLine1.setTextBounds(0, 0, 1000, 700);
        var tween1 = game.add.tween(introTextLine1);
        tween1.onComplete.add(function() {
            inPause = false;
            initialiseNewRound = true;
        });
        tween1.to( { alpha: 0 }, 2000, Phaser.Easing.Linear.None, true, 2000, 0, false);
        inPause = true;
        giveTitle = false;
        return;
    }

    if (initialiseNewRound) {
        var gameSpec;
        if (direction === TestDirectionsEnum.Biggest) {
            biggestRoundIndex++;
            gameSpec = biggestGames[biggestRoundIndex]
        }
        else {
            smallestRoundIndex++;
            gameSpec = smallestGames[smallestRoundIndex];
        }
        gameRound =  createGameRound(coins, direction, criteria, gameSpec.gameCards, gameSpec.flipOrder);
        drawGameRound(gameRound);
        initialiseNewRound = false;

        return;

    }


    if (gameRound.finished) {
        coins = gameRound.coins();
        var xLocation;
        var yLocation;

        if (gameRound.guessMade == 'T') {
            xLocation = 250;
            yLocation = 150;
        }
        else {
            xLocation = 250;
            yLocation = 540;
        }

        if (gameRound.guessCorrect) {
            game.add.sprite(xLocation, yLocation, 'scoreIncreased');
        }
        else {
            game.add.sprite(xLocation, yLocation, 'scoreDecreased');
        }



        inPause = true;
        game.time.events.add(2000, finishRound, this);
        for (var i = 0; i < 4; i++) {
            cardSprites[i].inputEnabled = false;
        }
        guessBottom.inputEnabled = false;
        guessTop.inputEnabled = false;
    }

    updateGameRound(gameRound);
    if (gameRound.finished) {
        if (gameRound.isTopRow()) {
            cardSprites[0].tint = 0xb3ffc7;
            cardSprites[1].tint = 0xb3ffc7;
            cardSprites[2].tint = 0xffb3b3;
            cardSprites[3].tint = 0xffb3b3;
            game.add.text(650, cardSprites[2].centerY-32, gameRound.calculateBottom(), { font: 'Courier New', fontStyle:'bold', fontSize: '64px', boundsAlignH: "center", boundsAlignV: "middle", align: "center", fill:'#f21111'});
            game.add.text(650, cardSprites[0].centerY-32, gameRound.calculateTop(), { font: 'Courier New', fontStyle:'bold', fontSize: '64px', boundsAlignH: "center", boundsAlignV: "middle", align: "center", fill:'#62fa86'});
        }
        else {
            cardSprites[0].tint = 0xffb3b3;
            cardSprites[1].tint = 0xffb3b3;
            cardSprites[2].tint = 0xb3ffc7;
            cardSprites[3].tint = 0xb3ffc7;
            game.add.text(650, cardSprites[2].centerY-32, gameRound.calculateBottom(), { font: 'Courier New', fontStyle:'bold', fontSize: '64px', boundsAlignH: "center", boundsAlignV: "middle", align: "center", fill:'#62fa86'});
            game.add.text(650, cardSprites[0].centerY-32, gameRound.calculateTop(), { font: 'Courier New', fontStyle:'bold', fontSize: '64px', boundsAlignH: "center", boundsAlignV: "middle", align: "center", fill:'#f21111'});
        }
    }
}


function finishRound()
{
    inPause = false;
    gameChoices.push(gameRound.outputRoundChoices());
    game.world.removeAll(true);
    if (rounds === 0) {
        giveTitle = true;
        direction = null;
        criteria = null;
        rounds = 9;
        numOfGameTypes--;
        return;
    }

    initialiseNewRound = true;
    rounds--;
}

function drawGameRound(gameRound) {
    cardSprites = [];
    costTexts = [];
    for (var i = 0; i < 4; i++) {
        var cardSprite = game.add.sprite(cardXPositions[i],cardYPositions[i], 'cards', 40);
        cardSprite.inputEnabled = true;
        attachEvent(cardSprite, gameRound.cards[i], 'flip');
        cardSprites.push(cardSprite);
        var costText = game.add.text(cardSprite.centerX, cardSprite.centerY, gameRound.flipCost,
            {font: 'Courier New', fill:'#FFFFFF', fontSize: '64px',  fontStyle: 'bold', wordWrap: true, wordWrapWidth: cardSprite.width, align: "center"});
        costText.visible = false;
        costText.anchor.set(0.5);
        costTexts.push(costText);
    }

    var gameTypeTextXPos = 120;
    if (criteria === TestCriteriaEnum.Multiple) {
        gameTypeTextXPos = 60;
    }
    gameTypeText = game.add.text(gameTypeTextXPos, 20, direction + ' ' + criteria, { font: 'Courier New', fontSize: '64px', fill:'#FFFFFF' });
    scoreText = game.add.text(750, 20, 'Coins: ' + gameRound.coins(), { font: 'Courier New', fontSize: '32px', fill:'#FFFFFF' });
    guessTop = game.add.sprite(800, 150, 'guessTop');
    guessTop.inputEnabled = true;
    guessBottom = game.add.sprite(800, 550, 'guessBottom');
    guessBottom.inputEnabled = true;
    attachEvent(guessTop, gameRound, 'guessTop');
    attachEvent(guessBottom, gameRound, 'guessBottom');

}


function updateGameRound(gameRound) {
    for (var i = 0; i < 4; i++) {
        var card = gameRound.cards[i];
        if (gameRound.cards[i].visible) {
            cardSprites[i].frame = cardToFrame(card.suit, card.value);
        }

        if (gameRound.cards[i].flippable) {
            costTexts[i].text = -gameRound.flipCost;
            costTexts[i].visible = true;
            cardSprites[i].tint = 0xFFA500;
        }
        else {
            costTexts[i].visible = false;
            cardSprites[i].tint = 0xFFFFFF;
        }
    }
    scoreText.text = 'Coins: ' + gameRound.coins();

}
