import { CoinCounter } from '../../gameObjects/CoinCounter.js';
import { ExitSign } from '../../gameObjects/ExitSign.js';

export class CoinFlip extends Phaser.Scene {
    constructor() {
        super('CoinFlip');
    }

    create() {
        this.coin = this.add.sprite(400, 300, 'coin_flip');

        this.face = true // True = heads, False = tails

        this.coin.anims.create({
            key: 'heads',
            frames: this.coin.anims.generateFrameNumbers('coin_flip', {start: 0, end: 0})
        });
        this.coin.anims.create({
            key: 'tails',
            frames: this.coin.anims.generateFrameNumbers('coin_flip', {start: 1, end: 1})
        });

        this.tweens.add({
            targets: [this.coin],
            scaleY: 0,
            duration: 250,
            ease: 'Sine.inOut',
            yoyo: true,
            loop: -1,
            onYoyo: (tween, target, key) => {
                if (this.face) {
                    target.anims.play('heads');
                } else {
                    target.anims.play('tails');
                }
                this.face = !this.face
            }
        });
    }

    update() {
        
    }
}