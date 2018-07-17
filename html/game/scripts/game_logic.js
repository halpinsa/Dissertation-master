/**
 * Created by joelwork on 01/06/2017.
 */
var SuitsEnum = {
   Spades: 'Spades',
    Hearts: 'Hearts',
    Diamonds: 'Diamonds',
    Clubs: 'Clubs'
};

var TestDirectionsEnum = {
    Smallest: 'Smallest',
    Biggest: 'Biggest'
};

var TestCriteriaEnum = {
    Card: 'Card',
    Multiple: 'Multiple',
    Sum: 'Sum'
};


if (Object.freeze) {
    Object.freeze(SuitsEnum);
    Object.freeze(TestDirectionsEnum);
    Object.freeze(TestCriteriaEnum);
}

var createTestType = function(criteria, direction) {
    return {
        criteria: criteria,
        direction: direction
    };
};

var Suits = [SuitsEnum.Spades, SuitsEnum.Hearts, SuitsEnum.Diamonds, SuitsEnum.Clubs];
var TestTypes = [createTestType(TestCriteriaEnum.Card, TestDirectionsEnum.Smallest), createTestType(TestCriteriaEnum.Multiple, TestDirectionsEnum.Smallest),
    createTestType(TestCriteriaEnum.Sum, TestDirectionsEnum.Smallest), createTestType(TestCriteriaEnum.Card, TestDirectionsEnum.Biggest),
    createTestType(TestCriteriaEnum.Multiple, TestDirectionsEnum.Biggest), createTestType(TestCriteriaEnum.Sum, TestDirectionsEnum.Biggest)];
var takeSample = function(array) {
    return jsPsych.randomization.sample(array, 1, false)[0];
};

var createNewCard = function(value) {
    var card = {};
    var beforeSubscribers = [];
    var afterSubscribers = [];
    card.flippable = false;
    card.suit = takeSample(Suits);
    card.value = value;
    card.visible = false;
    card.flip = function () {
        if (!this.flippable) {
            return;
        }
        for (var i = 0; i < beforeSubscribers.length; i++) {
            beforeSubscribers[i]();
        }
        this.reveal();
        for (var j = 0; j < afterSubscribers.length; j++) {
            afterSubscribers[j]();
        }
    };

    card.reveal = function() {
        this.visible = true;
        this.flippable = false;
    };

    card.makeFlippable = function() {
        if (this.visible) {
            throw 'Visible cards cannot be flipped';
        }
        this.flippable = true;
    };

    card.beforeFlip = function(f) {
        beforeSubscribers.push(f);
    };

    card.afterFlip = function(f) {
        afterSubscribers.push(f);
    };

    card.data = function() {
        return {
            suit: card.suit,
            value: card.value
        };
    };
    return card;

};

var createGameRow = function(criteria, direction, card1_value, card2_value) {
    var cardRow = {};
    cardRow.cards = [createNewCard(card1_value), createNewCard(card2_value)];

    if (criteria === TestCriteriaEnum.Sum) {
        cardRow.calculate = function() {
            return cardRow.cards[0].value + cardRow.cards[1].value;
        }
    }
    else if (criteria === TestCriteriaEnum.Multiple) {
        cardRow.calculate = function() {
            return cardRow.cards[0].value * cardRow.cards[1].value;
        }
    }
    else if (criteria === TestCriteriaEnum.Card) {
        if (direction === TestDirectionsEnum.Smallest) {
            cardRow.calculate = function () {
                if (cardRow.cards[0].value < cardRow.cards[1].value) {
                    return cardRow.cards[0].value;
                }
                return cardRow.cards[1].value;
            }
        }
        else {
            cardRow.calculate = function () {
                if (cardRow.cards[0].value > cardRow.cards[1].value) {
                    return cardRow.cards[0].value;
                }
                return cardRow.cards[1].value;
            };
        }
    }
    return cardRow;
};



