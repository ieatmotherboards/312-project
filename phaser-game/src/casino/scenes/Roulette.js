/*
    FOR DOMINIC: Changes to be made to migrate this to phaser (first two have comments of what to change to)
    - Line 7
    - 116 (can keep the var named exitSign2)
    - 439 - 454, not sure how your Phaser implementation handles this
*/

import { CoinCounter } from '../../gameObjects/CoinCounter.js';
import { ExitSign2 } from '../../gameObjects/ExitSign2.js'; // import { ExitSign } from '../../gameObjects/ExitSign.js';

export class Roulette extends Phaser.Scene {

    constructor() {
        super({ key: 'Roulette' });
    }

    preload() {
        this.load.image('roulette', '/phaser-game/assets/roulette/roulette_bg_2.png'); 
        this.load.image('wheel', '/phaser-game/assets/roulette/roulette_wheel.png'); 
        this.load.image('up1', '/phaser-game/assets/roulette/up1.png');
        this.load.image('up5', '/phaser-game/assets/roulette/up5.png'); 
        this.load.image('down1', '/phaser-game/assets/roulette/down1.png'); 
        this.load.image('down5', '/phaser-game/assets/roulette/down5.png'); 
        this.load.image('ball', '/phaser-game/assets/roulette/ball.png');
        this.load.image('youwin', '/phaser-game/assets/youwin.png');
        this.load.image('youlose', '/phaser-game/assets/youlose.png');
        this.load.image('place_bet', '/phaser-game/assets/roulette/place_bet.png');
        this.load.image('heart','/phaser-game/assets/roulette/heart.png');

    }

