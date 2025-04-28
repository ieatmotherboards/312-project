import { CoinCounter } from '../../gameObjects/CoinCounter.js';
import { ExitSign } from '../../gameObjects/ExitSign.js';

export class Slots extends Phaser.Scene {
    constructor() {
        super('Slots');
    }

    create() {
        this.add.image(400, 300, 'slots_bg').setDisplaySize(800, 600);
        this.coinCounter = new CoinCounter(this, 28, 28);

        this.slotsIcons = new SlotsIcons(this, 403, 226);

        this.spinning = false;
        this.currentBet = 1;

        this.exitSign = new ExitSign(this, 730, 32, 'Game');

        // initialize spin button
        this.button = this.add.sprite(700, 500, 'button').setScale(2);
        this.button.scene = this;
        this.button.setInteractive();
        this.button.on('pointerdown', pointer => {
            if (this.spinning) {return}
            this.spinning = true;
            this.slotsIcons.startSpin();
            this.coinCounter.addCoins(-1 * this.currentBet);
            let request = new Request('/phaser/playSlots', {
                method: "POST",
                body: JSON.stringify({"bet": this.currentBet}),
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
                    setTimeout(function (scene) {
                        scene.coinCounter.setCoins(data['newCoins']);
                        let slots = data['slots'];
                        scene.slotsIcons.setSlots(slots);
                        scene.spinning = false;
                    }, 1000, this);
                }
            });
        });

        // getting user info
        let request = new Request('/phaser/@me');
        fetch(request).then(response => {
            return response.json();
        }).then(data => {
            this.coinCounter.setCoins(data['coins']);
        });
    }
}

class SlotsIcons {
    // 403, 226
    // 262, 99
    constructor(scene, x, y) {
        this.scene = scene;
        this.x = x;
        this.y = y;
        this.spriteNames = ['coal', 'stone', 'scrip', 'pick', 'crystal', 'gold', 'obsidian', 'diamond'];
        this.iconsMatrix = [[], [], []];
        y -= 127;
        let x_start = x - 141;
        for (let i_y = 0; i_y < 3; i_y++) {
            x = x_start;
            for (let i_x = 0; i_x < 3; i_x++) {
                let sprite = this.scene.add.sprite(x, y, 'slot_icons').setScale(3);
                sprite.anims.create({
                    key: 'spin',
                    frames: sprite.anims.generateFrameNumbers('slot_icons', {start: 0, end: 7}),
                    frameRate: 10,
                    repeat: -1
                });

                for (let sp = 0; sp < 8; sp++) {
                    sprite.anims.create({
                        key: this.spriteNames[sp],
                        frames: sprite.anims.generateFrameNumbers('slot_icons', {start: sp, end: sp})
                    });
                }
                this.iconsMatrix[i_y].push(sprite);
                x += 141;
            }
            y += 127;
        }
        this.randomIcons();
    }

    startSpin() {
        for (let y = 0; y < 3; y++) {
            for (let x = 0; x < 3; x++) {
                this.iconsMatrix[y][x].anims.play({key: 'spin', startFrame: randomInt(8)}, true);
            }
        }
    }

    randomIcons() {
        for (let y = 0; y < 3; y++) {
            for (let x = 0; x < 3; x++) {
                let r = randomInt(8);
                this.iconsMatrix[y][x].anims.play(this.spriteNames[r]);
            }
        }
    }

    setSlots(slotsMatrix) {
        for (let y = 0; y < 3; y++) {
            for (let x = 0; x < 3; x++) {
                this.iconsMatrix[y][x].anims.play(this.spriteNames[slotsMatrix[y][x]]);
            }
        }
    }
}

function randomInt(max) {
    return Math.floor(Math.random() * 8);
}