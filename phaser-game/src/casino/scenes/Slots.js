import { CoinCounter } from '../../gameObjects/CoinCounter.js';

export class Slots extends Phaser.Scene {
    constructor() {
        super('Slots');

    }

    create() {
        
        this.add.image(400, 300, 'slots_bg').setDisplaySize(800, 600);
        this.coinCounter = new CoinCounter(this, 28, 28);
        this.button = this.add.sprite(700, 500, 'button').setScale(2);
        this.button.scene = this;
        this.button.setInteractive();
        this.button.on('pointerdown', pointer => {
            let request = new Request('/phaser/playSlots', {
                method: "POST",
                body: JSON.stringify({"bet": 1}),
                headers: {"Content-Type": "application/json"}
                });
            fetch(request).then(response => {
                if (response.status == 200) {
                    return response.json();
                } else {
                    // HANDLE ERROR
                    return {'error': true};
                }
            }).then(data => {
                if (!data['error']) {
                    this.coinCounter.setCoins(data['newCoins']);    
                }
            });
        });
        
    }
}