    create() {
        const width = this.scale.width;
        const height = this.scale.height;

        const bg = this.add.image(width / 2, height / 2, 'roulette');
        bg.setOrigin(0.5);

        const scaleX = width / bg.width;
        const scaleY = height / bg.height;
        const scale = Math.max(scaleX, scaleY); // fill the screen
        bg.setScale(scale);


        // debugging box
        // const debug = this.add.graphics();
        // debug.lineStyle(4, 0x00ff00);
        // debug.strokeRect(0, 0, this.scale.width, this.scale.height);


        //wheel logic
        const imageStartX = width * .25;
        const imageStartY = height * .5;
        this.rouletteWheel = this.add.image(imageStartX, imageStartY, 'wheel');

        const originalWidth = this.rouletteWheel.width;
        const originalHeight = this.rouletteWheel.height;

        const maxDisplayWidth = width * 0.6;
        const maxDisplayHeight = height * 0.6;

        const wheel_scale = Math.min(maxDisplayWidth / originalWidth, maxDisplayHeight / originalHeight);
        this.rouletteWheel.setDisplaySize(originalWidth * wheel_scale, originalHeight * wheel_scale);

        // Ball positions based on wheel
        this.ballPositions = [
            { number: '0', x: 430, y: 40 },
            { number: '28', x: 494, y: 45 },
            { number: '9', x: 556, y: 61 },
            { number: '26', x: 614, y: 87 },
            { number: '30', x: 668, y: 122 },
            { number: '11', x: 716, y: 165 },
            { number: '7', x: 757, y: 215 },
            { number: '20', x: 789, y: 271 },
            { number: '32', x: 811, y: 331 },
            { number: '17', x: 823, y: 394 },
            { number: '5', x: 826, y: 458 },
            { number: '22', x: 818, y: 522 },
            { number: '34', x: 800, y: 583 },
            { number: '15', x: 773, y: 640 },
            { number: '3', x: 736, y: 693 },
            { number: '24', x: 691, y: 739 },
            { number: '36', x: 639, y: 775 },
            { number: '13', x: 582, y: 802 },
            { number: '1', x: 520, y: 818 },
            { number: '00', x: 456, y: 823 },
            { number: '27', x: 392, y: 816 },
            { number: '10', x: 330, y: 799 },
            { number: '25', x: 273, y: 770 },
            { number: '29', x: 220, y: 730 },
            { number: '12', x: 174, y: 682 },
            { number: '8', x: 136, y: 625 },
            { number: '19', x: 106, y: 561 },
            { number: '31', x: 88, y: 494 },
            { number: '18', x: 82, y: 426 },
            { number: '6', x: 88, y: 359 },
            { number: '21', x: 105, y: 293 },
            { number: '33', x: 134, y: 232 },
            { number: '16', x: 172, y: 176 },
            { number: '4', x: 219, y: 127 },
            { number: '23', x: 271, y: 89 },
            { number: '35', x: 328, y: 62 },
            { number: '14', x: 391, y: 45 },
            { number: '2', x: 0, y: 0 } // dummy fallback
        ];
        
        this.coinCounter = new CoinCounter(this, 28, 28);

        this.betInfo = {
            type: null,
            value: null,
            amount: 0,
            numOfNums: 0
        };
    
        // 1. Build the board
        this.createRouletteBoard(); // <- Generates the number grid and common bets

        // this.createBackButton();

        this.exitSign2 = new ExitSign2(this, this.scale.width, 0, 'Game').setOrigin(1, 0); // this.exitSign2 = new ExitSign(this, this.scale.width, 0, 'Game').setOrigin(1, 0);
        
        const betResult = this.add.text(imageStartX, imageStartY, '',{
            fontSize: '40px',
            fill: '#fd0000'
        }).setOrigin(.5);

        // 2. Add Place Bet button
        // const confirmBtn = this.add.text(width, height, 'Place Bet!', {
        //     fontSize: '20px',
        //     fill: '#ffffff',
        //     backgroundColor: '#007bff',
        //     padding: { x: 50, y: 25 }
        // })
        // .setOrigin(1,1) 
        // .setInteractive();

        const confirmBtn = this.add.image(width * .75, height * .85, "place_bet").setOrigin(.5).setScale(.5).setInteractive();
        
        const yourBet = this.add.text(width * .5, height * .1, 'Your Bet:',{
            fontSize: '65px',
            fill: '#ffffff'
        }).setOrigin(.5);

        // list of numbers that you bet on. cleared when you select a diff type of bet
        this.numBet = this.add.text(width * .5, height * .25, '',{ 
            fontSize: '20px',
            fill: '#ffffff'
        }).setOrigin(.5,.5);

        this.coinsWagered = this.add.text(width*.5, height * .83, "Coins Wagered:",{
            fontSize: '20px',
            fill: '#ffffff'
        }).setOrigin(.5,.5);

        this.coinsWageredNumber = this.add.text(width*.5, height * .88, "0",{
            fontSize: '20px',
            fill: '#ffffff'
        }).setOrigin(.5,.5);

        this.createWagerButtons();

        // the type of the bet that you select. "Number(s)" or something else like "Red"
        this.valueBet = this.add.text(width * .5, height * .2, '',{
            fontSize: '20px',
            fill: '#ffffff'
        }).setOrigin(.5,.5);

        confirmBtn.on('pointerdown', () => {
            console.log(this.valueBet.text);
            if (this.valueBet.text === "") {
                alert('No bet selected!');
                return;
            }else if(parseInt(this.coinsWageredNumber.text) <= 0){
                alert("Please select a positive number of coins");
                return;
            }

            // if(this.numBet.text === "11, 29, 24"){
            //     this.add.image(this.scale.width* .75, this.scale.height* .2, "heart").setScale(.5);
            // }


            console.log(' --- BET INFO ---');
            console.log("wagering " + this.betInfo.amount.toString() + " coins");
            console.log("betting on type " + this.valueBet.text);
            console.log("numbers are (if applicable):" + this.numBet.text);

            let request = new Request('/phaser/playRoulette', {
                method: "POST",
                body: JSON.stringify({
                    wager: parseInt(this.coinsWageredNumber.text),
                    bet_type: this.valueBet.text,
                    numbers: this.numBet.text
                }),
                headers: { "Content-Type": "application/json" }
            });
    
            this.tweens.add({
                targets: this.rouletteWheel,
                angle: 360 * 3,
                duration: 2000,
                ease: 'Cubic.easeOut',
                onComplete: () => {
                    this.rouletteWheel.angle = this.rouletteWheel.angle % 360;
                }
            });
            
            fetch(request)
                .then(response => response.json())
                .then(data => {

                    let outcome = parseInt(data['user_cashout']);

                    let resultImage;
                    if (outcome < 0){
                        resultImage = this.add.image(this.scale.width * .5, this.scale.height *.5, "youlose").setScale(3.5).setOrigin(.5);
                    }else{
                        resultImage = this.add.image(this.scale.width * .5, this.scale.height *.5, "youwin").setScale(3.5).setOrigin(.5);
                    }

                    const flashDurations = [0, 300, 500, 700, 900, 1100]; // in ms
                    flashDurations.forEach((delay, index) => {
                        this.time.delayedCall(delay, () => {
                            resultImage.setVisible(index % 2 === 0); // show on even index, hide on odd
                        }, [], this);
                    });

                    // Finally destroy after last flash
                    this.time.delayedCall(1200, () => {
                        resultImage.destroy();
                    }, [], this);

                    console.log("Number outcome:", data['outcome']);
                    console.log("Winnings:", data['user_cashout']);
                    
                    //unncessary redeclaration of redNumbers here
                    const redNumbers = new Set([
                        1, 3, 5, 7, 9, 12, 14, 16, 18,
                        19, 21, 23, 25, 27, 30, 32, 34, 36
                    ]);

                    if (redNumbers.has(data['outcome'])){
                        betResult.setText(data['outcome'].toString());
                        betResult.setColor("#fd0000");
                    }else{
                        betResult.setText(data['outcome'].toString());
                        betResult.setColor("#000000"); 
                    }

                    if (this.ballSprite) {
                        this.ballSprite.destroy();
                    }
                    
                    let match = this.ballPositions.find(p => p.number === data['outcome'].toString());
                    if (!match && data['outcome'] === 0) {
                        match = this.ballPositions.find(p => p.number === '0');
                    }
                    if (!match && data['outcome'] === '00') {
                        match = this.ballPositions.find(p => p.number === '00');
                    }
                    
                    if (match) {
                        const wheelX = this.rouletteWheel.x - this.rouletteWheel.displayWidth / 2;
                        const wheelY = this.rouletteWheel.y - this.rouletteWheel.displayHeight / 2;
                        const scale = this.rouletteWheel.displayWidth / this.rouletteWheel.width;
                    
                        this.ballSprite = this.add.image(
                            wheelX + match.x * scale,
                            wheelY + match.y * scale,
                            'ball'
                        ).setScale(scale * 0.15); // adjust size as needed
                    }
                    
                })
                .catch(err => console.error('Error placing bet:', err));
        });
    }
    

