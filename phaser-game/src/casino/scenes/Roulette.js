import { CoinCounter } from '../../gameObjects/CoinCounter.js';

export class Roulette extends Phaser.Scene {

    constructor() {
        super({ key: 'Roulette' });
    }

    preload() {
        this.load.image('roulette', '/phaser-game/assets/roulette/roulette_bg_2.png'); 
        this.load.image('wheel', '/phaser-game/assets/roulette/roulette_wheel.png'); 
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
        const debug = this.add.graphics();
        debug.lineStyle(4, 0x00ff00);
        debug.strokeRect(0, 0, this.scale.width, this.scale.height);


        //wheel logic
        const imageStartX = width * .25;
        const imageStartY = height * .5;
        const rouletteWheel = this.add.image(imageStartX, imageStartY, 'wheel');

        const originalWidth = rouletteWheel.width;
        const originalHeight = rouletteWheel.height;

        const maxDisplayWidth = width * 0.6;
        const maxDisplayHeight = height * 0.6;

        const wheel_scale = Math.min(maxDisplayWidth / originalWidth, maxDisplayHeight / originalHeight);
        rouletteWheel.setDisplaySize(originalWidth * wheel_scale, originalHeight * wheel_scale);

        // add number to be populated of result of wheel text -- placeholder right now, will be blank until roulette result
        // this same logic will be copied and pasted after the result of a successful roulette spin
        const betResult = this.add.text(imageStartX, imageStartY, '',{
            fontSize: '40px',
            fill: '#ffffff'
        }).setOrigin(.5);
        
        // add coin counter AND FIX
        this.coinCounter = new CoinCounter(this, 28, 28);

        this.betInfo = {
            type: null,
            value: null,
            amount: 0,
            numOfNums: 0
        };
    
        // 1. Build the board
        this.createRouletteBoard(); // <- Generates the number grid and common bets

        this.createBackButton();
    
        // 2. Add Place Bet button
        const confirmBtn = this.add.text(width, height, 'Place Bet!', {
            fontSize: '20px',
            fill: '#ffffff',
            backgroundColor: '#007bff',
            padding: { x: 50, y: 25 }
        })
        .setOrigin(1,1) 
        .setInteractive();

        const yourBet = this.add.text(width * .5, height * .1, 'Your Bet:',{
            fontSize: '65px',
            fill: '#ffffff'
        }).setOrigin(.5);

        // list of numbers that you bet on. cleared when you select a diff type of bet
        this.numBet = this.add.text(width * .4, height * .2, '',{ 
            fontSize: '20px',
            fill: '#ffffff'
        });

        // the type of the bet that you select. "Number(s)" or something else like "Red"
        this.valueBet = this.add.text(width * .55, height * .2, '',{
            fontSize: '20px',
            fill: '#ffffff'
        });

        confirmBtn.on('pointerdown', () => {
            console.log(this.valueBet.text);
            if (this.valueBet.text === "") {
                console.log('No bet selected!');
                return;
            }


            console.log(' --- BET INFO ---');
            console.log("wagering " + this.betInfo.amount.toString() + " coins");
            console.log("betting on type " + this.valueBet.text);
            console.log("numbers are (if applicable):" + this.numBet.text);

            let request = new Request('/phaser/playRoulette', {
                method: "POST",
                body: JSON.stringify({
                    wager: this.betInfo.amount,
                    bet_type: this.valueBet.text,
                    numbers: this.numBet.text
                }),
                headers: { "Content-Type": "application/json" }
            });
    
            fetch(request)
                .then(response => response.json())
                .then(data => {
                    console.log("Number outcome:", data['outcome']);
                    console.log("Winnings:", data['user_cashout']);
                    betResult.setText(data['outcome'].toString());

                    // You can show a result popup or animate the wheel here!
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
                            console.log("You may only bet on maximum 6 numbers at once");
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