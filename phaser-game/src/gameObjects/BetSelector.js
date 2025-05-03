export class BetSelector extends Phaser.GameObjects.GameObject {
    constructor(scene, x, y) {
        super(scene, "betSelector");
        this.x = x;
        this.y = y;

        this.bet = 1;

        this.coinsWagered = this.scene.add.text(this.x, this.y - 25, "Coins Wagered:",{
            fontSize: '20px',
            fill: '#ffffff'
        }).setOrigin(.5,.5);

        this.coinsWageredNumber = this.scene.add.text(this.x, this.y + 25, "1",{
            fontSize: '20px',
            fill: '#ffffff'
        }).setOrigin(.5,.5);

        this.createWagerButtons();
    }

    createWagerButtons() {
        const up1 = this.scene.add.image(this.x + 125,  this.y, "up1").setScale(.3).setInteractive();
        up1.on('pointerdown', () => {
            this.changeBet(1);
        });

        const up5 = this.scene.add.image(this.x + 225,  this.y, "up5").setScale(.3).setInteractive();
        up5.on('pointerdown', () => {
            this.changeBet(5);
        });

        const down1 = this.scene.add.image(this.x - 125,  this.y, "down1").setScale(.3).setInteractive();
        down1.on('pointerdown', () => {
            this.changeBet(-1);
        });

        const down5 = this.scene.add.image(this.x - 225,  this.y, "down5").setScale(.3).setInteractive();
        down5.on('pointerdown', () => {
            this.changeBet(-5);
        });
    }

    changeBet(change) {
        let prevNum = this.bet;
        let newNum = prevNum + change;
        if(newNum < 0){
            newNum = 0;
        }
        let newText = (newNum).toString();
        this.coinsWageredNumber.setText(newText);
        this.bet = newNum;
    }
}