    createBetButton(label, x, y, type, color) {
        let btn = this.add.text(x, y, label, {
            fontSize: '18px',
            fill: '#fff',
            backgroundColor: color,
            padding: { x: 13, y: 7 }
        }).setInteractive();

        btn.on('pointerdown', () => {
            this.betInfo.type = type;
            this.numBet.setText("");
            this.valueBet.setText(type);
            this.betInfo.numOfNums = 0;
            console.log(`Selected Bet: ${type}`);
            
        });
    }
    
    createRouletteBoard() {
        const gridStartX = this.scale.width * .5;
        const gridStartY = this.scale.height * .55; 
        const cellSize = 55;
    
        this.betButtons = [];

        const redNumbers = new Set([
            1, 3, 5, 7, 9, 12, 14, 16, 18,
            19, 21, 23, 25, 27, 30, 32, 34, 36
        ]);

        for (let col = 0; col < 12; col++) {
            for (let row = 0; row < 3; row++) { //
                const x = gridStartX + col * cellSize;
                const y = gridStartY - row * cellSize;

                let number = col * 3 + row + 1;

                const isRed = redNumbers.has(number);
                const bgColor = isRed ? '#fd0000' : '#000000';
    
                const numText = this.add.text(x, y, number.toString(), {
                    fontSize: '16px',
                    fill: '#fff',
                    backgroundColor: bgColor,
                    padding: { x: 13, y: 7 }
                }).setInteractive();
    
                numText.on('pointerdown', () => {
                    this.betInfo.type = 'number';
                    this.betInfo.value = number;
                    console.log(`Bet on number ${number}`);
                    // change value in bet info to num here
                    if(this.numBet.text === ""){
                        this.numBet.setText(number.toString());
                        this.betInfo.numOfNums++;
                    }else{
                        if(this.betInfo.numOfNums < 6){
                            this.numBet.setText(this.numBet.text + ", " + number.toString());
                            this.betInfo.numOfNums ++;
                        }else{
                            alert("You may only bet on maximum 6 numbers at once");
                        }
                        
                    }
                    this.valueBet.setText("Number(s)");
                        
                });
    
                this.betButtons.push(numText);
            }
        }
    
        // Add 0 button
        const zeroBtn = this.add.text(gridStartX - 75, this.scale.height * .55 , '0', {
            fontSize: '16px',
            fill: '#fff',
            backgroundColor: '#004d4d',
            padding: { x: 10, y: 5 }
        }).setInteractive();

        // add 00
        const doubleZeroBtn = this.add.text(gridStartX - 75, this.scale.height * .45, '00', {
            fontSize: '16px',
            fill: '#fff',
            backgroundColor: '#004d4d',
            padding: { x: 10, y: 5 }
        }).setInteractive();
    
        zeroBtn.on('pointerdown', () => {
            this.betInfo.type = 'number';
            this.betInfo.value = 0;
            if(this.numBet.text === ""){
                this.numBet.setText("0");
                this.betInfo.numOfNums++;
            }else{
                if(this.betInfo.numOfNums < 6){
                    this.numBet.setText(this.numBet.text + ", " + "0");
                    this.betInfo.numOfNums ++;
                }else{
                    console.log("You may only bet on maximum 6 numbers at once");
                }
                
            }
            this.valueBet.setText("Number(s)");
        });

        doubleZeroBtn.on('pointerdown', () => {
            this.betInfo.type = 'number';
            this.betInfo.value = "00";
            console.log('Bet on number 00');
            if(this.numBet.text === ""){
                this.numBet.setText("00");
                this.betInfo.numOfNums++;
            }else{
                if(this.betInfo.numOfNums < 6){
                    this.numBet.setText(this.numBet.text + ", " + "00");
                    this.betInfo.numOfNums ++;
                }else{
                    console.log("You may only bet on maximum 6 numbers at once");
                }
                
            }
            this.valueBet.setText("Number(s)");
        });
        
        //generate bet buttons
        this.createBetButton('1st Twelve', gridStartX, gridStartY + 50, '1st Twelve', '#004d4d' );
        this.createBetButton('2nd Twelve', gridStartX + 150, gridStartY + 50, '2nd Twelve', '#004d4d' );
        this.createBetButton('3rd Twelve', gridStartX + 300, gridStartY + 50, '3rd Twelve', '#004d4d' );

        this.createBetButton('1-18', gridStartX, gridStartY + 100, 'First 18', '#004d4d' );
        this.createBetButton('Even', gridStartX + 100, gridStartY + 100, 'Even', '#004d4d' );
        this.createBetButton('Red', gridStartX + 200, gridStartY + 100, 'Red', '#fd0000' );
        this.createBetButton('Black', gridStartX + 300, gridStartY + 100, 'Black', '#000000' );
        this.createBetButton('Odd', gridStartX + 400, gridStartY + 100, 'Odd', '#004d4d' );
        this.createBetButton('19-36', gridStartX + 500, gridStartY + 100, 'Second 18', '#004d4d');
        
    }

