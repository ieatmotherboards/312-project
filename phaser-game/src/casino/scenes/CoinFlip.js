import { CoinCounter } from '../../gameObjects/CoinCounter.js';
import { ExitSign } from '../../gameObjects/ExitSign.js';

export class CoinFlip extends Phaser.Scene {
    constructor() {
        super('CoinFlip');
    }

    create() {
        this.coin = this.add.sprite(400, 300, 'coin_flip');
    }

    update() {
        
    }
}