var createGameRound = function(startCoins, direction, criteria, card_values, flip_order) {
    var gameRound = {};
    var cardsFlipped = [];
    var trialType;
    gameRound.direction = direction;
    gameRound.criteria = criteria;
    gameRound.flipCost = 0;
    gameRound.finished = false;
    var coins = startCoins;
    var topRow = createGameRow(gameRound.criteria, gameRound.direction, card_values[0], card_values[1]);
    var bottomRow = createGameRow(gameRound.criteria, gameRound.direction, card_values[2], card_values[3]);
    gameRound.cards = topRow.cards.concat(bottomRow.cards);
    for (var i = 0; i < 4; i++) {
        gameRound.cards[i].index = i;
    }
    var revealAll = function() {
        for (var i = 0; i < gameRound.cards.length; i++) {
            gameRound.cards[i].reveal();
        }
    };

    var findHiddenCards = function() {
        var hiddenCards = [];
        for (var i=0; i < gameRound.cards.length; i++) {
            var card = gameRound.cards[i];
            if (!card.visible) {
                hiddenCards.push(card);
            }
        }
        return hiddenCards;
    };

    var updateFlipCost = function() {
        var numHiddenCards = findHiddenCards().length;
        switch (numHiddenCards) {
            case 4:
                gameRound.flipCost = 0;
                break;
            case 3:
                gameRound.flipCost = 10;
                break;
            case 2:
                gameRound.flipCost = 15;
                break;
            case 1:
                gameRound.flipCost = 20;
                break;
        }
    };

    var chooseFlippableCards = function() {
        var hiddenCards = findHiddenCards();
        var card;
        var cardIndex = 4 - hiddenCards.length;
        if (hiddenCards.length > 2) {
            card = gameRound.cards[flip_order[cardIndex]];
            card.makeFlippable();
            if (cardsFlipped.length === 1) {
                if (((cardsFlipped[0] === 0 || cardsFlipped[0] === 1) && (card.index === 2 || card.index === 3))
                    || ((cardsFlipped[0] === 2 || cardsFlipped[0] === 3) && (card.index === 0 || card.index === 1))) {
                    trialType = 'AB'
                }
                else {
                    trialType = 'AA'
                }
            }
        }
        else {
            for (var i = 0; i < hiddenCards.length; i++) {
                card = hiddenCards[i];
                card.makeFlippable();
            }
        }
    };

    var recordFlip = function(i) {
        return function() {
            cardsFlipped.push(i);
        }
    };

    gameRound.findFlippableCards = function() {
        var flippableCards = [];
        for (var i=0; i < gameRound.cards.length; i++) {
            var card = gameRound.cards[i];
            if (card.flippable) {
                flippableCards.push(card);
            }
        }
        return flippableCards;
    };


    var updateCoinsOnFlip = function() {
        coins = coins - gameRound.flipCost;
    };



    if (gameRound.direction === TestDirectionsEnum.Smallest) {
        gameRound.isTopRow = function() {
            return (topRow.calculate() < bottomRow.calculate());
        };

        gameRound.isBottomRow = function() {
            return (bottomRow.calculate() < topRow.calculate());
        };
    }
    else {
        gameRound.isTopRow = function () {
            return (topRow.calculate() > bottomRow.calculate());
        };
        gameRound.isBottomRow = function () {
            return (bottomRow.calculate() > topRow.calculate());
        };
    }

    gameRound.coins = function() {
        return coins;
    };

    gameRound.calculateTop = function() {
        return topRow.calculate();
    };

    gameRound.calculateBottom = function() {
        return bottomRow.calculate();
    };

    gameRound.guessTop = function() {
        gameRound.guessMade = 'T';
        if (gameRound.isTopRow()) {
            gameRound.guessCorrect = true;
            coins = coins + 60;
        }
        else {
            gameRound.guessCorrect = false;
            coins = coins - 50;
        }
        revealAll();
        gameRound.finished = true;
    };

    gameRound.guessBottom = function() {
        gameRound.guessMade = 'B';
        if (gameRound.isBottomRow()) {
            gameRound.guessCorrect = true;
            coins = coins + 60;
        }
        else {
            gameRound.guessCorrect = false;
            coins = coins - 50;
        }
        revealAll();
        gameRound.finished = true;
    };

    gameRound.outputRoundChoices = function() {
        if (!gameRound.finished) {
            throw 'Game round not finished!';
        }

        var cardData = [];
        for (var i=0; i < 4; i++) {
            cardData.push(gameRound.cards[i].data());
        }

        return {
            cardsFlipped : cardsFlipped,
            guessCorrect: gameRound.guessCorrect,
            guessMade: gameRound.guessMade,
            criteria: gameRound.criteria,
            direction: gameRound.direction,
            cards: cardData,
            trialType: trialType,
            coins: coins
        };
    };

   for (var i =0; i < gameRound.cards.length; i++) {
       gameRound.cards[i].afterFlip(updateFlipCost);
       gameRound.cards[i].afterFlip(chooseFlippableCards);
       gameRound.cards[i].beforeFlip(recordFlip(i));
       gameRound.cards[i].beforeFlip(updateCoinsOnFlip);
   }

   chooseFlippableCards();
   return gameRound;
};


/*var gameRound = createGameRound(100, TestDirectionsEnum.Smallest, TestCriteriaEnum.Multiple);
console.log('Game Type: ' + gameRound.direction + ' ' + gameRound.criteria);
console.log('Coins ' + gameRound.coins());
gameRound.findFlippableCards()[0].flip();
gameRound.findFlippableCards()[0].flip();
console.log('Coins ' + gameRound.coins());
gameRound.findFlippableCards()[0].flip();
console.log('Coins ' + gameRound.coins());
gameRound.findFlippableCards()[0].flip();
console.log('Coins ' + gameRound.coins());
var newGameRound = createGameRound(100, TestDirectionsEnum.Smallest, TestCriteriaEnum.Multiple);
console.log('New round established');
console.log('Card 1 visible: ' + newGameRound.cards[0].visible);
console.log('Card 2 visible: ' + newGameRound.cards[1].visible);
console.log('Card 3 visible: ' + newGameRound.cards[2].visible);
console.log('Card 4 visible: ' + newGameRound.cards[3].visible);
console.log('Card 1 flippable: ' + newGameRound.cards[0].flippable);
console.log('Card 2 flippable: ' + newGameRound.cards[1].flippable);
console.log('Card 3 flippable: ' + newGameRound.cards[2].flippable);
console.log('Card 4 flippable: ' + newGameRound.cards[3].flippable);
newGameRound.guessBottom();
console.log('Made guess');
console.log('Card 1 visible: ' + newGameRound.cards[0].visible);
console.log('Card 2 visible: ' + newGameRound.cards[1].visible);
console.log('Card 3 visible: ' + newGameRound.cards[2].visible);
console.log('Card 4 visible: ' + newGameRound.cards[3].visible);
console.log('Card 1 flippable: ' + newGameRound.cards[0].flippable);
console.log('Card 2 flippable: ' + newGameRound.cards[1].flippable);
console.log('Card 3 flippable: ' + newGameRound.cards[2].flippable);
console.log('Card 4 flippable: ' + newGameRound.cards[3].flippable);*/