    createWagerButtons(){
        const up1 = this.add.image(this.scale.width *.6 ,  this.scale.height * .85, "up1").setScale(.2).setInteractive();
        up1.on('pointerdown', () => {
            console.log('up1 clicked!');
            let prevNum = this.coinsWageredNumber.text;
            let newNum = (parseInt(prevNum) + 1).toString();
            this.coinsWageredNumber.setText(newNum);
        });

        const up5 = this.add.image(this.scale.width *.65 ,  this.scale.height * .85, "up5").setScale(.2).setInteractive();
        up5.on('pointerdown', () => {
            console.log('up5 clicked!');
            let prevNum = this.coinsWageredNumber.text;
            let newNum = (parseInt(prevNum) + 5).toString();
            this.coinsWageredNumber.setText(newNum);
        });

        const down1 = this.add.image(this.scale.width *.4 ,  this.scale.height * .85, "down1").setScale(.2).setInteractive();
        down1.on('pointerdown', () => {
            console.log('down1 clicked!');
            let prevNum = this.coinsWageredNumber.text;
            if((parseInt(prevNum) - 1) < 0){
                console.log("please don't select a negative number :DD");
                return;
            }
            let newNum = (parseInt(prevNum) - 1).toString();
            this.coinsWageredNumber.setText(newNum);
        });

        const down5 = this.add.image(this.scale.width *.35 ,  this.scale.height * .85, "down5").setScale(.2).setInteractive();
        down5.on('pointerdown', () => {
            console.log('down5 clicked!');
            let prevNum = this.coinsWageredNumber.text;
            if((parseInt(prevNum) - 5) < 0){
                console.log("please don't select a negative number :DD");
                return;
            }
            
            let newNum = (parseInt(prevNum) - 5).toString();
            this.coinsWageredNumber.setText(newNum);
        });
    }

    createBackButton(){
        const backButton = this.add.text(this.scale.width, 0, 'Back', {
            fontSize: '16px',
            fill: '#fff',
            backgroundColor: '#004d4d',
            padding: { x: 10, y: 5 }
        }).setInteractive().setOrigin(1, 0);

        backButton.on('pointerdown', () => {
            window.location.href = '/casino';
        });
    }
    
}


const config = {
    type: Phaser.AUTO,
    width: window.innerWidth,
    height: window.innerHeight,
    scale: {
        mode: Phaser.Scale.RESIZE,
        autoCenter: Phaser.Scale.CENTER_BOTH,
        width: '100%',
        height: '100%',
    },
    backgroundColor: '#1a1a1a',
    parent: 'game-container',
    scene: [Roulette]
};

const game = new Phaser.Game(config);