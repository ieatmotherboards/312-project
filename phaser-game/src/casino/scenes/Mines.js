import { CoinCounter } from '../../gameObjects/CoinCounter.js';
import { ExitSign } from '../../gameObjects/ExitSign.js';

export class Mines extends Phaser.Scene {
    constructor() {
        super('Mines');
    }

    create() {
        this.add.image(400, 300, 'cave');
        
        this.timePassed = 0;
        this.timeToNext = Math.random() * 1000 + 1000;
        this.makeCoal();
        this.physics.world.on('worldbounds', function(body) {
            body.setVelocityX(0);
            setTimeout(function(world) {
                world.scene.collectCoin(body);
            }, Math.random() * 500 + 1500, this)
        });
        this.bodyMap = new Map();
        this.coalCount = 0;
        this.coalBroken = 0;

        this.coinCounter = new CoinCounter(this, 28, 28);
        this.exit = new ExitSign(this, 730, 32, 'Game');

        // getting user info
        let request = new Request('/phaser/@me');
        fetch(request).then(response => {
            return response.json();
        }).then(data => {
            this.coinCounter.setCoins(data['coins']);
        });
   }

    update(time, delta) {
        this.timePassed += delta;
        while (this.timePassed >= this.timeToNext) {
            this.makeCoal();
            this.timePassed -= this.timeToNext;
            // this.timePassed = this.timePassed / 2;
            this.timeToNext = (Math.random() * 750 + 2250) * (1.4 + this.coalBroken * 0.2) ** (this.coalCount + 1);
        }
    }

    makeCoal() {
        let coal = this.add.sprite(Math.random() * 600 + 100, Math.random() * 400 + 100, 'coal').setInteractive().setScale(4, 4);
        coal.breaking = false;
        this.coalCount += 1;

        coal.on('pointerdown', function (pointer) {
            if (!this.breaking) {
                this.setTexture('coal_breaking');
                this.breaking = true;
            } else {
                let coin = this.scene.physics.add.sprite(this.x, this.y, 'coin');
                this.scene.bodyMap.set(coin.body, coin);
                this.scene.coalCount -= 1;
                this.scene.coalBroken += 1;
                this.scene.timePassed = this.scene.timePassed / 3;
                this.scene.timeToNext = this.scene.timeToNext / 2;
                coin.setScale(2.5, 2.5);
                coin.setGravityY(500);
                coin.setCollideWorldBounds(true, 1, 0.5, true);
                coin.setVelocity(Math.random() * 200 - 100, Math.random() * -200 - 100);
                coin.setInteractive();
                coin.on('pointerdown', function() {
                    this.scene.collectCoin(this.body);
                });
                coin.collected = false;
                this.destroy();
            }
        });
   }

   collectCoin(body) {
        let coin = this.bodyMap.get(body);
        if (coin != undefined && !coin.collected) {
            this.coinCounter.incrementCoins();
            coin.collected = true;
            let request = new Request ("/addCoins", {
                method: "POST",
                body: JSON.stringify({"coins": 1}),
                headers: {"Content-Type": "application/json"}
                });
            fetch(request);
            coin.destroy();
        }
   }
}