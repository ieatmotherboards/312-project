import { CoinCounter } from '../../gameObjects/CoinCounter.js';
import { ExitSign } from '../../gameObjects/ExitSign.js';

export class CoinFlip extends Phaser.Scene {
    constructor() {
        super('CoinFlip');
    }

    create() {
        this.coin = this.add.sprite(400, 300, 'coin_flip');

        this.face = true; // True = heads, False = tails

        this.myCoinCounter = new CoinCounter(this, 28, 28);
        this.myUserText = this.add.text(20, 65, '', { fontSize: '16px', align: 'center', color: '#000', fontStyle: "bold"}).setOrigin(0, 0.5);
        this.enemyUserText = this.add.text(780, 65, '', { fontSize: '16px', align: 'center', color: '#000', fontStyle: "bold"}).setOrigin(1, 0.5);
        this.enemyCoinCounter = new CoinCounter(this, 650, 28);
        this.exitSign = new ExitSign(this, 400, 32, 'Game');

        this.keyText = this.add.text(400, 450, 'Press SPACE to flip the coin!', { fontSize: '32px', align: 'center', color: '#000', fontStyle: "bold"}).setOrigin(0.5, 0.5);

        this.flipped = false;

        // getting user info
        let request = new Request('/phaser/@me');
        fetch(request).then(response => {
            return response.json();
        }).then(data => {
            this.myCoinCounter.setCoins(data['coins']);
            this.username = data['username'];
            this.myUserText.setText(this.username);
            this.websocket.emit('get_opponent', { 'username': this.username });
        });

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
                this.face = !this.face;
            }
        });

        this.keySpace = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.SPACE);

        this.interacted = false;

        // websocket initialization
        this.websocket = io();
        this.websocket.scene = this;

        this.websocket.on('coins', function(data) {
            let username = data['username'];
            if (username == this.scene.username) {
                this.scene.myCoinCounter.setCoins(data['coins']);
            } else if (username == this.scene.opponent) {
                this.scene.enemyCoinCounter.setCoins(data['coins']);
            }
        });

        this.websocket.on('opponent', function(data) {
            this.scene.opponent = data['opponent'];
            this.scene.enemyUserText.setText(this.scene.opponent);
            this.scene.websocket.emit('get_coins', { 'username': this.scene.opponent });
        });

        this.websocket.on('flip_result', function(data) {
            this.scene.myCoinCounter.setCoins(data[this.scene.username]);
            this.scene.enemyCoinCounter.setCoins(data[this.scene.opponent]);
            let result = '';
            if (data['result']) {
                result = 'heads';
            } else {
                result = 'tails';
            }
            if (!this.scene.flipped) {
                this.scene.flipped = true;
                this.scene.tweens.killAll();
                this.scene.coin.scaleY = 1;
            }
            this.scene.coin.anims.play(result);
        });
    }

    update() {
        if (this.keySpace.isDown && !this.interacted) {
            this.interacted = true;
            this.websocket.emit('flip_coin', { 'to': this.opponent, 'from': this.username });
        } else if (!this.keySpace.isDown && this.interacted) {
            this.interacted = false;
        }
    }
}